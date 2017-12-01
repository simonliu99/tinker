y = [1550, 1500, 1450, 1420, 1370, 1320, 1280, 1230];
height = [850, 800, 750, 720, 670, 620, 580, 530];
width2 = [110, 120, 160, 150, 180, 220, 250, 380];
height2 = [450, 400, 370, 330, 300, 220, 160, 150];
width3 = [260, 260, 260, 260, 247, 250, 245, 260];
height3 = [450, 400, 380, 370, 340, 320, 340, 360];

ang = ones(8,8);
for j = 1:8
    for k = 1:8
        if j == 1 && k == 6
            ang(j,k) = img(sprintf('Raw/%d-%d.jpg',j,k),1320,220,220,240,320,j,k);
        elseif j == 2 && k == 8
            ang(j,k) = img(sprintf('Raw/%d-%d.jpg',j,k),1230,380,150,240,360,j,k);
        elseif j == 3 && k == 8
            ang(j,k) = img(sprintf('Raw/%d-%d.jpg',j,k),1230,380,150,270,360,j,k);
        else
            ang(j,k) = img(sprintf('Raw/%d-%d.jpg',j,k),y(k),width2(k),height2(k),width3(k),height3(k),j,k);
        end
    end
end
ang

function theta = img(i,y,w2,h2,w3,h3,j,k)
I = imread(i);
S = sum(I,3);
I2 = imcrop(I,[1100,y,120,100]);
S2 = imcrop(S,[1100,y,120,100]);
I3 = imcrop(I,[1900,1200,w2,h2]);
S3 = imcrop(S,[1900,1200,w2,h2]);
I4 = imcrop(I,[2400,1200,w3,h3]);
S4 = imcrop(S,[2400,1200,w3,h3]);

[r2,c2] = find(S2 == max(S2(:)));
[tr2,tc2] = toR(r2,c2);
[r3,c3] = find(S3 == max(S3(:)));
[tr3,tc3] = toR(r3,c3);
[r4,c4] = find(S4 == max(S4(:)));
[tr4,tc4] = toR(r4,c4);

r = vertcat(tr2+y,tr3+1200,tr4+1200);
c = vertcat(tc2+1100,tc3+1900,tc4+2400);

% figure;
imshow(I);
hold on;
line([c(1),c(2)],[r(1),r(2)], 'Color', 'red', 'LineWidth', 2);
line([c(2),c(3)],[r(2),r(3)], 'Color', 'red', 'LineWidth', 2);
rectangle('Position', [1100,y,120,100], 'EdgeColor', 'r', 'LineWidth', 2)
rectangle('Position', [1900,1200,w2,h2], 'EdgeColor', 'r', 'LineWidth', 2)
rectangle('Position', [2400,1200,w3,h3], 'EdgeColor', 'r', 'LineWidth', 2)
plot(c, r, 'r*', 'LineWidth', 2, 'MarkerSize', 3);

% cd RegionOverlays/
% print(sprintf('%d-%d',j,k),'-dpng')
% cd ..

theta = angle(c,r)
end

function theta = angle(x,y)
a = [x(3)-x(2),y(3)-y(2)];
b = [x(1)-x(2),y(1)-y(2)];
theta = acosd(dot(a,b)/(norm(a)*norm(b)));
end

function [r,c] = toR(x,y)
r = sum(x)/size(x,1);
c = sum(y)/size(y,1);
end
