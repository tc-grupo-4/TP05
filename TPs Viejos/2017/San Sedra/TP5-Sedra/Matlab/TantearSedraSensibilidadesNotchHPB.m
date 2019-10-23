function [c22_opt_wo_wz_Q,n_opt_wo_wz_Q,gb_opt_wo_wz_Q, componentes_wo_opt, componentes_wz_opt, componentes_q_opt] = TantearSedraSensibilidadesNotchHPB(wo,wz,Q,GBW,Q0)

syms ga1 ga2 gb c21 c22 g41 g42 c3 g1 k K m n n0 n2;

%------------------------------%
%seteo con que precision calcular varibles (VPA)%

digits(8);

%-------------------------------%
%PASO 1: sacar k,K,n,m

K = 1+(1-Q0/Q)/(2*Q0^2);
ecuacion2 = k == m*(K/(K-1))/(1+2*(Q0^2)*((wo/wz)^2));
ecuacion3 = k == n/(1-Q0/(K*Q)) ;

%-------------------------------%
%PASO 2: elegir c21,c22,c3 (que verifiquen siguientes ecuaciones)

ecuacion5 = c21 == c22*1.05*(1-m)/m; %el 1,05 por el 5%

ecuacion8 = c3 == c21+c22;

%-------------------------------%
%PASO 3: tengo en cuenta la correccion que se hace por el amplificador
%operacional real

wp = wo*(1+Q0*(wo/(GBW*2*pi)));
Qp = Q*(1-2*Q0*Q*(wo/(2*pi*GBW))*(1/(2*Q)-wo/(2*pi*GBW)));


%-------------------------------%
%PASO 4: calculo g1 y (g42+g41), teniendo en cuenta la correcion de wo por
%wp

ecuacion9 = g1 == 2*Q0*wp*sqrt(c3*(c21+c22));
ecuacion10 = g41+g42==g1/(4*Q0^2);


%-------------------------------%
%PASO 5:  determinando gb, obtenemos ga1+ga2

ecuacion11 = ga1+ga2 == (gb*c3/g1)*(1/Qp + 2*(g41+g42)/c3);


%-------------------------------%
%PASO 6: ecuacion que tiene relacion entre ga2 y g42

ecuacion12 = ga2 == g42*2*(ga1+gb)/(g1+g41*2);


%-------------------------------%
%PASO 7: otra relacion que tiene ga2 y g42
ecuacion13 = ga2 == ((g1/c3)*(ga1+gb)*g42-(wz^2)*c22*(ga1+gb))/((wz^2)*(c22-c3)+(g1/c3)*g41);


%-------------------------------%
%PASO 8: resuelvo Paso7 y Paso6 para determinar ga2 (y por ende ga1) y g42
%(y por ende g41)



ecuacion14 = ga2 == -(2*(wz^2)*c22*(ga1+gb)*c3)/(2*c22*c3*(wz^2)-2*(c3^2)*(wz^2)-(g1^2));
ecuacion15 = g42 == (g1+2*g41)*(wz^2)*c22*c3/((2*c22*c3*wz^2)-2*(c3^2)*wz*(g1^2));

%PASO 9: determino el valor de n2

ecuacion16 = n2 == (ga1+ga2+gb)*c22/(gb*(c3))-ga2/gb;




%-------------------------------%%-------------------------------%%-------------------------------%%-------------------------------%
%DESPEJES EN FUNCIÓN DE LAS VARIABLES A OPTIMIZAR


%k
k_1 = vpa(ecuacion3); %en funcion de n


%m
m_1 = subs(ecuacion2,k,solve(k_1,k)); %me saco de encima k
m_1 = vpa(m_1);

%c21
c21_1 = subs(ecuacion5,m,solve(m_1,m)); %me saco de encima m
c21_1 = vpa(c21_1);

%c3
c3_1 = subs(ecuacion8,c21,solve(c21_1,c21)); %me saco de encima c21
c3_1 = vpa(c3_1);

%g1
g1_1 = subs(ecuacion9,c3,expand(solve(c3_1,c3))); %me saco de encima c3
g1_1 = vpa(g1_1);
g1_2 = subs(g1_1,c21,solve(c21_1,c21)); %me saco de encima c21
g1_2 = vpa(g1_2);
g1_3 = expand(g1_2);


