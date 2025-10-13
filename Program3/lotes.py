import tkinter as tk
from tkinter import ttk
import time
import random as rm
import msvcrt

root = tk.Tk()
root.title("Procesamiento por lotes")
root.geometry("854x480")

Procesos = []
Contador = 0
ids = []
Num_Procesos = 0
MAX_TME_TIME = 20
 
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
            NewProceso = Proc(False)
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
    resultado = 0
    p_id = ""
    tt = 0
    ttb = 0
    Erroru = False
    t_comienzo = 0
    t_llegada = 0
    t_respuesta = 0
    t_finalizacion = 0
    t_espera = 0
    t_retorno = 0
    t_servicio = 0
    first_time = True
    
    def __init__(self, nulo=False):
        if nulo:
            self.generar_nulo()
        else:
            self.generar_campos()
        
    def generar_nulo(self):
        self.id = 0
        self.ope = "Nulo"
        self.TimeMax = 1

    def generar_campos(self):
        self.id = self.generar_id()
        self.ope = self.generar_operacion()
        self.TimeMax = rm.randint(6,MAX_TME_TIME)
        self.string_proc()
        self.print_proc()

    def generar_id(self):
        temp_id = rm.randint(1,1000)
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
    bloqueados = []
    Terminados = []
    global Contador
    proceso_nulo = Proc(True)
    P_NULO = False
    
    if len(Procesos) < 4:
        cantidad = len(Procesos)
    else: 
        cantidad = 4
    
    for iter in range(cantidad):  #Inserta los primeros 4 procesos en la cola
        proc_temp = Procesos.pop(0)
        proc_temp.t_llegada = Contador
        proc_id = tree_listos.insert("", "end", values=(proc_temp.id, proc_temp.TimeMax, proc_temp.tt))
        proc_temp.p_id = proc_id
        Procesos_QUEUE.append(proc_temp)
    
    while len(Procesos_QUEUE) > 0 or len(bloqueados) > 0 or len(Procesos) > 0: # PROCESADO DE PROCESOS, # COMIENZO #
        if len(Procesos_QUEUE) > 0:
            proc = Procesos_QUEUE.pop(0)
            if proc.p_id:  # borrar solo si existe un item en el treeview
                try:
                    tree_listos.delete(proc.p_id)
                except Exception:
                    pass
            P_NULO = False
        else:
            proc = proceso_nulo
            P_NULO = True
            print("Entrada Nulo")
            
        if proc.first_time:
            proc.t_comienzo = Contador
            proc.first_time = False
    
        if P_NULO:
            time_ejec = 15
        else:
            time_ejec = proc.TimeMax - proc.tt
        w_error = False
        e_blocking = False
        i = 0
        
        while i <= time_ejec: # PROCESA ACTUAL -----------------
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
                    if not P_NULO:
                        bloqueados.append(proc)
                        e_blocking = True
                        time_ejec = 0

            
            # fin funciones de teclas
            
            # ACTUALIZACION INTERFAZ POR SEGUNDO /////
            # Tabla de ejecucion ---
            
            lbl_id.config(text=f"ID: {proc.id}")
            if w_error or P_NULO:
                lbl_ope.config(text=f"Operacion: X")
                lbl_tme.config(text=f"TME: Esperando...")
                lbl_tr.config(text=f"TR: N/A")
            else:
                lbl_ope.config(text=f"Operacion: {proc.ope}")
                lbl_tme.config(text=f"TME: {proc.TimeMax}")
                lbl_tr.config(text=f"TR: {time_ejec - i}")
            lbl_contador.config(text=f"Contador: {Contador}")
            lbl_tt.config(text=f"TT: {i}")
            
            print(f"Contando... {i}")
            
                #Bloqueados
            labels_bloqueados = [lbl_bloq1, lbl_bloq2, lbl_bloq3, lbl_bloq4]
            qindex = 0
            for lbl in labels_bloqueados:
                if qindex < len(bloqueados):
                    lbl.config(text=f"{bloqueados[qindex].id}    {bloqueados[qindex].ttb}")
                else:
                    lbl.config(text="")
                qindex += 1
            
            nuevos_bloqueados = []
            for b_proc in bloqueados:
                b_proc.ttb += 1
                if b_proc.ttb > 8:   # ya cumplió, pasa a listos
                    if P_NULO:
                        time_ejec = 0
                        P_NULO = False
                    b_proc.ttb = 0
                    proc_id = tree_listos.insert("", "end", values=(b_proc.id, b_proc.TimeMax, b_proc.tt))
                    b_proc.p_id = proc_id
                    Procesos_QUEUE.append(b_proc)
                else:
                    nuevos_bloqueados.append(b_proc)

            bloqueados = nuevos_bloqueados
                    
                    
            #cambiando tiempo transcurrido interno
            proc.tt += 1
            i += 1
            root.update()
            time.sleep(1)
            
        # ^^^^^^^ TERMINA DEL PROCESO ^^^^^^^
        proc.t_finalizacion = Contador
        proc.t_retorno = proc.t_finalizacion - proc.t_llegada
        proc.t_espera = proc.t_retorno - proc.tt - 1
        proc.t_respuesta = proc.t_comienzo - proc.t_llegada
            
        if e_blocking:
            pass
        elif not w_error and not P_NULO:
            try:
                result = eval(proc.ope)
                proc.resultado = result
                tree_terminados.insert("", "end", values=(proc.id, proc.ope, result))
                Terminados.append(proc)
                
            except Exception:
                result = "Error eval"
        else:
            proc.resultado = "Error"
            proc.Erroru = True
            tree_terminados.insert("", "end", values=(proc.id, proc.ope, "Error"))
            
            Terminados.append(proc)

         # añade nuevo proceso a la memoria
        if((len(Procesos_QUEUE) + len(bloqueados)) < 4 and len(Procesos) > 0):
            proc = Procesos.pop(0)
            proc.t_llegada = Contador
            proc_id = tree_listos.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
            proc.p_id = proc_id
            Procesos_QUEUE.append(proc)
                
                
    # ^^^^ FIN DE EJECUCION ^^^^

    print("Procesos terminado")
    proceso_terminado(Terminados)

    
