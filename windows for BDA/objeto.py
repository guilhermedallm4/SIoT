import json
import tkinter as tk

def start():
    label.pack_forget()
    for i in button:
        i.pack(fill=tk.BOTH)
        i.bind("<Button-1>", click)

def click(e):
    for i in button:
        i.pack_forget()
	
    index = 0
    if(e.widget._name[len(e.widget._name) - 1] != 'n'):
        index = int(e.widget._name[len(e.widget._name) - 1]) - 1
	
    s = ''
    for i in objs['objeto'][index]:
        if(len(str(objs['objeto'][index][i])) > 0):
            s += i[4:] + ": " + str(objs['objeto'][index][i]) + "\n"
        else:
            s += i[4:] + ": **subdevice**\n"
	    
    label['text'] = s
    label.pack(fill=tk.BOTH)
    
def importJsonTuya():
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
	
	importMongo = {"objeto":[]}
	for i in dados['devices']:
		importMongo['objeto'].append({'obj_Id': i['id'],
					'obj_MACRede': i['mac'],
					'obj_Nome': i['name'],
					'obj_Proprietario': i['owner_id'],
					'obj_Modelo': i['model'],
					'obj_Marca': i['product_name'],
					'obj_Categoria': i['category'],
					'obj_Funcao': False,
					'obj_Limitacao': False,
					'obj_Acesso': 'Private',
					'obj_Localizacao': False
		})

	return importMongo

objs = importJsonTuya()

window = tk.Tk()
window.title("Objetos")
window.configure(bg="white")
window.minsize(500, 400)
window.maxsize(500, 400)

menu = tk.Menu(window)
window.config(menu=menu)
menu.add_command(label="Voltar", command=start)

button = []
label = tk.Label(text="a", font=("Calibri", 14, "normal"), width=window.winfo_screenwidth(), height=window.winfo_screenheight(), relief=tk.RIDGE, borderwidth=5, bg="white", fg="black", justify="left")
for i in objs['objeto']:
	button.append(tk.Button(text=i['obj_Nome'], font=("Calibri", 16, "normal"), height=2, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black"))

start()
window.mainloop()