%g42
g42_1 = subs(ecuacion15,g41,solve(ecuacion10,g41)); %me saco de encima g41
g42_1 = vpa(g42_1);
g42_2 = subs(g42_1, g1, solve(g1_3,g1)); %me saco de encima g1
g42_2 = vpa(g42_2);
g42_3 = subs(g42_2,c3, solve(c3_1,c3)); %me saco de encima c3
g42_3 = vpa(g42_3);

%g41
g41_1 = subs(ecuacion10,g42,solve(g42_3,g42)); %me saco de encima g42
g41_1 = vpa(g41_1);
g41_2 = subs(g41_1, g1, solve(g1_3,g1)); %me saco de encima g1
g41_2 = vpa(g41_2);



%ga2
ga2_1 = subs(ecuacion11,ga1,solve(ecuacion14,ga1)); %me saco de encima ga1
ga2_1 = vpa(ga2_1);
ga2_2 = subs(ga2_1, c3, solve(c3_1,c3)); %me saco de encima c3
ga2_2 = vpa(ga2_2);
ga2_3 = subs(ga2_2, g1, solve(g1_3, g1)); %me saco de encima g1
ga2_3 = vpa(ga2_3);
ga2_4 = subs(ga2_3, g41, solve(g41_2,g41)); %me saco de encima g41
ga2_4 = vpa(ga2_4);
ga2_5 = subs(ga2_4, g42, solve(g42_3,g42)); %me saco de encima g42
ga2_5 = vpa(ga2_5);


%ga1
ga1_1 = subs(ecuacion11,ga2,solve(ga2_5,ga2)); %me saco de encima ga2
ga1_1 = vpa(ga1_1);
ga1_2 = subs(ga1_1, c3, solve(c3_1,c3)); %me saco de encima c3
ga1_2 = vpa(ga1_2);
ga1_3 = subs(ga1_2, g1, solve(g1_3, g1)); %me saco de encima g1
ga1_3 = vpa(ga1_3);
ga1_4 = subs(ga1_3, g41, solve(g41_2,g41)); %me saco de encima g41
ga1_4 = vpa(ga1_4);
ga1_5 = subs(ga1_4, g42, solve(g42_3,g42)); %me saco de encima g42
ga1_5 = vpa(ga1_5);



% %n2
% n2_1 = subs(ecuacion16, ga1, solve(ga1_5,ga1));
% n2_1 = vpa(n2_1);
% n2_2 = subs(n2_1, ga2, solve(ga2_5,ga2));
% n2_2 = vpa(n2_2);
% n2_3 = subs(n2_2, c3, solve(c3_1,c3));
% n2_3 = vpa(n2_3);


%-------------------------------%%-------------------------------%%-------------------------------%%-------------------------------%

%utilizo funcion magica 'fminsearch' para determinar que a partir de Q, Wz,
%Wo que valores de C22 o Gb o n es mejor


options = optimset('MaxIter',200); %determino la cantidad maxima de iteraciones que va a realizar cada fminsearch

%-------------------------------%
%empiezo por wo

wo_1 = wp;

wo_1 = wo_1+0.5*(1/g1)*0.005;
wo_2 = subs(wo_1,g1,expand(solve(g1_3,g1)));
wo_2 =vpa(wo_2);

wo_3 = wo_2 + 0.5*(1/(c21+c22))*0.005;
wo_4 = subs(wo_3,c21,solve(c21_1,c21));
wo_4 =vpa(wo_4);

wo_5= wo_4+0.5*(1/c3)*0.005;
wo_6 = subs(wo_5,c3,solve(c3_1,c3));
wo_6 = vpa(wo_6);

wo_7 = wo_6 + 0.5*(1/(g41+g42))*0.005;
wo_8 = subs(wo_7,g41,solve(g41_2,g41));
wo_8 = vpa(wo_8);

wo_9 = subs(wo_8,g42,solve(g42_3,g42));
wo_9 = vpa(wo_9);

wo_optimo = symfun(abs(wo_9),[c22,n,gb]);
[wo_min, wo_opt] = fminsearch(@(x) wo_optimo(x(1),x(2),x(3)),[20*(10^-9),0.5,0.0004],options);


%-------------------------------%
%sigo por wz
wz_1= wz;

wz_2 = wz_1 + 0.5*(1/c3)*0.005;
wz_3 = subs(wz_2,c3,solve(c3_1,c3));
wz_3=vpa(wz_3);

