import tkinter as tk
from tkinter import ttk
import time
import random as rm
import msvcrt

root = tk.Tk()
root.title("Paginacion Simple - DJCE")
root.geometry("1620x780")
root.resizable(True, True)

Procesos = []
Memoria = [[False, []] for _ in range(44)]
Celdas_numMarcos = []
Procesos_Existentes = [] # Lo mismo que 'Procesos' pero no se usa como cola sino como estatico para mostrar en tabla.
Contador = 0
ids = []
Num_Procesos = 0
labels_bloqueados = []
Suspendidos = []
NUM_QUANTUM = 0
MAX_TME_TIME = 20
MAX_SIZE = 30


Colores_mem = [
    # Azules oscuros
    "#2C3E50", "#34495E", "#22313F", "#1B2631",
    # Grises oscuros
    "#2B2B2B", "#3C3C3C", "#4D4D4D", "#6E6E6E",
    # Verdes oscuros
    "#0E421A", "#1D4928", "#0F3D33",
    # Rojos oscuros
    "#58151C", "#6A1E1E", "#7B2D26",
    # Morados oscuros
    "#3A1A47", "#4B2E5A", "#5C3B6C",
    # Marrones oscuros
    "#4B2E1E", "#5A3A28", "#6C4A30",
]

 
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
    size = 0
    fsize = 0
    dir_in = 0
    dir_fin = 0
    color = None
    suspendido = False
    respuesta_positiva = False

    def __init__(self, nulo=False):
        if nulo:
            self.generar_nulo()
        else:
            self.generar_campos()
        
    def generar_nulo(self):
        self.id = 0
        self.ope = "Nulo"
        self.TimeMax = 10000
        self.dir_in = None
        self.dir_fin = None

    def generar_campos(self):
        self.id = self.generar_id()
        self.ope = self.generar_operacion()
        self.TimeMax = rm.randint(6,MAX_TME_TIME)
        self.size = rm.randint(6,MAX_SIZE)
        self.fsize = (self.size + 4) // 5
        self.string_proc()
        self.print_proc()

    def generar_id(self):
        temp_id = rm.randint(1,1000)
        if temp_id in ids:
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
        print(f"ID: {self.id} - Operacion: {self.ope} - TME: {self.TimeMax}")        
    
    def string_proc(self):
        self.string_proc = f"-ID:{self.id} -TME: {self.TimeMax} - TAM: {self.size} Frames:{self.fsize} -Ope:{self.ope}\n"
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
    Mem_QUEUE = []
    bloqueados = []
    Terminados = []
    global Contador
    global Procesos
    proceso_nulo = Proc(True)
    P_NULO = False

    lbl_status.config(text="Comienza Procesamiento!", bg="LawnGreen")
        
    # Insercion de procesos en memoria
    anadir_proceso_memoria(Mem_QUEUE) # AÑADE PROCESOS QUE PUEDAN CABER
    
    while len(Mem_QUEUE) > 0 or len(bloqueados) > 0 or len(Procesos) > 0 or len(Suspendidos) > 0: # PROCESADO DE PROCESOS, # COMIENZO #
        ''' Al comenzar proceso esta primera parte verifrica is hay procesos en la cola de nuevos
        para poder ingresarlos en ememoria, tambien verifica que si el proceso activo es un proceso nulo
        '''
        if len(Mem_QUEUE) > 0:
            proc = Mem_QUEUE.pop(0)
            # Verificar si es el proceso nulo
            if proc.id != 0:
                if proc.p_id:  # borrar solo si existe un item en el treeview
                    try:
                        tree_listos.delete(proc.p_id)
                    except Exception:
                        pass
                P_NULO = False
                #Cambiar colores de direccion en ejecucion
                if proc.dir_in is None or proc.dir_fin is None:
                    # simplemente no lo proceses
                    continue
                pintar_marcos_en_ejecucion(proc)
        else:
            proc = proceso_nulo
            P_NULO = True
            print("Entrada Nulo")
            
        if proc.first_time:
            proc.t_comienzo = Contador
            proc.first_time = False
    
        if P_NULO:
            time_ejec = 1000
        else:
            time_ejec = proc.TimeMax - proc.tt
        
        w_error = False
        e_blocking = False
        
        i = 0
        local_counter = 0 
        '''En este caso como el proceso ya lopea cada 0.2 segundos, los contadores solo pueden hacerlo
        activarse cada segundo, entonces se hizo un local counter que cada que pasa un segundo (5 iteraciones de este)
        ahora si se aumenta 1 a los contadores que estan por segundo
        '''

        while i < time_ejec: #///// PROCESA ACTUAL ////////// Ejecuta por segundo
            if local_counter % 5 == 0 and local_counter > 0:
                Contador += 1
            proc.en_ejecucion = True
            suspension_activated = False
            proc.respuesta_positiva = True #El proceso toca memoria para confirmar respuesta
            
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
                    if not P_NULO:
                        w_error = True
                        time_ejec = 0 #establece el tiempo restante en 0 cuando se da error para que pase directo a terminados, estaba en 1
                        anadir_proceso_memoria(Mem_QUEUE)
                        pintar_marcos_en_ejecucion(proc)

                if tecla == 'e':
                    if not P_NULO:
                        proc.bloqueado = True
                        bloqueados.append(proc)
                        e_blocking = True
                        time_ejec = 0
                        print("Proceso mandado a bloqueado.")
                    else:
                        print("No hay procesos para mandar a bloqueados")
                    

                if tecla == 'n':
                    NewProceso = Proc(False)
                    Procesos.append(NewProceso)
                    Procesos_Existentes.append(NewProceso)
                    anadir_proceso_memoria(Mem_QUEUE)
                    pintar_marcos_en_ejecucion(proc)

                if tecla == 'b':
                    print("Programa en pausa...")
                    lbl_status.config(text="Programa en Pausa!", bg="gold")
                    mostrar_tabla_constrol_de_procesos()
                    esperar_tecla()

                if tecla == 's':
                    if len(bloqueados) > 0:
                        suspension_activated = True 
                        #Fucncion para activar suspension llamada en la parte de bloqueados
                    else:
                        print("No hay procesos bloqueados para mandar a suspension")
                    
                if tecla == 'r':
                    regresar_suspendido()
                    anadir_proceso_memoria(Mem_QUEUE)
                    if not P_NULO:
                        pintar_marcos_en_ejecucion(proc)

                # ^^^^^^ fin funciones de teclas

                # ACTUALIZACION INTERFAZ POR SEGUNDO /////
            
            # Tabla de ejecucion
            tabla_contador(proc, w_error, P_NULO, i)
      
            # ///////////  Bloqueados]
            qindex = 0
            for lbl in labels_bloqueados:
                if qindex < len(bloqueados):
                    lbl.config(text=f"{bloqueados[qindex].id}    {bloqueados[qindex].ttb}")
                else:
                    lbl.config(text="")
                qindex += 1
            
            nuevos_bloqueados = []
            for b_proc in bloqueados:
                for bc in range(b_proc.dir_in, b_proc.dir_fin+1):
                    Celdas_numMarcos[bc].config(bg="firebrick1")
                if local_counter % 5 == 0 and local_counter > 0:
                    b_proc.ttb += 1
                if b_proc.ttb > 8:   # ya cumplió, pasa a listos
                    if P_NULO:
                        time_ejec = 0
                        P_NULO = False
                    b_proc.ttb = 0
                    b_proc.bloqueado = False
                    # Evitar insertar procesos nulos en la tabla
                    if b_proc.id != 0:
                        b_proc_id = tree_listos.insert("", "end", values=(b_proc.id, b_proc.TimeMax, b_proc.tt, b_proc.size))
                        b_proc.p_id = b_proc_id
                        Mem_QUEUE.append(b_proc)
                    refrescar_visual_memoria() #Cuando un proceso termina debe volver a refrescar la vizual
                    pintar_marcos_en_ejecucion(proc)
                elif suspension_activated:
                    suspension_activated = False
                    b_proc.bloqueado = False
                    b_proc.suspendido = True
                    b_proc.ttb = 0
                    liberar_memoria(b_proc)
                    Suspendidos.append(b_proc)
                    modificar_suspendidos()
                    refrescar_visual_memoria() #tambien se debe refrescar cuando este sea suspendido y salga de bloqueados
                    pintar_marcos_en_ejecucion(proc)
                else:
                    nuevos_bloqueados.append(b_proc)
                
            bloqueados = nuevos_bloqueados
                    
            if len(Procesos) > 0:
                prid = Procesos[0].id
                prtam = Procesos[0].size
            else:
                prid = 0
                prtam = 0
            lbl_procesos_restantes.config(text=f"Procesos por entrar: {prid}: Tam: {prtam} \n Procesos suspendidos: {len(Suspendidos)}")        
            #cambiando tiempo transcurrido interno
            if local_counter % 5 == 0 and local_counter > 0:
                proc.tt += 1
                proc.ttq += 1
            
            if proc.ttq >= NUM_QUANTUM:
                proc.ttq = 0
                time_ejec = 0

            if local_counter % 5 == 0 and local_counter > 0:
                i += 1
            local_counter += 1
            proc.en_ejecucion = False
            root.update()
            time.sleep(0.2)
        
            
        # ^^^^^^^ TERMINA DEL PROCESO ^^^^^^^s
       
        if proc.TimeMax - proc.tt > 0 and not e_blocking:
            fin_quantum = True
            # No agregar el proceso nulo a la cola visualmente
            if not P_NULO:
                proc_id = tree_listos.insert("", "end", values=(proc.id, proc.TimeMax, proc.tt, proc.size))
                proc.p_id = proc_id
                Mem_QUEUE.append(proc)
        else: 
            fin_quantum = False
            
        proc.ttq = 0
    
        terminacion_de_proceso(proc, Lista_terminados=Terminados, E_bloqueo_activado=e_blocking, Fin_QUANTUM=fin_quantum, W_error_act=w_error, Proceso_Nulo_Active=P_NULO)
        anadir_proceso_memoria(Mem_QUEUE) # añade nuevo proceso a la memoria
            
    # ^^^^ FIN DE EJECUCION ^^^^

    print("Procesos terminado")
    proceso_terminado()

