clear;
clc;
%--TP Pablo--%
%con Ap = 1db, As = 45db, wp = 11000, ws = 20500 -0.5db
wz = 71273.16;
w0 = 129062.66;
Q = 4.41;
% estas cosas no dependen de n2
n2 = 10^(-3.23/20);
%---Esto lo fijo yo-%
Q0 = (1/1.6)*Q;
%Q0 = (1/3)*Q; % Q0
C = 10e-9;
Gb = 1/100;
%------------%
for i = 0:0.1:2
    base = 1;
    Q0 = i+base;
    nominalVal = 6.8e-9;
    [Gb,G1,Ga1,Ga2,G41,G42,C21,C22,C3] = getCompValues(Q,w0,wz, n2 , Q0, C , Gb);
    if(abs(C22-nominalVal)< nominalVal*5/100)
        fprintf('Gb = %e KOhm G1 = %e KOhm \n Ga1= %e KOhm Ga2= %e KOhm \n G41= %e KOhm G42= %e KOhm \n C21= %e nf C22=%e nf C3= %e nf \n',1/Gb/1e3,1/G1/1e3,1/Ga1/1e3,1/Ga2/1e3,1/G41/1e3,1/G42/1e3,C21/1e-9,C22/1e-9,C3/1e-9);
        disp(' ')
    end
end


G1 = (1/(1.760949e-01*1e3));
G4= (1/(4.373903*1e3)) + (1/(1.545703e+01*1e3));
Q0 = sqrt(G1/(4*G4))

% Ahora estoy con este
%Con Gb = 108 anda JOYITISIMA sola
% Gb = 1.000000e-01 KOhm G1 = 1.760949e-01 KOhm 
%  Ga1= 3.327871e+00 KOhm Ga2= 4.603886e+00 KOhm 
%  G41= 4.373903e+00 KOhm G42= 1.545703e+01 KOhm 
%  C21= 3.238385e+00 nf C22=6.761615e+00 nf C3= 1.000000e+01 nf 

% VSAT = 13.5;
% GMaxdB = 12;
% GMax = 10^(12/20);
% Vimax = VSAT/GMax;
%Gmax es donde esta el sobrepico
%vi min piso de ruido
% Vimin = 10e-3;
% RD = 20 * log10(Vimax/Vimin);
% GMax
