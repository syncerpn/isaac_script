item_name = '635_stitches';

full_image_name = 'E:/SYNCER STUDIO/YT/Repentance/common/minimap_icons.png';

found_file = ['E:/SYNCER STUDIO/YT/Repentance/', item_name, '/pool.txt'];
out_image = ['E:/SYNCER STUDIO/YT/Repentance/', item_name, '/pool_icon.png'];
icon_size = 128;

image_spec = {'shop', 'secret', 'super_secret', 'library', 'treasure', 'angel', 'devil', 'dice';
'miniboss', 'boss', 'challenge', 'boss_challenge', 'curse', 'sacrifice', 'arcade', 'chest';
'bed', 'worn_bed', 'x', 'x', 'planetarium', 'u', 'u', 'u';
'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u';
'item', 'trinket', 'battery', 'card', 'pill', 'rune', 'golden_key', 'golden_bomb';
'chest', 'golden_chest', 'red_chest', 'bomb_chest', 'holy_chest', 'spiked_chest', 'sack', 'charged_key';
'slot_machine', 'blood_donation', 'fortuner', 'donation_machine', 'u', 'mirror', 'beggar', 'devil_beggar';
'golden_heart', 'half_soul_heart', 'bone_heart', 'blended_heart', 'rotten_heart', 'battery_bum', 'key_bum', 'bomb_bum';
'ultra_secret', 'u', 'mega_chest', 'u', 'golden_pill', 'golden_battery', 'confessional', 'crane_game';
'rotten_beggar', 'golden_penny', 'mirror_room', 'crawl_space', 'u', 'u', 'u', 'u';};

[full_image, map, alpha] = imread(full_image_name);

pool_list = {};
fid = fopen(found_file);
tline = fgetl(fid);
while ischar(tline)
    pool_list = [pool_list; tline];
    tline = fgetl(fid);
end
fclose(fid);

nh = size(full_image,1) / icon_size;
nw = size(full_image,2) / icon_size;
np = size(pool_list, 1);

pool_image = [];
pool_image_alpha = [];

for ih = 1:nh
    for iw = 1:nw
        for k = 1:np
            if strcmp(pool_list{k}, image_spec{ih, iw})
                pool_image = [pool_image full_image(icon_size*ih-icon_size+1:icon_size*ih, icon_size*iw-icon_size+1:icon_size*iw, :)];
                pool_image_alpha = [pool_image_alpha alpha(icon_size*ih-icon_size+1:icon_size*ih, icon_size*iw-icon_size+1:icon_size*iw, :)];
                
            end
        end
    end
end
imshow(pool_image);
imwrite(pool_image, out_image, 'Alpha', pool_image_alpha);