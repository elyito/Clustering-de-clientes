# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:23:47 2018

@author: Anibal Siriany
"""
import numpy as np
import os
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('max_columns',10)

oficinas=['OFICINA ARICA','OFICINA IQUIQUE','OFICINA LA SERENA',
          'OFICINA PARRAL','OFICINA PUERTO MONTT','OFICINA VALPARAISO'
          'OFICINA RANCAGUA','OFICINA SANTIAGO','OFICINA TEMUCO', 'OFICINA ANTOFAGASTA']
mesones=['SALA VENTA SANTIAGO','VENTA MESON ARICA',
         'VENTA MESON GALPON (IQUIQUE)','VENTA MESON TEMUCO']
proveedores=["PROVEEDORES","BONIFICACIONES CLIENTES","SUPERMERCADOS Y MAYORISTAS"]
mes=[18,19,29,44]

def ventas2018():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2018")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    ventas08=pd.read_csv("PLANILLA_VTA_2018.csv", delimiter=";", encoding='iso-8859-1')
    ventas08=ventas08[(ventas08["DESCRIPCION VENDEDOR"]!="PROVEEDORES") & (~ventas08["RUBRO"].isin([3,78]))]
    ventas08["BONIFICACIONES"]= 0
    ventas08.loc[ventas08["RUBRO"]==471,"BONIFICACIONES"]=ventas08["TOTAL VENTAS"]*0.07926957
    ventas08.loc[ventas08["RUBRO"]==583,"BONIFICACIONES"]=ventas08["TOTAL VENTAS"]*0.093268809
    ventas08.loc[ventas08["RUBRO"]==594,"BONIFICACIONES"]=ventas08["TOTAL VENTAS"]*0.00609723
    ventas08.loc[ventas08["% COMISION"]==5, "% COMISION"]=3
    ventas08.loc[ventas08["% COMISION"]==3, "COMISIONES"]=ventas08["TOTAL VENTAS"]*0.03
    ventas08["COMISIONES"]=(ventas08["% COMISION"]/100)*ventas08["TOTAL VENTAS"]
    ventas08.loc[(ventas08["DESCRIPCION VENDEDOR"].isin(oficinas+mesones+proveedores)) | (ventas08["LOCAL"].isin(mes)),"COMISIONES"]=0
    ventas08["INDICE FT"]=0
    for l in ventas08["LOCAL"].unique():
        for m in ventas08["MES"].unique():
            ventas08.loc[(ventas08["LOCAL"]==l) & (ventas08["MES"]==m), "INDICE FT"]=indice_ft_2018().loc[(l,m),"indice08"]
    ventas08["GASTOS FT"]=0
    ventas08.loc[ventas08["DESCRIPCION VENDEDOR"]!="PROVEEDORES","GASTOS FT"]=ventas08["TOTAL VENTAS"]*ventas08["INDICE FT"]

    rubros=[936,106,239,671,134,135,154,206,352,78,222,137,118,3,181,117]
    ventas08["INDICE RUBRO"]=0
    for i in rubros:
            ventas08.loc[ventas08["RUBRO"]==i,"INDICE RUBRO"]=ventas08.loc[ventas08["RUBRO"]==i ,"TOTAL VENTAS"]/ventas08.loc[ventas08["RUBRO"]==i,"TOTAL VENTAS"].sum()
    ventas08.loc[(ventas08["RUBRO"]==260) & (ventas08["MES"].isin([9,10])),"INDICE RUBRO"]=(ventas08.loc[(ventas08["RUBRO"]==260) & (ventas08["MES"].isin([9,10])) ,"TOTAL VENTAS"])/(ventas08.loc[(ventas08["RUBRO"]==260) & (ventas08["MES"].isin([9,10])),"TOTAL VENTAS"].sum())          
    suma_ventas={936:3750542,106:68400,239:266811,671:816000,134:930924,135:1310978,154:1417447,206:2208750,352:2538230,78:4194000,222:5447790,137:5988837,3:14391227,181:17003567,117:120493172,118:8342556}
    ventas08["BONIFICACIONES_2"]=0
    for i in suma_ventas:
        ventas08.loc[ventas08["RUBRO"]==i, "BONIFICACIONES_2"]=ventas08.loc[ventas08["RUBRO"]==i, "INDICE RUBRO"]*suma_ventas[i]
    ventas08.loc[(ventas08["RUBRO"]==260) & (ventas08["MES"].isin([9,10])), "BONIFICACIONES_2"]=ventas08.loc[(ventas08["RUBRO"]==260) & (ventas08["MES"].isin([9,10])), "INDICE RUBRO"]*19733400
    ventas08["MARGEN_E"]=ventas08["MARGEN"]-ventas08["TOTAL CONDUCCION"]-ventas08["GASTOS RAPEL"]-ventas08["COMISIONES"]-ventas08["GASTOS FT"]+ventas08["BONIFICACIONES"]+ventas08["BONIFICACIONES_2"]
    for j in ventas08["MES"].unique():
        for k in ventas08["LOCAL"].unique():
                ventas08.loc[(ventas08["LOCAL"]==k) & (ventas08["MES"]==j),"INDICE GA"]=ventas08.loc[(ventas08["LOCAL"]==k) & (ventas08["MES"]==j),"TOTAL VENTAS"]/ventas08.loc[(ventas08["LOCAL"]==k) & (ventas08["MES"]==j),"TOTAL VENTAS"].sum()
                ventas08.loc[(ventas08["LOCAL"]==k) & (ventas08["MES"]==j),"GASTOS ADMINISTRACION"]=ventas08.loc[(ventas08["LOCAL"]==k) & (ventas08["MES"]==j),"INDICE GA"]*eerr2018().loc[(k,j),"TOTAL GASTOS ADMINISTRACION"]

    ventas08["MARGEN_GA"]=ventas08["MARGEN_E"]-ventas08["GASTOS ADMINISTRACION"] 
    return ventas08

    
def eerr2018():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2018")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    eerr08=pd.read_excel("EERR resumen08.xlsx", header=[0], index_col=[0,1])
    return eerr08

def indice_ft_2018():
    import os
    import pandas as pd
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2018")
    df = pd.read_excel("indice_ft.xlsx", header=[0], index_col=[0,1])
    return df


