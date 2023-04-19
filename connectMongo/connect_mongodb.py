from pymongo import MongoClient

host = 'locahost'
port = 27017

#Conecte ao MongoDB. Para se conectar ao MongoDB, 
# você precisa criar uma instância do cliente do MongoDB.

def connectMongo(host, documment):
    try:
        client = MongoClient(host, port)
        db = client[documment]
        return db
    except Exception as e:
        print("Is not possible connect in database\n Error:", e)
        
    
#Acesse um banco de dados. Para acessar um banco de dados no MongoDB, 
# você precisa usar a instância do cliente para obter uma referência ao banco de dados desejado. 
#Substitua "nome_do_banco_de_dados" pelo nome do banco de dados que deseja acessar.

#Acesse uma coleção. Para acessar uma coleção dentro do banco de dados,
#você precisa usar a referência do banco de dados para obter uma referência à coleção desejada.





# inserindo vários documentos


#resultados = collection.insert_many(documentos)
