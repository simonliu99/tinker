% constant values
y = [1550, 1500, 1450, 1420, 1370, 1320, 1280, 1230]; % height of box 1
width2 = [110, 120, 160, 150, 180, 220, 250, 380]; % width of box 2
height2 = [450, 400, 370, 330, 300, 220, 160, 150]; % height of box 2
width3 = [260, 260, 260, 260, 247, 250, 245, 260]; % width of box 3
height3 = [450, 400, 380, 370, 340, 320, 340, 360]; % height of box 3
theta1 = [0, 0.1310941218, 0.2645116236, 0.4029750993, 0.5502212263, 0.7123244348, 0.9015891079, 1.155588928]; % constant theta1 values
ri = [1.375177282, 1.379726782, 1.384001458, 1.388024636, 1.391817202, 1.395397886, 1.398783522, 1.401989263]; % constant refractive index values

% begin script
[phi,ax,ay,bx,by] = initImg(y,width2,height2,width3,height3);
[theta2,focallen] = initAng(theta1,ri,phi);
focallenM = zeros(8,8);
for i = 1:8
    for j = 1:8
        focallenM(i,j) = focallen(i*8-8+j);
    end
end

% analyze raw data pictures for angles and locations of points
function [ang,ax,ay,bx,by] = initImg(y,w2,h2,w3,h3)
ax = zeros(8,8);
ay = zeros(8,8);
bx = zeros(8,8);
by = zeros(8,8);
ang = zeros(8,8);
for j = 1:8
    for k = 1:8
        if j == 1 && k == 6 % manual box location corrections
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),1320,220,220,240,320,j,k);
        elseif j == 2 && k == 8 % manual
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),1230,380,150,240,360,j,k);
        elseif j == 3 && k == 8 % manual
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),1230,380,150,270,360,j,k);
        else % predefined box locations
            [ang(j,k), a, b] = img(sprintf('Raw/%d-%d.jpg',j,k),y(k),w2(k),h2(k),w3(k),h3(k),j,k);
        end 
        ax(j,k) = a(1);
        ay(j,k) = a(2);
        bx(j,k) = b(1);
        by(j,k) = b(2);
    end
end
end

% calculate values and plot with mesh on plot of fl vs dC and ri
function [theta2,flFlat] = initAng(theta1,ri,ang)
theta2 = zeros(8,8);
flFlat = zeros(1,64);
for i = 1:8
    for j = 1:8
        theta2(i,j) = abs(ang(i,j)-90+theta1(j)-90);
        flFlat((j-1)*8+i) = abs((i-1)*0.5*tan(deg2rad(theta2(i,j)+90-theta1(j))))*0.0116;
    end
end

% degree of curvature and refractive index organization
thet = [2.3	1.1475	0.57375	0.3825	0.286875	0.2295	0.19125	0.1639285714];
riG = zeros(1,64);
dC = zeros(1,64);
for k = 1:8
    for l = 1:8
        riG((k-1)*8+l) = ri(l);
        dC((k-1)*8+l) = 1/thet(k);
    end
end

% manual calculation
flFlat(1,6) = 2.056;
flFlat(1,7) = 2.108;

% normalization of focal lengths to match model
flFlatNorm = zeros(1,64);
for m = 1:64
    flFlatNorm(m) = flFlat(m)*6.130435155/max(flFlat);
end

% mesh plot
figure;
[xq,yq] = meshgrid(0.16:0.05:6.25,1.35:0.0003:1.41);
vq = griddata(dC,flip(riG),flFlatNorm,xq,yq);
mesh(xq,yq,vq)
hold on
plot3((dC),flip(riG),flFlatNorm,'o');
xlim([0.16 6.25])
zlim([0 6.14])
xlabel('Curvature (cm^-^1)')
ylabel('Refractive Index')
zlabel('Focal Length (cm)')
title('Experimental Focal Length versus Degree of Curvature and Refraction Index')

% model plot
figure;
[xq,yq] = meshgrid(0.16:0.02:6.25,1.35:0.001:1.41);
vq = griddata(dC,riG,model(),xq,yq);
mesh(xq,yq,vq)
hold on
plot3((dC),riG,model(),'o');
xlim([0.16 6.25])
zlim([0 6.14])
xlabel('Curvature (cm^-^1)')
ylabel('Refractive Index')
zlabel('Focal Length (cm)')
title('Maths Model of Focal Length versus Degree of Curvature and Refraction Index')

