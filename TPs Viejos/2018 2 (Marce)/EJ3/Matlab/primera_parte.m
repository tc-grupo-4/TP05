clear;
clc;
%--TP Pablo--%
%con Ap = 1db, As = 45db, wp = 11000, ws = 20500 -0.5db
w0 = 129062.66;
wz = 31779.06;
Q = 4.41;
% estas cosas no dependen de n2
n2 = 10^(-3.23/20);
%---Esto lo fijo yo-%
Q0 = (1/1.6)*Q;
%Q0 = (1/3)*Q; % Q0
C = 10e-9;
Gb = 1/100;
%------------%
getCompValues(Q,w0,wz, n2 , Q0, C , Gb)

VSAT = 13.5;
GMaxdB = 12;
GMax = 10^(12/20);
Vimax = VSAT/GMax;
%Gmax es donde esta el sobrepico
%vi min piso de ruido
Vimin = 10e-3;
RD = 20 * log10(Vimax/Vimin);
GMax
