
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%% read emission data
df = pd.read_excel("TGP 1986-2019.xlsx", sheet_name = "zgoščen prikaz")
matrix = df.as_matrix()

sectors = matrix[2:,0]
years = matrix[1,1:-1]
values = matrix[2:,1:-1]

#%% read negative emission data Land use, land-use change and forestry = LULUCF = negative emissions

df = pd.read_excel("TGP 1986-2019.xlsx", sheet_name = "izpis iz poročevalskih tabel")
matrix = df.as_matrix()
values_lulucf = matrix[37:45,2:-1]
sectors_lulucf = matrix[37:45,1]

#%% read projections (Aljoša Slameršak)
df = pd.read_excel("ProjekcijeGHG_Slovenija.xlsx")
matrix = df.as_matrix()
bau = matrix[:11,3]
nepn = matrix[:11,5]
ec = matrix[:11,7]
paris20 = matrix[:11,9]
paris15 = matrix[:11,11]




#%% future emission data
values_proj = np.zeros((8,11))
for i in range(8):
    values_proj[i,:] = values[i,-1] 



#%% 2019 data energetics (from Jan Bohinec)
switch_tes = True
switch_tes_year = 2023
emission_tes = np.zeros(11) + 3817
emission_tes[switch_tes_year-2020:] = 0
if switch_tes:
    emission_tes[switch_tes_year-2020:] = 0

switch_tetol = True
swtich_tetol_year = 2028
emission_tetol = np.zeros(11) + 488
if switch_tetol:
    emission_tetol[swtich_tetol_year-2020:] = 0

switch_brestanica = False
switch_brestanica_year = 2029
emission_brestanica = np.zeros(11) + 16
if switch_brestanica:
    emission_brestanica[switch_brestanica_year-2020:] = 0


values_proj[1,:] = emission_tes + emission_tetol + emission_brestanica
#%% aforestation/reforestation
# https://www.theguardian.com/environment/2019/jul/04/planting-billions-trees-best-tackle-climate-crisis-scientists-canopy-emissions
# https://www.pnas.org/content/117/40/24649
# https://science.sciencemag.org/content/365/6448/76
# http://www.fao.org/3/y0900e/y0900e06.htm
# https://www.nature.com/articles/d41586-019-00122-z
# 20 t CO2/ha/leto  # 1000 dreves/ha, 20 ton CO2/leto za odrasla drevesa

# simplest model (adult trees take more co2)
switch_ff_year = 2022
years_proj = np.arange(2020,2031,1)
values_lulucf_proj = -20*100*300*(years_proj-switch_ff_year+1)*(years_proj-switch_ff_year>=0)/1000 # v kt CO2


#%% electric cars
# 5%/leto, 50% do 2030
osebni_promet_proj = 2/3.*values_proj[0,:]
tovorni_promet_proj = 1/3.*values_proj[0,:]


ratio = 1 - np.arange(0,0.51,0.05)

osebni_promet_proj = osebni_promet_proj * ratio


#%% work @ home
# https://www.stat.si/statweb/News/Index/7596
# 34.6% voženj (v km) na delo

switch_wah = 2025
osebni_promet_proj = osebni_promet_proj * (1 - 0.346*2/5.*(years_proj-switch_wah>=0))
values_proj[0,:] = osebni_promet_proj + tovorni_promet_proj


#%% stavbni sektor zmanjševanje emisij


#%% plot data - positive emissions (historial)

fig,ax = plt.subplots(1,figsize=(22,11))
plt.bar(years,2/3.*values[0,:],align="edge",label="osebni promet",color="blue",alpha=0.5)
plt.bar(years,1/3.*values[0,:],bottom=2./3*values[0,:],align="edge",label="tovorni promet",color="blue")
plt.bar(years,values[1,:],bottom=values[0,:],align="edge",label="energetika",color="gray")
plt.bar(years,values[2,:],bottom=values[0:2,:].sum(axis=0),align="edge",label="industrijski procesi",color="red")
plt.bar(years,values[3,:],bottom=values[0:3,:].sum(axis=0),align="edge",label="goriva v industriji",color="lime")
plt.bar(years,values[4,:],bottom=values[0:4,:].sum(axis=0),align="edge",label="goriva v gospodinjstvih in ostala raba",color="fuchsia")
plt.bar(years,values[5,:],bottom=values[0:5,:].sum(axis=0),align="edge",label="kmetijstvo",color="cyan")
plt.bar(years,values[6,:],bottom=values[0:6,:].sum(axis=0),align="edge",label="odpadki",color="yellow")
plt.bar(years,values[7,:],bottom=values[0:7,:].sum(axis=0),align="edge",label="drugo",color="brown")
plt.grid()

plt.xlabel("leto",fontsize=18)
plt.ylabel(r"emisije [kt CO$_2$ equiv.]",fontsize=18)
plt.xlim([1984,2033])
plt.ylim([-12000,33000])


