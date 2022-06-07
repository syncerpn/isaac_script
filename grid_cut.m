root = 'E:/SYNCER STUDIO/YT/Repentance/common/';
file_name = 'background alt.png';

col_step = [208, 156 ,84, 96, 84, 84, 88];
row_step = [96, 96, 96, 96, 96, 96, 96, 96, 96, 96];

[full_image, ~, full_alpha] = imread([root, file_name]);

sy = 1;
for i = 1:numel(col_step)
    sx = 1;
    ey = sy + col_step(i) - 1;
    for j = 1:numel(row_step)-1
        ex = sx + row_step(j) - 1;
        part_image = full_image(sy:ey, sx:ex, :);
        part_alpha = full_alpha(sy:ey, sx:ex, :);
        part_name = [file_name(1:end-4), num2str(i), '_', num2str(j), '.png'];
        sx = ex + 1;
        imwrite(part_image, [root, part_name], 'Alpha', part_alpha);
    end
    sy = ey + 1;
end