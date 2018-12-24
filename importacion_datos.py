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

#USO ESTE CÓDIGO PARA GENERAR 1 SOLO ARCHIVO PARA LOS OTROS AÑOS    
def ventas_concat():
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2016")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    ventas_con=pd.DataFrame()
    alist=[]
#    planillas_01_10=["PLANILLA_VTA_012018_T51.csv","PLANILLA_VTA_022018_T51.csv",
#                 "PLANILLA_VTA_032018_T51.csv","PLANILLA_VTA_042018_T51.csv",
#                 "PLANILLA_VTA_052018_T51.csv","PLANILLA_VTA_062018_T51.csv",
#                 "PLANILLA_VTA_072018_T51.csv","PLANILLA_VTA_082018_T51.csv",
#                 "PLANILLA_VTA_092018_T51.csv","PLANILLA_VTA_102018_T51.csv"]
    
    planillas_01_10=["PLANILLA_VTA_012016.csv","PLANILLA_VTA_022016.csv","PLANILLA_VTA_032016.csv"
                     ,"PLANILLA_VTA_042016.csv","PLANILLA_VTA_052016.csv","PLANILLA_VTA_062016.csv"
                     ,"PLANILLA_VTA_072016.csv","PLANILLA_VTA_082016.csv","PLANILLA_VTA_092016.csv"
                     ,"PLANILLA_VTA_102016.csv","PLANILLA_VTA_112016.csv","PLANILLA_VTA_122016.csv"]
    
#    planillas_01_10=["PLANILLA_VTA_012015.csv","PLANILLA_VTA_022015.csv","PLANILLA_VTA_032015.csv"
#                     ,"PLANILLA_VTA_042015.csv","PLANILLA_VTA_052015.csv","PLANILLA_VTA_062015.csv"
#                     ,"PLANILLA_VTA_072015.csv","PLANILLA_VTA_082015.csv","PLANILLA_VTA_092015.csv"
#                     ,"PLANILLA_VTA_102015.csv","PLANILLA_VTA_112015.csv","PLANILLA_VTA_122015.csv"]
    for i in planillas_01_10:
        ventas_con=pd.read_csv(i, delimiter=";", encoding='iso-8859-1')
        ventas_con.rename(columns={" COSTO TOTAL VENTAS":"COSTO TOTAL VENTAS"},inplace=True)
#        if i!=planillas_01_10[3]:
#            for j in ["MARGEN","COSTO TOTAL VENTAS"]:
#                ventas_con[j]=ventas_con[j].str.replace(",", ".")
#                ventas_con[j]=ventas_con[j].astype(float)
        alist.append(ventas_con)
    ventas_con=pd.concat(alist, axis=0 ,ignore_index=True)
#    ventas_con=ventas_con.drop(["Unnamed: 43"], axis=1)
    ventas_con.replace(" ", 0, inplace=True)
#    ventas_con["MONTO FLETE"]=ventas_con["MONTO FLETE"].astype(float)
    return ventas_con
    
#vta06=ventas_concat()
#writer = pd.ExcelWriter('PLANILLA_VTA_2016.xlsx')
#vta06.to_excel(writer,"aux",index=False)
#writer.save()
#
#vta06=ventas_concat()
#vta06.to_csv("PLANILLA_VTA_2016.csv",index=False)


