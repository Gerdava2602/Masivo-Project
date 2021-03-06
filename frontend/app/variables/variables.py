import psycopg2
import pandas as pd
from joblib import dump, load
from tensorflow import keras

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
historico_demanda = get_table('historico_demanda_v2',10)
oferta = get_table('actividades', 10000)

models = {
    
    0 : keras.models.load_model('modelos/nn_cluster_0'),
    1 : keras.models.load_model('modelos/nn_cluster_1'),
    2 : keras.models.load_model('modelos/nn_cluster_2'),
    3 : load('modelos/forest_cluster_3.joblib'),
    4 : keras.models.load_model('modelos/nn_cluster_4/'),
}

#Model Dataframes
cluster_0 = pd.DataFrame(columns=['val_month',
'val_day',
'val_hour',
'Transbordo',
'Viaje Inicial',
'0.0',
'1.0',
'9.0',
'68.0',
'69.0',
'90.0',
'160.0',
'240.0',
'306.0',
'329.0',
'369.0',
'394.0',
'475.0',
'480.0',
'487.0',
'527.0',
'538.0',
'559.0',
'605.0',
'640.0',
'649.0',
'650.0',
'727.0',
'779.0',
'822.0',
'824.0',
'833.0',
'923.0',
'956.0',
'958.0',
'974.0',
'1007.0',
'1009.0',
'1052.0',
'1055.0',
'1056.0',
'1058.0',
'1063.0',
'1084.0',
'1088.0',
'1092.0',
'1101.0',
'1102.0',
'1110.0',
'1111.0',
'1112.0',
'1113.0',
'1130.0',
'1131.0',
'1138.0',
'1173.0',
'1208.0',
'1218.0',
'1227.0',
'1231.0',
'1247.0',
'1252.0',
'1260.0',
'1274.0',
'1276.0',
'1291.0',
'1326.0',
'1345.0',
'1347.0',
'1379.0',
'1381.0',
'1383.0',
'1384.0',
'1387.0',
'1392.0',
'1396.0',
'1398.0',
'1402.0',
'1418.0',
'1419.0',
'1420.0',
'1425.0',
'1426.0',
'1430.0',
'1433.0',
'1436.0',
'1437.0',
'61606.0',
'0.0',
'1.0',
'871.0',
'1157.0',
'1445.0',
'1497.0',
'1498.0',
'1500.0',
'1903.0',
'1904.0',
'2093.0',
'2094.0',
'2107.0',
'2471.0',
'2472.0',
'2524.0',
'2974.0',
'3004.0',
'3005.0',
'3139.0',
'3140.0',
'3141.0',
'3142.0',
'3379.0',
'3380.0',
'3491.0',
'3492.0',
'3595.0',
'3596.0',
'3657.0',
'3823.0',
'3980.0',
'3981.0',
'4009.0',
'4012.0',
'4013.0',
'4014.0',
'4130.0',
'4131.0',
'4132.0',
'4133.0',
'4135.0',
'4136.0',
'4149.0',
'4162.0',
'4245.0',
'4251.0',
'4294.0',
'4295.0',
'4296.0',
'4307.0',
'4371.0',
'4372.0',
'4388.0',
'4389.0',
'4613.0',
'4623.0',
'4625.0',
'4645.0',
'4775.0',
'4806.0',
'4827.0',
'4828.0',
'4870.0',
'4871.0',
'4873.0',
'4875.0',
'4876.0',
'4878.0',
'4879.0',
'4918.0',
'4919.0',
'4920.0',
'4921.0',
'4924.0',
'4925.0',
'4926.0',
'4937.0',
'4942.0',
'4943.0',
'4944.0',
'4992.0',
'4993.0',
'4994.0',
'5023.0',
'5135.0',
'5136.0',
'5221.0',
'5356.0',
'5357.0',
'5408.0',
'5423.0',
'5451.0',
'5453.0',
'5494.0',
'5506.0',
'5545.0',
'5574.0',
'5575.0',
'5602.0',
'5620.0',
'5621.0',
'5643.0',
'5769.0',
'5770.0',
'5850.0',
'5854.0',
'5855.0',
'5949.0',
'5960.0',
'5961.0',
'5970.0',
'5987.0',
'5988.0',
'5989.0',
'5990.0',
'5998.0',
'6012.0',
'6032.0',
'6033.0',
'6039.0',
'6041.0',
'6060.0',
'6061.0',
'6066.0',
'6081.0',
'6082.0',
'6083.0',
'6118.0',
'6120.0',
'6180.0',
'6187.0',
'6188.0',
'6190.0',
'6199.0',
'6200.0',
'6208.0',
'6209.0',
'6210.0',
'6220.0',
'6225.0',
'6226.0',
'6227.0',
'6228.0',
'6229.0',
'6230.0',
'6231.0',
'6232.0',
'6237.0',
'6238.0',
'6323.0',
'Friday',
'Monday',
'Saturday',
'Sunday',
'Thursday',
'Tuesday',
'Wednesday',])

