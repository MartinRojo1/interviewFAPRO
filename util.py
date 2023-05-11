
from bs4 import BeautifulSoup
import pandas as pd
import requests

############################################################################################
####################################### FUNCIONES ##########################################

def tomar_tabla(anio: int, mes: int) -> BeautifulSoup :

    '''
    El objetivo de esta funcion es hacer un scraping de la tabla.

    '''
    
    # Se construye la URL de la página web que contiene la tabla de la UF del año
    url = f'https://www.sii.cl/valores_y_fechas/uf/uf{anio}.htm'
    
    # Se realiza la petición GET a la URL
    response = requests.get(url)
    
    # Si la petición fue exitosa (código 200)
    if response.status_code == 200:
    
        # Se crea un objeto Beautiful Soup a partir del contenido HTML de la respuesta
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Se buscan todas las tablas de la página, y se selecciona la tabla correspondiente al mes indicado
        tabla= soup.find_all('table')[int(mes)]

        return tabla
    
##################################################################################################################################################

def transformar_tabla(tabla : BeautifulSoup) -> pd.DataFrame:
    
    '''
    Esta funcion se encarga de transformar el HTML a Dataframe.

    '''
    
    # Con la función "read_html" de pandas podemos leer una tabla en formato HTML y obtener un dataframe
    df = pd.read_html(str(tabla))[0]

    ''' Separamos las columnas en 3 grupos (primeros 10 días, segundos 10 días, últimos días) '''
    ################################################################################################
    
    primeros = df.iloc[:, :2]
    primeros.columns = ['Dia', 'Valor']

    segundos = df.iloc[:, 2:4]
    segundos.columns = ['Dia', 'Valor']

    terceros = df.iloc[:, 4:]
    terceros.columns = ['Dia', 'Valor']
    
    ################################################################################################
    
    # Unimos los tres grupos de columnas en un solo dataframe
    DataFrame = pd.concat([primeros, segundos,terceros], axis=0)

    return DataFrame

##################################################################################################################################################

def buscar_valor(Dataframe : pd.DataFrame, dia : int) -> str:
    
    '''
    Esta funcion busca en un DataFrame el valor asociado a un día ingresado por parámetro.
    
    '''
    
    # Si el DataFrame está vacío
    if Dataframe.empty:
        return "No se encontró ningún valor para el día ingresado. Intente con otra fecha."
    
    else:
        
        # Creo una variable con el valor encontrado
        valor_encontrado= Dataframe[Dataframe['Dia'] == dia]
        return str(valor_encontrado['Valor'].iloc[0]).replace('.', '').replace(',', '.')
    
##################################################################################################################################################

def cambio_mes(mes : int, anio : int) -> int:
    
    '''
    Esta funcion tiene como objetivo podes comparar los meses y tomar en base al mes cargado, el valor correcto para crear el request a la pagina.
    
    '''
    # Se crea un diccionario con los datos
    data = {'mes': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
        'carga_usuario': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'python': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'api': [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        'api2023' : [5,4,3,2,1,0,None,None,None,None,None,None]}
    
    # Se convierte el diccionario en un DataFrame de Pandas
    df = pd.DataFrame(data) 
        
    # Si el año es 2023, se devuelve la carga de la columna 'api2023' correspondiente al mes ingresado
    if anio == 2023:
        return mes,df['api2023'][df['carga_usuario'] == mes]
    
    # Si no, se devuelve la carga de la columna 'api' correspondiente al mes ingresado
    else:
        return mes,df['api'][df['carga_usuario'] == mes]


