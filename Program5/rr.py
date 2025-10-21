import tkinter as tk
from tkinter import ttk
import time
import random as rm
import msvcrt

root = tk.Tk()
root.title("First Come, First Served")
root.geometry("1620x780")
root.resizable(True, True)

Procesos = []
Procesos_Existentes = [] # Lo mismo que 'Procesos' pero no se usa como cola sino como estatico para mostrar en tabla.
Contador = 0
ids = []
Num_Procesos = 0
NUM_QUANTUM = 0
MAX_TME_TIME = 10
 
# GENERA DATOS PRIMERO LLAMANDO A CAPTURAR EL NUMERO DE PROCESO
def generar_datos():
        global NUM_QUANTUM
        try: 
            NUM_QUANTUM = capturar_num_quantum()
            Num_Procesos = capturar_Num_Procesos()
            label_datos_save.config(text="Datos Generados Correctamente!", bg="LawnGreen")
        except ValueError as e:
            label_datos_save.config(text=str(e), background="red")
        except Exception as e:
            label_datos_save.config(text=str(e), background="red")
            
        for i in range(Num_Procesos):
            NewProceso = Proc(False)
            Procesos.append(NewProceso)
            Procesos_Existentes.append(NewProceso)
            
    
def capturar_Num_Procesos():
    temp_num = entrada_procesos.get()
    try: 
        temp_num = int(temp_num)
    except ValueError:
        raise ValueError("Numero de proceos no valido.")

    if temp_num < 1:
        raise ValueError("Numero de proceso no puede ser negativo.")
    
    if temp_num == None:
        raise ValueError("Numero de procesos vacio.")
    
    return temp_num   

def capturar_num_quantum():
    temp_num = entrada_quantum.get()
    try: 
        temp_num = int(temp_num)
    except ValueError:
        raise ValueError("Numero de quantum no valido.")

    if temp_num < 1:
        raise ValueError("Numero de quantum no puede ser negativo.")
    
    if temp_num == None:
        raise ValueError("Numero quantum vacio.")
    
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
    ttq = 0
    Erroru = False #salida por tecla error
    t_comienzo = 0
    t_llegada = 0
    t_respuesta = 0
    t_finalizacion = 0
    t_espera = 0
    t_retorno = 0
    t_servicio = 0
    first_time = True
    terminado = False
    en_memoria = False
    bloqueado = False
    en_ejecucion = False
    
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
        
        operaciones = ['+','-','*','/','%']
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
        
        
"""
    -Hay 2 momentos en los que un proceso llega a memoria, uno es cuando es insertado al iniciar el proceso
    -> Inicio de funcion procesar (Linea 147 aprox)
    otro cuando al terminar un proceso se libera espacio de memoria y se añade uno nuevo.
    -> Final de funcion procesar (Line 265 aprox)
    
    -Tambien hay 2 momentos cuando un proceso es generado, al inicio y tecla N
    ->
"""   