cluster_1 = pd.DataFrame(columns=['val_month',
'val_day',
'val_hour',
'Transbordo',
'Viaje Inicial',
'0.0',
'69.0',
'160.0',
'306.0',
'394.0',
'480.0',
'487.0',
'543.0',
'605.0',
'640.0',
'650.0',
'748.0',
'789.0',
'803.0',
'824.0',
'882.0',
'923.0',
'1007.0',
'1009.0',
'1052.0',
'1055.0',
'1063.0',
'1084.0',
'1101.0',
'1110.0',
'1113.0',
'1131.0',
'1138.0',
'1160.0',
'1167.0',
'1168.0',
'1169.0',
'1231.0',
'1247.0',
'1260.0',
'1274.0',
'1291.0',
'1326.0',
'1347.0',
'1381.0',
'1392.0',
'1396.0',
'1402.0',
'1415.0',
'1419.0',
'1420.0',
'1425.0',
'1430.0',
'1436.0',
'0.0',
'371.0',
'871.0',
'1157.0',
'1445.0',
'2093.0',
'2094.0',
'2391.0',
'2848.0',
'3004.0',
'3005.0',
'3139.0',
'3140.0',
'3491.0',
'3492.0',
'3657.0',
'3823.0',
'3974.0',
'3980.0',
'3981.0',
'4149.0',
'4251.0',
'4294.0',
'4295.0',
'4296.0',
'4327.0',
'4328.0',
'4371.0',
'4372.0',
'4388.0',
'4389.0',
'4411.0',
'4613.0',
'4623.0',
'4775.0',
'4870.0',
'4873.0',
'4875.0',
'4876.0',
'4918.0',
'4919.0',
'4924.0',
'4925.0',
'4926.0',
'4942.0',
'4943.0',
'4944.0',
'4992.0',
'4993.0',
'4994.0',
'5023.0',
'5134.0',
'5183.0',
'5186.0',
'5187.0',
'5188.0',
'5423.0',
'5494.0',
'5506.0',
'5574.0',
'5575.0',
'5602.0',
'5621.0',
'5643.0',
'5769.0',
'5770.0',
'5854.0',
'5855.0',
'5960.0',
'5961.0',
'5970.0',
'5987.0',
'5988.0',
'6012.0',
'6032.0',
'6033.0',
'6060.0',
'6061.0',
'6082.0',
'6083.0',
'6174.0',
'6187.0',
'6188.0',
'6190.0',
'6191.0',
'6199.0',
'6200.0',
'6220.0',
'6225.0',
'6226.0',
'6237.0',
'6238.0',
'Friday',
'Monday',
'Saturday',
'Sunday',
'Thursday',
'Tuesday',
'Wednesday',])

