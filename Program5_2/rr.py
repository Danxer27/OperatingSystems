import tkinter as tk
from tkinter import ttk
import time
import random as rm
import msvcrt

root = tk.Tk()
root.title("Algoritmo Round Robin - DJCE")
root.geometry("1200x720")
root.minsize(1000, 600)

# Variables y estructuras (igual que tu código original)
Procesos = []
Procesos_Existentes = []
Contador = 0
ids = []
Num_Procesos = 0
NUM_QUANTUM = 0
MAX_TME_TIME = 20

# --- (Todas tus funciones y clases quedan exactamente igual que antes) ---
# Para acortar el ejemplo aquí, copié tus funciones principales y la clase Proc
# Debes pegar las funciones tal cual las tenías en tu script (generar_datos, capturar_Num_Procesos, etc.)
# A continuación coloco exactamente tus definiciones (sin cambios lógicos), excepto la sección de interfaz.
# --------------------------------------------------------------------------------
def generar_datos():
    global NUM_QUANTUM
    try:
        NUM_QUANTUM = capturar_num_quantum()
        Num_Procesos = capturar_Num_Procesos()
        label_datos_save.config(text="Datos Generados Correctamente!", background="LawnGreen")
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
    Erroru = False
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
        self.TimeMax = rm.randint(6, MAX_TME_TIME)
        self.string_proc()
        self.print_proc()

    def generar_id(self):
        temp_id = rm.randint(1, 1000)
        for i in ids:
            if i == temp_id:
                print("Generacion de ID invalido.")
                temp_id = self.generar_id()

        return temp_id

    def generar_operacion(self):
        num1 = rm.randint(1, 1000)
        num2 = rm.randint(1, 1000)

        operaciones = ['+', '-', '*', '/', '%']
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


# --- funciones de procesamiento (procesar, anadir_proceso_memoria, esperar_tecla, tabla_contador,
# terminacion_de_proceso, mostrar_tabla_constrol_de_procesos, proceso_terminado) ---
# Copia tus implementaciones exactamente como las tenías (no modificadas).
# Para que el ejemplo de interfaz funcione, aqui deberían estar todas esas funciones.
# --------------------------------------------------------------------------------
def procesar():
    Procesos_QUEUE = []
    bloqueados = []
    Terminados = []
    global Contador
    proceso_nulo = Proc(True)
    P_NULO = False

    lbl_status.config(text="Comienza Procesamiento!", background="LawnGreen")

    if len(Procesos) < 4:
        cantidad = len(Procesos)
    else:
        cantidad = 4

    for iter in range(cantidad):  # Inserta los primeros 4 procesos en la cola
        proc_temp = Procesos.pop(0)  # Sale de cola de procesos y se inserta en memoria
        proc_temp.t_llegada = Contador
        proc_temp.en_memoria = True
        proc_id = tree_listos.insert("", "end", values=(proc_temp.id, proc_temp.TimeMax, proc_temp.tt))
        proc_temp.p_id = proc_id
        Procesos_QUEUE.append(proc_temp)

    while len(Procesos_QUEUE) > 0 or len(bloqueados) > 0 or len(Procesos) > 0:
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

        while i < time_ejec:
            Contador += 1
            proc.en_ejecucion = True

            if msvcrt.kbhit():
                tecla = msvcrt.getch().decode().lower()
                print("Tecla presionada: ", tecla)

                if tecla == 'p':
                    pausa = True
                    print("Programa en pausa...")
                    lbl_status.config(text="Programa en Pausa!", background="gold")
                    while pausa:
                        time.sleep(0.2)
                        if msvcrt.kbhit():
                            tecla_en_pausa = msvcrt.getch().decode().lower()
                            print("Tecla presionada: ", tecla_en_pausa)
                            if tecla_en_pausa == 'c':
                                pausa = False
                                print("Programa reaunudado!")
                                lbl_status.config(text="Programa Reaunudado!", background="LawnGreen")

                if tecla == 'w':
                    w_error = True
                    time_ejec = 0

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

                if tecla == 'b':
                    print("Programa en pausa...")
                    lbl_status.config(text="Programa en Pausa!", background="gold")
                    mostrar_tabla_constrol_de_procesos()
                    esperar_tecla()

            tabla_contador(proc, w_error, P_NULO, i)

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
                if b_proc.ttb > 8:
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
            proc.tt += 1
            proc.ttq += 1

            if proc.ttq >= NUM_QUANTUM:
                proc.ttq = 0
                time_ejec = 0

            i += 1
            proc.en_ejecucion = False
            root.update()
            time.sleep(1.0)

        if proc.TimeMax - proc.tt > 0 and not e_blocking:
            fin_quantum = True
            proc_id = tree_listos.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt))
            proc.p_id = proc_id
            Procesos_QUEUE.append(proc)
        else:
            fin_quantum = False

        proc.ttq = 0

        terminacion_de_proceso(proc, Lista_terminados=Terminados, E_bloqueo_activado=e_blocking, Fin_QUANTUM=fin_quantum, W_error_act=w_error, Proceso_Nulo_Active=P_NULO)
        anadir_proceso_memoria(Procesos_QUEUE, bloqueados)

    print("Procesos terminado")
    proceso_terminado()