# FUNCION PRINCIPAL DE PROCESOS
def procesar():
    Procesos_QUEUE = []
    bloqueados = []
    Terminados = []
    global Contador
    proceso_nulo = Proc(True)
    P_NULO = False
    
    lbl_status.config(text="Comienza Procesamiento!", bg="LawnGreen")
    
    if len(Procesos) < 4:
        cantidad = len(Procesos)
    else: 
        cantidad = 4
    
    for iter in range(cantidad):  #Inserta los primeros 4 procesos en la cola
        proc_temp = Procesos.pop(0) # Sale de cola de procesos y se inserta en memoria
        proc_temp.t_llegada = Contador
        proc_temp.en_memoria = True
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
        
        #  $$$$$$ CALCULAR TIEMPO RESTANTE Y CALCULAR SU TIEMPO DE QUANTUM
        
        while i < time_ejec: #///// PROCESA ACTUAL ////////// Ejecuta por segundo
            Contador += 1
            proc.en_ejecucion = True
            
            #ESTRUCTURA DE KHBIT:
            if msvcrt.kbhit():  # detecta si hay una tecla presionada
                tecla = msvcrt.getch().decode().lower()  # obtiene la tecla
                print("Tecla presionada: ", tecla)

                if tecla == 'p':
                    pausa = True
                    print("Programa en pausa...")
                    lbl_status.config(text="Programa en Pausa!", bg="gold")
                    while pausa:
                        time.sleep(0.2)
                        if msvcrt.kbhit():
                            tecla_en_pausa = msvcrt.getch().decode().lower()  
                            print("Tecla presionada: ", tecla_en_pausa)
                            if tecla_en_pausa == 'c':
                                pausa = False
                                print("Programa reaunudado!")
                                lbl_status.config(text="Programa Reaunudado!", bg="LawnGreen")

                if tecla == 'w':
                    w_error = True
                    time_ejec = 0 #establece el tiempo restante en 0 cuando se da error para que pase directo a terminados, estaba en 1

                if tecla == 'e':
                    if not P_NULO:
                        proc.bloqueado = True
                        bloqueados.append(proc)
                        e_blocking = True
                        time_ejec = 0

                if tecla == 'n':
                    NewProceso = Proc(False)
                    Procesos.append(NewProceso)
                    Procesos_Existentes.append(NewProceso)
                    #anadir_proceso_memoria(Procesos_QUEUE, bloqueados) // estaba dando errores xdxd

                if tecla == 'b':
                    print("Programa en pausa...")
                    lbl_status.config(text="Programa en Pausa!", bg="gold")
                    mostrar_tabla_constrol_de_procesos()
                    esperar_tecla()


                # ^^^^^^ fin funciones de teclas

                # ACTUALIZACION INTERFAZ POR SEGUNDO /////
            
            # Tabla de ejecucion
            tabla_contador(proc, w_error, P_NULO, i)
            
            # ///////////  Bloqueados
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
                    b_proc.bloqueado = False
                    b_proc_id = tree_listos.insert("", "end", values=(b_proc.id, b_proc.TimeMax, b_proc.tt))
                    b_proc.p_id = b_proc_id
                    Procesos_QUEUE.append(b_proc)
                else:
                    nuevos_bloqueados.append(b_proc)

            bloqueados = nuevos_bloqueados
                    
            lbl_procesos_restantes.config(text=f"Procesos restantes(en Nuevos): {len(Procesos)}")        
            #cambiando tiempo transcurrido interno
            proc.tt += 1
            proc.ttq += 1
            
            if proc.ttq >= NUM_QUANTUM:
                proc.ttq = 0
                time_ejec = 0
            
            i += 1
            proc.en_ejecucion = False
            root.update()
            time.sleep(1.0)
        
            
        # ^^^^^^^ TERMINA DEL PROCESO ^^^^^^^s
       
        if proc.TimeMax - proc.tt > 0 and not e_blocking:
            fin_quantum = True
            proc_id = tree_listos.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
            proc.p_id = proc_id
            Procesos_QUEUE.append(proc)
        else: 
            fin_quantum = False
            
        proc.ttq = 0
    
        terminacion_de_proceso(proc, Lista_terminados=Terminados, E_bloqueo_activado=e_blocking, Fin_QUANTUM=fin_quantum, W_error_act=w_error, Proceso_Nulo_Active=P_NULO)
        anadir_proceso_memoria(Procesos_QUEUE, bloqueados) # añade nuevo proceso a la memoria
            
    # ^^^^ FIN DE EJECUCION ^^^^

    print("Procesos terminado")
    proceso_terminado()

# ^^^^ FIN funcion principal ^^^^