cluster_2 = pd.DataFrame(columns=['val_month',
'val_day',
'val_hour',
'Transbordo',
'Viaje Inicial',
'0.0',
'9.0',
'55.0',
'68.0',
'69.0',
'90.0',
'240.0',
'306.0',
'369.0',
'394.0',
'475.0',
'480.0',
'487.0',
'538.0',
'559.0',
'605.0',
'640.0',
'649.0',
'650.0',
'727.0',
'779.0',
'789.0',
'822.0',
'824.0',
'833.0',
'882.0',
'920.0',
'923.0',
'956.0',
'958.0',
'1007.0',
'1009.0',
'1010.0',
'1052.0',
'1055.0',
'1058.0',
'1063.0',
'1084.0',
'1088.0',
'1092.0',
'1101.0',
'1102.0',
'1110.0',
'1111.0',
'1113.0',
'1131.0',
'1138.0',
'1160.0',
'1168.0',
'1173.0',
'1208.0',
'1247.0',
'1252.0',
'1260.0',
'1274.0',
'1291.0',
'1326.0',
'1345.0',
'1347.0',
'1379.0',
'1381.0',
'1383.0',
'1384.0',
'1387.0',
'1392.0',
'1395.0',
'1396.0',
'1398.0',
'1401.0',
'1402.0',
'1418.0',
'1419.0',
'1425.0',
'1426.0',
'1430.0',
'1433.0',
'1436.0',
'61606.0',
'0.0',
'1157.0',
'1445.0',
'1497.0',
'1498.0',
'1500.0',
'1903.0',
'1904.0',
'2093.0',
'2094.0',
'2107.0',
'2471.0',
'2472.0',
'2524.0',
'2848.0',
'2974.0',
'3004.0',
'3005.0',
'3139.0',
'3140.0',
'3141.0',
'3142.0',
'3379.0',
'3380.0',
'3491.0',
'3492.0',
'3595.0',
'3596.0',
'3657.0',
'3684.0',
'3788.0',
'3789.0',
'3811.0',
'3823.0',
'3974.0',
'3980.0',
'3981.0',
'4009.0',
'4012.0',
'4013.0',
'4014.0',
'4135.0',
'4136.0',
'4149.0',
'4162.0',
'4251.0',
'4294.0',
'4295.0',
'4296.0',
'4371.0',
'4372.0',
'4388.0',
'4389.0',
'4394.0',
'4613.0',
'4623.0',
'4645.0',
'4775.0',
'4806.0',
'4827.0',
'4828.0',
'4870.0',
'4871.0',
'4873.0',
'4875.0',
'4876.0',
'4878.0',
'4879.0',
'4918.0',
'4919.0',
'4924.0',
'4925.0',
'4926.0',
'4942.0',
'4943.0',
'4944.0',
'4992.0',
'4993.0',
'4994.0',
'5023.0',
'5134.0',
'5135.0',
'5136.0',
'5186.0',
'5221.0',
'5356.0',
'5357.0',
'5494.0',
'5506.0',
'5545.0',
'5574.0',
'5575.0',
'5602.0',
'5621.0',
'5643.0',
'5769.0',
'5770.0',
'5850.0',
'5854.0',
'5855.0',
'5949.0',
'5960.0',
'5961.0',
'5970.0',
'5987.0',
'5988.0',
'5989.0',
'5990.0',
'5998.0',
'6012.0',
'6032.0',
'6033.0',
'6055.0',
'6060.0',
'6061.0',
'6066.0',
'6071.0',
'6072.0',
'6081.0',
'6082.0',
'6083.0',
'6118.0',
'6120.0',
'6180.0',
'6187.0',
'6188.0',
'6199.0',
'6200.0',
'6208.0',
'6209.0',
'6220.0',
'6225.0',
'6226.0',
'6227.0',
'6228.0',
'6237.0',
'6238.0',
'6323.0',
'Friday',
'Monday',
'Saturday',
'Sunday',
'Thursday',
'Tuesday',
'Wednesday',])

cluster_3 = pd.DataFrame(columns=['val_month',
'val_day',
'val_hour',
'Transbordo',
'Viaje Inicial',
'0.0',
'394.0',
'480.0',
'543.0',
'605.0',
'640.0',
'650.0',
'779.0',
'789.0',
'803.0',
'882.0',
'1052.0',
'1110.0',
'1131.0',
'1138.0',
'1160.0',
'1168.0',
'1169.0',
'1247.0',
'1260.0',
'1291.0',
'1381.0',
'1384.0',
'1415.0',
'1419.0',
'1430.0',
'0.0',
'2093.0',
'2094.0',
'2391.0',
'2848.0',
'3004.0',
'3139.0',
'3140.0',
'3142.0',
'3491.0',
'3492.0',
'3974.0',
'4251.0',
'4294.0',
'4295.0',
'4296.0',
'4327.0',
'4328.0',
'4613.0',
'4918.0',
'4919.0',
'4942.0',
'4943.0',
'4944.0',
'4992.0',
'4993.0',
'4994.0',
'5134.0',
'5186.0',
'5187.0',
'5188.0',
'5506.0',
'5574.0',
'5621.0',
'5960.0',
'5961.0',
'5970.0',
'5990.0',
'6174.0',
'6187.0',
'6188.0',
'6220.0',
'6225.0',
'6226.0',
'Friday',
'Monday',
'Saturday',
'Sunday',
'Thursday',
'Tuesday',
'Wednesday',])

