function[H,L] = margin( Ga, Ga2, Gb, G1, G4, G42, C2, C22, C3 , wp, A0)
    
    s = tf('s')
   
    Avol = A0/(1+s/wp)
    
    corazon = s*C3/(G4+s*C2)
    estrella =  s*C2+s*C3+G1

    aux = corazon / estrella
    
    carita1 = Ga2/(Ga+Gb)
    carita2 = Gb/(Ga+Gb)
    carita3 = (G42/(G4+s*C2) + s*C22*aux)/(1-s*C3*aux)
    carita4 = (G1*aux)/(1-s*C3*aux)
    
    H = (carita3 - carita1)*Avol/(1+Avol*(carita2-carita4))
    L = Avol*(carita2-carita4)
    
    figure;
    bode(H)
    setoptions(gcr,'FreqUnits','Hz')
    figure;
    pzplot(H)