# ^^^^ FIN funcion principal ^^^^

def pintar_marcos_en_ejecucion(proc):
    if proc.dir_in and proc.dir_fin:
        for cc in range(proc.dir_in, proc.dir_fin+1):
            Celdas_numMarcos[cc].config(bg="lawnGreen")

def anadir_proceso_memoria(Mem_QUEUE):
    global Procesos
    Procesos_after = []
    for proc_new in Procesos:
        if(cabe_en_memoria(proc_new)):
                #parte logica
                # Solo asignar t_llegada la primera vez que entra a memoria
                if proc_new.t_llegada == 0:
                    proc_new.t_llegada = Contador
                # No mostrar procesos nulos en el árbol de listos
                if proc_new.id != 0:
                    proc_id = tree_listos.insert("", "end", values=(proc_new.id, proc_new.TimeMax, proc_new.tt, proc_new.size))
                    proc_new.p_id = proc_id
                else:
                    proc_new.p_id = None
                proc_new.en_memoria = True
                 
                #parte visual fisica
                icolor = rm.choice(Colores_mem)
                l,r = disponibilidad(proc_new.fsize) #Consulta el sector disponible de frames para añadir el proceso
                if l == -1:
                    # por si algo raro: no hay espacio
                    Procesos_after.append(proc_new)
                    continue
                proc_new.dir_in = l
                proc_new.dir_fin = r
                proc_new.color = icolor
                
                remaining_cells = proc_new.size
                for frame_idx in range(l, r + 1):
                    Memoria[frame_idx][0] = True
                    paint_count = min(5, remaining_cells)
                    for pi in range(paint_count):
                        try:
                            Memoria[frame_idx][1][pi].config(bg=icolor)
                        except Exception:
                            pass
                    remaining_cells -= paint_count

                # finalmente, añade a la cola de listos
                Mem_QUEUE.append(proc_new)
        else:
            Procesos_after.append(proc_new)
            
    Procesos = list(Procesos_after)
    refrescar_visual_memoria()
            