wz_4 = wz_3 + 0.5*(1/c22)*0.005;  %%capaz esta demas este%%%%%%%%%%%%%%%%%%%%%%%%
wz_4 = vpa(wz_4);


wz_5 = wz_4 - 0.5*(1/g1)*0.005;
wz_6 = subs(wz_5,g1,expand(solve(g1_3,g1)));
wz_6 = vpa(wz_6);

wz_7  = wz_6 - 0.5*(1/g42)*0.005;           
wz_8 = subs(wz_7, g42, solve(g42_3,g42));
wz_8 = vpa(wz_8);
                                        %las otras no las considero porque
                                        %son muy chicas

                                        

wz_optimo = symfun(abs(wz_8),[c22,n,gb]);
[wz_min, wz_opt] = fminsearch(@(x) wz_optimo(x(1),x(2),x(3)),[20*(10^-9),0.5,0.0004],options);


%-------------------------------%
%ahora viene Q

q_1 = Qp;

q_1 = q_1 - (Qp/Q0-1/2)*(1/g1)*0.01;
q_2 = subs(q_1, g1, expand(solve(g1_3,g1)));
q_2 = vpa(q_2);

q_3 = q_2 + 0.5*(Qp/Q0-1)*(1/c3)*0.005;
q_4 = subs(q_3, c3, solve(c3_1,c3));
q_4 = vpa(q_4);

q_5 = q_4 + (Qp/Q0 -1/2)*(1/(g41+g42))*0.01;
q_6 = subs(q_5, g41, solve(g41_2,g41));
q_6 = vpa(q_6);

q_7 = subs(q_6, g42, solve(g42_3,g42));
q_7 = vpa(q_7);


q_8 = q_7 + (Qp/Q0-1)*(1/(ga1+ga2))*0.005;
q_9 = subs(q_8, ga1, solve(ga1_5,ga1));
q_9 = vpa(q_9);
q_10 = subs(q_9, ga2, solve(ga2_5,ga2));
q_10 = vpa(q_10);
q_11 = q_10 - 0.5*(Qp/Q0-1)*(1/c22+c21)*0.005;
q_12 = subs(q_11, c21, solve(c21_1,c21));
q_12 = vpa(q_12);

q_13 = q_12 - (Qp/Q0-1)*(1/gb)*0.005;


q_optimo = symfun(abs(q_13),[c22,n,gb]);
[q_min, q_opt] = fminsearch(@(x) q_optimo(x(1),x(2),x(3)),[20*(10^-9),0.5,0.0004],options);


c22_opt_wo_wz_Q = [wo_min(1),wz_min(1),q_min(1)];
n_opt_wo_wz_Q = [wo_min(2),wz_min(2),q_min(2)];
gb_opt_wo_wz_Q = [wo_min(3),wz_min(3),q_min(3)];


%-------------------------------%%-------------------------------%%-------------------------------%%-------------------------------%
%-------------------------------%
%componentes_wo_opt

%c21
c21_aux = c21_1;
c21_wo_1 = subs(c21_aux, c22, wo_min(1));
c21_wo_1 = vpa(c21_wo_1);
c21_wo_2 = subs(c21_wo_1, n, wo_min(2));
c21_wo_2 = vpa(c21_wo_2);
c21_wo_2 = c21 == solve(c21_wo_2,c21);

%c3
c3_aux = c3_1;
c3_wo_1 = subs(c3_aux, c22, wo_min(1));
c3_wo_1 = vpa(c3_wo_1);
c3_wo_2 = subs(c3_wo_1, n, wo_min(2));
c3_wo_2 = vpa(c3_wo_2);
c3_wo_2 = c3 == solve(c3_wo_2,c3);


%g1
g1_aux = g1_3;
g1_wo_1 = subs(g1_aux, c22, wo_min(1));
g1_wo_1 = vpa(g1_wo_1);
g1_wo_2 = subs(g1_wo_1, n, wo_min(2));
g1_wo_2 = vpa(g1_wo_2);
g1_wo_2 = g1 == solve(g1_wo_2,g1);

%g42
g42_aux = g42_3;
g42_wo_1 = subs(g42_aux, c22, wo_min(1));
g42_wo_1 = vpa(g42_wo_1);
g42_wo_2 = subs(g42_wo_1, n, wo_min(2));
g42_wo_2 = vpa(g42_wo_2);
g42_wo_3 = subs(g42_wo_2, gb, wo_min(3));
g42_wo_3 = vpa(g42_wo_3);
g42_wo_3 = g42 == solve(g42_wo_3,g42);


