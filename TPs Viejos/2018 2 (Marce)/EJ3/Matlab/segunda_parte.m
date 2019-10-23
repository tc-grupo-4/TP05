clear;
clc;
%--TP Pablo--%
%con Ap = 1db, As = 45db, wp = 11000, ws = 20500 -0.5db
w0 = 220935.8;
wz = 71273.11;
Q = 0.81;
% estas cosas no dependen de n2
n2 = 10^(1.73/20);
%---Esto lo fijo yo-%
Q0 = (1/2.57)*Q;
%Q0 = (1/3)*Q; % Q0
C = 22e-9;
Gb = 1/1000;
%------------%
getCompValues(Q,w0,wz, n2 , Q0, C , Gb)