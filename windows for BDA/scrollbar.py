import json
import tkinter as tk

def start():
    if(label.winfo_ismapped()):
        label.pack_forget()
        for i in button2:
            i.pack(fill=tk.BOTH)
            i.bind("<Button-1>", click2)
    else:
        for i in button2:
            i.pack_forget()
            i.destroy()
        button2.clear()
        
        for i in button:
            i.pack(fill=tk.BOTH)
            i.bind("<Button-1>", click)
    frame2.update()
    canvas.yview_moveto(0)
    canvas.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())

def click(e):
    for i in button:
        i.pack_forget()
	
    index = button.index(e.widget)

    global collection
    collection = button[index]['text']

    for i in range(len(collections[collection])):
        button2.append(tk.Button(frame2, text=collection + " " + str(i), font=("Calibri", 16, "normal"), width=42, height=2, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black"))

    for i in button2:
        i.pack(fill=tk.BOTH)
        i.bind("<Button-1>", click2)

    frame2.update()
    canvas.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
        
def click2(e):
    for i in button2:
        i.pack_forget()
    
    index = button2.index(e.widget)

    s = ''
    for i in collections[collection][index]:
        s += i + ": " + str(collections[collection][index][i]) + "\n"
        
    label['text'] = s
    label.pack(fill=tk.BOTH)

    frame2.update()
    canvas.yview_moveto(0)
    canvas.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
    
def importObjetos():
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
					'obj_Funcao': i['status'],
                    			'obj_Restricao': [],
					'obj_Limitacao': [],
					'obj_Acesso': 0,
					'obj_Localizacao': i['lat'] + ', ' + i['lon']
		})

	return importMongo

def importJsonTuya(nomeJson):
    f1 = open("csvOutPut.json", 'r')
    dados = json.loads(f1.read())
    f1.close()

    importMongo = {nomeJson: []}
    for i in range(len(dados[nomeJson]) if len(dados[nomeJson]) < 300 else 300):
        importMongo[nomeJson].append(dados[nomeJson][i])
        
    return importMongo

collections = {'objeto': importObjetos()['objeto'], 
               'ambiente_ONA': importJsonTuya('ambiente_ONA')['ambiente_ONA'], 
               'interacao': importJsonTuya('interacao')['interacao']}

window = tk.Tk()
window.title("Collections")
window.configure(bg="white")
window.minsize(500, 400)
window.maxsize(500, 400)

menu = tk.Menu(window)
window.config(menu=menu)
menu.add_command(label="Voltar", command=start)

frame = tk.Frame(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas = tk.Canvas(frame, width=window.winfo_screenwidth() - 800, height=window.winfo_screenheight())
frame2 = tk.Frame(canvas, width=window.winfo_screenwidth(), height=window.winfo_screenheight())

myscrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.create_window((0,0), window=frame2, anchor='nw')

button = []
button2 = []
label = tk.Label(frame2, text="a", font=("Calibri", 14, "normal"), width=46, height=16, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black", justify="left")
for i in collections:
    button.append(tk.Button(frame2, text=i, font=("Calibri", 16, "normal"), width=42, height=2, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black"))

canvas.pack(side=tk.LEFT)
myscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

frame.pack()
start()
window.mainloop()
