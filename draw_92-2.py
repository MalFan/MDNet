import matplotlib
matplotlib.use('Agg')

import numpy as np
import os, glob
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def main():
    col_list = ['b','g','r','c','m','y','k','pink','orange','yellow']

    num_frame = 325
    num_seq = 10
    frame_mat = np.zeros((num_frame, num_seq), np.int32)

    # frame_mat[:, 0] = 1
    frame_mat[18:65, 1] = 1
    # frame_mat[32:319, 2] = 1
    frame_mat[20:97, 3] = 1
    frame_mat[12:70, 4] = 1
    frame_mat[123:180, 5] = 1
    frame_mat[109:160, 6] = 1
    frame_mat[233:294, 7] = 1
    frame_mat[233:301, 8] = 1
    frame_mat[219:281, 9] = 1

    # Don't plot when some frames are occluded in 92-2-1 and 92-2-4
    occl_frame_idx_92_2_1 = range(0,46) + range(55,71) + range(84,144) + range(157,176) + range(201,223) + \
                            range(237,247) + range(253,287) + range(299,310) + range(318,325) 
    frame_mat[occl_frame_idx_92_2_1, 0] = 1
    occl_frame_idx_92_2_4 = range(17,67) + range(75,189) + range(200,229) + range(252,265) + range(278,304)
    occl_frame_idx_92_2_4 = [x + 15 for x in occl_frame_idx_92_2_4]
    frame_mat[occl_frame_idx_92_2_4, 2] = 1


    frame_counter_for_seq = [0] * num_seq

    # Read file to get a bbox position list for each seq
    seq_list = ['92-2-1','92-2-2','92-2-4','92-2-5','92-2-6','92-2-7','92-2-8','92-2-9','92-2-10','92-2-11']
    seq_id_2_bbox_list = []
    for seq_idx, seq in enumerate(seq_list):
        file_name = os.path.join('result', '92-2', seq, 'result_mdnet_%s.txt' % seq)
        with open(file_name) as f:
            lines = f.readlines()
            lines = [x.rstrip() for x in lines]

            seq_id_2_bbox_list.append(lines)

            print frame_mat.sum(axis=0)[seq_idx]
            print len(lines)
            assert frame_mat.sum(axis=0)[seq_idx] == len(lines)

    img_list = glob.glob(os.path.join('dataset', '92-2', '92-2-1', 'img', '*.jpg'))
    img_list.sort()

    for frame_idx in xrange(num_frame):
        img_file = img_list[frame_idx]
        img = Image.open(img_file)

        plt.figure(0)
        plt.imshow(img)

        for seq_idx in xrange(num_seq):
            if frame_mat[frame_idx, seq_idx] == 1:
                bbox_pos = seq_id_2_bbox_list[seq_idx][frame_counter_for_seq[seq_idx]]
                frame_counter_for_seq[seq_idx] += 1

                bbox_pos = [int(float(x)) for x in bbox_pos.split(',')]

                current_axis = plt.gca()
                current_axis.add_patch(Rectangle((bbox_pos[0], bbox_pos[1]), bbox_pos[2], bbox_pos[3], edgecolor=col_list[seq_idx], facecolor='none', linewidth=2))
        
        plt.show()

        if not os.path.exists(os.path.join('result', '92-2-all')):
            os.mkdir(os.path.join('result', '92-2-all'))

        plt.axis('off')
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        
        fig = plt.gcf()

        DPI = fig.get_dpi()
        # print DPI
        fig.set_size_inches(1280/float(DPI)*1280/1240,720/float(DPI)*720/697)

        plt.savefig(os.path.join('result', '92-2-all', '%04d.jpg' % (frame_idx + 86)), 
                    bbox_inches='tight', pad_inches=0.0)
        plt.clf()

        print 'Drawing frame: %04d.jpg' % (frame_idx + 86)



if __name__ == '__main__':
    main()