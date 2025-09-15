import tkinter as tk
from tkinter import ttk
import time
import random as rm
import msvcrt

root = tk.Tk()
root.title("Procesamiento por lotes")
root.geometry("854x480")

#root.bind("<p>", pausa)

Lotes = []
Procesos = []
Contador = 0
ids = []
num_lotes = 1
Num_Procesos = 0
MAX_TME_TIME = 10
 
# GENERA DATOS PRIMERO LLAMANDO A CAPTURAR EL NUMERO DE PROCESO
def generar_datos():
        
        try: 
            Num_Procesos = capturar_Num_Procesos()
            label_datos_save.config(text="Datos Generados Correctamente!", bg="LawnGreen")
        except ValueError as e:
            label_datos_save.config(text=str(e), background="red")
        except Exception as e:
            label_datos_save.config(text=str(e), background="red")
            
        for i in range(Num_Procesos):
            NewProceso = Proc()
            global num_lotes
            Procesos.append(NewProceso)

            if len(Procesos) == 4:
                for pi in Procesos:
                    pi.num_lote = num_lotes
                Lotes.append(list(Procesos))
                Procesos.clear()
                num_lotes += 1
            
    
def capturar_Num_Procesos():
    temp_num = entrada_procesos.get()
    try: 
        temp_num = int(temp_num)
    except ValueError:
        raise ValueError("Numero no valido.")

    if temp_num < 1:
        raise ValueError("Numero no puede ser negativo.")
    
    if temp_num == None:
        raise ValueError("Numero vacio.")
    
    return temp_num        
        
# OBJETO DE PROCESO QUE GENERA UTOMATIMANETE SUS DATOS
class Proc:
    id = 0
    ope = ""
    TimeMax = 0
    datos_string = ""
    proces_id = ""
    num_lote = 0
    tt = 0
    
    def __init__(self):
        self.generar_campos()

    def generar_campos(self):
        self.id = self.generar_id()
        self.ope = self.generar_operacion()
        self.TimeMax = rm.randint(6,MAX_TME_TIME)
        self.string_proc()
        self.print_proc()

    def generar_id(self):
        temp_id = rm.randint(1,100000)
        for i in ids:
            if i == temp_id:
                print("Generacion de ID invalido.")
                temp_id = self.generar_id()
                
        return temp_id
    
    
    def generar_operacion(self):
        num1 = rm.randint(1,1000)
        num2 = rm.randint(1,1000)
        
        operaciones = ['+','-','*','/','%','**']
        operador = rm.choice(operaciones)
        
        OPERACION = f"{num1} {operador} {num2}"
        
        try:
            eval(OPERACION)
        except:
            print("Generacion de operacion invalida.")
            OPERACION = self.generar_operacion()
        
        return OPERACION
            
    def print_proc(self):
        print(f"ID: {self.id}\nOperacion: {self.ope}\nTME: {self.TimeMax}")        
    
    def string_proc(self):
        self.string_proc = f"-ID:{self.id} -Operacion:{self.ope} -TME: {self.TimeMax}\n"
        Guardados.insert('1.0', str(self.string_proc))
        


def procesar():
    global num_lotes
    if len(Procesos) > 0:
        for ip in Procesos:
            ip.num_lote = num_lotes
        Lotes.append(list(Procesos))
        Procesos.clear()
        num_lotes += 1
    
    Procesos_QUEUE = []    
    
    print("Comenzando Proceso!...")
    rlotes = 0
    nlotes = 1
    for l in range(len(Lotes)): #itera en los lotes
        
        frame_trabajando.config(text=f"Lote Trabjando: {nlotes}")
        lbl_lotes_restantes.config(text=f"Lotes Restantes: {num_lotes-rlotes-1}")
        Procesos_QUEUE = Lotes[l]
        
        for p in range(len(Procesos_QUEUE)): #inserta los proceso en el frame de lote trabajando
            proc = Procesos_QUEUE[p]
            proc_id = tree_trajando.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
            proc.proces_id = proc_id
            
        while len(Procesos_QUEUE) > 0: #procesa cada proceso
            proc = Procesos_QUEUE.pop(0)
            tree_trajando.delete(proc.proces_id)
            ejecucion_proces(proc, Procesos_QUEUE)
            
        
        rlotes += 1
        nlotes += 1

    print("Proceso terminado")
    proceso_terminado()

