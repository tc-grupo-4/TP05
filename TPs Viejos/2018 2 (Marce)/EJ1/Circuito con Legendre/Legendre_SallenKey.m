% PB de orden 5 - Aproximado con Legendre %
clc;
s = tf('s');
D1N = s + 0.4681;
D2N = s^2 + 0.7762*s + 0.4971; 
D3N = s^2 + 0.3072*s + 0.9608;

fo = 32000;
wp = 2*pi*fo;

SLP = s/wp;

H1 = 1/(SLP + 0.4681);
H2 = 1/(SLP^2 + 0.7762*SLP + 0.4971);
H3 = 1/(SLP^2 + 0.3072*SLP + 0.9608);

% De la H1
wo1 = 9.412e4;
C_H1 = 10e-9
R_H1 = 1/(wo1*C_H1)

% % De la H2
wo2 = sqrt(4.04e15/2.011e5);
Q2 = wo2*2.011e5/3.138e10
K2 = 3-(1/Q2);

% % C1 = C2 = C
C_H2 = 150e-12 
% % R1 = R2 = R
R_H2 = 1/(wo2*C_H2)
RA_H2 = 1.2e3
RB_H2 = RA_H2*(2-(1/Q2))

% De la H3
wo3 = sqrt(7.809e15/2.011e5);
Q3 = wo2*2.011e5/1.242e10
K3 = 3-(1/Q3);
 
% C1 = C2 = C
C_H3 = 3.3e-9
% R1 = R2 = R
R_H3 = 1/(wo3*C_H3)
RA_H3 = 1e3
RB_H3 = RA_H3*(2-(1/Q3))

% H = H1*H2*H3
