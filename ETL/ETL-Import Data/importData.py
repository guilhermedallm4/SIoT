import json
import csv
from pymongo import MongoClient, InsertOne

ambiente = {'ambiente_ONA':[], 
					'interacao':[]}
importMongo = {"objeto":[]}
host = 'localhost'
port = 27017
documment = 'LUPS'

def importJsonTuya():
	dados = {'jsons':[]}
	with open("snapshot.json", 'r') as my_json:
		dados['jsons'].append(json.loads(my_json.read()))

	with open("tuya-raw.json", 'r') as my_json:
		dados['jsons'].append(json.loads(my_json.read()))


	for i in range(len(dados['jsons'][0]['devices'])):
		importMongo['objeto'].append({
					'obj_MACRede':dados['jsons'][0]['devices'][i]['mac'],
					'obj_Nome':dados['jsons'][0]['devices'][i]['name'],
					'obj_Proprietario':dados['jsons'][1]['result'][i]['owner_id'],
					'obj_Modelo':dados['jsons'][0]['devices'][i]['model'],
					'obj_Marca':dados['jsons'][0]['devices'][i]['product_name'],
					'obj_Categoria': dados['jsons'][0]['devices'][i]['category'],
					'obj_Funcao': False,
					'obj_Limitacao':False,
					'obj_Acesso': 'Private',
					'obj_Localizacao': False
		})


	apiOutPut = json.dumps(importMongo, sort_keys=True, indent=4)

	f = open("apiOutPut.json", 'w')
	f.write(apiOutPut)
	f.close()

def importCSV():


	with open('1000 NoCentral.csv', newline='') as csvfile:
		ambienteOna = csv.DictReader(csvfile)
		for row in ambienteOna:
			ambiente['ambiente_ONA'].append({
				'amb_Obj_j': int(row['Objeto']),
				'amb_Total_Intera': int(row['Interacao']),
				'amb_Total_Valida': int(row['Interacao']),
				'amb_Total_Nova': int(row['Exclusiva']),
				'amb_Adjacencia': False
			})

	with open('5000 Interacoes.csv', newline='') as csvfile:
		interacao = csv.DictReader(csvfile)
		for row in interacao:
			ambiente['interacao'].append({
				'intera_Obj_i': int(row['obj_i']),
				'intera_Obj_j': int(row['obj_j']),
				'intera_Feed': False if int(row['status']) == 0 else True,
				'intera_Servico': False
			})
	csvOutPut = json.dumps(ambiente, sort_keys=True, indent=4)

	
	f = open("csvOutPut.json", 'w')
	f.write(csvOutPut)
	f.close()

def connectMongo():
    try:
        client = MongoClient(host, port)
        db = client[documment]
        return db
    except Exception as e:
        print("Is not possible connect in database\n Error:", e)

def importDataBase(db):
	try:
		collection = db['Objeto']
		result = collection.insert_many(importMongo['objeto'])
		print(result)
	except Exception as e:
		print("Is not possible connect in database\n Error:", e)

	try:
		collection = db['Ambiente_ONA']
		result = collection.insert_many(ambiente['ambiente_ONA'])
		print(result)		
	except Exception as e:
		print("Is not possible connect in database\n Error:", e)

	try:
		collection = db['Interacao']
		result = collection.insert_many(ambiente['interacao'])
		print(result)
	except Exception as e:
		print("Is not possible connect in database\n Error:", e)
	
def main():
	importJsonTuya()
	importCSV()
	db = connectMongo()
	importDataBase(db)

main()