#%% plot data - negative emissions (historical) aggregate
plt.bar(years,values_lulucf[0,:],align="edge",label="gozd, travniki, kmet. zemlj.\nmokrišča, naselja,\nlesni proizvodi (LULUCF)",color="darkgreen")
#plt.bar(years,-values_lulucf[2,:],bottom=values_lulucf[0,:]-values_lulucf[1,:],align="edge",label="kmetijska zemljišča",color="yellow")
#plt.bar(years,-values_lulucf[3,:],bottom=values_lulucf[0,:]-values_lulucf[1,:]-values_lulucf[2,:],align="edge",label="travišča",color="lightgreen")


#%% plot net emission total
plt.plot(years+0.5,values_lulucf[0,:]+values[-1,:],"k-",lw=7,label="neto emisije")


#%% plot emission goals
plt.plot(years_proj,bau,"r-",label="business as usual",lw=4)
plt.plot(years_proj,nepn,"m-",label="NEPN SLO",lw=4)
plt.plot(years_proj,ec,"k-",label="cilj EU 2030",lw=4)
plt.plot(years_proj,paris20,"g-",label="cilj PA $\Delta T < 2.0^\circ$C (66%)",lw=4)
plt.plot(years_proj,paris15,"b-",label="cilj PA $\Delta T < 1.5^\circ$C (66%)",lw=4)


#%% plot projected emissions
plt.rcParams['hatch.linewidth'] = 1.5
plt.rcParams.update({'hatch.color': 'white'})
#




plt.bar(years_proj,osebni_promet_proj,align="edge",label="osebni promet",color="blue",alpha=0.5,hatch="/")
plt.bar(years_proj,tovorni_promet_proj,bottom=osebni_promet_proj,align="edge",label="tovorni promet [projekcija]",color="blue",hatch="/")
plt.bar(years_proj,values_proj[1,:],bottom=values_proj[0,:],align="edge",label="energetika [projekcija]",color="gray",hatch="/")
plt.bar(years_proj,values_proj[2,:],bottom=values_proj[0:2,:].sum(axis=0),align="edge",label="industrijski procesi [projekcija]",hatch="/",color="red")
plt.bar(years_proj,values_proj[3,:],bottom=values_proj[0:3,:].sum(axis=0),align="edge",label="goriva v industriji [projekcija]",hatch="/",color="lime")
plt.bar(years_proj,values_proj[4,:],bottom=values_proj[0:4,:].sum(axis=0),align="edge",label="goriva v gospodinjstvih in \n ostala raba [projekcija]",hatch="/",color="fuchsia")
plt.bar(years_proj,values_proj[5,:],bottom=values_proj[0:5,:].sum(axis=0),align="edge",label="kmetijstvo [projekcija]",hatch="/",color="cyan")
plt.bar(years_proj,values_proj[6,:],bottom=values_proj[0:6,:].sum(axis=0),align="edge",label="odpadki [projekcija]",hatch="/",color="yellow")
plt.bar(years_proj,values_proj[7,:],bottom=values_proj[0:7,:].sum(axis=0),align="edge",label="drugo [projekcija]",hatch="/",color="brown")



plt.vlines(switch_tes_year,0,23000,color="grey")
plt.vlines(swtich_tetol_year,0,23000,color="grey")
plt.text(switch_tes_year,24000,"[ukrep] \nTEŠ 5/6 izklop",fontsize=14,horizontalalignment="center",color="gray")
plt.text(swtich_tetol_year,24000,"[ukrep] \nTETOL izklop",fontsize=14,horizontalalignment="center",color="gray")


plt.bar(years_proj,values_lulucf_proj,color="darkgreen",align="edge",hatch="/",label="LULUCF [projekcija]")
plt.vlines(switch_ff_year,0,-6000,color="darkgreen")
plt.text(switch_ff_year,-10000,"[ukrep] \n pogozdovanje\n 300 km$^2$/leto",fontsize=14,\
         horizontalalignment="center",color="darkgreen")

plt.vlines(2014,0,-7000,color="darkgreen")
plt.text(2014,-11000,"žledolom: \n poškodovanih\n 5000 km$^2$ gozda",fontsize=14,\
         horizontalalignment="center",color="darkgreen")


plt.vlines(switch_wah,0,26000,color="blue",alpha=0.5)
plt.text(switch_wah,27000,"[ukrep] \ndelo od doma 2/5 dni\n tedensko",fontsize=14,horizontalalignment="center",color="blue",alpha=0.5)

plt.vlines(2021,0,20000,color="blue",alpha=0.5)
plt.text(2021,21000,"[ukrep] \n+5%/leto delež EV",fontsize=14,horizontalalignment="center",color="blue",alpha=0.5)


#%% plot total projected_emissions
plt.plot(years_proj+0.5,values_lulucf_proj+values_proj.sum(axis=0),"k-",lw=7)#,label="neto emisije [projekcija]")


plt.axvspan(0, 2020, alpha=0.1, color='gray')
plt.legend(ncol=4,fontsize=14,loc=2)

plt.tight_layout()
plt.savefig("blah.png",dpi=300)
