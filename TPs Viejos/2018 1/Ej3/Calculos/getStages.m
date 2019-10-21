function [H1, H2] = getStages()
w0_p1 = 21319*2*pi;
Q_p1 = 4.97;
%w0_z1 = 5875*2*pi;  %Q = infinito
w0_z1 = 12937*2*pi;


w0_p2 = 35655*2*pi;
Q_p2 = 0.82;
%w0_z2 = 12937*2*pi;
w0_z2 = 5875*2*pi;  %Q = infinito

s = tf('s')

H1 = 10^(-0.5/20)*(s^2+w0_z1^2)/(s^2 + s*w0_p1/Q_p1 + w0_p1^2);
H2 = 10^(-1/20)*(s^2+w0_z2^2)/(s^2 + s*w0_p2/Q_p2 + w0_p2^2);

