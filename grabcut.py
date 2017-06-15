import matplotlib
matplotlib.use('Agg')

import numpy as np
import os, glob
import cv2
from matplotlib import pyplot as plt


# seq_list = ['92-2-1','92-2-2','92-2-4','92-2-5','92-2-6','92-2-7','92-2-8','92-2-9','92-2-10','92-2-11']
seq_list = ['92-2-2']

for seq in seq_list:

    img_list = glob.glob(os.path.join('dataset', '92-2', seq, 'img', '*.jpg'))
    img_list.sort()
    # img_list = [os.path.join('dataset', '92-2', seq, 'img', x) for x in img_list]

    if seq == '92-2-1':
        img_list = [img_list[:46], img_list[55:71], img_list[84:144], img_list[157:176], img_list[201:223], img_list[237:247], img_list[253:287], img_list[299:310], img_list[318:]]
        img_list = [item for sublist in img_list for item in sublist]
    elif seq == '92-2-4':
        img_list = [img_list[:50], img_list[58:172], img_list[183:212], img_list[235:248], img_list[261:]]
        img_list = [item for sublist in img_list for item in sublist]

    rect_list = glob.glob(os.path.join('result', '92-2', seq, 'cur_pos_examples', '*.txt'))
    rect_list.sort()
    # rect_list = [os.path.join('result', '92-2', seq, 'cur_pos_examples', x) for x in rect_list]

    # print img_list
    # print len(img_list)
    # print len(rect_list)

    assert len(img_list) == len(rect_list)

    for idx in xrange(1,len(img_list)):

        img_file = img_list[idx]
        rect_file = rect_list[idx]

        print img_file

        img = cv2.imread(img_file)

        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        # print img.shape

        heatmap = np.zeros(img.shape[:2],np.uint8)

        with open(rect_file) as f:
            cur_rect_list = f.readlines()
            cur_rect_list = [x.rstrip() for x in cur_rect_list]
            print cur_rect_list

        for rect_idx, rect_str in enumerate(cur_rect_list):

            mask = np.zeros(img.shape[:2],np.uint8)
            bgdModel = np.zeros((1,65),np.float64)
            fgdModel = np.zeros((1,65),np.float64)

            rect = rect_str.split(',')
            rect = tuple([int(x) for x in rect])
            
            cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

            mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

            heatmap += mask2

            print rect_idx

        max_heat = heatmap.max()
        heatmap /= max_heat

        plt.figure()

        # plt.imshow(img),plt.colorbar(),plt.show()

        img = img*heatmap[:,:,np.newaxis]

        plt.imshow(img),plt.colorbar(),plt.show()

        plt.savefig(os.path.join('result', '92-2', seq, 'grabcut', 'cur_pos_examples', '*.txt')'%d.jpg' % (idx + 1))