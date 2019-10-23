% Sallen-Key Bessel %
clc;
R1 = sym('R1');
R2 = sym('R2');
C = sym('C');
K = sym('K');
RA = sym('RA');
RB = sym('RB');
wo = sym('wo');

H = (K/(R1*R2*(C^2))) / ((1i*wo)^2 + 1i*wo*(((1/R1)+((2-K)/R2))/(C)) + (1/(R1*R2*(C^2))));
Habs = (K/(R1*R2*(C^2))) / sqrt((wo*(((1/R1)+((2-K)/R2))/(C)))^2 + ((1/(R1*R2*(C^2))) - wo^2)^2);

wof = sqrt(1/(R1*R2*(C^2)));
Q = sqrt(1/(R1*R2)) / ((1/R1) + ((1-(RB/RA))/R2));

dwof_R1 = diff(wof,R1);
dwof_R2 = diff(wof,R2);
dwof_C = diff(wof,C);

Swof_R1 = dwof_R1 * R1 / wof;
Swof_R2 = dwof_R2 * R2 / wof;
Swof_C = dwof_C * C / wof;


dQ_R1 = diff(Q,R1);
dQ_R2 = diff(Q,R2);
dQ_RA = diff(Q,RA);
dQ_RB = diff(Q,RB);

SQ_R1 = dQ_R1 * R1 / Q;
SQ_R2 = dQ_R2 * R2 / Q;
SQ_RA = dQ_RA * RA / Q;
SQ_RB = dQ_RB * RB / Q;


dG_R1 = diff(Habs,R1);
dG_R2 = diff(Habs,R2);
dG_C = diff(Habs,C);

SG_R1 = dG_R1 * R1 / Habs;
SG_R2 = dG_R2 * R2 / Habs;
SG_C = dG_C * C / Habs;

% Celda 1
% R1 = 172e3;
% RA = 10e3;
% RB = 2.2e3;
% K = 1+(RB/RA);
% C = 1e-9;
% R2 = 172e3;
% wo = 2*pi*1040;
% 
% eval(Swof_C)
% eval(Swof_R1)
% eval(Swof_R2)
% eval(SQ_R1)
% eval(SQ_R2)
% eval(SQ_RA)
% eval(SQ_RB)
% eval(SG_R1)
% eval(SG_R2)
% eval(SG_C)

% Celda 2
R1 = 1.53e3;
RA = 2.2e3;
RB = 2e3;
K = 1+(RB/RA);
C = 100e-9;
R2 = 1.53e3;
wo = 2*pi*873.76;

eval(Swof_C)
eval(Swof_R1)
eval(Swof_R2)
eval(SQ_R1)
eval(SQ_R2)
eval(SQ_RA)
eval(SQ_RB)
eval(SG_R1)
eval(SG_R2)
eval(SG_C)