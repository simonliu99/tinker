% Question 1
A1 = eye(3) + flip(eye(3),1);

% 1d
B1 = A1;
for r = 1:3
    for c = 1:3
        if B1(r,c) > 1; B1(r,c) = 1; end
    end
end
B1

%1e
C1 = B1;
for r = 1:3
    for c = 1:3
        if C1(r,c) == 0; C1(r,c) = 1; end
    end
end
C1

% Question 2

% 2a
A2 = zeros(4,4);
for i = 1:length(A2(:,1))
    for j = 1:length(A2(1,:))
        if(i==j); A2(i,j) = 1; end
    end
end
A2

% 2b
Asig = [659,751,429,997,950,582,934,582,950,583,797,490,1105;561,681,317,983,880,512,878,512,880,527,713,392,1105;632,780,374,969,810,611,822,611,810,640,798,463,1105;703,710,431,955,740,710,766,710,740,753,714,534,1105;618,653,501,941,670,822,879,822,670,879,643,618,1105;533,765,571,1096,613,921,823,921,613,992,572,702,1105;448,695,472,1082,543,864,767,864,543,949,488,617,1105;363,625,373,1068,486,794,711,794,486,893,417,519,1105;265,555,274,1054,416,737,668,737,416,850,333,434,1105;349,667,344,1040,528,667,625,667,528,794,431,518,1105;420,610,414,1039,627,610,569,610,627,751,516,433,1105;504,709,484,1025,739,540,695,540,739,695,614,504,1105;575,639,541,1011,838,470,808,470,838,639,699,406,1105];
imagesc(Asig);
title('Signal downloaded from Blackboard')
Bsig = magic(13)\Asig;
figure;imagesc(Bsig);
title('Inverse Matrix Unmasking')

% Question 3

% 3a
computeC_b = @(D,V,k_a,k_e,t) ((D/V)*(k_a/(k_a-k_e))*(exp(-k_e*t)-exp(-k_a*t)));

% 3b
t = linspace(0,8,10000);
C_b = computeC_b(80, 25, 1.6, 0.4, t);
figure;plot(t,C_b);
title('C_b from t=0 to t=8')

% 3c
t = linspace(0,12,10000);
C_b2 = computeC_b(80, 25, 1.6, 0.4, t);
figure;plot(t,C_b2);
title('C_b from t=0 to t=12')

% 3d
M = find(max(C_b2) == C_b2);
xM = t(M);
yM = C_b2(M);
maxM = [xM,yM]

% 3e
t = linspace(0,12,10000);
C_b3 = computeC_b(80, 25, 1.6, 0.4, t);
for i = 1:length(C_b3)
    if(C_b3(i) > 1.5); C_b3(i) = 1.5; end
end
figure;plot(t,C_b3);
title('Controlled C_b from t=0 to t=12')

% Question 4
bmt = @(x1,x2) [sqrt(-2*log(x1))*cos(2*pi*x2),sqrt(-2*log(x1))*sin(2*pi*x2)];
bmt(rand,rand);
params = main(1000);
figure;
hist(params(:,1:1));
title('z_1 Distribution')
figure;
hist(params(:,2:2));
title('z_2 Distribution')
figure;
hist(params(:,3:3));
title('rand Distribution')
figure;
hist(params(:,4:4));
title('randn Distribution')

function y = main(n)
bmt = @(x1,x2) [sqrt(-2*log(x1))*cos(2*pi*x2),sqrt(-2*log(x1))*sin(2*pi*x2)];
z = [];
for i = 1:n
    z = cat(1,z,[bmt(rand,rand),rand, randn]);
end
y = z;
end