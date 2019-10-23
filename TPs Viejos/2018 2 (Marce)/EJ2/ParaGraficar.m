% Formulas para graficos %
clc;
s = tf('s');

R1 = 3.3e3;
K = 0.162;
C = 470e-12;
a = 0.033;
R2 = 29.7e3;

H1 = (1/(1-K))*(a*s/(C*R1))/((s^2) + s*(2/(C*R2))*(1-(R2*K/(2*R1*(1-K)))) + (1/((C^2)*R1*R2)));

R1 = 1.39e3;
K = 0.165;
C = 1e-9;
a = 0.033;
R2 = 12.6e3;

H2 = (1/(1-K))*(a*s/(C*R1))/((s^2) + s*(2/(C*R2))*(1-(R2*K/(2*R1*(1-K)))) + (1/((C^2)*R1*R2)));

% Esta es la transferencia %
H = H1*H2;
%%% 

K = 0.162;
C = 470e-12;
R2 = 29.7e3;

% Esta es la Zin % 
Zin = 100000/(1 - H1*(((1-K)/(s*C*R2)) + K));
bode(Zin)
%%%