def proceso_terminado(terminados): #limpia la tabla de procesos en ejecucion
        lbl_id.config(text="ID: ")
        lbl_ope.config(text="Operacion: ")
        lbl_tme.config(text="TME: ")
        lbl_tt.config(text="TT: ")
        lbl_tr.config(text="TR: 0")
        
        #meter a resultados
        for proc in terminados:
            if not proc.Erroru:
                tree_resultados.insert("", "end", values=(proc.id, proc.ope, proc.resultado, proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax))
            else:
                tree_resultados.insert("", "end", values=(proc.id, "X", "Error", proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax))

# /// INTERFAZ GRAFICA ///

frame_left = tk.Frame(root)   #formulario
frame_left.pack(side="left", fill="y", padx=10, pady=10)

frame_right = tk.Frame(root)  #tablas y procesos
frame_right.pack(side="left", fill="both", expand=True, padx=10, pady=5)

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
frame_tablas.pack(fill="both", expand=True, padx=10, pady=5)

frame_listos = tk.LabelFrame(frame_tablas, text="Procesos trabajando")
frame_listos.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tree_listos = ttk.Treeview(frame_listos, columns=("id", "tme", "tt"), show="headings")
tree_listos.heading("id", text="ID")
tree_listos.heading("tme", text="TME")
tree_listos.heading("tt", text="TT")

tree_listos.column("id", width=80, anchor="center")
tree_listos.column("tme", width=80, anchor="center")  
tree_listos.column("tt", width=80, anchor="center")  

tree_listos.pack(fill="both", expand=True)

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
frame_bottom = tk.Frame(root) #frame de abajo
frame_bottom.pack(side="bottom", fill="both", expand=True, padx=10, pady=2)

frame_bloqueados = tk.LabelFrame(frame_bottom, text="Bloqueados")
frame_bloqueados.pack(side="left", fill="both", expand=True, padx=10, pady=10)

lbl_bloqueados_data = tk.Label(frame_bloqueados, text="ID   TTB")
lbl_bloqueados_data.grid(row=0, column=0, sticky="w", padx=10, pady=5)

lbl_bloq1 = tk.Label(frame_bloqueados, text="")
lbl_bloq1.grid(row=1, column=0, sticky="w", padx=10)
lbl_bloq2 = tk.Label(frame_bloqueados, text="")
lbl_bloq2.grid(row=2, column=0, sticky="w", padx=10)
lbl_bloq3 = tk.Label(frame_bloqueados, text="")
lbl_bloq3.grid(row=3, column=0, sticky="w", padx=10)
lbl_bloq4 = tk.Label(frame_bloqueados, text="")
lbl_bloq4.grid(row=4, column=0, sticky="w", padx=10)

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
