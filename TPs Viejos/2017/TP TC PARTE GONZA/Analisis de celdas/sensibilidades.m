syms R1 R2 R3 R4 R5 R6 C1 C2 RA RB
G = -R2/R6;
Q = R1/(R2*R3)^(1/2)*(C1/C2)^(1/2);
wp=sqrt(RA/(C1*C2*R2*R3*RB));
wz=sqrt(R5/(C1*C2*R2*R3*RA));
s1 = -wp/(2*Q)+sqrt(1/(2*Q)^2-1);
s2 = -wp/(2*Q)+sqrt(1/(2*Q)^2-1);
s1 = eval(s1);
s2 = eval(s2);