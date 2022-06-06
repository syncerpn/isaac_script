# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:59:45 2021

@author: nghia_sv
"""

name_file_name = 'D:/python_workspace/tags.txt'
name_file = open(name_file_name, 'r')
name_list = name_file.readlines()
name_list = [name.strip('\n') for name in name_list]

all_tags = {}

for i, text in enumerate(name_list):
    if i > 612:
        break
    item_desc = text.split('|')
    if (len(item_desc) > 1):
        item_tags = item_desc[1].split(' ')
        for tag in item_tags:
            tag = tag.split(':')
            if len(tag) > 1:
                tag_name = tag[0]
                tag_sublist = tag[1].split(',')
                if tag_name in all_tags:
                    all_tags[tag_name] += tag_sublist
                else:
                    all_tags[tag_name] = tag_sublist

for tag_name in all_tags:
    all_tags[tag_name] = sorted(list(set(all_tags[tag_name])))
    print(all_tags[tag_name])
    
out_file = open('D:/python_workspace/list_tags.txt','w')
for tag_name in all_tags:
    out_file.write(tag_name + '\n')
    for tag_sub in all_tags[tag_name]:
        out_file.write('  ' + tag_sub + '\n')

out_file.close()