% residual plot preparation
mod = model();
flFlatNormSwap = zeros(1,64);
for n = 1:8
    for o = 1:8
        flFlatNormSwap((n-1)*8+o) = flFlatNorm((n-1)*8+(8-o+1));
    end
end

% ssim calculation between experimental and model data
[ssimval, ssimmap] = ssim(flFlatNormSwap,mod);
ssimval
figure, imshow(ssimmap,[]);
res = mod - flFlatNormSwap;
figure, scatter(1:64, res);
xlim([0,64])
xlabel('Trial')
ylabel('Residual (cm)')
title('Discrepancy Between Model and Experimental Data')

% residual plot
figure;
[xq,yq] = meshgrid(0.16:0.001:6.25,1.35:0.0001:1.41);
vq = griddata(dC,riG,res,xq,yq);
mesh(xq,yq,vq)
hold on
xlabel('Curvature (cm^-^1)')
ylabel('Refractive Index')
zlabel('Residual (cm)')
title('Residual Heat Map')

end

% analyze image to find bright spots and return vectors and angle
function [phi, a, b] = img(i,y,w2,h2,w3,h3,j,k)
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

% display output image
% figure; % commented to reduce system lag
imshow(I);
hold on;
line([c(1),c(2)],[r(1),r(2)], 'Color', 'red', 'LineWidth', 2);
line([c(2),c(3)],[r(2),r(3)], 'Color', 'red', 'LineWidth', 2);
rectangle('Position', [1100,y,120,100], 'EdgeColor', 'r', 'LineWidth', 2)
rectangle('Position', [1900,1200,w2,h2], 'EdgeColor', 'r', 'LineWidth', 2)
rectangle('Position', [2400,1200,w3,h3], 'EdgeColor', 'r', 'LineWidth', 2)
plot(c, r, 'r*', 'LineWidth', 2, 'MarkerSize', 3);

% save output image
cd Overlays/
print(sprintf('%d-%d',j,k),'-dpng')
cd ..

[phi, a, b] = angle(c,r);
end

% find angle between two vectors given three points
function [theta, a, b] = angle(x,y)
a = [x(1)-x(2),y(1)-y(2)];
b = [x(3)-x(2),y(3)-y(2)];
theta = acosd(dot(a,b)/(norm(a)*norm(b)));
end

% average multiple bright spots to one point
function [r,c] = toR(x,y)
r = sum(x)/size(x,1);
c = sum(y)/size(y,1);
end

function [xG] = model()
ri = [1.375177282, 1.379726782, 1.384001458, 1.388024636, 1.391817202, 1.395397886, 1.398783522, 1.401989263]; % constant refractive index values

% data from Google Sheets
x = [6.130435155	3.058554061	1.52927703	1.01951802	0.7646385152	0.6117108122	0.5097590101	0.4369362943
6.056986527	3.021909583	1.510954791	1.007303194	0.7554773956	0.6043819165	0.5036515971	0.4317013689
5.98956059	2.98269903	1.494134952	0.9960899677	0.7470674758	0.5976539806	0.4980449839	0.4268957004
5.927458682	2.957286451	1.478643226	0.9857621504	0.7393216128	0.5914572902	0.4928810752	0.422469493
5.870084292	2.92866162	1.46433081	0.9762205399	0.7321654049	0.5857323239	0.4881102699	0.4183802313
5.816925388	2.902139949	1.451069975	0.9673799831	0.7255349873	0.5804279898	0.4836899915	0.4145914212
5.767540221	2.877501045	1.438750523	0.959167015	0.7193752613	0.575500209	0.4795835075	0.4110715778
5.721545844	2.854553851	1.427276925	0.9515179502	0.7136384627	0.5709107701	0.4757589751	0.4077934072];

% create one-dimensional matrix
xG = zeros(1,64);
for i = 1:8
    for j = 1:8
        xG((j-1)*8+i) = x(i,j);
    end
end
% xG

% create dC and riG matrices
thet = [2.3	1.1475	0.57375	0.3825	0.286875	0.2295	0.19125	0.1639285714];
dC = zeros(1,64);
riG = zeros(1,64);

for k = 1:8
    for l = 1:8
        riG((k-1)*8+l) = ri(l);
        dC((k-1)*8+l) = 1/thet(k);
    end
end
end