def cabe_en_memoria(proc):
    mi, mf = disponibilidad()
    if mi == -1:
        return False
    sector_disponible = mf - mi + 1
    return sector_disponible >= proc.fsize
    
def disponibilidad(necesario_disponible=0):
    """
    Si se pasa un necesario_disponible, es para encontrar el siguiente ajuste
    Si no, encuentra el sector maximo para decir si un proceso cabe
    Retorna la direccion inicial y final del sector disponible consultado
    """
    sector_disponible = 0
    dir_inicial = None

    max_sector = 0
    max_dir_inicial = -1
    max_dir_final = -1

    for i in range(len(Memoria)):
        if not Memoria[i][0]:
            if sector_disponible == 0:
                dir_inicial = i
            sector_disponible += 1

            # FIRST-FIT (siguiente ajuste)
            if necesario_disponible > 0 and sector_disponible >= necesario_disponible:
                # devolver end como índice INCLUSIVE
                return dir_inicial, i

            # SECTOR MÁS GRANDE
            if sector_disponible > max_sector:
                max_sector = sector_disponible
                max_dir_inicial = dir_inicial
                max_dir_final = i
        else:
            sector_disponible = 0
            dir_inicial = None

    if max_sector > 0:
        return max_dir_inicial, max_dir_final

    return -1, -1