def anadir_proceso_memoria(Procesos_QUEUE, bloqueados):
    if((len(Procesos_QUEUE) + len(bloqueados)) < 4 and len(Procesos) > 0):
            proc_new = Procesos.pop(0)
            proc_new.t_llegada = Contador
            proc_id = tree_listos.insert("", "end", values=(proc_new.id, proc_new.TimeMax, proc_new.tt))
            proc_new.p_id = proc_id
            proc_new.en_memoria = True
            Procesos_QUEUE.append(proc_new)


def esperar_tecla():
     # Espera bloqueante pero sin congelar la GUI: presiona 'c' para continuar.
    print("Pausa activada. Presiona 'c' para continuar...")
    while True:
        if msvcrt.kbhit():
            tecla_en_pausa = msvcrt.getch().decode().lower()
            print("Tecla presionada en pausa:", tecla_en_pausa)
            if tecla_en_pausa == 'c':
                for item in tree_resultados.get_children():
                    tree_resultados.delete(item)
                print("Programa reanudado!")
                lbl_status.config(text="Programa Reaunudado!", bg="LawnGreen")
                break
        root.update()
        time.sleep(0.1)

def tabla_contador(proc, w_error, P_NULO, i):
    lbl_id.config(text=f"ID: {proc.id}")
    if w_error or P_NULO:
        lbl_ope.config(text=f"Operacion: X")
        lbl_tme.config(text=f"TME: Esperando...")
        lbl_tr.config(text=f"TR: N/A")
    else:
        lbl_ope.config(text=f"Operacion: {proc.ope}")
        lbl_tme.config(text=f"TME: {proc.TimeMax}")
        lbl_tr.config(text=f"TR: {proc.TimeMax - proc.tt}")
    lbl_contador.config(text=f"Contador: {Contador}")
    lbl_tt.config(text=f"TT: {proc.tt}")
    
    print(f"Contando... {i}")
    

def terminacion_de_proceso(proc, Lista_terminados, E_bloqueo_activado, Fin_QUANTUM, W_error_act, Proceso_Nulo_Active):
    proc.t_finalizacion = Contador
    proc.t_retorno = proc.t_finalizacion - proc.t_llegada
    proc.t_espera = proc.t_retorno - proc.tt
    proc.t_respuesta = proc.t_comienzo - proc.t_llegada
    
        
    if E_bloqueo_activado or Fin_QUANTUM:
        pass #Si fue bloqueado o solo fue cambio de quantum no debe hacer nada con el proceso.
    elif not W_error_act and not Proceso_Nulo_Active:
        try:
            result = eval(proc.ope)
            proc.resultado = result
            proc.terminado = True
            tree_terminados.insert("", "end", values=(proc.id, proc.ope, result))
            Lista_terminados.append(proc)
            
        except Exception:
            result = "Error eval"
    else:
        proc.resultado = "Error"
        proc.Erroru = True
        tree_terminados.insert("", "end", values=(proc.id, proc.ope, "Error"))
        Lista_terminados.append(proc)
        
        
def mostrar_tabla_constrol_de_procesos():
    for proc in Procesos_Existentes:
            if proc.Erroru:
                tree_resultados.insert("", "end", values=(proc.id, "Error" ,"X", "Error", proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax))
            elif not proc.terminado:
                if proc.en_memoria: # en Listo
                    llegada = proc.t_llegada 
                    temp_espera = Contador - llegada - proc.tt
                    if proc.bloqueado:
                        status = "Bloqueado"
                    else:
                        if proc.en_ejecucion:
                            status = "Ejecutando"
                        else:
                            status = "Listo"
                    if proc.tt > 0:
                        temp_respuesta = proc.t_comienzo - proc.t_llegada
                    else: 
                        temp_respuesta = "--"
               
                else:  #nuevo (no en memoria)
                    temp_espera = temp_respuesta = llegada = "--"
                    status = "Nuevo"
                
                tree_resultados.insert("", "end", values=(proc.id, status, proc.ope, "X", llegada, "--", temp_espera, temp_respuesta, "--", proc.tt, proc.TimeMax))
            else:
                tree_resultados.insert("", "end", values=(proc.id, "Terminado", proc.ope, proc.resultado, proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax))

    
