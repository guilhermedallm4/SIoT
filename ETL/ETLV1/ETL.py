import json

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

f = open("saida.json", 'w')
f.write(importMongo)
f.close()