def liberar_memoria(proc):
    l, r = proc.dir_in, proc.dir_fin
    # protección
    if l is None or r is None or l < 0 or r < 0:
        return
    for i in range(l, r + 1):
        Memoria[i][0] = False
        for pi in range(5):
            try:
                Memoria[i][1][pi].config(bg="#f0f0f0")
            except Exception:
                pass
    # limpiar metadatos del proceso
    proc.en_memoria = False
    proc.dir_in = None
    proc.dir_fin = None
    proc.color = None

    # repintar coherente desde la memoria lógica (opcional redundante, pero recomendable)
    refrescar_visual_memoria()
    
def refrescar_visual_memoria():
    """
    Reconstuye la vista de memoria **solo** a partir de los datos lógicos:
    - Limpia todo el grid
    - Para cada proceso en Procesos_Existentes que tenga en_memoria True, pinta sus celdas usando proc.dir_in/dir_fin y proc.size
    - Actualiza también el color del marco (Celdas_numMarcos)
    """
    # limpiar toda la visual (todos los frames y celdas)
    for frame_idx in range(len(Memoria)):
        # restablece label del marco
        try:
            Celdas_numMarcos[frame_idx].config(bg="#f0f0f0")
        except Exception:
            pass
        # restablece celdas internas
        for pi in range(5):
            try:
                Memoria[frame_idx][1][pi].config(bg="#f0f0f0")
            except Exception:
                pass

    # pintar según los procesos cargados (la fuente de verdad)
    for proc in Procesos_Existentes:
        if not getattr(proc, "en_memoria", False):
            continue
        if proc.dir_in is None or proc.dir_fin is None:
            continue
        remaining = proc.size
        for frame_idx in range(proc.dir_in, proc.dir_fin + 1):
            paint_count = min(5, remaining)
            for pi in range(paint_count):
                try:
                    # si el proceso tiene color lo usa, sino usa gris oscuro por defecto
                    color = getattr(proc, "color", "#cccccc")
                    Memoria[frame_idx][1][pi].config(bg=color)
                except Exception:
                    pass

            remaining -= paint_count
            if remaining <= 0:
                break

def modificar_suspendidos():
    with open('Memoria_susprocs.txt', 'w') as archivo:
        archivo.write("<Memoria Secundaria>")
        for sproc in Suspendidos:
            archivo.write(f"\nProceso: {sproc.id}\n\tOpe: {sproc.ope}\n\tTT: {sproc.tt}\n\tTmax: {sproc.TimeMax}\n\tTamanio {sproc.size}\n") 
        archivo.close()

def regresar_suspendido():
    if len(Suspendidos) > 0:
        rproc = Suspendidos.pop(0)
        rproc.suspendido = False
        Procesos.append(rproc)
        modificar_suspendidos()
    else:
        print("No hay procesos supsendidos para regresar")

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
        lbl_tm.config(text=f"TM: N/A")
    else:
        lbl_ope.config(text=f"Operacion: {proc.ope}")
        lbl_tme.config(text=f"TME: {proc.TimeMax}")
        lbl_tr.config(text=f"TR: {proc.TimeMax - proc.tt}")
        lbl_tm.config(text=f"TM: {proc.size}")
    lbl_contador.config(text=f"Contador: {Contador}")
    lbl_tt.config(text=f"TT: {proc.tt}")
    lbl_dirs.config(text=f"Marcos: {proc.dir_in} - {proc.dir_fin}")
    
    print(f"Contando... {i}")
    