cluster_4 = pd.DataFrame(columns=['val_month',
'val_day',
'val_hour',
'Transbordo',
'Viaje Inicial',
'0.0',
'55.0',
'69.0',
'160.0',
'240.0',
'306.0',
'369.0',
'394.0',
'475.0',
'480.0',
'487.0',
'527.0',
'538.0',
'543.0',
'559.0',
'573.0',
'574.0',
'575.0',
'578.0',
'605.0',
'640.0',
'649.0',
'650.0',
'727.0',
'748.0',
'779.0',
'789.0',
'803.0',
'822.0',
'824.0',
'833.0',
'852.0',
'856.0',
'882.0',
'920.0',
'956.0',
'958.0',
'974.0',
'1003.0',
'1007.0',
'1009.0',
'1010.0',
'1049.0',
'1052.0',
'1056.0',
'1058.0',
'1063.0',
'1084.0',
'1088.0',
'1092.0',
'1101.0',
'1102.0',
'1110.0',
'1111.0',
'1112.0',
'1113.0',
'1130.0',
'1131.0',
'1138.0',
'1157.0',
'1158.0',
'1160.0',
'1167.0',
'1168.0',
'1169.0',
'1173.0',
'1208.0',
'1231.0',
'1247.0',
'1252.0',
'1260.0',
'1276.0',
'1291.0',
'1326.0',
'1345.0',
'1347.0',
'1379.0',
'1381.0',
'1383.0',
'1384.0',
'1387.0',
'1392.0',
'1395.0',
'1396.0',
'1398.0',
'1399.0',
'1400.0',
'1401.0',
'1402.0',
'1415.0',
'1417.0',
'1418.0',
'1419.0',
'1420.0',
'1425.0',
'1426.0',
'1430.0',
'1433.0',
'1434.0',
'1436.0',
'1437.0',
'7945.0',
'61606.0',
'0.0',
'371.0',
'871.0',
'1157.0',
'1400.0',
'1445.0',
'1903.0',
'1904.0',
'1925.0',
'2077.0',
'2093.0',
'2094.0',
'2391.0',
'2471.0',
'2472.0',
'2524.0',
'2743.0',
'2848.0',
'2974.0',
'3004.0',
'3005.0',
'3139.0',
'3140.0',
'3141.0',
'3142.0',
'3379.0',
'3380.0',
'3459.0',
'3464.0',
'3491.0',
'3492.0',
'3595.0',
'3596.0',
'3657.0',
'3684.0',
'3788.0',
'3789.0',
'3811.0',
'3974.0',
'3980.0',
'3981.0',
'4009.0',
'4012.0',
'4013.0',
'4014.0',
'4130.0',
'4131.0',
'4132.0',
'4133.0',
'4135.0',
'4136.0',
'4149.0',
'4162.0',
'4245.0',
'4251.0',
'4288.0',
'4294.0',
'4295.0',
'4296.0',
'4327.0',
'4328.0',
'4371.0',
'4372.0',
'4388.0',
'4389.0',
'4394.0',
'4411.0',
'4585.0',
'4613.0',
'4625.0',
'4645.0',
'4775.0',
'4827.0',
'4828.0',
'4870.0',
'4871.0',
'4873.0',
'4875.0',
'4876.0',
'4878.0',
'4879.0',
'4918.0',
'4919.0',
'4920.0',
'4921.0',
'4924.0',
'4925.0',
'4926.0',
'4937.0',
'4942.0',
'4943.0',
'4944.0',
'4992.0',
'4993.0',
'4994.0',
'5023.0',
'5131.0',
'5132.0',
'5134.0',
'5135.0',
'5136.0',
'5183.0',
'5186.0',
'5187.0',
'5188.0',
'5221.0',
'5356.0',
'5357.0',
'5423.0',
'5506.0',
'5545.0',
'5574.0',
'5575.0',
'5620.0',
'5621.0',
'5643.0',
'5769.0',
'5770.0',
'5850.0',
'5854.0',
'5855.0',
'5949.0',
'5961.0',
'5970.0',
'5987.0',
'5988.0',
'5989.0',
'5990.0',
'5998.0',
'6012.0',
'6032.0',
'6033.0',
'6039.0',
'6041.0',
'6055.0',
'6060.0',
'6061.0',
'6066.0',
'6067.0',
'6068.0',
'6071.0',
'6072.0',
'6081.0',
'6082.0',
'6083.0',
'6118.0',
'6120.0',
'6174.0',
'6177.0',
'6180.0',
'6187.0',
'6188.0',
'6190.0',
'6191.0',
'6199.0',
'6200.0',
'6208.0',
'6209.0',
'6210.0',
'6220.0',
'6222.0',
'6225.0',
'6226.0',
'6227.0',
'6228.0',
'6229.0',
'6230.0',
'6231.0',
'6232.0',
'6237.0',
'6238.0',
'6323.0',
'8808.0',
'Friday',
'Monday',
'Saturday',
'Sunday',
'Thursday',
'Tuesday',
'Wednesday',])
