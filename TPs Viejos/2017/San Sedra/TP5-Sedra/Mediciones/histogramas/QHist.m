function [ meanQ,stdDeviation,h  ] = QHist(R1,R4,C2,C3,Ra,Rb,w0,Q0,Q )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
tolR=0.01;
tolC=0.05;
N=6; %Número de numeros random por variable, con mas de 20 se me tildo la cpu

%%%Inicializo los vecotres
R1t = zeros(1,N);
R1t= zeros(1,N); %%Esto viene de suponer que (1-tolR)R = R- 3o, debido a que el 99.7 de proab esta en esa campana
R4t= zeros(1,N);
Rat= zeros(1,N);
Rbt= zeros(1,N);
C2t= zeros(1,N);
C3t= zeros(1,N);
%newW0s= zeros(N,N,N,N,N,N);
newQs= zeros(N,N,N,N,N,N);
%%%%%%%%
R1t= normrnd(R1,R1*tolR/3,1,N); %%Esto viene de suponer que (1-tolR)R = R- 3o, debido a que el 99.7 de proab esta en esa campana
R4t= normrnd(R4,R4*tolR/3,1,N);
Rat= normrnd(Ra,Ra*tolR/3,1,N);
Rbt= normrnd(Rb,Rb*tolR/3,1,N);
C2t= normrnd(C2,C2*tolC/3,1,N);
C3t= normrnd(C3,C3*tolC/3,1,N);

for z=1:N
     for a=1:N
        for b=1:N
            for c=1:N
                for d=1:N
                    for e=1:N
                        %%%lAS Diferencias seràn:
                        DR1=(R1t(z)-R1)/R1;
                        DR4=(R4t(a)-R4)/R4;
                        DRa=(Rat(b)-Ra)/Ra;
                        DRb=(Rbt(c)-Rb)/Rb;
                        DC2=(C2t(d)-C2)/C2;
                        DC3=(C3t(e)-C3)/C3;
                        %%
                        %newW0 = w0*(- DR1/2 - DC2/2 - DC3/2 - DR4/2) + w0; %%Se calcula el nuevo w0 con las sensibilidades y las var relativas
                        %newW0s(z,a,b,c,d,e)=newW0;
                        newQ= Q *(- ((Q/Q0)-1/2)*DR1 - ((Q/Q0)-1)*DC2/2 + ((Q/Q0)-1)*DC3/2 + ((Q/Q0)-1/2)*DR4 - ((Q/Q0)-1)*DRa + ((Q/Q0)-1)*DRb)+Q; %% lo mismo con el Q
                        newQs(z,a,b,c,d,e)=newQ;
                    end
                end
            end
        end
    end
end
%newW0s=reshape(newW0s,1, []); %%Se pone todo en un vector para el histograma
newQs=reshape(newQs,1, []);


%histogram(newW0s,40);
meanQ = mean(newQs);
stdDeviation = std(newQs);
h=histogram(newQs,'Normalization','probability');

title('Dispersión de Q');
xlabel('Q');
ylabel('Probabilidad ');


end

