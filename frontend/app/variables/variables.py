import psycopg2
import pandas as pd

def get_table(table_name, limit=0):
    conexion = psycopg2.connect(host="team-82.cc7kkbiuuvan.us-east-2.rds.amazonaws.com", database="masivo_capital", user="team_82", password="Ds4ateam_82")
    # Creamos el cursor con el objeto conexion
    cur = conexion.cursor()
    if limit == 0:
        cur.execute('SELECT * FROM '+table_name+'')
    else:
        cur.execute('SELECT * FROM '+table_name+' LIMIT '+str(limit))
    data = cur.fetchall()
    cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='{}'".format(table_name))
    table = pd.DataFrame(data, columns=[c[0] for c in cur])
    return table

def my_variables(request):
    global validaciones
    return {
        "flotas": validaciones['vehiculo'].unique().size,
        "paradas": validaciones['parada'].unique().size,
        "rutas": validaciones['ruta_modificada'].unique().size,
        "tipo": validaciones['tipo_vahiculo'].mode()[0],
    }

validaciones = get_table('validaciones_v2',10000)
validaciones_lite = get_table('validaciones_v2',20)
historico_demanda = get_table('historico_demanda_v2',10000)

