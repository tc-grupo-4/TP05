a=csvread('IMPEDANCIA ENTRADA ETAPA1.txt');


semilogx(a(:,1),10.^(a(:,2)/20),'LineWidth',1.5);

% hold on
 %semilogx(a(:,1),(a(:,3)),'LineWidth',1.5);


 hold on
 grid on 
 title('Impedancia de entrada')
 ylabel('Impedancia (Ohms)')
 xlabel('Frecuencia (Hz)')
 