def ventas2017():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2017")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    ventas07=pd.read_csv("PLANILLA_VTA_2017.csv", delimiter=";", encoding='iso-8859-1')
    ventas07.rename(columns={"Distribución GFIN":"GASTOS FINANCIEROS"},inplace=True)
    ventas07.rename(columns={"Distribución Rapel":"GASTOS RAPEL"},inplace=True)
    ventas07.rename(columns={"TOTAL CONDUCCIÓN":"TOTAL CONDUCCION"},inplace=True)
    ventas07.rename(columns={"NOMBRE VENDEDOR":"DESCRIPCION VENDEDOR"},inplace=True)
    ventas07["BONIFICACIONES"]= 0
    ventas07.loc[ventas07["RUBRO"]==471,"BONIFICACIONES"]=ventas07["TOTAL VENTAS"]*0.066834567
    ventas07.loc[ventas07["RUBRO"]==583,"BONIFICACIONES"]=ventas07["TOTAL VENTAS"]*0.227051678
    ventas07.loc[ventas07["RUBRO"]==594,"BONIFICACIONES"]=ventas07["TOTAL VENTAS"]*0.005214259
    ventas07.loc[ventas07["% COMISION"]==5, "% COMISION"]=3
    ventas07.loc[ventas07["% COMISION"]==3, "COMISIONES"]=ventas07["TOTAL VENTAS"]*0.03
    ventas07["COMISIONES"]=(ventas07["% COMISION"]/100)*ventas07["TOTAL VENTAS"]
    ventas07.loc[(ventas07["DESCRIPCION VENDEDOR"].isin(oficinas+mesones+proveedores)) | (ventas07["LOCAL"].isin(mes)),"COMISIONES"]=0
    ventas07["INDICE FT"]=0
    for l in ventas07["LOCAL"].unique():
        for m in ventas07["MES"].unique():
            ventas07.loc[(ventas07["LOCAL"]==l) & (ventas07["MES"]==m), "INDICE FT"]=indice_ft_2017().loc[(l,m),"indice"]
    ventas07["GASTOS FT"]=ventas07["TOTAL VENTAS"]*ventas07["INDICE FT"]
    ventas07["MARGEN_E"]=ventas07["MARGEN"]-ventas07["TOTAL CONDUCCION"]-ventas07["GASTOS RAPEL"]+-ventas07["GASTOS FINANCIEROS"]-ventas07["COMISIONES"]-ventas07["GASTOS FT"]+ventas07["BONIFICACIONES"]
    for j in ventas07["MES"].unique():
        for k in ventas07["LOCAL"].unique():
                ventas07.loc[(ventas07["LOCAL"]==k) & (ventas07["MES"]==j),"INDICE GA"]=ventas07.loc[(ventas07["LOCAL"]==k) & (ventas07["MES"]==j),"TOTAL VENTAS"]/ventas07.loc[(ventas07["LOCAL"]==k) & (ventas07["MES"]==j),"TOTAL VENTAS"].sum()
                ventas07.loc[(ventas07["LOCAL"]==k) & (ventas07["MES"]==j),"GASTOS ADMINISTRACION"]=ventas07.loc[(ventas07["LOCAL"]==k) & (ventas07["MES"]==j),"INDICE GA"]*eerr2017().loc[(k,j),"TOTAL GASTOS ADMINISTRACION"]

    ventas07["MARGEN_GA"]=ventas07["MARGEN_E"]-ventas07["GASTOS ADMINISTRACION"] 
    return ventas07
    
def ventas2016():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2016")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    ventas06=pd.read_csv("PLANILLA_VTA_2016.csv",delimiter=";",header=0, encoding='iso-8859-1')
    ventas06["INDICE FT"]=0
    for l in ventas06["LOCAL"].unique():
        for m in ventas06["MES"].unique():
            ventas06.loc[(ventas06["LOCAL"]==l) & (ventas06["MES"]==m), "INDICE FT"]=indice_ft_2016().loc[(l,m),"indice06"]
    ventas06["GASTOS FT"]=ventas06["TOTAL VENTAS"]*ventas06["INDICE FT"]
    ventas06["COMISIONES"]=0
    ventas06["COMISIONES"]=(ventas06["% COMISION"]/100)*ventas06["TOTAL VENTAS"]
    ventas06.loc[(ventas06["DESCRIPCION VENDEDOR"].isin(oficinas+mesones+proveedores)) | (ventas06["LOCAL"].isin(mes)),"COMISIONES"]=0
    for j in ventas06["MES"].unique():
        for k in ventas06["LOCAL"].unique():
                ventas06.loc[(ventas06["LOCAL"]==k) & (ventas06["MES"]==j),"INDICE GA"]=ventas06.loc[(ventas06["LOCAL"]==k) & (ventas06["MES"]==j),"TOTAL VENTAS"]/ventas06.loc[(ventas06["LOCAL"]==k) & (ventas06["MES"]==j),"TOTAL VENTAS"].sum()
                ventas06.loc[(ventas06["LOCAL"]==k) & (ventas06["MES"]==j),"GASTOS ADMINISTRACION"]=ventas06.loc[(ventas06["LOCAL"]==k) & (ventas06["MES"]==j),"INDICE GA"]*eerr2016().loc[(k,j),"TOTAL GASTOS ADMINISTRACION"]
    ventas06["INDICE FC"]=0
    ventas06["TOTAL CONDUCCION"]=0
    for i in ventas06["LOCAL"].unique():
        ventas06.loc[(ventas06["LOCAL"]==i) & (ventas06["OBSERVACION"]=="CON PLANILLA"), "INDICE FC"]=ventas06.loc[(ventas06["LOCAL"]==i) & (ventas06["OBSERVACION"]=="CON PLANILLA"), "TOTAL VENTAS"]/ventas06.loc[(ventas06["LOCAL"]==i) & (ventas06["OBSERVACION"]=="CON PLANILLA"), "TOTAL VENTAS"].sum()
        ventas06.loc[(ventas06["LOCAL"]==i) & (ventas06["OBSERVACION"]=="CON PLANILLA"),"TOTAL CONDUCCION"]=ventas06.loc[(ventas06["LOCAL"]==i) & (ventas06["OBSERVACION"]=="CON PLANILLA"),"INDICE FC"]*eerr2016().loc[(i),"TOTAL CONDUCCION"].sum()
    return ventas06

