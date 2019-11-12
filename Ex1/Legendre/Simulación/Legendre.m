%Polos sacados del programa de Pablo
clearvars;
p1 = -3.284e4 + 2.069e5*i;
p1c = conj(p1);
p2 = -8.299e4 + 1.258e5*i;
p2c = conj(p2);
p3 = -1.001e5;

syms s;

eq1= (s+p1)*(s+p1c);
eq2 = (s+p2)*(s+p2c);
eq3 = s + p3;

expand(eq1);
eq1 = eq1/43886075600; %Normalizo dividiendo por el termino independiente
expand(eq1);
wo1=sqrt(43886075600); %El termino que acompaña s^2 es 1/wo
Q1 = 548575945 / (821*wo1);  %El termino que acompaña s es 1/(Q*wo)

expand(eq2);
eq2 = eq2/22712980100;
wo2=sqrt(22712980100); %El termino que acompaña s^2 es 1/wo
Q2 = 1135649005 / (8299*wo2);  %El termino que acompaña s es 1/(Q*wo)

H= 1/((s+p1)*(s+p1c)*(s+p2)*(s+p2c)*(s+p3));
expand(H)