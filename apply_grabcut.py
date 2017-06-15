__author__ = 'dfan'

import matplotlib
matplotlib.use('Agg')

import os, glob, cv2, argparse
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches


def get_seq_list(dataset):
    if dataset == 'OTB':
        with open('tb_100.txt') as f:
            lines = f.readlines()
            seq_list = [x.rstrip() for x in lines]
    elif dataset == '92-2-small':
        seq_list = os.listdir(os.path.join('dataset', dataset))
        seq_list = [x for x in seq_list if os.path.isdir(os.path.join('dataset', dataset, x))]
    elif dataset == '92-2':
        seq_list = os.listdir(os.path.join('dataset', dataset))
        seq_list = [x for x in seq_list if os.path.isdir(os.path.join('dataset', dataset, x))]
    else:
        print 'Invalid dataset name'
        exit(1)

    print 'Running in dataset: %s' % dataset
    return seq_list


def propose_two(rect, x_max, y_max):
    # Input: a tuple of rect, formatted as (x, y, w, h)
    # x_max, y_max could be, e.g., 1279x719
    # propose 2 bboxes, scaled at 1.0x, 1.4x, located at middle

    x_orig, y_orig, w_1, h_1 = rect
    proposals = [rect]

    # Append four centered bboxes
    for scale in np.arange(1.4, 1.5, 0.1):
        x = x_orig - (scale - 1) / 2.0 * w_1
        y = y_orig - (scale - 1) / 2.0 * h_1
        w = w_1 * scale
        h = h_1 * scale

        proposals.append((x, y, w, h))

    # restrict bbox within range
    valid_proposals = []
    for bbox in proposals:
        x1, y1, w, h = bbox
        x2, y2 = x1 + w, y1 + h

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(x_max, x2)
        y2 = min(y_max, y2)

        valid_proposals.append((int(x1), int(y1), int(max(x2 - x1, 0)), int(max(y2 - y1, 0))))

    return valid_proposals


def construct_global_mask(img, proposals):
    # Construct the only mask
    global_mask = cv2.GC_BGD * np.ones(img.shape[:2], np.uint8)

    largest_bbox = proposals[-1]
    x, y, w, h = largest_bbox
    global_mask[y:y + h, x:x + w] = cv2.GC_PR_BGD

    orig_bbox = proposals[0]
    x, y, w, h = orig_bbox
    global_mask[y:y + h, x:x + w] = cv2.GC_PR_FGD

    global_mask[(y + h / 4):(y + h * 3 / 4), x + w / 2] = cv2.GC_FGD
    global_mask[y + h / 2, (x + w / 4):(x + w * 3 / 4)] = cv2.GC_FGD

    return global_mask


def plot_img_with_mask(img, rect, mask, dataset, seq, img_file):
    ############
    # Plotting #
    ############
    fig = plt.figure(figsize=(10, 4))

    ax1 = fig.add_subplot(121, aspect='equal')

    ax1.imshow(img)
    rectangle = patches.Rectangle((rect[0], rect[1]), rect[2], rect[3], linewidth=2, edgecolor='r', facecolor='none')
    ax1.add_patch(rectangle)

    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 2, 2)
    plt_im = plt.imshow(mask, cmap='hot', interpolation='nearest')
    plt.colorbar(plt_im, fraction=0.026, pad=0.04)
    plt.xticks([])
    plt.yticks([])

    plt.tight_layout()

    #################
    # Saving images #
    #################
    dir_name = 'grabcut'

    if not os.path.exists(os.path.join('result', dataset, seq, dir_name)):
        os.makedirs(os.path.join('result', dataset, seq, dir_name))
    plt.savefig(os.path.join('result', dataset, seq, dir_name, img_file.split('/')[-1]))



def main(dataset):
    seq_list = get_seq_list(dataset)
    seq_list.sort()

    for seq in seq_list:
        print 'Processing sequence: %s' % seq

        img_list = glob.glob(os.path.join('dataset', dataset, seq, 'img', '*.jpg'))
        img_list.sort()

        rect_file = os.path.join('result', dataset, seq, 'result_mdnet_%s.txt' % seq)
        with open(rect_file) as f:
            rect_list = f.readlines()
            rect_list = [tuple([int(float(z)) for z in x.rstrip().split(',')]) for x in rect_list]

        for idx in xrange(2, len(img_list)):
            img_file = img_list[idx]
            rect = rect_list[idx]
            if dataset.endswith('small'):
                rect = (rect[0]/2, rect[1]/2, rect[2]/2, rect[3]/2)
            print '\tProcessing image: %s' % img_file

            img = cv2.imread(img_file)

            b,g,r = cv2.split(img)
            img = cv2.merge([r,g,b])

            x_max = img.shape[1] - 1
            y_max = img.shape[0] - 1
            proposals = propose_two(rect, x_max, y_max)

            global_mask = construct_global_mask(img, proposals)

            # Use opencv's grabcut function to get the segementation mask
            mask = np.zeros(img.shape[:2], np.uint8)  # Must be np.uint8
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            mask = global_mask
            cv2.grabCut(img, mask, None, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_MASK)

            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')


            bg = -1 * np.ones(img.shape[:2], np.float32)

            x, y, w, h = proposals[-1]
            bg[y:y+h, x:x+w] = mask2[y:y+h, x:x+w]

            plot_img_with_mask(img, rect, bg, dataset, seq, img_file)



def resize_imgs(dataset):
    from PIL import Image

    if not os.path.exists(os.path.join('dataset', dataset + '-small')):
        os.mkdir(os.path.join('dataset', dataset + '-small'))

    seq_list = get_seq_list(dataset)
    # seq_list = ['92-2-1', '92-2-2', '92-2-4', '92-2-5', '92-2-6', '92-2-7', '92-2-8', '92-2-9', '92-2-10', '92-2-11']

    for seq in seq_list:
        img_list = glob.glob(os.path.join('dataset', dataset, seq, 'img', '*.jpg'))
        img_list.sort()

        if not os.path.exists(os.path.join('dataset', dataset + '-small', seq, 'img')):
            os.makedirs(os.path.join('dataset', dataset + '-small', seq, 'img'))

        # Copy result file
        from shutil import copyfile
        copyfile(os.path.join('result', dataset, seq, 'result_mdnet_%s.txt' % seq),
                 os.path.join('result', dataset + '-small', seq, 'result_mdnet_%s.txt' % seq))

        for img_file in img_list:
            img = Image.open(img_file)
            w = img.size[0]
            h = img.size[1]
            img = img.resize((w / 2, h / 2), Image.ANTIALIAS)

            img_file_contents = img_file.split('/')
            img_file_contents[1] = dataset + '-small'

            img.save('/'.join(img_file_contents))

            print img_file




if __name__ == '__main__':
    # dataset = 'OTB'
    dataset = '92-2-small'

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', help='Specify the dataset. Choose from OTB, 92-2 or 92-2-small.', default='92-2-small')
    parser.add_argument('--gen_small', help='Generate the corresponding small dataset.')

    args = parser.parse_args()

    if args.gen_small:
        resize_imgs(args.dataset.replace('-small', ''))

    dataset = args.dataset

    if not dataset:
        print 'You must specify a dataset by -d or --dataset'
        exit(1)

    main(dataset)