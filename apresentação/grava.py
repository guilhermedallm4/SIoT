from pymongo import MongoClient
import json

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["bda"]

def gravaAmbienteOuInteracao(db, nomeJson):
    collection = db[nomeJson]

    f1 = open("csvOutPut.json", 'r')
    dados = json.loads(f1.read())
    f1.close()

    documentos = []
    for i in range(len(dados[nomeJson]) if len(dados[nomeJson]) < 100 else 100):
        documentos.append(dados[nomeJson][i])

    collection.insert_many(documentos)

def gravaObjeto(db):
    collection = db["objeto"]

    f1 = open("snapshot.json", 'r')
    dados = json.loads(f1.read())

    f2 = open("tuya-raw.json", 'r')
    dados2 = json.loads(f2.read())

    for i in dados['devices']:
        for j in dados2['result']:
            if(i['id'] == j['id']):
                for k in j:
                    i[k] = j[k]

    f1.close()
    f2.close()

    documentos = []
    for i in dados['devices']:
        documentos.append({'obj_Id': i['id'],
                    'obj_MACRede': i['mac'],
                    'obj_Nome': i['name'],
                    'obj_Proprietario': i['owner_id'],
                    'obj_Modelo': i['model'],
                    'obj_Marca': i['product_name'],
                    'obj_Categoria': i['category'],
                    'obj_Funcao': i['status'],
                    'obj_Restricao': [],
                    'obj_Limitacao': [],
                    'obj_Acesso': 0,
                    'obj_Localizacao': i['lat'] + ', ' + i['lon']
        })

    collection.insert_many(documentos)

db.drop_collection('objeto')
db.drop_collection('ambiente_ONA')
db.drop_collection('interacao')

gravaObjeto(db)
gravaAmbienteOuInteracao(db, 'ambiente_ONA')
gravaAmbienteOuInteracao(db, 'interacao')