def terminacion_de_proceso(proc, Lista_terminados, E_bloqueo_activado, Fin_QUANTUM, W_error_act, Proceso_Nulo_Active):
    proc.t_finalizacion = Contador
    proc.t_retorno = proc.t_finalizacion - proc.t_llegada
    proc.t_espera = max(0, proc.t_retorno - proc.tt)
    proc.t_respuesta = max(0, proc.t_comienzo - proc.t_llegada)
    
    if E_bloqueo_activado or Fin_QUANTUM and not W_error_act:
        pass #Si fue bloqueado o solo fue cambio de quantum no debe hacer nada con el proceso.
    elif not W_error_act and not Proceso_Nulo_Active: #Si temrino naturalmente
        try:
            result = eval(proc.ope)
            proc.resultado = result
            proc.terminado = True
            tree_terminados.insert("", "end", values=(proc.id, proc.ope, result))
            Lista_terminados.append(proc)
            liberar_memoria(proc)
            
        except Exception:
            result = "Error eval"
    elif Proceso_Nulo_Active or proc.id == 0:
        pass
    else: # Si fue sacado por error
        proc.resultado = "Error"
        proc.Erroru = True
        tree_terminados.insert("", "end", values=(proc.id, proc.ope, "Error"))
        Lista_terminados.append(proc)
        liberar_memoria(proc)
    
    
def mostrar_tabla_constrol_de_procesos():
    for proc in Procesos_Existentes:
            if proc.Erroru:
                tree_resultados.insert("", "end", values=(proc.id, "Error" ,"X", "Error", proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax, proc.size))
            elif not proc.terminado:
                if proc.en_memoria or proc.suspendido: # en Listo
                    llegada = proc.t_llegada 
                    temp_espera = Contador - llegada - proc.tt
                    if proc.bloqueado:
                        status = "Bloqueado"
                    if proc.suspendido:
                        status = "Suspendido"
                    else:
                        if proc.en_ejecucion:
                            status = "Ejecutando"
                        else:
                            status = "Listo"
                    if proc.respuesta_positiva:
                        temp_respuesta = proc.t_comienzo - proc.t_llegada
                    else: 
                        temp_respuesta = "--"
               
                else:  #no en memoria
                    temp_espera = temp_respuesta = llegada = "--"
                    status = "Nuevo"
                
                tree_resultados.insert("", "end", values=(proc.id, status, proc.ope, "X", llegada, "--", temp_espera, temp_respuesta, "--", proc.tt, proc.TimeMax, proc.size))
            else: #Terminado normalmemnte
                tree_resultados.insert("", "end", values=(proc.id, "Terminado", proc.ope, proc.resultado, proc.t_llegada, proc.t_finalizacion, proc.t_espera, proc.t_respuesta, proc.t_retorno, proc.tt, proc.TimeMax, proc.size))

    
def proceso_terminado(): #limpia la tabla de procesos en ejecucion
        lbl_id.config(text="ID: ")
        lbl_ope.config(text="Operacion: ")
        lbl_tme.config(text="TME: ")
        lbl_tt.config(text="TT: ")
        lbl_tr.config(text="TR: 0")
        lbl_status.config(text="Programa Terminado!", bg="cyan")
        
        mostrar_tabla_constrol_de_procesos()
        

        
# /// INTERFAZ GRAFICA ///
"""
 PRIMER FRAME PRINCIPAL (DE ROOT)
"""
frame_left = tk.Frame(root)   #formulario
frame_left.pack(side="left", fill="y", padx=10, pady=3)
# frame_left.grid(row=0, column=0)

frame_right = tk.Frame(root)  #tablas y procesos
# frame_right.grid(row=0, column=1)
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
label_datos_save.pack(pady=1)

btn_guardar_datos = tk.Button(frame_left, text="Generar proceso(s)", command=generar_datos)
btn_guardar_datos.pack(pady=3)

Guardados = tk.Text(frame_left, width=60, height=10, wrap=tk.WORD)
Guardados.pack(padx=5)


btn_comenzar_proceso = tk.Button(root, text="Comenzar Proceso", command=procesar, background="DarkSeaGreen")
btn_comenzar_proceso.pack(pady=10)

lbl_procesos_restantes = tk.Label(root, text=f"Procesos restantes: ")
lbl_procesos_restantes.pack(pady=3, padx=50)

lbl_status = tk.Label(root, text=f":")
lbl_status.pack(pady=3, padx=50)

# FRAME DE MEMORIA

frame_memoria = tk.LabelFrame(frame_left, text='Memoria', padx=5, pady=5)
frame_memoria.pack(side="left", fill="both", expand=True, padx=3, pady=2)

for r in range(25):  
    frame_memoria.grid_rowconfigure(r, weight=1)
for c in range(12):  
    frame_memoria.grid_columnconfigure(c, weight=1)

