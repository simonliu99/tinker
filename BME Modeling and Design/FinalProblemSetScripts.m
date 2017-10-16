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

% 2b ## NOT DONE
%imagesc(Asig);
B2 = Asig/magic(13);
%B2 = inv(magic(13))*Asig
%imagesc(B2)

% Question 3

% 3a
computeC_b = @(D,V,k_a,k_e,t) ((D/V)*(k_a/(k_a-k_e))*(exp(-k_e*t)-exp(-k_a*t)));

% 3b
t = linspace(0,8);
C_b = computeC_b(80, 25, 1.6, 0.4, t);
figure;plot(t,C_b);

% 3c
t = linspace(0,12);
C_b = computeC_b(80, 25, 1.6, 0.4, t);
figure;plot(t,C_b);

% 3d
M = find(max(C_b) == C_b);
xM = t(M);
yM = C_b(M);
maxM = [xM,yM]

% 3e
t = linspace(0,12);
C_b = computeC_b(80, 25, 1.6, 0.4, t);
for i = 1:length(C_b)
    if(C_b(i) > 1.5); C_b(i) = 1.5; end
end
figure;plot(t, C_b);

% Question 4
bmt = @(x1,x2) [sqrt(-2*log(x1))*cos(2*pi*x2),sqrt(-2*log(x1))*sin(2*pi*x2)];
bmt(rand,rand);
params = main(1000);
hist(params(:,1:1));
figure;
hist(params(:,2:2));
figure;
hist(params(:,3:3));
figure;
hist(params(:,4:4));

function y = main(n)
bmt = @(x1,x2) [sqrt(-2*log(x1))*cos(2*pi*x2),sqrt(-2*log(x1))*sin(2*pi*x2)];
z = [];
for i = 1:n
    z = cat(1,z,[bmt(rand,rand),rand, randn]);
end
y = z;
end