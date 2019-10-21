clearvars;

opt = bodeoptions();
opt.FreqUnits = 'Hz';
opt.Grid = 'on';

%%%% Transferencia del filtro Legendre
s = tf('s');
H1 = -1/(s*1000*5.4e-9 + 1); % primera etapa: integrador compensado
% figure;
% bode(H1, opt);
H2 = get_sk_stage(3.5e3, 2.21e3, 3e-9, 1.5e-9);
% figure;
% bode(H2, opt);
H3 = get_sk_stage(1.1e3, 1.1e3, 16.3e-9, 820e-12);
% figure;
% bode(H3, opt);    
HL = H1*H2*H3;

w = 2*pi*logspace(3, 5, 1000);
superponedor('', 'leg-hf.csv', 'tc_tp5_ej1_leg_hf_spice.csv', HL, w)%, ...
%    'tc_tp5_ej1_leg_hf');
figHandles = findobj('Type', 'figure');
mag = figHandles(2);
mag = mag.CurrentAxes;
mag.NextPlot = 'add';
plot(mag, [1000, 33000, 33000], [-3, -3, -50], 'LineWidth',3, 'Color', 'r');
fase = figHandles(1);
fase = fase.CurrentAxes;

archivo = 'tc_tp5_ej1_leg';
saveas(fase,strcat(archivo,'_fase','.png'));
saveas(mag,strcat(archivo,'_mag','.png'));

% %%% Transferencia del filtro Bessel
% H1 = get_sk_stage(1e3, 1e3, 42.9e-9, 28.7e-9);
% H2 = get_sk_stage(18.1e3, 18.1e3, 2.1e-9, 2e-9);
% H3 = get_sk_stage(1.e3, 1e3, 63.7e-9, 15.2e-9);
% HB = H1*H2*H3;
% 
% w = 2*pi()*logspace(2, 5, 1000);
% superponedor('', 'bes-hf.csv', 'tc_tp5_ej1_bes6_hf_spice.csv', HB, w);
% figHandles = findobj('Type', 'figure');
% fase = figHandles(1);
% fase = fase.CurrentAxes;
% mag = figHandles(2);
% mag = mag.CurrentAxes;
% mag.NextPlot = 'add';
% plot(mag, [100, 2200, 2200], [-3, -3, -200], 'LineWidth', 3, 'Color', 'r');
% plot(mag, [10400, 10400, 100000], [50, -40, -40], 'LineWidth', 3, 'Color', 'r');

% archivo = 'tc_tp5_ej1_bes';
% saveas(fase,strcat(archivo,'_fase','.png'));
% saveas(mag,strcat(archivo,'_mag','.png'));
