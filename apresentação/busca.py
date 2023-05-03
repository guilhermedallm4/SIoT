from pymongo import MongoClient
import tkinter as tk

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["bda"]

def visualizarCollections():
    def atualizaFrame():
        frame2.update()
        canvas.yview_moveto(0)
        canvas.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())

    def start():
        if(label.winfo_ismapped()):
            label.pack_forget()
            for i in button2:
                i.pack(fill=tk.BOTH)
        else:
            for i in button2:
                i.pack_forget()
                i.destroy()
            button2.clear()
            for i in button:
                i.pack(fill=tk.BOTH)
                i.bind("<Button-1>", click)

        label['height'] = 16
        atualizaFrame()

    def click(e):
        for i in button:
            i.pack_forget()
        
        index = button.index(e.widget)

        global collection
        collection = button[index]['text']

        for i in range(len(collections[collection])):
            button2.append(tk.Button(frame2, text=collection + " " + str(collections[collection][i]['_id']), font=("Calibri", 16, "normal"), width=42, height=2, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black"))
        for i in button2:
            i.pack(fill=tk.BOTH)
            i.bind("<Button-1>", click2)

        atualizaFrame()
            
    def click2(e):
        for i in button2:
            i.pack_forget()
        
        index = button2.index(e.widget)

        s = ''
        for i in collections[collection][index]:
            s += i + ": " + str(collections[collection][index][i]) + "\n"
            
        label['text'] = s
        label.pack(fill=tk.BOTH)

        atualizaFrame()



############################################################################################################
############################################################################################################
    def consultar():
        label.pack_forget()
        label['height'] = 16
        
        for i in button2:
            i.pack_forget()
            i.destroy()
        button2.clear()
        for i in button:
            i.pack_forget()
        
        button2.append(tk.Button(frame2, text='Buscar interações qualificadas pelo solicitante', font=("Calibri", 16, "normal"), width=42, height=2, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black"))
        button2.append(tk.Button(frame2, text='Buscar categorias dos objetos', font=("Calibri", 16, "normal"), width=42, height=2, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black"))
        button2.append(tk.Button(frame2, text='Consultar número de documentos', font=("Calibri", 16, "normal"), width=42, height=2, relief=tk.RIDGE, borderwidth=5, bg="white", fg="black"))
        
        clicks = [click3, click4, click5]
        for i in range(3):
            button2[i].pack(fill=tk.BOTH)
            button2[i].bind("<Button-1>", clicks[i])
        
        atualizaFrame()
    
    def atualizaLabelConsulta(documentos):
        for i in button2:
            i.pack_forget()
        
        s = ''
        for i in documentos:
            s += str(i) + "\n"

        label['text'] = s[:-2].replace(",", ",\n").replace("}", "\n").replace("{", "").replace("'", "").replace("ObjectId(", "").replace(")", "")
        label['height'] = 0
        label.pack(fill=tk.BOTH)

        atualizaFrame()

    def click3(e):
        collection = db['interacao']
        documentos = collection.find({'intera_Feed': True}, {'intera_Obj_i': 0, 'intera_Obj_j': 0, 'intera_Id': 0, 'intera_Servico': 0})
        atualizaLabelConsulta(documentos)

    def click4(e):
        collection = db['objeto']
        documentos = collection.find({}, {'obj_Id': 0, 'obj_MACRede': 0, 'obj_Nome': 0, 'obj_Proprietario': 0, 'obj_Modelo': 0, 'obj_Marca': 0, 'obj_Funcao': 0, 'obj_Restricao': 0, 'obj_Limitacao': 0, 'obj_Acesso': 0, 'obj_Localizacao': 0})
        atualizaLabelConsulta(documentos)
        
    def click5(e):
        for i in button2:
            i.pack_forget()
        
        s = "O banco de dados possui\n"

        collection = db['objeto']
        qtdd = collection.count_documents({})
        s += str(qtdd) + " objetos, "

        collection = db['ambiente_ONA']
        qtdd = collection.count_documents({})
        s += str(qtdd) + " ambientes e\n"

        collection = db['interacao']
        qtdd = collection.count_documents({})
        s += str(qtdd) + " interações armazenadas."
        
        label['text'] = s
        label.pack(fill=tk.BOTH)

        atualizaFrame()
############################################################################################################
############################################################################################################



    def busca(nomeCollection):
        collection = db[nomeCollection]
        documentos = collection.find()

        array = []
        for i in documentos:
            array.append(i)

        return array

    collections = {'objeto': busca('objeto'),
                'ambiente_ONA': busca('ambiente_ONA'), 
                'interacao': busca('interacao')}

    window = tk.Tk()
    window.title("Collections")
    window.configure(bg="white")
    window.minsize(500, 400)
    window.maxsize(500, 400)

    menu = tk.Menu(window)
    window.config(menu=menu)
    menu.add_command(label="Voltar", command=start)

############################################################################################################
    menu.add_command(label="Consultar", command=consultar)
############################################################################################################

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

visualizarCollections()