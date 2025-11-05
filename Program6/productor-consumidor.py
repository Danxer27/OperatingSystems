import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import random as rm

root = tk.Tk()
root.title("Productor - Consumidor ~ DJCE")
root.geometry("1620x780")
root.resizable(True, True)

""" AJUSTAR GRID 
    (FILAS X COLUMNAS)
    Y AJUSTAR EL NUMERO DE CONTENEDORES
    # El contenido es la cantidad de contenedores con las que se va a trabajar
    # Filas x Columnas solo es los contenedores a renderizar vizualmente
"""
FILAS = 3
COLUMNAS = 6
NUM_CONTENIDO = FILAS * COLUMNAS
VELOCIDAD_TICS = 1000   #En milisegundos

# FRAME DE LA INFO DE PROD-CONS
frame_info = ttk.Frame(root, borderwidth=5, relief="ridge", width=500, height=100)
frame_info.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

titulo_font = tkFont.Font(family="Inter", size=20, weight="bold")
estado_font = tkFont.Font(family="Inter", size=42)

ANCHO_LABEL = 20
ALTO_LABEL = 2

lbl_turno = tk.Label(frame_info, text="Turno: ", width=20, height=1, font=titulo_font)
lbl_turno.grid(row=0, column=0)

lbl_productor = tk.LabelFrame(frame_info, text="Productor", width=ANCHO_LABEL, height=ALTO_LABEL, font=titulo_font)
lbl_productor.grid(row=1, column=0)

lbl_consumidor = tk.LabelFrame(frame_info, text="Consumidor", width=ANCHO_LABEL, height=ALTO_LABEL, font=titulo_font)
lbl_consumidor.grid(row=1, column=1)

lbl_productor_estado = tk.Label(lbl_productor, text="Dormido", width=ANCHO_LABEL, height=ALTO_LABEL, font=estado_font)
lbl_productor_estado.grid(row=0, column=0, padx=10)

lbl_consumidor_estado = tk.Label(lbl_consumidor, text="Dormido", width=ANCHO_LABEL, height=ALTO_LABEL, font=estado_font)
lbl_consumidor_estado.grid(row=0, column=1, padx=10)


# FRAME DE LOS CONTENEDORES

frame_contenedores = ttk.Frame(root, borderwidth=5, relief="ridge", width=500, height=100)
frame_contenedores.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

contenedores = []
for i in range(FILAS):
    for j in range (COLUMNAS):
        x = tk.LabelFrame(frame_contenedores, text=f'C{((COLUMNAS*i) + j)+1}', width=150, height=150)
        x.grid(row=i, column=j)
        contenedores.append(x)
        
# OBJETOS DE PRODUCTOR CONSUMIDOR:
class Proceso:
    id_proc = 0
    ubicacion = -1
    
    def __init__(self, poc):
        self.id_proc = poc
    
    def dormido(self):
        if self.id_proc == 1:
            lbl_productor_estado.config(text="Dormido", background="SlateBlue")
        else:
            lbl_consumidor_estado.config(text="Dormido", background="SlateBlue")

    def intento_entrar(self):
        if self.id_proc == 1:
            lbl_productor_estado.config(text="Intenando entrar", background="yellow2")
        else:
            lbl_consumidor_estado.config(text="Intentando entrar", background="yellow2")

    def en_ejecucion(self):
        global ultimo_producido, ultimo_consumido, productos
        if self.id_proc == 1:
            self.ubicacion = ultimo_producido
            lbl_productor_estado.config(text="Trabajando", background="lawngreen")
    
            contenedores[ultimo_producido].config(background='lawngreen')
                
            ultimo_producido = (ultimo_producido + 1) % NUM_CONTENIDO
            productos += 1
            
        else:
            lbl_consumidor_estado.config(text="Trabajando", background="VioletRed")

            self.ubicacion = ultimo_consumido
            contenedores[ultimo_consumido].config(background='VioletRed')
            
            ultimo_consumido = (ultimo_consumido + 1) % NUM_CONTENIDO
            productos -= 1
            
            

# ///  PARTE MAIN DEL CODIGO  ////
Productor = Proceso(1)
Consumidor = Proceso(2)

productos = 0
ultimo_consumido = 0
ultimo_producido = 0

def ejecucion():
    """Funcion principal para ejecutar el programa
    Hace un ciclo de un segundo, donde cambia de turno"""
    global productos
    desocupa()
    num = rm.randint(1, 1000)
    if num % 2 > 0:
        turno = 1 # Productor
        lbl_turno.config(text="Turno: Productor")
    else:
        turno = 2 # Consumidor
        lbl_turno.config(text="Turno: Consumidor")
        
    if turno == 1:
        if productos < NUM_CONTENIDO: # Hay espacio
            Productor.en_ejecucion()
        else: # Buffer lleno
            Productor.intento_entrar()
        Consumidor.dormido()
    else: # Turno del Consumidor
        if productos > 0: # Hay productos
            Consumidor.en_ejecucion()
        else: # Buffer vacío
            Consumidor.intento_entrar()
        Productor.dormido()

    root.after(VELOCIDAD_TICS, ejecucion)

def desocupa():
    """Despues de que un un proceso(Productor o consumidor) 
    acabo de trabajar establece el contenido del contenedor"""
    if Productor.ubicacion != -1: 
        contenedores[Productor.ubicacion].config(background='DarkCyan') #RoyalBlue4
        Productor.ubicacion = -1
        
    if Consumidor.ubicacion != -1: 
        contenedores[Consumidor.ubicacion].config(background='silver')
        Consumidor.ubicacion = -1
        
ejecucion()

root.mainloop()
