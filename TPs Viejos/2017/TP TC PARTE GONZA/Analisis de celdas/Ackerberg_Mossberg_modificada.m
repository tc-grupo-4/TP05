clear
%Real OpAmps
p = @(x,y) (x.*y./(x+y));
syms R k C Q Vin V1 V2 V3 V4 V5 V6 s A0 wp a b c r
A = A0/(s/wp+1);
ZC = 1/(s*C);
ZaC =1/(s*a*C);
eq1 = (Vin-V1)/(p(R/k,ZaC))+(V4-V1)/R+(V2-V1)/(p(Q*R,ZC)) == 0;
eq2 = V2 == -A*V1;
eq3 = (V2-V3)/R + (V6-V3)/ZC+(Vin-V3)/(R/c) == 0;
eq4 = V4 == A*V3;
eq5 = (V4-V5)/r+(V6-V5)/r+(Vin-V5)/(R/b)==0;
eq6 = V6 == -A*V5;
eqsys = [eq1,eq2,eq3,eq4,eq5,eq6];
sol = solve(eqsys,V1,V2,V3,V4,V5,V6);
%Ideal case
names = fieldnames(sol);
sol_ideal = sol;
for i=1:length(names)
    sol_ideal.(names{i}) = simplify(limit(sol.(names{i}),A0,inf));
end
%Variables

C = 2.2e-9;
R = 1/(2*pi*26.1e3*2.2e-9);
k = 0;
Q = 4.5;
A0 = 200000;
fp = 75;
a = 1;
b =0;
c = 1;
r = R;
%
wp = 2*pi*fp;
%Evaluate function
func2graf(1) = simplify(sol.V2/Vin);
func2graf(2) = simplify(sol_ideal.V2/Vin);
for i=1:length(func2graf)
    [num, den] = numden(func2graf(i));
    num1 = eval(num);
    den1 = eval(den);
    num1 = sym2poly(num1+0*s);
    den1 = sym2poly(den1+0*s);
    figure(1);
    hamm = tf(num1,den1);
    opt = bodeplot(hamm,2*pi*logspace(log10(23e3),log10(29e3),2000));
    setoptions(opt,'FreqUnits','Hz','PhaseVisible','off');
    hold on;
    figure(2);
    hamm = tf(num1,den1);
    opt = bodeplot(hamm);
    setoptions(opt,'FreqUnits','Hz','PhaseVisible','off');
    hold on;
end
hold off
