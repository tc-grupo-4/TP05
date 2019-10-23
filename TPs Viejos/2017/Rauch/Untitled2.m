s=tf('s');
H1=-(s*7.3715e-6)/(s^2*1.3785e-11+s*1.843e-6+1);
H2=-(s*1.0428e-6)/(s^2*1.54856e-11+2.6289e-6*s+1);
bodeplot(H1,'green');
hold on;
grid on;
Htot=H1+H2;
bodeplot(H2,'blue');
bodeplot(Htot,'red');
