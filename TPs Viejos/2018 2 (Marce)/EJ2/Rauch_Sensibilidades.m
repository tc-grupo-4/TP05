% Rauch - Sensibilidades%
clc;
R1 = sym('R1');
R2 = sym('R2');
C = sym('C');

wo = (2/(R2*C))*sqrt(R2/(4*R1));
dwo_R1 = diff(wo,R1);
dwo_R2 = diff(wo,R2);
dwo_C = diff(wo,C);
Swo_R1 = dwo_R1 * R1 / wo;
Swo_R2 = dwo_R2 * R2 / wo;
Swo_C = dwo_C * C / wo;

% Celda 1 %
% R1 = 2280;
% R2 = 20500;
% C = 680e-12;
% 
% eval(Swo_R1)
% eval(Swo_R2)
% eval(Swo_C)

% Celda 2 %
% R1 = 1390;
% R2 = 12600;
% C = 1e-9;
% 
% eval(Swo_R1)
% eval(Swo_R2)
% eval(Swo_C)
K = sym('K');
% 
% Q = 1.5/(1-(2*1.5*1.5*K/(1-K)));
% dQ_K = diff(Q,K);
% SQ_K = dQ_K * K / Q;

% K = 0.155;
% eval(SQ_K)

a = sym('a');
wo = sym('wo');

H = (1/(1-K))*(a*1i*wo/(C*R1))/(((1i*wo)^2) + 1i*wo*(2/(C*R2))*(1-(K/(2*R1*R2*(1-K)))) + (1/((C^2)*R1*R2)));
Habs = a*wo/(C*R1*(K-1)*sqrt((-(wo^2) + (1/(C*C*R1*R2)))^2 + (2*wo*(1+(K/(2*R1*R2*(K-1))))/(C*R2))^2));
dH_R1 = diff(Habs,R1);
dH_R2 = diff(Habs,R2);
dH_C = diff(Habs,C);
dH_K = diff(Habs,K);

SH_R1 = dH_R1 * R1 / Habs;
SH_R2 = dH_R2 * R2 / Habs;
SH_C = dH_C * C / Habs;
SH_K = dH_K * K / Habs;

R1 = 3300;
R2 = 29700;
C = 470e-12;
K = 0.155;
a = 0.033;
wo = 2*pi*36000;

eval(SH_R1)
eval(SH_R2)
eval(SH_C)
eval(SH_K)