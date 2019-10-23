% Formulas para graficos Legendre %
clc;
s = tf('s');

R1 = 172e3;
RA = 10e3;
RB = 2.2e3;
K = 1+(RB/RA);
C = 1e-9;
R2 = 172e3;
a = 1;

% s = sym('s');
% R1 = sym('R1');
% R2 = sym('R2');
% RA = sym('RA');
% RB = sym('RB');
% C = sym('C');
% K = sym('K');
% a = sym('a');

H1 = (a*K/(R1*R2*(C^2))) / ((s)^2 + s*(((1/R1)+((2-K)/R2))/(C)) + (1/(R1*R2*(C^2))));

R1 = 1.5e3;
RA = 2.2e3;
RB = 2e3;
K = 1+(RB/RA);
C = 100e-9;
R2 = 1.5e3;
a = 1.5/2.2;

H2 = (a*K/(R1*R2*(C^2))) / ((s)^2 + s*(((1/R1)+((2-K)/R2))/(C)) + (1/(R1*R2*(C^2))));

Cf = 100e-9;
Rf = 1.8e3;
Rr = 2.9e3;

H3 = Rf/(Rr*(s*Cf*Rf+1));

% Esta es la transferencia %
H = H1*H2*H3;
%%% 

R1 = 172e3;
RA = 10e3;
RB = 2.2e3;
K = 1+(RB/RA);
C = 1e-9;
R2 = 172e3;
a = 1;

% Esta es la Zin % 
Zin = R1/(a*(1-(H1*RA*(s*C*R2+1)/(RA+RB))));
%%%