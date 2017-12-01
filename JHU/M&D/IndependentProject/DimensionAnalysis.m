I = imread('Raw/2-8.jpg');
S = sum(I,3);
I2 = imcrop(I,[1100,1230,120,100]);
S2 = imcrop(S,[1100,1230,120,100]);
I3 = imcrop(I,[1900,1200,380,150]);
S3 = imcrop(S,[1900,1200,380,150]);
I4 = imcrop(I,[2400,1200,240,360]);
S4 = imcrop(S,[2400,1200,240,360]);

[r2,c2] = find(S2 == max(S2(:)));
[tr2,tc2] = toR(r2,c2);
[r3,c3] = find(S3 == max(S3(:)));
[tr3,tc3] = toR(r3,c3);
[r4,c4] = find(S4 == max(S4(:)));
[tr4,tc4] = toR(r4,c4);

r = vertcat(tr2+1230,tr3+1200,tr4+1200);
c = vertcat(tc2+1100,tc3+1900,tc4+2400);

imshow(I);
hold on;
line([c(1),c(2)],[r(1),r(2)], 'Color', 'red', 'LineWidth', 2);
line([c(2),c(3)],[r(2),r(3)], 'Color', 'red', 'LineWidth', 2);
rectangle('Position', [1100,1230,120,100], 'EdgeColor', 'r', 'LineWidth', 2)
rectangle('Position', [1900,1200,380,150], 'EdgeColor', 'r', 'LineWidth', 2)
rectangle('Position', [2400,1200,260,360], 'EdgeColor', 'r', 'LineWidth', 2)
% cd RegionOverlays/
% print('1-6','-dpng')
% cd ..

% y = [1550, 1500, 1450, 1420, 1370, 1320, 1280, 1230];
% height = [850, 800, 750, 720, 670, 620, 580, 530];
% width2 = [110, 120, 160, 150, 180, 220, 250, 380];
% height2 = [450, 400, 370, 330, 300, 220, 160, 150];
% width3 = [260, 260, 260, 260, 247, 250, 245, 260];
% height3 = [450, 400, 380, 370, 340, 320, 340, 360];

function [r,c] = toR(x,y)
r = sum(x)/size(x,1);
c = sum(y)/size(y,1);
end