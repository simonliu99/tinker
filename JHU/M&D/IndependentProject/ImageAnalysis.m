y = [1550, 1500, 1450, 1420, 1370, 1320, 1280, 1230];
width2 = [110, 120, 160, 150, 180, 220, 250, 380];
height2 = [450, 400, 370, 330, 300, 220, 160, 150];
width3 = [260, 260, 260, 260, 247, 250, 245, 260];
height3 = [450, 400, 380, 370, 340, 320, 340, 360];
theta1 = [0, 0.1310941218, 0.2645116236, 0.4029750993, 0.5502212263, 0.7123244348, 0.9015891079, 1.155588928];
ri = [1.375177282, 1.379726782, 1.384001458, 1.388024636, 1.391817202, 1.395397886, 1.398783522, 1.401989263];

[ang,ax,ay,bx,by] = initImg(y,width2,height2,width3,height3);
[theta2,focallen] = initAng(theta1,ri,ang);
focallenM = zeros(8,8);
for i = 1:8
    for j = 1:8
        focallenM(i,j) = focallen(i*8-8+j);
    end
end

d2 = zeros(8,8);
for i = 1:8
    for j = 1:8
        d2(i,j) = abs(cos((deg2rad(theta2(i,j)+90-theta1(j))))*norm([bx(i,j),by(i,j)]))*0.0116;
%         7.65/norm([bx(i,j),by(i,j)])
    end
end
d2

function [ang,ax,ay,bx,by] = initImg(y,w2,h2,w3,h3)
ax = zeros(8,8);
ay = zeros(8,8);
bx = zeros(8,8);
by = zeros(8,8);
ang = zeros(8,8);
for j = 1:8
    for k = 1:8
        if j == 1 && k == 6
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),1320,220,220,240,320,j,k);
        elseif j == 2 && k == 8
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),1230,380,150,240,360,j,k);
        elseif j == 3 && k == 8
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),1230,380,150,270,360,j,k);
        else
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),y(k),w2(k),h2(k),w3(k),h3(k),j,k);
        end
        ax(j,k) = a(1);
        ay(j,k) = a(2);
        bx(j,k) = b(1);
        by(j,k) = b(2);
%         [j,k]
    end
    j
end
end

function [theta2,flFlat] = initAng(theta1,ri,ang)
theta2 = zeros(8,8);
fl = zeros(8,8);
flFlat = zeros(1,64);
for i = 1:8
    for j = 1:8
        theta2(i,j) = abs(ang(i,j)-90+theta1(j)-90);
        fl(j,i) = abs((i-1)*0.5*tan(deg2rad(theta2(i,j)+90-theta1(j))))*0.0116*48;
        flFlat((j-1)*8+i) = abs((i-1)*0.5*tan(deg2rad(theta2(i,j)+90-theta1(j))))*0.0116*48;
    end
end

theta1G = zeros(1,64);
riG = zeros(1,64);

for k = 1:8
    for l = 1:8
        theta1G((k-1)*8+l) = theta1(k);
        riG((k-1)*8+l) = ri(l);
    end
end

figure;
[xq,yq] = meshgrid(0:0.01:1.2,1.35:0.001:1.41);
vq = griddata(theta1G,flip(riG),flFlat,xq,yq);

mesh(xq,yq,vq)
hold on
plot3(theta1G,flip(riG),flFlat,'o')
xlim([0.1310941218 1.175])
% ylim([1.383 1.4025])
zlim([0 55])

end

function [theta, a, b] = img(i,y,w2,h2,w3,h3,j,k)
I = imread(i);
S = sum(I,3);
S2 = imcrop(S,[1100,y,120,100]);
S3 = imcrop(S,[1900,1200,w2,h2]);
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
% imshow(I);
% hold on;
% line([c(1),c(2)],[r(1),r(2)], 'Color', 'red', 'LineWidth', 2);
% line([c(2),c(3)],[r(2),r(3)], 'Color', 'red', 'LineWidth', 2);
% rectangle('Position', [1100,y,120,100], 'EdgeColor', 'r', 'LineWidth', 2)
% rectangle('Position', [1900,1200,w2,h2], 'EdgeColor', 'r', 'LineWidth', 2)
% rectangle('Position', [2400,1200,w3,h3], 'EdgeColor', 'r', 'LineWidth', 2)
% plot(c, r, 'r*', 'LineWidth', 2, 'MarkerSize', 3);

% cd RegionOverlays/
% print(sprintf('%d-%d',j,k),'-dpng')
% cd ..

[theta, a, b] = angle(c,r);
end

function [theta, a, b] = angle(x,y)
a = [x(1)-x(2),y(1)-y(2)];
b = [x(3)-x(2),y(3)-y(2)];
theta = acosd(dot(a,b)/(norm(a)*norm(b)));
end

function [r,c] = toR(x,y)
r = sum(x)/size(x,1);
c = sum(y)/size(y,1);
end