%g41
g41_aux = g41_2;
g41_wo_1 = subs(g41_aux, c22, wo_min(1));
g41_wo_1 = vpa(g41_wo_1);
g41_wo_2 = subs(g41_wo_1, n, wo_min(2));
g41_wo_2 = vpa(g41_wo_2);
g41_wo_3 = subs(g41_wo_2, gb, wo_min(3));
g41_wo_3 = vpa(g41_wo_3);
g41_wo_3 = g41 == solve(g41_wo_3,g41);

%ga1
ga1_aux = ga1_5;
ga1_wo_1 = subs(ga1_aux, c22, wo_min(1));
ga1_wo_1 = vpa(ga1_wo_1);
ga1_wo_2 = subs(ga1_wo_1, n, wo_min(2));
ga1_wo_2 = vpa(ga1_wo_2);
ga1_wo_3 = subs(ga1_wo_2, gb, wo_min(3));
ga1_wo_3 = vpa(ga1_wo_3);
ga1_wo_3 = ga1 == solve(ga1_wo_3,ga1);

%ga2
ga2_aux = ga2_5;
ga2_wo_1 = subs(ga2_aux, c22, wo_min(1));
ga2_wo_1 = vpa(ga2_wo_1);
ga2_wo_2 = subs(ga2_wo_1, n, wo_min(2));
ga2_wo_2 = vpa(ga2_wo_2);
ga2_wo_3 = subs(ga2_wo_2, gb, wo_min(3));
ga2_wo_3 = vpa(ga2_wo_3);
ga2_wo_3 = ga2 == solve(ga2_wo_3,ga2);


componentes_wo_opt = [c21_wo_2, c22 == vpa(wo_min(1)), c3_wo_2 , g1_wo_2 , g41_wo_3 , g42_wo_3 , ga1_wo_3 , ga2_wo_3,  vpa(wo_opt)];

%-------------------------------%
%componentes_wz_opt

%c21
c21_aux = c21_1;
c21_wz_1 = subs(c21_aux, c22, wz_min(1));
c21_wz_1 = vpa(c21_wz_1);
c21_wz_2 = subs(c21_wz_1, n, wz_min(2));
c21_wz_2 = vpa(c21_wz_2);
c21_wz_2 = c21 == solve(c21_wz_2,c21);

%c3
c3_aux = c3_1;
c3_wz_1 = subs(c3_aux, c22, wz_min(1));
c3_wz_1 = vpa(c3_wz_1);
c3_wz_2 = subs(c3_wz_1, n, wz_min(2));
c3_wz_2 = vpa(c3_wz_2);
c3_wz_2 = c3 == solve(c3_wz_2,c3);


%g1
g1_aux = g1_3;
g1_wz_1 = subs(g1_aux, c22, wz_min(1));
g1_wz_1 = vpa(g1_wz_1);
g1_wz_2 = subs(g1_wz_1, n, wz_min(2));
g1_wz_2 = vpa(g1_wz_2);
g1_wz_2 = g1 == solve(g1_wz_2,g1);

%g42
g42_aux = g42_3;
g42_wz_1 = subs(g42_aux, c22, wz_min(1));
g42_wz_1 = vpa(g42_wz_1);
g42_wz_2 = subs(g42_wz_1, n, wz_min(2));
g42_wz_2 = vpa(g42_wz_2);
g42_wz_3 = subs(g42_wz_2, gb, wz_min(3));
g42_wz_3 = vpa(g42_wz_3);
g42_wz_3 = g42 == solve(g42_wz_3,g42);


%g41
g41_aux = g41_2;
g41_wz_1 = subs(g41_aux, c22, wz_min(1));
g41_wz_1 = vpa(g41_wz_1);
g41_wz_2 = subs(g41_wz_1, n, wz_min(2));
g41_wz_2 = vpa(g41_wz_2);
g41_wz_3 = subs(g41_wz_2, gb, wz_min(3));
g41_wz_3 = vpa(g41_wz_3);
g41_wz_3 = g41 == solve(g41_wz_3,g41);