def crear_celda(parent, texto="", color="white", ancho=2):
    return tk.Label(
        parent,
        text=texto,
        bg=color,
        width=ancho,
        height=2,
        relief="solid",
        borderwidth=.5,
    )
    
crear_celda(frame_memoria, "Marco", "#e0e0e0",ancho=6).grid(row=0, column=0, sticky="nsew")
crear_celda(frame_memoria, "Marco", "#e0e0e0",ancho=6).grid(row=0, column=6, sticky="nsew")

for i in range(22):
    Elemem = []
    cx = crear_celda(frame_memoria, f"{i*2}", "#f0f0f0")
    cx.grid(row=i+1, column=0, sticky="nsew")
    Celdas_numMarcos.append(cx)
    for j in range(5):
        celda = crear_celda(frame_memoria, "")
        celda.grid(row=i+1, column=j+1, sticky="nsew")
        Elemem.append(celda)

    Memoria[i*2][1] = list(Elemem)

    Elemem = []
    cy = crear_celda(frame_memoria, f"{i*2+1}", "#f0f0f0")
    cy.grid(row=i+1, column=6, sticky="nsew")
    Celdas_numMarcos.append(cy)
    for j in range(5):
        celda = crear_celda(frame_memoria, "")
        celda.grid(row=i+1, column=j+7, sticky="nsew") 
        Elemem.append(celda)

    Memoria[i*2+1][1] = list(Elemem)

for i in range(22,24):
    crear_celda(frame_memoria, f"{i}", "#f0f0f0").grid(row=i+1, column=0, sticky="nsew")
    for j in range(5):
        celda = crear_celda(frame_memoria, "", color="#1D4928")
        celda.grid(row=i+1, column=j+1, sticky="nsew")
    
    crear_celda(frame_memoria, f"{i+24}", "#f0f0f0").grid(row=i+1, column=6, sticky="nsew")
    for j in range(5):
        celda = crear_celda(frame_memoria, "", color="#1D4928")
        celda.grid(row=i+1, column=j+7, sticky="nsew")


#Frames de procesos
"""
 SEGUNDO FRAME PRINCIPAL (DE ROOT), FRAME TABLAS
"""
frame_tablas = tk.Frame(root)
frame_tablas.pack(fill="both", expand=True, padx=5, pady=3)

frame_listos = tk.LabelFrame(frame_tablas, text="Memoria")
frame_listos.pack(side="left", fill="both", expand=True, padx=5, pady=3)

tree_listos = ttk.Treeview(frame_listos, columns=("id", "tme", "tt", "tm"), show="headings")
tree_listos.heading("id", text="ID")
tree_listos.heading("tme", text="TME")
tree_listos.heading("tt", text="TT")
tree_listos.heading("tm", text="Tamaño")

tree_listos.column("id", width=80, anchor="center")
tree_listos.column("tme", width=80, anchor="center")  
tree_listos.column("tt", width=80, anchor="center")  
tree_listos.column("tm", width=80, anchor="center")  

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
lbl_tm = tk.Label(frame_proceso, text="TM: -")
lbl_tm.pack(anchor="w")
lbl_dirs = tk.Label(frame_proceso, text="Dirs: -")
lbl_dirs.pack(anchor="w")

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
"""
 TERCER FRAME PRINCIPAL (DE ROOT), FRAME BOTTOM
"""
frame_bottom = tk.Frame(root) #frame de abajo
frame_bottom.pack(side="bottom", fill="both", expand=True, padx=3, pady=1)

frame_bloqueados = tk.LabelFrame(frame_bottom, text="Bloqueados")
frame_bloqueados.pack(side="left", fill="both", expand=True, padx=3, pady=2)

lbl_bloqueados_data = tk.Label(frame_bloqueados, text="ID   TTB")
lbl_bloqueados_data.grid(row=0, column=0, sticky="w", padx=3, pady=2)

for i in range(30):
    lbl_bloq = tk.Label(frame_bloqueados, text="")
    lbl_bloq.grid(row=i+1, column=0, sticky="w", padx=10)
    labels_bloqueados.append(lbl_bloq)


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

tree_resultados = ttk.Treeview(frame_end_proces, columns=("id","status","operacion","respuesta","t_llegada","t_final","t_espera","t_respuesta","t_retorno","t_servicio","tme", "tam"), show="headings")
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
tree_resultados.heading("tam", text="Tam")

tree_resultados.pack(fill="both", expand=True)

root.mainloop()
