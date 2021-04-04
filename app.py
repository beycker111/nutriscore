from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import win32api
import os

from tkinter import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import tkinter as tk

app = Flask(__name__) #Archivo main

@app.route('/', methods=['GET', 'POST']) #Ruta raíz, retornando la plantilla principal de la carpeta "templates"
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        #file = request.get_data['upload-file'] #form['upload-file'] ---->POR AQUI
        #Perfil = pd.read_excel(file) # data= Perfil 
        #return render_template('data.html', Perfil=data.to_dict())
        # data=data.to_html())
        # data=data.to_dict())
        #f = request.form['csvfile']
        #print('BEYCKER AQUI' + os.path.abspath(request.form['csvfile']))
        #filename = 'C:/Users/Lenovo/Desktop/Nutriscore (Todas).xlsx'
        filename = request.form['ruta'] + request.form['csvfile']
        Perfil = pd.read_excel(pd.ExcelFile(filename))

        #2. Transformación de valores nutricionales a 100g -----------------------------------------------
        Perfil_100 = Perfil
        Perfil_100['Calorías totales (Kcal)'] = 100*4.184*Perfil['Calorías totales (Kcal)']/Perfil['Tamaño de porción (g)'] #Se convierte a KJ
        Perfil_100['Azúcares (g)'] = 100*Perfil['Azúcares (g)']/Perfil['Tamaño de porción (g)']
        Perfil_100['Grasa total (g)'] = 100*Perfil['Grasa total (g)']/Perfil['Tamaño de porción (g)']
        Perfil_100['Grasa saturada (g)'] = 100*Perfil['Grasa saturada (g)']/Perfil['Tamaño de porción (g)']
        Perfil_100['Sodio (mg)'] = 100*Perfil['Sodio (mg)']/Perfil['Tamaño de porción (g)']
        Perfil_100['Proteína (g)'] = 100*Perfil['Proteína (g)']/Perfil['Tamaño de porción (g)']
        Perfil_100['Fibra (g)'] = 100*Perfil['Fibra (g)']/Perfil['Tamaño de porción (g)']
        
        Perfil_100['Tamaño de porción (g)'] = 100


    #------------------------------------------------------------------------------------------------------------
    #3. Cálculo de puntos N (Negativos) --------------------------------------------------------------
            #3.1 Puntos N por energía
            #3.1.1 Para todo menos bebidas
        Perfil_100['Puntos_energia'] = -1
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']<=355) & (Perfil_100['category'] != 'Beverages')] = 0
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>355) & (Perfil_100['Calorías totales (Kcal)']<=670) & (Perfil_100['category'] != 'Beverages')] = 1
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>670) & (Perfil_100['Calorías totales (Kcal)']<=1005) & (Perfil_100['category'] != 'Beverages')] = 2
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>1005) & (Perfil_100['Calorías totales (Kcal)']<=1340) & (Perfil_100['category'] != 'Beverages')] = 3
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>1340) & (Perfil_100['Calorías totales (Kcal)']<=1675) & (Perfil_100['category'] != 'Beverages')] = 4
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>1675) & (Perfil_100['Calorías totales (Kcal)']<=2010) & (Perfil_100['category'] != 'Beverages')] = 5
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>2010) & (Perfil_100['Calorías totales (Kcal)']<=2345) & (Perfil_100['category'] != 'Beverages')] = 6
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>2345) & (Perfil_100['Calorías totales (Kcal)']<=2680) & (Perfil_100['category'] != 'Beverages')] = 7
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>2680) & (Perfil_100['Calorías totales (Kcal)']<=3015) & (Perfil_100['category'] != 'Beverages')] = 8
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>3015) & (Perfil_100['Calorías totales (Kcal)']<=3350) & (Perfil_100['category'] != 'Beverages')] = 9
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>3550) & (Perfil_100['category'] != 'Beverages')] = 10
            #3.1.2 Para bebidas
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']<=0) & (Perfil_100['category'] == 'Beverages')] = 0
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>0) & (Perfil_100['Calorías totales (Kcal)']<=30) & (Perfil_100['category'] == 'Beverages')] = 1
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>30) & (Perfil_100['Calorías totales (Kcal)']<=60) & (Perfil_100['category'] == 'Beverages')] = 2
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>60) & (Perfil_100['Calorías totales (Kcal)']<=90) & (Perfil_100['category'] == 'Beverages')] = 3
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>90) & (Perfil_100['Calorías totales (Kcal)']<=120) & (Perfil_100['category'] == 'Beverages')] = 4
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>120) & (Perfil_100['Calorías totales (Kcal)']<=150) & (Perfil_100['category'] == 'Beverages')] = 5
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>150) & (Perfil_100['Calorías totales (Kcal)']<=180) & (Perfil_100['category'] == 'Beverages')] = 6
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>180) & (Perfil_100['Calorías totales (Kcal)']<=210) & (Perfil_100['category'] == 'Beverages')] = 7
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>210) & (Perfil_100['Calorías totales (Kcal)']<=240) & (Perfil_100['category'] == 'Beverages')] = 8
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>240) & (Perfil_100['Calorías totales (Kcal)']<=270) & (Perfil_100['category'] == 'Beverages')] = 9
        Perfil_100['Puntos_energia'][(Perfil_100['Calorías totales (Kcal)']>270) & (Perfil_100['category'] == 'Beverages')] = 10
        
            #3.2 Puntos N por saturados
        Perfil_100['Puntos_saturados'] = -1
        Perfil_100['Puntos_saturados'][Perfil_100['Grasa saturada (g)']<=1] = 0
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>1) & (Perfil_100['Grasa saturada (g)']<=2)] = 1
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>2) & (Perfil_100['Grasa saturada (g)']<=3)] = 2
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>3) & (Perfil_100['Grasa saturada (g)']<=4)] = 3
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>4) & (Perfil_100['Grasa saturada (g)']<=5)] = 4
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>5) & (Perfil_100['Grasa saturada (g)']<=6)] = 5
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>6) & (Perfil_100['Grasa saturada (g)']<=7)] = 6
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>7) & (Perfil_100['Grasa saturada (g)']<=8)] = 7
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>8) & (Perfil_100['Grasa saturada (g)']<=9)] = 8
        Perfil_100['Puntos_saturados'][(Perfil_100['Grasa saturada (g)']>9) & (Perfil_100['Grasa saturada (g)']<=10)] = 9
        Perfil_100['Puntos_saturados'][Perfil_100['Grasa saturada (g)']>10] = 10
        
            #3.3 Puntos N por azucar
            #3.3.1 Para todo menos bebidas
        Perfil_100['Puntos_azucar'] = -1
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']<=4.5) & (Perfil_100['category'] != 'Beverages')] = 0
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>4.5) & (Perfil_100['Azúcares (g)']<=9) & (Perfil_100['category'] != 'Beverages')] = 1
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>9) & (Perfil_100['Azúcares (g)']<=13.5) & (Perfil_100['category'] != 'Beverages')] = 2
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>13.5) & (Perfil_100['Azúcares (g)']<=18) & (Perfil_100['category'] != 'Beverages')] = 3
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>18) & (Perfil_100['Azúcares (g)']<=22.5) & (Perfil_100['category'] != 'Beverages')] = 4
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>22.5) & (Perfil_100['Azúcares (g)']<=27) & (Perfil_100['category'] != 'Beverages')] = 5
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>27) & (Perfil_100['Azúcares (g)']<=31) & (Perfil_100['category'] != 'Beverages')] = 6
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>31) & (Perfil_100['Azúcares (g)']<=36) & (Perfil_100['category'] != 'Beverages')] = 7
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>36) & (Perfil_100['Azúcares (g)']<=40) & (Perfil_100['category'] != 'Beverages')] = 8
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>40) & (Perfil_100['Azúcares (g)']<=45) & (Perfil_100['category'] != 'Beverages')] = 9
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>45) & (Perfil_100['category'] != 'Beverages')] = 10
            #3.3.2 Para bebidas
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']<=0) & (Perfil_100['category'] == 'Beverages')] = 0
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>0) & (Perfil_100['Azúcares (g)']<=1.5) & (Perfil_100['category'] == 'Beverages')] = 1
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>1.5) & (Perfil_100['Azúcares (g)']<=3) & (Perfil_100['category'] == 'Beverages')] = 2
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>3) & (Perfil_100['Azúcares (g)']<=4.5) & (Perfil_100['category'] == 'Beverages')] = 3
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>4.5) & (Perfil_100['Azúcares (g)']<=6) & (Perfil_100['category'] == 'Beverages')] = 4
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>6) & (Perfil_100['Azúcares (g)']<=7.5) & (Perfil_100['category'] == 'Beverages')] = 5
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>7.5) & (Perfil_100['Azúcares (g)']<=9) & (Perfil_100['category'] == 'Beverages')] = 6
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>9) & (Perfil_100['Azúcares (g)']<=10.5) & (Perfil_100['category'] == 'Beverages')] = 7
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>10.5) & (Perfil_100['Azúcares (g)']<=12) & (Perfil_100['category'] == 'Beverages')] = 8
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>12) & (Perfil_100['Azúcares (g)']<=13.5) & (Perfil_100['category'] == 'Beverages')] = 9
        Perfil_100['Puntos_azucar'][(Perfil_100['Azúcares (g)']>13.5) & (Perfil_100['category'] == 'Beverages')] = 10  
            
            #3.4 Puntos N por sodio
        Perfil_100['Puntos_sodio'] = -1
        Perfil_100['Puntos_sodio'][Perfil_100['Sodio (mg)']<=90] = 0
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>90) & (Perfil_100['Sodio (mg)']<=180)] = 1
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>180) & (Perfil_100['Sodio (mg)']<=270)] = 2
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>270) & (Perfil_100['Sodio (mg)']<=360)] = 3
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>360) & (Perfil_100['Sodio (mg)']<=450)] = 4
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>450) & (Perfil_100['Sodio (mg)']<=540)] = 5
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>540) & (Perfil_100['Sodio (mg)']<=630)] = 6
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>630) & (Perfil_100['Sodio (mg)']<=720)] = 7
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>720) & (Perfil_100['Sodio (mg)']<=810)] = 8
        Perfil_100['Puntos_sodio'][(Perfil_100['Sodio (mg)']>810) & (Perfil_100['Sodio (mg)']<=900)] = 9
        Perfil_100['Puntos_sodio'][Perfil_100['Sodio (mg)']>900] = 10
        
            #3.5 Ratio grasas saturadas, solo para categoria 'Added Fats' PENDIENTE
            
            #3.6 Puntos N = P_energia + P_saturados + P_azucar + P_sodio
        Perfil_100['PuntosN'] = Perfil_100['Puntos_energia']+Perfil_100['Puntos_saturados']+Perfil_100['Puntos_azucar']+Perfil_100['Puntos_sodio']
        
        #4. Cálculo de puntos P (Positivos) ---------------------------------------------------------------
            #4.1 Puntos P por FVP (frutas, verduras, nueves y otros)
            #4.1.1 Para todo menos bebidas
        Perfil_100['Puntos_FVP'] = 0
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']<=40) & (Perfil_100['category'] != 'Beverages')] = 0
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']>40) & (Perfil_100['Frutas_verduras_otros (%)']<=60) & (Perfil_100['category'] != 'Beverages')] = 1
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']>60) & (Perfil_100['Frutas_verduras_otros (%)']<=80) & (Perfil_100['category'] != 'Beverages')] = 2
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']>80) & (Perfil_100['category'] != 'Beverages')] = 5
            #4.1.2 Para bebidas
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']<=40) & (Perfil_100['category'] == 'Beverages')] = 0
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']>40) & (Perfil_100['Frutas_verduras_otros (%)']<=60) & (Perfil_100['category'] == 'Beverages')] = 2
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']>60) & (Perfil_100['Frutas_verduras_otros (%)']<=80) & (Perfil_100['category'] == 'Beverages')] = 4
        Perfil_100['Puntos_FVP'][(Perfil_100['Frutas_verduras_otros (%)']>80) & (Perfil_100['category'] == 'Beverages')] = 10
            
            #4.2 Puntos P por fibra
        Perfil_100['Puntos_fibra'] = -1
        Perfil_100['Puntos_fibra'][Perfil_100['Fibra (g)']<=0.9] = 0
        Perfil_100['Puntos_fibra'][(Perfil_100['Fibra (g)']>0.9) & (Perfil_100['Fibra (g)']<=1.9)] = 1
        Perfil_100['Puntos_fibra'][(Perfil_100['Fibra (g)']>1.9) & (Perfil_100['Fibra (g)']<=2.8)] = 2
        Perfil_100['Puntos_fibra'][(Perfil_100['Fibra (g)']>2.8) & (Perfil_100['Fibra (g)']<=3.7)] = 3
        Perfil_100['Puntos_fibra'][(Perfil_100['Fibra (g)']>3.7) & (Perfil_100['Fibra (g)']<=4.7)] = 4
        Perfil_100['Puntos_fibra'][Perfil_100['Fibra (g)']>4.7] = 5
            
            #4.3 Puntos P por proteina
        Perfil_100['Puntos_proteina'] = -1
        Perfil_100['Puntos_proteina'][Perfil_100['Proteína (g)']<=1.6] = 0
        Perfil_100['Puntos_proteina'][(Perfil_100['Proteína (g)']>1.6) & (Perfil_100['Proteína (g)']<=3.2)] = 1
        Perfil_100['Puntos_proteina'][(Perfil_100['Proteína (g)']>3.2) & (Perfil_100['Proteína (g)']<=4.8)] = 2
        Perfil_100['Puntos_proteina'][(Perfil_100['Proteína (g)']>4.8) & (Perfil_100['Proteína (g)']<=6.4)] = 3
        Perfil_100['Puntos_proteina'][(Perfil_100['Proteína (g)']>6.4) & (Perfil_100['Proteína (g)']<=8)] = 4
        Perfil_100['Puntos_proteina'][Perfil_100['Proteína (g)']>8] = 5
        
            #4.4 Puntos P = P_FVP + P_fibra + P_proteina
        Perfil_100['PuntosP'] = Perfil_100['Puntos_FVP'] + Perfil_100['Puntos_fibra'] + Perfil_100['Puntos_proteina']
                
        #5. Cálculo del Nutriscore ----------------------------------------------------------------------
        #Si Puntos_N>11, no cuenta puntos_proteina, a menos que Puntos_FVP>5
        Perfil_100['Nutriscore'] = 999
        for i,row in Perfil_100.iterrows():
            if Perfil_100.loc[i,'category'] == 'Cheese':
                Perfil_100.loc[i,'Nutriscore'] = Perfil_100.loc[i,'PuntosN'] - Perfil_100.loc[i,'PuntosP']
            #elif Perfil_100.loc[i,'category'] == 'Added fats':
            elif Perfil_100.loc[i,'category'] == 'Beverages' or Perfil_100.loc[i,'category'] == 'Others':
                if Perfil_100.loc[i,'PuntosN'] < 11:
                    Perfil_100.loc[i,'Nutriscore'] = Perfil_100.loc[i,'PuntosN'] - Perfil_100.loc[i,'PuntosP']
                elif Perfil_100.loc[i,'PuntosN'] >= 11 and Perfil_100.loc[i,'Puntos_FVP'] >= 5: 
                    Perfil_100.loc[i,'Nutriscore'] = Perfil_100.loc[i,'PuntosN'] - Perfil_100.loc[i,'PuntosP']
                else:
                    Perfil_100.loc[i,'Nutriscore'] = Perfil_100.loc[i,'PuntosN'] - (Perfil_100.loc[i,'Puntos_FVP'] + Perfil_100.loc[i,'Puntos_fibra'])
                    
        #6. Determinación de NutriLetra -----------------------------------------------------------------
        Perfil_100['NutriLetra'] = ''
        for i,row in Perfil_100.iterrows():
            if Perfil_100.loc[i,'category'] == 'Beverages':
                if Perfil_100.loc[i,'Nutriscore'] <= 1:
                    Perfil_100.loc[i,'NutriLetra'] = 'B'
                elif Perfil_100.loc[i,'Nutriscore'] >= 2 and Perfil_100.loc[i,'Nutriscore'] <= 5:
                    Perfil_100.loc[i,'NutriLetra'] = 'C'
                elif Perfil_100.loc[i,'Nutriscore'] >= 6 and Perfil_100.loc[i,'Nutriscore'] <= 9:
                    Perfil_100.loc[i,'NutriLetra'] = 'D'
                elif Perfil_100.loc[i,'Nutriscore'] >= 10:
                    Perfil_100.loc[i,'NutriLetra'] = 'E'
            else:
                if Perfil_100.loc[i,'Nutriscore'] <= -1:
                    Perfil_100.loc[i,'NutriLetra'] = 'A'
                elif Perfil_100.loc[i,'Nutriscore'] >= 0 and Perfil_100.loc[i,'Nutriscore'] <= 2:
                    Perfil_100.loc[i,'NutriLetra'] = 'B'
                elif Perfil_100.loc[i,'Nutriscore'] >= 3 and Perfil_100.loc[i,'Nutriscore'] <= 10:
                    Perfil_100.loc[i,'NutriLetra'] = 'C'
                elif Perfil_100.loc[i,'Nutriscore'] >= 11 and Perfil_100.loc[i,'Nutriscore'] <= 18:
                    Perfil_100.loc[i,'NutriLetra'] = 'D'
                elif Perfil_100.loc[i,'Nutriscore'] >= 19:
                    Perfil_100.loc[i,'NutriLetra'] = 'E'
                    
        #-------------------------------------------------------------------------------------------
        #7. Impresión de resultados --------------------------------------------------------------------
        Perfil['Nutriscore'] = Perfil_100['Nutriscore']
        Perfil['NutriLetra'] = Perfil_100['NutriLetra']
        
        Totales = [sum(Perfil['NutriLetra']=='A'),
                sum(Perfil['NutriLetra']=='B'),
                sum(Perfil['NutriLetra']=='C'),
                sum(Perfil['NutriLetra']=='D'),
                sum(Perfil['NutriLetra']=='E')]
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    #Impresión y excel    
        #lbl_Resultados.configure(text='Totales: '+str(sum(Totales))+' | A: '+str(Totales[0])+' B: '+str(Totales[1])+' C: '+str(Totales[2])+' D: '+str(Totales[3])+' E: '+str(Totales[4]))
        
        filename_salida = filename.replace(".xlsx", " (Calculado).xlsx")
        Perfil.to_excel(filename_salida,index=False)
        #messagebox.showinfo(message='Nutriscore calculado, puede encontrar el resultado completo en: '+str(filename_salida), title="Listolas")
        #win32api.MessageBox(0, 'Nutriscore calculado, puede encontrar el resultado completo en: '+str(filename_salida), 'Listolas')
        return 'Nutriscore calculado, puede encontrar el resultado completo en: '+str(filename_salida)
    