def proceso_terminado(): #limpia la tabla de procesos en ejecucion
        lbl_id.config(text="ID: ")
        lbl_ope.config(text="Operacion: ")
        lbl_tme.config(text="TME: ")
        lbl_tt.config(text="TT: ")
        lbl_tr.config(text="TR: 0")
        lbl_status.config(text="Programa Terminado!", bg="cyan")
        
        mostrar_tabla_constrol_de_procesos()
        

        
# /// INTERFAZ GRAFICA ///

frame_left = tk.Frame(root)   #formulario
frame_left.pack(side="left", fill="y", padx=10, pady=3)

frame_right = tk.Frame(root)  #tablas y procesos
frame_right.pack(side="left", fill="both", expand=True, padx=10, pady=5)

#botones para captura de datos
label_Num_Procesos = tk.Label(frame_left, text="Ingresa cantidad de procesos: ")
label_Num_Procesos.pack(pady=1)
entrada_procesos = tk.Entry(frame_left)
entrada_procesos.pack(pady=1)
label_Num_quantum = tk.Label(frame_left, text="Ingresa el tamaño del Quantum: ")
label_Num_quantum.pack(pady=1)
entrada_quantum = tk.Entry(frame_left)
entrada_quantum.pack(pady=1)

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

lbl_status = tk.Label(root, text=f":")
lbl_status.pack(pady=3, padx=50)

#Frames de procesos
frame_tablas = tk.Frame(root)
frame_tablas.pack(fill="both", expand=True, padx=5, pady=3)

frame_listos = tk.LabelFrame(frame_tablas, text="Procesos trabajando")
frame_listos.pack(side="left", fill="both", expand=True, padx=5, pady=3)

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
frame_proceso.pack(side="left", fill="y", padx=5, pady=3)

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
frame_terminados.pack(side="left", fill="both", expand=True, padx=5, pady=3)

tree_terminados = ttk.Treeview(frame_terminados, columns=("id", "ope", "res"), show="headings")
tree_terminados.heading("id", text="ID")
tree_terminados.heading("ope", text="Ope")
tree_terminados.heading("res", text="Res")
tree_terminados.column("id", width=100, anchor="center")

tree_terminados.pack(fill="both", expand=True)

#frame de gui de Bloqueados
frame_bottom = tk.Frame(root) #frame de abajo
frame_bottom.pack(side="bottom", fill="both", expand=True, padx=3, pady=1)

frame_bloqueados = tk.LabelFrame(frame_bottom, text="Bloqueados")
frame_bloqueados.pack(side="left", fill="both", expand=True, padx=3, pady=2)

lbl_bloqueados_data = tk.Label(frame_bloqueados, text="ID   TTB")
lbl_bloqueados_data.grid(row=0, column=0, sticky="w", padx=3, pady=2)

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
frame_contador.pack(fill="x", padx=3, pady=2)

lbl_contador = tk.Label(frame_contador, text="Contador: 0", font=("Arial", 14))
lbl_contador.pack(anchor="center", pady=3)

#frame tabla final
frame_tabla_final = tk.Frame(frame_bottom)
frame_tabla_final.pack(side="bottom", fill="both", expand=True, padx=3, pady=1)

frame_end_proces = tk.LabelFrame(frame_bottom, text="Resultados")
frame_end_proces.pack(anchor="center", padx=10, pady=5)
frame_end_proces.pack(anchor="center", padx=10, pady=5)

tree_resultados = ttk.Treeview(frame_end_proces, columns=("id","status","operacion","respuesta","t_llegada","t_final","t_espera","t_respuesta","t_retorno","t_servicio","tme"), show="headings")
tree_resultados.heading("id", text="ID")
tree_resultados.heading("status", text="Estado")
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
