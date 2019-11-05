%Polos sacados del programa de Pablo
clearvars;
p1 = -1.326e4 + 2.037e4*i;
p1c = conj(p1);
p2 = -1.912e4 + 9940*i;
p2c = conj(p2);
p3 = -2.08e4;

syms s;

eq1= (s+p1)*(s+p1c);
eq2 = (s+p2)*(s+p2c);
eq3 = s + p3;

expand(eq1);
eq1 = eq1/590764500; %Normalizo dividiendo por el termino independiente
expand(eq1);
wo1=sqrt(590764500); %El termino que acompaña s^2 es 1/wo
Q1 = 9846075 / (442*wo1);  %El termino que acompaña s es 1/(Q*wo)

expand(eq2);
eq2 = eq2/464378000; %Normalizo dividiendo por el termino independiente
expand(eq2);
wo2=sqrt(464378000); %El termino que acompaña s^2 es 1/wo
Q2 = 9846075 / (478*wo2);  %El termino que acompaña s es 1/(Q*wo)

H = 1/(eq1*eq2*eq3);