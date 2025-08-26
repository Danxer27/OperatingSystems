import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Procesamiento por lotes")
root.geometry("854x480")


Lotes = []
Procesos = []

def guardar_datos():
    NewProceso = Proc()
    NewProceso.captura_datos()
    
    if len(Procesos) >= 4:
        Lotes.append(Procesos)
        Procesos.clear()
        
    Procesos.append(NewProceso)
    

class Proc:
    nombre = ""
    id = 0
    ope = ""
    TimeMax = 0
    datos_string = ""
    
    def __init__(self):
        pass

    def captura_datos(self):
        try:
            self.nombre = self.capturar_nombre()
            self.id = self.captura_id()
            self.ope = self.captura_operacion()
            self.TimeMax = self.captura_temp_max()
            entrada_id.delete(0, tk.END)
            entrada_nombre.delete(0, tk.END)
            entrada_operacion.delete(0, tk.END)
            entrada_tiempomax.delete(0, tk.END)
            self.print_proc()
            self.string_proc()
            label_datos_save.config(text="Datos Guardados Correctamente!", bg="LawnGreen")
        except ValueError:
            #label_datos_save.config(text="Error al guardar datos.", background="red")
            pass
            
        
            
    def capturar_nombre(self):
        temp_nombre = entrada_nombre.get()
        if not temp_nombre:
            print("Nombre no valido")
            label_datos_save.config(text="ID no valido", background="red") #avisto en gui
            return self.capturar_nombre()
        else: 
            return temp_nombre
        
    def captura_id(self):
        temp_id = entrada_id.get()
        try: 
            temp_id = int(temp_id)
        except ValueError:
            print("ID no valido")
            label_datos_save.config(text="ID no valido", background="red") # aviso en gui
            temp_id = self.captura_id()
        return temp_id
    
    def captura_operacion(self):
        temp_op = entrada_operacion.get()
        try:
            eval(temp_op)
            return temp_op
        except ValueError:
            print("operacion no valida")
            label_datos_save.config(text="Formato de operacion no valido", background="red")
            
    def captura_temp_max(self):
        temp_time = entrada_tiempomax.get()
        try: 
            temp_time = int(temp_time)
        except ValueError:
            print("Teimpo no valido")
            label_datos_save.config(text="Tiempo no valido", background="red")
            temp_time = self.captura_temp_max()
        return temp_time   
    
    def print_proc(self):
        print(f"Nombre: {self.nombre}\nID: {self.id}\nOperacion: {self.ope}\nTME: {self.TimeMax}")        
    
    def string_proc(self):
        self.string_proc = f"N:{self.nombre} -ID:{self.id} -Operacion:{self.ope} -TME: {self.TimeMax}\n"
        Guardados.insert('1.0', str(self.string_proc))
        
    
def procesar():
    for l in range(len(Lotes)):
        for p in range(len(Lotes[l])):
            proc = Lotes[l][p]
            
            
            tree_trajando.insert("", "end", values=(proc.nombre, proc.TimeMax))
            lbl_nombre.config(text=f"Nombre: {proc.nombre}")
            lbl_id.config(text=f"ID: {proc.id}")
            lbl_ope.config(text=f"Operacion: {proc.ope}")
            lbl_tme.config(text=f"TME: {proc.TimeMax}")
            
            #poner esta mamada de los segundos
            #lbl_contador.config(text=f"Contador: {segundos}")
            


#GUI

frame_left = tk.Frame(root)   #formulario
frame_left.pack(side="left", fill="y", padx=10, pady=10)

frame_right = tk.Frame(root)  #tablas y procesos
frame_right.pack(side="left", fill="both", expand=True, padx=10, pady=10)


#botones para captura de datos
label_nombre = tk.Label(frame_left, text="Ingresa el nombre: ")
label_nombre.pack(pady=1)
entrada_nombre = tk.Entry(frame_left)
entrada_nombre.pack(pady=1)

label_id = tk.Label(frame_left, text="Ingresa un ID: ")
label_id.pack(pady=1)
entrada_id = tk.Entry(frame_left)
entrada_id.pack(pady=1)

label_operacion = tk.Label(frame_left, text="Ingresa la operacion: ")
label_operacion.pack(pady=1)
entrada_operacion = tk.Entry(frame_left)
entrada_operacion.pack(pady=1)

label_tiempomax = tk.Label(frame_left, text="Ingresa el Tiempo Maximo Estimado: ")
label_tiempomax.pack(pady=1)
entrada_tiempomax = tk.Entry(frame_left)
entrada_tiempomax.pack(pady=1)

label_datos_save = tk.Label(frame_left, text="")
label_datos_save.pack(pady=5)

btn_guardar_datos = tk.Button(frame_left, text="Guardar proceso", command=guardar_datos)
btn_guardar_datos.pack(pady=10)



Guardados = tk.Text(frame_left, width=40, height=100, wrap=tk.WORD)
Guardados.pack(padx=15)


btn_comenzar_proceso = tk.Button(root, text="Comenzar Proceso", command=procesar, background="DarkSeaGreen")
btn_comenzar_proceso.pack(pady=10)

#Frames de procesos
frame_tablas = tk.Frame(root)
frame_tablas.pack(fill="both", expand=True, padx=10, pady=10)

frame_trabajando = tk.LabelFrame(frame_tablas, text="Lotes Trabajando")
frame_trabajando.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tree_trajando = ttk.Treeview(frame_trabajando, columns=("nombre", "tme"), show="headings")
tree_trajando.heading("nombre", text="Nombre")
tree_trajando.heading("tme", text="TME")
tree_trajando.pack(fill="both", expand=True)

#proceso en ejecucion
frame_proceso = tk.LabelFrame(frame_tablas, text="Proceso en ejecucion")
frame_proceso.pack(side="left", fill="y", padx=10, pady=10)

lbl_nombre = tk.Label(frame_proceso, text="Nombre: -")
lbl_nombre.pack(anchor="w")
lbl_id = tk.Label(frame_proceso, text="ID: -")
lbl_id.pack(anchor="w")
lbl_ope = tk.Label(frame_proceso, text="Ope: -")
lbl_ope.pack(anchor="w")
lbl_tme = tk.Label(frame_proceso, text="TME: -")
lbl_tme.pack(anchor="w")
lbl_tt = tk.Label(frame_proceso, text="TT: -")
lbl_tt.pack(anchor="w")
lbl_tr = tk.Label(frame_proceso, text="TR: -")
lbl_tr.pack(anchor="w")

#terminados
frame_terminados = tk.LabelFrame(frame_tablas, text="Terminados")
frame_terminados.pack(side="left", fill="both", expand=True, padx=10, pady=5)

tree_terminados = ttk.Treeview(frame_terminados, columns=("id", "ope", "res", "nl"), show="headings")
tree_terminados.heading("id", text="ID")
tree_terminados.heading("ope", text="Ope")
tree_terminados.heading("res", text="Res")
tree_terminados.heading("nl", text="NL")
tree_terminados.pack(fill="both", expand=True)

frame_contador = tk.LabelFrame(root, text="Contador")
frame_contador.pack(fill="x", padx=10, pady=5)

lbl_contador = tk.Label(frame_contador, text="Contador: 0", font=("Arial", 14))
lbl_contador.pack(anchor="center", pady=5)

root.mainloop()
