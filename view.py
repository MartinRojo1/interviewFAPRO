from flask import Blueprint,render_template,request,make_response
from util import buscar_valor,cambio_mes,tomar_tabla,transformar_tabla

############################################################################################

# Creo instancia de Blueprint
router = Blueprint("app_router", __name__,template_folder='templates')

############################################################################################

@router.route("/", methods=["GET"])
def index():

    '''
    Index endpoint, retorna el HTML.

    '''

    return render_template("page.html",ver=True)

############################################################################################

@router.route("/", methods=["POST"])
def index_post():

    '''
    Endpoint para buscar el valor segun la fecha cargada.
    
    '''

    # Obtengo la fecha con el metodo get
    fecha = request.form.get('fecha')

    # Separo la fecha en mes,dia y anio
    anio,mes,dia = fecha.split("-")

    # Adapto el mes
    mes_normal,mes = cambio_mes(int(mes),int(anio))

    ################################################################################
 
    try:

        # llamo a la funcion tomar_tabla para extrar la tabla de la web
        tabla = tomar_tabla(anio, mes)

    except Exception as e:

        return render_template("error.html", message="Error al obtener la tabla: {}".format(e))


    ################################################################################

    try:

        # llamo a la funcion transformar_tabla para transformar la tabla en un Dataframe
        Dataframe = transformar_tabla(tabla)

    except Exception as e:

        return render_template("error.html", message="Error al transformar la tabla: {}".format(e))


    ################################################################################

    try:

        # llamo a la funcion buscar_valor para obtener el valor final
        valor_encontrado = buscar_valor(Dataframe,int(dia))

    except Exception as e:

        return render_template("error.html",message="Error al buscar el valor: {}".format(e))
    

    ################################################################################
    
    # Creo una variable con la fecha cargada
    valor = f'{dia}/{mes_normal}/{anio}'

    return render_template("page.html",ver=False,fecha=valor,valor_encontrado = valor_encontrado)

   
@router.route("/api", methods=["POST"])
def index_api():

    '''
    Esta vista es la que permite al usuario acceder a nuestra API para hacer consultas.

    '''
    # Obtengo la fecha con el metodo get
    fecha = request.args.get('fecha')
    
    # Chekep si se cargo una fecha
    if fecha is None:
        
        # Si es None retorna:
        return make_response({"Text": None, "Category": None}, 400)

    # Si la variable no es Nula
    else:
        
        # Separo la fecha en mes,dia y anio
        anio,mes,dia = fecha.split("/")
        
        # Adapto el mes
        mes_normal,mes = cambio_mes(int(mes),int(anio))
        
        ################################################################################
    
        try:

            # llamo a la funcion tomar_tabla para extrar la tabla de la web
            tabla = tomar_tabla(anio, mes)

        except Exception:

            return make_response({"Fecha": fecha, "Valor": None}, 400)


        ################################################################################

        try:

            # llamo a la funcion transformar_tabla para transformar la tabla en un Dataframe
            Dataframe = transformar_tabla(tabla)

        except Exception :

            return make_response({"Fecha": None, "Valor": None}, 400)


        ################################################################################

        try:

            # llamo a la funcion buscar_valor para obtener el valor final
            valor_encontrado = buscar_valor(Dataframe,int(dia))

        except Exception:

            return make_response({"Fecha": None, "Valor": None}, 400)
        

        ################################################################################

        # Creo una variable con la fecha cargada
        valor = f'{dia}/{mes_normal}/{anio}'

        # Si existe un valor
        if not valor_encontrado:

                return make_response("No se detecto ningun valor para esta fecha", 200)
            
        # Si no existe   
        else:

                return make_response({"Fecha": valor, "Valor": valor_encontrado}, 200)