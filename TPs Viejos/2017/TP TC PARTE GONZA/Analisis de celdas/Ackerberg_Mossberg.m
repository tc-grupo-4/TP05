clear
%Real OpAmps
p = @(x,y) (x.*y./(x+y));
syms R k C Q Vin V1 V2 V3 V4 V5 V6 s A0 wp Rsum a b c d Vm Vout
A = A0/(s/wp+1);
Ra = Rsum/a;
Rb = Rsum/b;
Rc = Rsum/c;
Rd = Rsum/d;
ZC = 1/(s*C);
eq1 = (Vin-V1)/(R/k)+(V4-V1)/R+(V2-V1)/(p(Q*R,ZC)) == 0;
eq2 = V2 == -A*V1;
eq3 = (V2-V3)/R + (V6-V3)/ZC == 0;
eq4 = V4 == A*V3;
eq5 = (V4-V5)+(V6-V5)==0;
eq6 = V6 == -A*V5;
eq7 = (Vin-Vm)/Ra+(V2-Vm)/Rb+(V4-Vm)/Rc+(V6-Vm)/Rd+(Vout-Vm)/Rsum==0;
eq8 = Vout == -A*Vm;
eqsys = [eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8];
sol = solve(eqsys,V1,V2,V3,V4,V5,V6,Vm,Vout);
%Ideal case
names = fieldnames(sol);
sol_ideal = sol;
for i=1:length(names)
    sol_ideal.(names{i}) = simplify(limit(sol.(names{i}),A0,inf));
end
%Variables
R = 1/(2*pi*26.1e3*2.2e-9);
C = 2.2e-9;
k = 1;
Q = 4.5;
A0 = 200000;
fp = 75;
a = 1;
b = 1/Q;
c = 0;
d = 0;
%
wp = 2*pi*fp;
%Evaluate function
func2graf(1) = simplify(sol.V3/sol.V4);
func2graf(2) = simplify(sol_ideal.V3/sol_ideal.V4);
for i=1:length(func2graf)
    [num, den] = numden(func2graf(i));
    num1 = eval(num);
    den1 = eval(den);
    num1 = sym2poly(num1+0*s);
    den1 = sym2poly(den1+0*s);
    figure(1);
    ham = tf(num1,den1);
    opt = bodeplot(ham,2*pi*logspace(4,7,2000));
    setoptions(opt,'FreqUnits','Hz');
    hold on;
    figure(2);
    ham = tf(num1,den1);
    opt = bodeplot(ham);
    setoptions(opt,'FreqUnits','Hz');
    hold on;
end
hold off
