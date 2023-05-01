
import json
import csv



def importJsonTuya():
	dados = {'jsons':[]}
	with open("snapshot.json", 'r') as my_json:
		dados['jsons'].append(json.loads(my_json.read()))

	with open("tuya-raw.json", 'r') as my_json:
		dados['jsons'].append(json.loads(my_json.read()))

	importMongo = {"objeto":[]}

	print(len(dados['jsons']))
	for i in range(len(dados['jsons'][0]['devices'])):
		importMongo['objeto'].append({'obj_Id':dados['jsons'][0]['devices'][i]['id'],
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


	importMongo = json.dumps(importMongo, sort_keys=True, indent=4)

	f = open("apiOutPut.json", 'w')
	f.write(importMongo)
	f.close()


def importCSV():
	
	ambiente = {'ambiente_ONA':[], 
					'interacao':[]}

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
				'intera_Id': int(row['id']),
				'intera_Obj_i': int(row['obj_i']),
				'intera_Obj_j': int(row['obj_j']),
				'intera_Feed': False if int(row['status']) == 0 else True,
				'intera_Servico': False
			})
	print(ambiente['interacao'][1])
	print(ambiente['ambiente_ONA'][1])
	ambiente = json.dumps(ambiente, sort_keys=True, indent=4)

	
	f = open("csvOutPut.json", 'w')
	f.write(ambiente)
	f.close()



def main():
	importJsonTuya()
	importCSV()


main()