%ga1
ga1_aux = ga1_5;
ga1_wz_1 = subs(ga1_aux, c22, wz_min(1));
ga1_wz_1 = vpa(ga1_wz_1);
ga1_wz_2 = subs(ga1_wz_1, n, wz_min(2));
ga1_wz_2 = vpa(ga1_wz_2);
ga1_wz_3 = subs(ga1_wz_2, gb, wz_min(3));
ga1_wz_3 = vpa(ga1_wz_3);
ga1_wz_3 = ga1 == solve(ga1_wz_3,ga1);

%ga2
ga2_aux = ga2_5;
ga2_wz_1 = subs(ga2_aux, c22, wz_min(1));
ga2_wz_1 = vpa(ga2_wz_1);
ga2_wz_2 = subs(ga2_wz_1, n, wz_min(2));
ga2_wz_2 = vpa(ga2_wz_2);
ga2_wz_3 = subs(ga2_wz_2, gb, wz_min(3));
ga2_wz_3 = vpa(ga2_wz_3);
ga2_wz_3 = ga2 == solve(ga2_wz_3,ga2);


componentes_wz_opt = [c21_wz_2, c22 == vpa(wz_min(1)), c3_wz_2 , g1_wz_2 , g41_wz_3 , g42_wz_3 , ga1_wz_3 , ga2_wz_3,  vpa(wz_opt)];


%-------------------------------%
%componentes_wz_opt

%c21
c21_aux = c21_1;
c21_q_1 = subs(c21_aux, c22, q_min(1));
c21_q_1 = vpa(c21_q_1);
c21_q_2 = subs(c21_q_1, n, q_min(2));
c21_q_2 = vpa(c21_q_2);
c21_q_2 = c21 == solve(c21_q_2,c21);

%c3
c3_aux = c3_1;
c3_q_1 = subs(c3_aux, c22, q_min(1));
c3_q_1 = vpa(c3_q_1);
c3_q_2 = subs(c3_q_1, n, q_min(2));
c3_q_2 = vpa(c3_q_2);
c3_q_2 = c3 == solve(c3_q_2,c3);

%g1
g1_aux = g1_3;
g1_q_1 = subs(g1_aux, c22, q_min(1));
g1_q_1 = vpa(g1_q_1);
g1_q_2 = subs(g1_q_1, n, q_min(2));
g1_q_2 = vpa(g1_q_2);
g1_q_2 = g1 == solve(g1_q_2,g1);

%g42
g42_aux = g42_3;
g42_q_1 = subs(g42_aux, c22, q_min(1));
g42_q_1 = vpa(g42_q_1);
g42_q_2 = subs(g42_q_1, n, q_min(2));
g42_q_2 = vpa(g42_q_2);
g42_q_3 = subs(g42_q_2, gb, q_min(3));
g42_q_3 = vpa(g42_q_3);
g42_q_3 = g42 == solve(g42_q_3,g42);


%g41
g41_aux = g41_2;
g41_q_1 = subs(g41_aux, c22, q_min(1));
g41_q_1 = vpa(g41_q_1);
g41_q_2 = subs(g41_q_1, n, q_min(2));
g41_q_2 = vpa(g41_q_2);
g41_q_3 = subs(g41_q_2, gb, q_min(3));
g41_q_3 = vpa(g41_q_3);
g41_q_3 = g41 == solve(g41_q_3,g41);

%ga1
ga1_aux = ga1_5;
ga1_q_1 = subs(ga1_aux, c22, q_min(1));
ga1_q_1 = vpa(ga1_q_1);
ga1_q_2 = subs(ga1_q_1, n, q_min(2));
ga1_q_2 = vpa(ga1_q_2);
ga1_q_3 = subs(ga1_q_2, gb, q_min(3));
ga1_q_3 = vpa(ga1_q_3);
ga1_q_3 = ga1 == solve(ga1_q_3,ga1);

%ga2
ga2_aux = ga2_5;
ga2_q_1 = subs(ga2_aux, c22, q_min(1));
ga2_q_1 = vpa(ga2_q_1);
ga2_q_2 = subs(ga2_q_1, n, q_min(2));
ga2_q_2 = vpa(ga2_q_2);
ga2_q_3 = subs(ga2_q_2, gb, q_min(3));
ga2_q_3 = vpa(ga2_q_3);
ga2_q_3 = ga2 == solve(ga2_q_3,ga2);


componentes_q_opt = [c21_q_2, c22 == vpa(q_min(1)), c3_q_2 , g1_q_2 , g41_q_3 , g42_q_3 , ga1_q_3 , ga2_q_3,  vpa(q_opt)];


end

