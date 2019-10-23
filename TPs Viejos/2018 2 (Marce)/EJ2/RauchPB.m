warning('off','all');
clc;
Ap = 1;
k = 1:1:4;
n = 2;

E = sqrt(10^(Ap/10) - 1);
a = (2*k-1)*pi/(2*n);
b = asinh(1/E)/n;

poles = sin(a)*sinh(b) + 1i*cos(a)*cosh(b);

s = tf('s');
H = 1/((s-poles(3))*(s-poles(4)));

wp = 2*pi*36000;
SBP = 8.5*((s/wp)+(wp/s));

HBP = 1/(SBP^2 + (-2*real(poles(3)))*SBP + (abs(poles(3)))^2 );

HBP_Poles = pole(HBP);

(s-HBP_Poles(2))*(s-HBP_Poles(3));
(s-HBP_Poles(4))*(s-HBP_Poles(5));

Qo = 1.5;
Q = 8.5;
wo1 = sqrt(5.685e10);
wo2 = sqrt(4.605e10);
alpha = (1-(Qo/Q))/(2*(Qo^2));
K = alpha/(1+alpha);
H = Qo*(1-K)/Q;

C = 470e-12
R2 = 2*Qo/(wo2*C)
R1 = R2/(4*(Qo^2))
a = H/(2*(Qo^2));
R1in = R1/a
R1masa = R1/(1-a)
Rmasa = 9900*K
Rfeed = 9900*(1-K)


