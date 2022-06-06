from matplotlib import pyplot as plt
import os
import numpy as np
    
name_file_name = 'E:/python_workspace/isaac_script/full_item_list.txt'
name_file = open(name_file_name, 'r')
name_list = name_file.readlines()

image_dir = 'E:/python_workspace/isaac_script/all_item/'
image_list = os.listdir(image_dir)

ih = 32
iw = 32

fh = 27
fw = 27

full_im = np.zeros([fh * ih, fw * iw, 4]);
orig_list = np.zeros([fh, fw], dtype=np.int32);
orig_im = np.zeros([fh * ih, fw * iw, 4]);
    
for i in range(len(image_list)):
    y = i // fh
    x = i %  fw
    cur_im = plt.imread(image_dir + image_list[i])
    full_im[y*ih:y*ih+ih, x*iw:x*iw+iw, :] = cur_im
    orig_im[y*ih:y*ih+ih, x*iw:x*iw+iw, :] = cur_im
    orig_list[y,x] = 1
        
def read_item(event):
    ix, iy = event.xdata, event.ydata
    if ix is not None and iy is not None:
        y = int(iy // ih)
        x = int(ix // iw)
        
        if y*fw+x < len(image_list):
            plt.suptitle(name_list[y*fw+x])
            plt.draw()
        
def pick_item(event):
    ix, iy = event.xdata, event.ydata
    if ix is not None and iy is not None:
        y = int(iy // ih)
        x = int(ix // iw)
        
        if y*fw+x < len(image_list):
            if orig_list[y,x] == 1:
                orig_list[y,x] = 0
                full_im[y*ih:y*ih+ih, x*iw:x*iw+iw, :] = 0
            elif orig_list[y,x] == 0:
                orig_list[y,x] = 1
                full_im[y*ih:y*ih+ih, x*iw:x*iw+iw, :] = orig_im[y*ih:y*ih+ih, x*iw:x*iw+iw, :]
            
            plt.clf()
            plt.suptitle(name_list[y*fw+x])
            plt.axis('off')
            plt.imshow(full_im)
            plt.draw()
    
plt.connect('button_press_event', pick_item)
plt.connect('motion_notify_event', read_item)
plt.axis('off')
plt.imshow(full_im)
plt.draw()
plt.show()