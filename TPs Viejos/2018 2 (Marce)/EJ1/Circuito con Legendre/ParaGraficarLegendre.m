% Formulas para graficos Legendre %
clc;
s = tf('s');

R1 = 47e3;
RA = 1.2e3;
RB = 1.08e3;
K = 1+(RB/RA);
C = 150e-12;
R2 = 47e3;
a = 47/68;

% s = sym('s');
% R1 = sym('R1');
% R2 = sym('R2');
% RA = sym('RA');
% RB = sym('RB');
% C = sym('C');
% K = sym('K');
% a = sym('a');

H1 = (a*K/(R1*R2*(C^2))) / ((s)^2 + s*(((1/R1)+((2-K)/R2))/(C)) + (1/(R1*R2*(C^2))));

R1 = 1.54e3;
RA = 1e3;
RB = 1.56e3;
K = 1+(RB/RA);
C = 3.3e-9;
R2 = 1.54e3;
a = 1.54/4.7;

H2 = (a*K/(R1*R2*(C^2))) / ((s)^2 + s*(((1/R1)+((2-K)/R2))/(C)) + (1/(R1*R2*(C^2))));

Cf = 10e-9;
Rf = 1e3;
Rr = 1.12e3;

H3 = Rf/(Rr*(s*Cf*Rf+1));

% Esta es la transferencia %
H = H1*H2*H3;
%%% 

R1 = 47e3;
RA = 1.2e3;
RB = 1.08e3;
K = 1+(RB/RA);
C = 150e-12;
R2 = 47e3;
a = 47/68;

% Esta es la Zin % 
Zin = R1/(a*(1-(H1*RA*(s*C*R2+1)/(RA+RB))));
bode(Zin)
%%%