def anadir_proceso_memoria(Procesos_QUEUE, bloqueados):
    if ((len(Procesos_QUEUE) + len(bloqueados)) < 4 and len(Procesos) > 0):
        proc_new = Procesos.pop(0)
        proc_new.t_llegada = Contador
        proc_id = tree_listos.insert("", "end", values=(proc_new.id, proc_new.TimeMax, proc_new.tt))
        proc_new.p_id = proc_id
        proc_new.en_memoria = True
        Procesos_QUEUE.append(proc_new)


def esperar_tecla():
    print("Pausa activada. Presiona 'c' para continuar...")
    while True:
        if msvcrt.kbhit():
            tecla_en_pausa = msvcrt.getch().decode().lower()
            print("Tecla presionada en pausa:", tecla_en_pausa)
            if tecla_en_pausa == 'c':
                for item in tree_resultados.get_children():
                    tree_resultados.delete(item)
                print("Programa reanudado!")
                lbl_status.config(text="Programa Reaunudado!", background="LawnGreen")
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

    print(f"Contando... {i}")


def terminacion_de_proceso(proc, Lista_terminados, E_bloqueo_activado, Fin_QUANTUM, W_error_act, Proceso_Nulo_Active):
    proc.t_finalizacion = Contador
    proc.t_retorno = proc.t_finalizacion - proc.t_llegada
    proc.t_espera = proc.t_retorno - proc.tt
    proc.t_respuesta = proc.t_comienzo - proc.t_llegada

    if E_bloqueo_activado or Fin_QUANTUM:
        pass
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
            tree_resultados.insert("", "end", values=(proc.id, "Error", "X", "Error", proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax))
        elif not proc.terminado:
            if proc.en_memoria:  # en Listo
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
            else:
                temp_espera = temp_respuesta = llegada = "--"
                status = "Nuevo"

            tree_resultados.insert("", "end", values=(proc.id, status, proc.ope, "X", llegada, "--", temp_espera, temp_respuesta, "--", proc.tt, proc.TimeMax))
        else:
            tree_resultados.insert("", "end", values=(proc.id, "Terminado", proc.ope, proc.resultado, proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax))


def proceso_terminado():
    lbl_id.config(text="ID: ")
    lbl_ope.config(text="Operacion: ")
    lbl_tme.config(text="TME: ")
    lbl_tt.config(text="TT: ")
    lbl_tr.config(text="TR: 0")
    lbl_status.config(text="Programa Terminado!", background="cyan")

    mostrar_tabla_constrol_de_procesos()


# --------------------------------------------------------------------------------
# --- Interfaz: reescrita usando grid y ttk ---
# --------------------------------------------------------------------------------
style = ttk.Style(root)
# Elegir theme disponible
try:
    style.theme_use('clam')
except Exception:
    pass

default_font = ("Segoe UI", 10)

root.columnconfigure(0, weight=0)   # columna izquierda (form)
root.columnconfigure(1, weight=1)   # columna derecha (tablas)
root.rowconfigure(0, weight=1)      # fila principal
root.rowconfigure(1, weight=0)      # fila inferior (botones/estado)

# FRAME IZQUIERDO: formulario y texto de guardados
frame_left = ttk.Frame(root, padding=(8, 8))
frame_left.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
frame_left.columnconfigure(0, weight=1)

lbl_title_left = ttk.Label(frame_left, text="Configuración", font=("Segoe UI", 12, "bold"))
lbl_title_left.grid(row=0, column=0, sticky="w", pady=(0, 8))

label_Num_Procesos = ttk.Label(frame_left, text="Ingresa cantidad de procesos:", font=default_font)
label_Num_Procesos.grid(row=1, column=0, sticky="w", pady=2)
entrada_procesos = ttk.Entry(frame_left)
entrada_procesos.grid(row=2, column=0, sticky="ew", pady=2)

