
from bs4 import BeautifulSoup
import pandas as pd
import requests

############################################################################################
####################################### FUNCIONES ##########################################

def tomar_tabla(anio: int, mes: int) -> BeautifulSoup :

    '''
    El objetivo de esta funcion es hacer un scraping de la tabla.

    '''
    url = f'https://www.sii.cl/valores_y_fechas/uf/uf{anio}.htm'

    response = requests.get(url)

    if response.status_code == 200:
    
        soup = BeautifulSoup(response.content, 'html.parser')
    
        tabla= soup.find_all('table')[int(mes)]

        return tabla

def transformar_tabla(tabla : BeautifulSoup) -> pd.DataFrame:
    
    '''
    Esta funcion se encarga de transformar el HTML a Dataframe.

    '''

    df = pd.read_html(str(tabla))[0]

    primeros = df.iloc[:, :2]
    primeros.columns = ['Dia', 'Valor']

    segundos = df.iloc[:, 2:4]
    segundos.columns = ['Dia', 'Valor']

    terceros = df.iloc[:, 4:]
    terceros.columns = ['Dia', 'Valor']

    DataFrame = pd.concat([primeros, segundos,terceros], axis=0)

    return DataFrame


def buscar_valor(Dataframe : pd.DataFrame, dia : int) -> str:
    
    if Dataframe.empty:
        return "No se encontró ningún valor para el día ingresado. Intente con otra fecha."
    else:
        valor_encontrado= Dataframe[Dataframe['Dia'] == dia]
        return str(valor_encontrado['Valor'].iloc[0]).replace('.', '').replace(',', '.')

def cambio_mes(mes : int, anio : int) -> int:

    data = {'mes': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
        'carga_usuario': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'python': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'api': [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        'api2023' : [5,4,3,2,1,0,None,None,None,None,None,None]}
    
    df = pd.DataFrame(data) 

    if anio == 2023:
        
        return mes,df['api2023'][df['carga_usuario'] == mes]
    
    else:

        return mes,df['api'][df['carga_usuario'] == mes]


############################################################################################