function [Gb,G1,Ga1,Ga2,G41,G42,C21,C22,C3]=   getCompValues( Q, w0, wz, n2 , Q0, C, Gb)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
K = 1+(1-Q0/Q)/(2*Q0^2);
G4 = C*w0/(2*Q0);
Ga = (K-1)*Gb;
k = n2*(wz/w0)^2/(1-Q0/Q);
n = k*(1-Q0/(K*Q));
m = k*(K-1)*(1+2*Q0^2*(w0/wz)^2)/K;
G1 = 4*Q0^2*G4;

Ga1 = (1-k)*Ga;
Ga2 = k * Ga;

G41 = (1-n)*G4;
G42 = n * G4;

C21 = (1-m)*C;
C22 = m *C;

C3 = C;

%fprintf('Gb = %e KOhm G1 = %e KOhm \n Ga1= %e KOhm Ga2= %e KOhm \n G41= %e KOhm G42= %e KOhm \n C21= %e nf C22=%e nf C3= %e nf \n',1/Gb/1e3,1/G1/1e3,1/Ga1/1e3,1/Ga2/1e3,1/G41/1e3,1/G42/1e3,C21/1e-9,C22/1e-9,C3/1e-9);

end