@app.route('/formato', methods=['GET', 'POST'])
def Formato():
    d_formato = {'Material': [2012282,1046489,0,1035440],	
                 'Descripción': ['Pas. Tosh Bizcocho Hierbas Bx6 132g','Pas. Pita Chips TOSH Cebolla Bs.  156g','Tosh Bebida Tres nueces','Gta. TOSH Wafer Multicereal KIWI Bs. X6'],	
                 'Tamaño de porción (g)': [22,26,240,27],	
                 'Calorías totales (Kcal)': [90,110,100,100],	
                 'Azúcares (g)': [1,2,0,1],
                 'Grasa total (g)': [3,4.5,5,6],	
                 'Grasa saturada (g)': [1.5,1.5,2.5,3],	
                 'Sodio (mg)': [140,80,20,25],	
                 'Frutas_verduras_otros (%)': [0,0,0,0],	
                 'Proteína (g)': [1,2,1,1],	
                 'Fibra (g)': [1.5,1,5,0],	
                 'category': ['Others','Others','Beverages','Others']}
    formato_xlsx = pd.DataFrame(data=d_formato)
    formato_xlsx.to_excel(request.form['ruta'] + 'Formato Nutriscore.xlsx',index=False)
    return 'El formato se guardó en:' + request.form['ruta'] + 'Formato Nutriscore.xlsx'
   # messagebox.showinfo(message="El formato se guardó en: "+str(pathlib.Path().absolute())+' con el nombre "Formato Nutriscore"', title="Listolas")

# Inicializar ventana    

    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------



#@app.route('/datos')
#def datos():
    #file.upload() #
 #   misdatos=("PHP", "JAVA","PYTHON","JAVA","C#")
  #  return render_template('datos.html', datos=misdatos)

if __name__ == '__main__':
    app.run(debug=True)