def ventas2015():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2015")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    ventas05=pd.read_csv("PLANILLA_VTA_2015.csv",delimiter=";",header=0, encoding='iso-8859-1')
    ventas05["INDICE FT"]=0
    for l in ventas05["LOCAL"].unique():
        for m in ventas05["MES"].unique():
            ventas05.loc[(ventas05["LOCAL"]==l) & (ventas05["MES"]==m), "INDICE FT"]=indice_ft_2015().loc[(l,m),"indice05"]
    ventas05["GASTOS FT"]=ventas05["TOTAL VENTAS"]*ventas05["INDICE FT"]
    ventas05["COMISIONES"]=(ventas05["% COMISION"]/100)*ventas05["TOTAL VENTAS"]
    ventas05.loc[(ventas05["DESCRIPCION VENDEDOR"].isin(oficinas+mesones+proveedores)) | (ventas05["LOCAL"].isin(mes)),"COMISIONES"]=0

    for j in ventas05["MES"].unique():
        for k in ventas05["LOCAL"].unique():
                ventas05.loc[(ventas05["LOCAL"]==k) & (ventas05["MES"]==j),"INDICE GA"]=ventas05.loc[(ventas05["LOCAL"]==k) & (ventas05["MES"]==j),"TOTAL VENTAS"]/ventas05.loc[(ventas05["LOCAL"]==k) & (ventas05["MES"]==j),"TOTAL VENTAS"].sum()
                ventas05.loc[(ventas05["LOCAL"]==k) & (ventas05["MES"]==j),"GASTOS ADMINISTRACION"]=ventas05.loc[(ventas05["LOCAL"]==k) & (ventas05["MES"]==j),"INDICE GA"]*eerr2015().loc[(k,j),"TOTAL GASTOS ADMINISTRACION"]
    ventas05["INDICE FC"]=0
    ventas05["TOTAL CONDUCCION"]=0
    for i in ventas05["LOCAL"].unique():
        ventas05.loc[(ventas05["LOCAL"]==i) & (ventas05["OBSERVACION"]=="CON PLANILLA"), "INDICE FC"]=ventas05.loc[(ventas05["LOCAL"]==i) & (ventas05["OBSERVACION"]=="CON PLANILLA"), "TOTAL VENTAS"]/ventas05.loc[(ventas05["LOCAL"]==i) & (ventas05["OBSERVACION"]=="CON PLANILLA"), "TOTAL VENTAS"].sum()
        ventas05.loc[(ventas05["LOCAL"]==i) & (ventas05["OBSERVACION"]=="CON PLANILLA"),"TOTAL CONDUCCION"]=ventas05.loc[(ventas05["LOCAL"]==i) & (ventas05["OBSERVACION"]=="CON PLANILLA"),"INDICE FC"]*eerr2015().loc[(i),"TOTAL CONDUCCION"].sum()
    return ventas05

def ventas2017_cliente():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2017")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    ventas07_cliente=ventas2017()
    ventas07_cliente=ventas07_cliente.sort_values(["RUT","PRODUCTO"])
    for i in ["MARGEN","MARGEN_E","MARGEN_GA","TOTAL VENTAS","COSTO TOTAL VENTAS","GASTOS FINANCIEROS","GASTOS FT","COMISIONES","GASTOS RAPEL"]:
        ventas07_cliente[i] = ventas07_cliente.groupby(["RUT", "PRODUCTO"])[i].transform('sum')
    ventas07_cliente=ventas07_cliente.drop_duplicates(subset=["RUT","PRODUCTO","MARGEN","MARGEN_E","MARGEN_GA","TOTAL VENTAS","COSTO TOTAL VENTAS","GASTOS FINANCIEROS","GASTOS FT"])
    return ventas07_cliente    
    
def eerr2017():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2017")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    eerr07=pd.read_excel("EERR resumen07.xlsx", header=[0], index_col=[0,1])
    return eerr07