def ejecucion_proces(proc, P_QUEUE):
    global Contador
    time_ejec = proc.TimeMax - proc.tt
    werror = False
    i = 0
    while i <= time_ejec: #asigna el proceso actual a la tabla de procesos
        Contador += 1
        
        #ESTRUCTURA DE KHBIT:
        if msvcrt.kbhit():  # detecta si hay una tecla presionada
            tecla = msvcrt.getch().decode().lower()  # obtiene la tecla
            print("Tecla presionada: ", tecla)
            
            if tecla == 'p':
                pausa = True
                print("Programa en pausa...")
                while pausa:
                    time.sleep(0.2)
                    if msvcrt.kbhit():
                        tecla_en_pausa = msvcrt.getch().decode().lower()  
                        print("Tecla presionada: ", tecla_en_pausa)
                        if tecla_en_pausa == 'c':
                            pausa = False
                            print("Programa reaunudado!")
                            
            if tecla == 'w':
                werror = True
                time_ejec = 1
                
            if tecla == 'e':
                P_QUEUE.append(proc)
                proc_id = tree_trajando.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
                proc.proces_id = proc_id
                return
        
        # FIN DE FUNCIONES DE TECLAS
        
        
        lbl_id.config(text=f"ID: {proc.id}")
        if werror:
            lbl_ope.config(text=f"Operacion: X")
        else:
            lbl_ope.config(text=f"Operacion: {proc.ope}")
        lbl_tme.config(text=f"TME: {proc.TimeMax}")
        lbl_contador.config(text=f"Contador: {Contador}")
        lbl_tt.config(text=f"TT: {i}")
        lbl_tr.config(text=f"TR: {time_ejec - i}")
        print(f"Contando... {i}")
        
        
        #cambiando tiempo transcurrido interno
        proc.tt += 1
        i += 1
        root.update()
        time.sleep(1)

    if not werror:
        result = eval(proc.ope)
        tree_terminados.insert("", "end", values=(proc.id, proc.ope, result, proc.num_lote))
    else:    
        tree_terminados.insert("", "end", values=(proc.id, proc.ope, "Error", proc.num_lote))
    
def proceso_terminado(): #limpia la tabla de procesos en ejecucion
    lbl_id.config(text="ID: ")
    lbl_ope.config(text="Operacion: ")
    lbl_tme.config(text="TME: ")
    lbl_tt.config(text="TT: ")
    lbl_tr.config(text="TR: 0")
        

#GUI

frame_left = tk.Frame(root)   #formulario
frame_left.pack(side="left", fill="y", padx=10, pady=10)

frame_right = tk.Frame(root)  #tablas y procesos
frame_right.pack(side="left", fill="both", expand=True, padx=10, pady=10)


#botones para captura de datos
label_Num_Procesos = tk.Label(frame_left, text="Ingresa cantidad de procesos: ")
label_Num_Procesos.pack(pady=1)
entrada_procesos = tk.Entry(frame_left)
entrada_procesos.pack(pady=1)

label_datos_save = tk.Label(frame_left, text="")
label_datos_save.pack(pady=5)

btn_guardar_datos = tk.Button(frame_left, text="Generar proceso(s)", command=generar_datos)
btn_guardar_datos.pack(pady=10)

Guardados = tk.Text(frame_left, width=40, height=100, wrap=tk.WORD)
Guardados.pack(padx=15)

btn_comenzar_proceso = tk.Button(root, text="Comenzar Proceso", command=procesar, background="DarkSeaGreen")
btn_comenzar_proceso.pack(pady=10)

lbl_lotes_restantes = tk.Label(root, text=f"Lotes pendientes: ")
lbl_lotes_restantes.pack(pady=3, padx=50)

#Frames de procesos
frame_tablas = tk.Frame(root)
frame_tablas.pack(fill="both", expand=True, padx=10, pady=10)

frame_trabajando = tk.LabelFrame(frame_tablas, text="Lote Trabajando")
frame_trabajando.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tree_trajando = ttk.Treeview(frame_trabajando, columns=("id", "tme", "tt"), show="headings")
tree_trajando.heading("id", text="ID")
tree_trajando.heading("tme", text="TME")
tree_trajando.heading("tt", text="TT")

tree_trajando.column("id", width=80, anchor="center")
tree_trajando.column("tme", width=80, anchor="center")  
tree_trajando.column("tt", width=80, anchor="center")  

tree_trajando.pack(fill="both", expand=True)

#frame de proceso en ejecucion
frame_proceso = tk.LabelFrame(frame_tablas, text="Proceso en ejecucion")
frame_proceso.pack(side="left", fill="y", padx=10, pady=10)

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

#frame de gui de terminados
frame_terminados = tk.LabelFrame(frame_tablas, text="Terminados")
frame_terminados.pack(side="left", fill="both", expand=True, padx=10, pady=5)

tree_terminados = ttk.Treeview(frame_terminados, columns=("id", "ope", "res", "nl"), show="headings")
tree_terminados.heading("id", text="ID")
tree_terminados.heading("ope", text="Ope")
tree_terminados.heading("res", text="Res")
tree_terminados.heading("nl", text="NL")
tree_terminados.column("id", width=100, anchor="center")

tree_terminados.pack(fill="both", expand=True)

#contador

frame_contador = tk.LabelFrame(root, text="Contador")
frame_contador.pack(fill="x", padx=10, pady=5)

lbl_contador = tk.Label(frame_contador, text="Contador: 0", font=("Arial", 14))
lbl_contador.pack(anchor="center", pady=5)

root.mainloop()
