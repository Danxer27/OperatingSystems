import tkinter as tk
from tkinter import ttk
import time
import random as rm
import msvcrt

root = tk.Tk()
root.title("Procesamiento por lotes")
root.geometry("854x480")

#root.bind("<p>", pausa)

#Lotes = []
Procesos = []
Contador = 0
ids = []
#num_lotes = 1
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
    p_id = ""
    tt = 0
    ttb = 0
    
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
    Procesos_QUEUE = []
    
    for i in range(4):  #Inserta los primeros 4 procesos en la cola
        proc = Procesos.pop()
        proc_id = tree_trajando.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
        proc.p_id = proc_id
        Procesos_QUEUE.append(proc)
    
    while len(Procesos_QUEUE) > 0: #procesa cada proceso
            proc = Procesos_QUEUE.pop(0)
            tree_trajando.delete(proc.p_id)
            ejecucion_proces(proc, Procesos_QUEUE)
        
    print("Procesos terminado")
    proceso_terminado()


def ejecucion_proces(proc, P_QUEUE):
    bloqueados = []
    global Contador
    time_ejec = proc.TimeMax - proc.tt
    w_error = False
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
                w_error = True
                time_ejec = 0 #establece el tiempo restante en 0 cuando se da error para que pase directo a terminados, estaba en 1
                
            if tecla == 'e':
                bloqueados.append(proc)
                tree_trajando.delete(proc.p_id)
                proc_bloc_id = tree_bloqueados.insert("", "end", values=(proc.id, proc.ttb))
                proc.p_id = proc_bloc_id
                
                # P_QUEUE.append(proc)
                # proc_id = tree_trajando.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
                # proc.p_id = proc_id
                #return
        
        # FIN DE FUNCIONES DE TECLAS
        # Tabla de ejecucion ---
        
        lbl_id.config(text=f"ID: {proc.id}")
        if w_error:
            lbl_ope.config(text=f"Operacion: X")
        else:
            lbl_ope.config(text=f"Operacion: {proc.ope}")
        lbl_tme.config(text=f"TME: {proc.TimeMax}")
        lbl_contador.config(text=f"Contador: {Contador}")
        lbl_tt.config(text=f"TT: {i}")
        lbl_tr.config(text=f"TR: {time_ejec - i}")
        print(f"Contando... {i}")
        
        #Bloqueados
        for b_proc in bloqueados:
            b_proc.ttb += 1
            
            if b_proc.ttb >= 8:
                tree_bloqueados.delete(b_proc.p_id)
                P_QUEUE.append(b_proc)
                
                
        #cambiando tiempo transcurrido interno
        proc.tt += 1
        i += 1
        root.update()
        time.sleep(1)
        
    # ^^^^^^^ TERMINA DEL PROCESO ^^^^^^^
    

    # añade nuevo proceso a la memoria
    if(len(P_QUEUE) + len(bloqueados) <= 4):
        if(len(Procesos) > 0):
            proc = Procesos.pop()
            proc_id = tree_trajando.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
            proc.p_id = proc_id
            P_QUEUE.append(proc)
    
    if not w_error:
        result = eval(proc.ope)
        tree_terminados.insert("", "end", values=(proc.id, proc.ope, result))
    else:    
        tree_terminados.insert("", "end", values=(proc.id, proc.ope, "Error"))



def proceso_terminado(): #limpia la tabla de procesos en ejecucion
    lbl_id.config(text="ID: ")
    lbl_ope.config(text="Operacion: ")
    lbl_tme.config(text="TME: ")
    lbl_tt.config(text="TT: ")
    lbl_tr.config(text="TR: 0")
        

# /// INTERFAZ GRAFICA ///

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

lbl_procesos_restantes = tk.Label(root, text=f"Procesos restantes: ")
lbl_procesos_restantes.pack(pady=3, padx=50)

#Frames de procesos
frame_tablas = tk.Frame(root)
frame_tablas.pack(fill="both", expand=True, padx=10, pady=10)

frame_trabajando = tk.LabelFrame(frame_tablas, text="Procesos trabajando")
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

tree_terminados = ttk.Treeview(frame_terminados, columns=("id", "ope", "res"), show="headings")
tree_terminados.heading("id", text="ID")
tree_terminados.heading("ope", text="Ope")
tree_terminados.heading("res", text="Res")
tree_terminados.column("id", width=100, anchor="center")

tree_terminados.pack(fill="both", expand=True)

#frame de gui de Bloqueados
frame_bottom = tk.Frame(root) #frame de bloqueados
frame_bottom.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

frame_bloqueados = tk.LabelFrame(frame_bottom, text="Bloqueados")
frame_bloqueados.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tree_bloqueados = ttk.Treeview(frame_bloqueados, columns=("id", "tb"), show="headings")
tree_bloqueados.heading("id", text="ID")
tree_bloqueados.heading("tb", text="TTB")

tree_bloqueados.column("id", width=50, anchor="center")
tree_bloqueados.column("tb", width=50, anchor="center")

tree_bloqueados.pack(fill="both", expand=True)

#contador
frame_contador = tk.LabelFrame(frame_bottom, text="Contador")
frame_contador.pack(fill="x", padx=10, pady=10,)

lbl_contador = tk.Label(frame_contador, text="Contador: 0", font=("Arial", 14))
lbl_contador.pack(anchor="center", pady=5)

#frame tabla final
frame_tabla_final = tk.Frame(root)
frame_tabla_final.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

frame_end_proces = tk.LabelFrame(frame_bottom, text="Resultados")
frame_end_proces.pack(anchor="center", padx=10, pady=10)

tree_resultados = ttk.Treeview(frame_end_proces, columns=("id","operacion","respuesta","t_llegada","t_final","t_espera","t_respuesta","t_retorno","t_servicio","tme"), show="headings")
tree_resultados.heading("id", text="ID")
tree_resultados.heading("operacion", text="Operacion")
tree_resultados.heading("respuesta", text="Respuesta")
tree_resultados.heading("t_llegada", text="T-Llegada")
tree_resultados.heading("t_final", text="T-Final")
tree_resultados.heading("t_espera", text="T-Espera")
tree_resultados.heading("t_respuesta", text="T-Respuesta")
tree_resultados.heading("t_retorno", text="T-Retorno")
tree_resultados.heading("t_servicio", text="T-Servicio")
tree_resultados.heading("tme", text="TME")

tree_resultados.pack(fill="both", expand=True)

root.mainloop()