def eerr2018():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2018")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    eerr08=pd.read_excel("EERR resumen08.xlsx", header=[0], index_col=[0,1])
    return eerr08
def eerr2016():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2016")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    eerr06=pd.read_excel("EERR resumen06.xlsx", header=[0], index_col=[0,1])
    return eerr06
def eerr2015():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2015")
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    eerr05=pd.read_excel("EERR resumen05.xlsx", header=[0], index_col=[0,1])
    return eerr05

def comisiones2017():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas")
    df = pd.read_excel("comisiones.xlsx", header=[0], index_col=[0,1,2])
    return df

def indice_ft_2018():
    import os
    import pandas as pd
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2018")
    df = pd.read_excel("indice_ft.xlsx", header=[0], index_col=[0,1])
    return df

def indice_ft_2017():
    import os
    import pandas as pd
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2017")
    df = pd.read_excel("indice ft.xlsx", header=[0], index_col=[0,1])
    return df

def indice_ft_2016():
    import os
    import pandas as pd
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2016")
    df = pd.read_excel("indice ft.xlsx", header=[0], index_col=[0,1])
    return df

def indice_ft_2015():
    import os
    import pandas as pd
#    os.chdir(r"C:\Users\siria\Desktop\Material Python\Comercial Chacao\Ventas")
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas\2016")
    df = pd.read_excel("indice ft.xlsx", header=[0], index_col=[0,1])
    return df

def maestro_rubros():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Maestros")
    df = pd.read_excel("Maestro de Rubros y Comisiones.xlsx", header=[0])
    df.drop(df.index[[261,262]],inplace=True)
    df["RUBRO"]=df["RUBRO"].astype("int64")
    return df

def porcentaje_gastos():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Ventas")
    df = pd.read_excel("%2019.xlsx", header=[0], index_col=[0])
    return df

def eerr_base():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Proyecciones")
    df = pd.read_excel("EERR_BASE.xlsx", header=[0], index_col=[0,1])
    return df

def EERR2019():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Proyecciones")
    df = pd.read_excel("EERR2019.xlsx", header=[0], index_col=[0,1])
    return df
def EERR2019_clientes():
    import os
    import pandas as pd
    os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Proyecciones")
    df = pd.read_excel("EERR_clientes.xlsx", header=[0], index_col=[0,1])
    return df
    
#os.chdir(r"C:\Users\PROYECTO\Desktop\Comercial Chacao\Proyecciones")
#eerr36_252 = pd.read_excel("Proyeccion 2019-(36 rubros, 252 clientes).xlsx", header=[0], index_col=[0])
#eerr36_252.reset_index(level=[0],inplace=True) 
#    df.loc[df["LOCAL"]==1,"LOCAL"]="EERR-001-SGO"
#    df.loc[df["LOCAL"]==4,"LOCAL"]="EERR-004-TPA"
#    df.loc[df["LOCAL"]==5,"LOCAL"]="EERR-005-RGA"
#    df.loc[df["LOCAL"]==8,"LOCAL"]="EERR-008-LSE"
#    df.loc[df["LOCAL"]==9,"LOCAL"]="EERR-009-TEM"
#    df.loc[df["LOCAL"]==13,"LOCAL"]="EERR-013-PMT"
#    df.loc[df["LOCAL"]==14,"LOCAL"]="EERR-014-ANF"
#    df.loc[df["LOCAL"]==16,"LOCAL"]="EERR-016-IQD"
#    df.loc[df["LOCAL"]==29,"LOCAL"]="EERR-029-SME"
#    df.loc[df["LOCAL"]==50,"LOCAL"]="EERR-050-SMO"
#    df.loc[df["LOCAL"]==3,"LOCAL"]="EERR-003-IQZ"
#    df.loc[df["LOCAL"]==21,"LOCAL"]="EERR-021-M21"
#    df.loc[df["LOCAL"]==10,"LOCAL"]="EERR-010-CMA"
#    df.loc[df["LOCAL"]==17,"LOCAL"]="EERR-017-PAR"
#    df.loc[df["LOCAL"]==38,"LOCAL"]="EERR-038-BSR"
#    df[["LOCAL","MES"]]=df[["LOCAL","MES"]].astype(str)
#    df["indice"] = df[["LOCAL", "MES"]].apply(lambda x: "_".join(x), axis=1)
#    df.set_index("indice", inplace=True)
#    df.drop(labels=["LOCAL","MES"],axis=1,inplace=True)
#
#    eerr09=df.transpose()