label_Num_quantum = ttk.Label(frame_left, text="Ingresa el tamaño del Quantum:", font=default_font)
label_Num_quantum.grid(row=3, column=0, sticky="w", pady=6)
entrada_quantum = ttk.Entry(frame_left)
entrada_quantum.grid(row=4, column=0, sticky="ew", pady=2)

label_datos_save = ttk.Label(frame_left, text="", font=default_font)
label_datos_save.grid(row=5, column=0, sticky="ew", pady=6)

btn_guardar_datos = ttk.Button(frame_left, text="Generar proceso(s)", command=generar_datos)
btn_guardar_datos.grid(row=6, column=0, sticky="ew", pady=4)

# Text Guardados con scrollbar
guardados_frame = ttk.Frame(frame_left)
guardados_frame.grid(row=7, column=0, sticky="nsew", pady=(8, 0))
guardados_frame.rowconfigure(0, weight=1)
guardados_frame.columnconfigure(0, weight=1)

Guardados = tk.Text(guardados_frame, width=40, height=18, wrap=tk.WORD, font=default_font)
Guardados.grid(row=0, column=0, sticky="nsew")

scroll_guardados = ttk.Scrollbar(guardados_frame, orient="vertical", command=Guardados.yview)
scroll_guardados.grid(row=0, column=1, sticky="ns")
Guardados.config(yscrollcommand=scroll_guardados.set)

# FRAME DERECHO: tablas y panel de ejecucion
frame_right = ttk.Frame(root, padding=(6, 6))
frame_right.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
frame_right.columnconfigure(0, weight=1)
frame_right.rowconfigure(0, weight=1)
frame_right.rowconfigure(1, weight=0)

# Arriba del derecho: panel de tablas principales
top_right = ttk.Frame(frame_right)
top_right.grid(row=0, column=0, sticky="nsew")
top_right.columnconfigure(0, weight=2)  # listos
top_right.columnconfigure(1, weight=1)  # proc ejec
top_right.columnconfigure(2, weight=2)  # terminados

# Frame: Procesos trabajando (tree_listos)
frame_listos = ttk.LabelFrame(top_right, text="Procesos trabajando")
frame_listos.grid(row=0, column=0, sticky="nsew", padx=4, pady=2)
frame_listos.rowconfigure(0, weight=1)
frame_listos.columnconfigure(0, weight=1)

tree_listos = ttk.Treeview(frame_listos, columns=("id", "tme", "tt"), show="headings", selectmode="browse")
tree_listos.heading("id", text="ID")
tree_listos.heading("tme", text="TME")
tree_listos.heading("tt", text="TT")
tree_listos.column("id", width=80, anchor="center")
tree_listos.column("tme", width=80, anchor="center")
tree_listos.column("tt", width=80, anchor="center")

vsb_listos = ttk.Scrollbar(frame_listos, orient="vertical", command=tree_listos.yview)
tree_listos.configure(yscrollcommand=vsb_listos.set)
tree_listos.grid(row=0, column=0, sticky="nsew")
vsb_listos.grid(row=0, column=1, sticky="ns")

# Frame: Proceso en ejecucion (panel de info)
frame_proceso = ttk.LabelFrame(top_right, text="Proceso en ejecución")
frame_proceso.grid(row=0, column=1, sticky="nsew", padx=4, pady=2)
frame_proceso.columnconfigure(0, weight=1)

lbl_id = ttk.Label(frame_proceso, text="ID: -", font=default_font)
lbl_id.grid(row=0, column=0, sticky="w", pady=2)
lbl_ope = ttk.Label(frame_proceso, text="Operacion: -", font=default_font, wraplength=260)
lbl_ope.grid(row=1, column=0, sticky="w", pady=2)
lbl_tme = ttk.Label(frame_proceso, text="TME: -", font=default_font)
lbl_tme.grid(row=2, column=0, sticky="w", pady=2)
lbl_tt = ttk.Label(frame_proceso, text="TT: -", font=default_font)
lbl_tt.grid(row=3, column=0, sticky="w", pady=2)
lbl_tr = ttk.Label(frame_proceso, text="TR: -", font=default_font)
lbl_tr.grid(row=4, column=0, sticky="w", pady=2)

# Frame: Terminados (tree_terminados)
frame_terminados = ttk.LabelFrame(top_right, text="Terminados")
frame_terminados.grid(row=0, column=2, sticky="nsew", padx=4, pady=2)
frame_terminados.rowconfigure(0, weight=1)
frame_terminados.columnconfigure(0, weight=1)

