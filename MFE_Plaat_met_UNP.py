import math
from operator import itemgetter

fyPl = 235 # = vloeispanning plaat in N/mm²
fyPr = 235 # = vloeispanning profiel in N/mm²
E = 210000 # = elasticiteitsmodulus in N/mm²
RhoS = 7850 # soortelijk gewicht staal in kg/m3

Lpr = 1400 # = lengte UNP profiel in mm.
maxRelUitnPl = 1.00 # = Maximale relatieve uitnutting van de vloeispanning van de plaat. Maximale waarde is 1.00.
maxRelUitnPr = 1.00 # = Maximale relatieve uitnutting van de vloeispanning van het profiel. Maximale waarde is 1.00.
uRelMaxPl = 1/500 # = maximaal toelaatbare relatieve doorbuiging plaat [-]
uRelMaxPr = 1/500 # = maximaal toelaatbare relatieve doorbuiging pprofiel [-]
RhoWater = 10.5 # = specific weight water in kN/m3
WaterLevel = 4.85 # = waterkolom op belaste oppervlak in m

p_k = 4.85*10.5 # = hydrostatic waterpressure in kN/m²
p_Ed = p_k*1.35 # = hydrostatic waterpressure in kN/m²
Results = []
t_list = [12,15,20,25] #plaatdikte t in mm.
profielen = [{'naam':'UNP80','G8':8.82,'G':8.65,'A':1102,'I_z_el':1060000,'W_z_el':26500},
             {'naam':'UNP100','G8':10.80,'G':10.56,'A':1345,'I_z_el':2050000,'W_z_el':41100},
             {'naam':'UNP120','G8':13.60,'G':13.34,'A':1699,'I_z_el':3640000,'W_z_el':60700},
             {'naam':'UNP140','G8':16.30,'G':15.99,'A':2037,'I_z_el':6050000,'W_z_el':86400},
             {'naam':'UNP160','G8':19.20,'G':18.85,'A':2401,'I_z_el':9250000,'W_z_el':116000},
             {'naam':'UNP180','G8':22.40,'G':21.96,'A':2797,'I_z_el':13540000,'W_z_el':150000},
             {'naam':'UNP200','G8':25.70,'G':25.26,'A':3218,'I_z_el':19110000,'W_z_el':191000}]

for profiel in profielen:
    for t in t_list:
        MRdPl = 1/6*1000*t**2*maxRelUitnPl*fyPl # =Toelaatbaar moment in de plaat in Nmm
        MRdPr = profiel['W_z_el']*maxRelUitnPr*fyPr # =Toelaatbaar moment in het profiel in Nmm
        ctcPrM = MRdPr/(1/8*p_Ed*0.001*Lpr**2)
        ctcPlM = math.sqrt(MRdPl/(1/8*p_Ed))
        ctcPlU = (uRelMaxPl*192*E*1/12*1000*t**3/p_k)**(1/3)
        ctcPrU = (uRelMaxPr*384*E*profiel['I_z_el'])/(5*p_k*0.001*Lpr**3)
        ctc = min(ctcPlM,ctcPlU,ctcPrM,ctcPrU)
        Weight = t/1000*RhoS+profiel['G']*1000/ctc
        Upl = (p_k*0.001*1000*ctc**4)/(192*E*1/12*1000*t**3)
        Upr = (5*p_k*0.001*ctc*Lpr**4)/(384*E*profiel['I_z_el'])
        stressPl = (1/8*p_Ed*0.001*1000*ctc**2)/(1/6*1000*t**2)
        stressPr = (1/8*p_Ed*0.001*ctc*Lpr**2)/(profiel['W_z_el'])
        UC_Upl = ctc/ctcPlU
        UC_Upr = ctc/ctcPrU
        UC_Mpl = ctc/ctcPlM
        UC_Mpr = ctc/ctcPrM
        Results.append([profiel['naam'],t,round(ctc),round(Weight,1),round(Upl,2),round(Upr,2),round(stressPl),round(stressPr),round(UC_Upl,3),round(UC_Upr,3),round(UC_Mpl,3),round(UC_Mpr,3)])

Results = sorted(Results, key=itemgetter(3))
for i in Results:
    print(i)