tree_terminados = ttk.Treeview(frame_terminados, columns=("id", "ope", "res"), show="headings")
tree_terminados.heading("id", text="ID")
tree_terminados.heading("ope", text="Ope")
tree_terminados.heading("res", text="Res")
tree_terminados.column("id", width=100, anchor="center")
tree_terminados.grid(row=0, column=0, sticky="nsew")

vsb_term = ttk.Scrollbar(frame_terminados, orient="vertical", command=tree_terminados.yview)
tree_terminados.configure(yscrollcommand=vsb_term.set)
vsb_term.grid(row=0, column=1, sticky="ns")

# FILA INFERIOR EN FRAME_RIGHT: botones y estado
bottom_right = ttk.Frame(frame_right)
bottom_right.grid(row=1, column=0, sticky="ew", pady=(8, 0))
bottom_right.columnconfigure(0, weight=1)
bottom_right.columnconfigure(1, weight=0)
bottom_right.columnconfigure(2, weight=0)

# Botones y labels principales
btn_comenzar_proceso = ttk.Button(bottom_right, text="Comenzar Proceso", command=procesar)
btn_comenzar_proceso.grid(row=0, column=0, sticky="w", padx=(0, 8))

lbl_procesos_restantes = ttk.Label(bottom_right, text=f"Procesos restantes: ", font=default_font)
lbl_procesos_restantes.grid(row=0, column=1, sticky="e", padx=6)

lbl_status = ttk.Label(bottom_right, text="Estado: -", font=default_font)
lbl_status.grid(row=0, column=2, sticky="e", padx=6)

# -----------------------------------------
# FRAME INFERIOR (span de columnas): bloqueados, contador, resultados
# -----------------------------------------
frame_bottom = ttk.Frame(root, padding=(6, 6))
frame_bottom.grid(row=1, column=0, columnspan=2, sticky="nsew")
frame_bottom.columnconfigure(0, weight=1)
frame_bottom.columnconfigure(1, weight=1)
frame_bottom.rowconfigure(0, weight=0)
frame_bottom.rowconfigure(1, weight=1)

# Bloqueados
frame_bloqueados = ttk.LabelFrame(frame_bottom, text="Bloqueados")
frame_bloqueados.grid(row=0, column=0, sticky="nsew", padx=4, pady=2)
lbl_bloqueados_data = ttk.Label(frame_bloqueados, text="ID   TTB")
lbl_bloqueados_data.grid(row=0, column=0, sticky="w", padx=3, pady=2)

lbl_bloq1 = ttk.Label(frame_bloqueados, text="")
lbl_bloq1.grid(row=1, column=0, sticky="w", padx=10)
lbl_bloq2 = ttk.Label(frame_bloqueados, text="")
lbl_bloq2.grid(row=2, column=0, sticky="w", padx=10)
lbl_bloq3 = ttk.Label(frame_bloqueados, text="")
lbl_bloq3.grid(row=3, column=0, sticky="w", padx=10)
lbl_bloq4 = ttk.Label(frame_bloqueados, text="")
lbl_bloq4.grid(row=4, column=0, sticky="w", padx=10)

# Contador
frame_contador = ttk.LabelFrame(frame_bottom, text="Contador")
frame_contador.grid(row=0, column=1, sticky="nsew", padx=4, pady=2)
lbl_contador = ttk.Label(frame_contador, text="Contador: 0", font=("Segoe UI", 12))
lbl_contador.grid(row=0, column=0, pady=6)

# Resultados (tabla extensa)
frame_results = ttk.LabelFrame(frame_bottom, text="Resultados")
frame_results.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=4, pady=6)
frame_results.rowconfigure(0, weight=1)
frame_results.columnconfigure(0, weight=1)

cols = ("id","status","operacion","respuesta","t_llegada","t_final","t_espera","t_respuesta","t_retorno","t_servicio","tme")
tree_resultados = ttk.Treeview(frame_results, columns=cols, show="headings")
for c in cols:
    tree_resultados.heading(c, text=c)
    tree_resultados.column(c, width=100, anchor="center")

tree_resultados.grid(row=0, column=0, sticky="nsew")

vsb_res = ttk.Scrollbar(frame_results, orient="vertical", command=tree_resultados.yview)
tree_resultados.configure(yscrollcommand=vsb_res.set)
vsb_res.grid(row=0, column=1, sticky="ns")

# Ajustes finales: hacer que algunos frames expandan al redimensionar
for w in (frame_right, frame_results, frame_listos, frame_terminados):
    w.grid_propagate(True)

# Iniciar loop
root.mainloop()
