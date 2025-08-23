

import tkinter as tk

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
    
    def __init__(self, name, id, ope):
        pass

    def captura_datos(self):
        self.nombre = self.capturar_nombre()
        self.id = self.captura_id()
        self.ope = self.captura_operacion()
            
    def capturar_nombre(self):
        temp_nombre = entrada_nombre.get()
        if not temp_nombre:
            print("Nombre no valido")  #cambiar por aviso en la gui
            return self.capturar_nombre()
        else: 
            return temp_nombre
        
    def captura_id(self):
        temp_id = entrada_id.get()
        try: 
            self.id = int(temp_id)
        except ValueError:
            print("ID no valido") #cambiar por aviso en la gui
            temp_id = self.captura_id()
        return temp_id
    
    def captura_operacion(self):
        pass
    

label_nombre = tk.Label(root, text="Ingresa el nombre: ")
label_nombre.pack(side="top", pady=1)
entrada_nombre = tk.Entry(root)
entrada_nombre.pack(pady=1)

label_id = tk.Label(root, text="Ingresa un ID: ")
label_id.pack(side="top", pady=1)
entrada_id = tk.Entry(root)
entrada_id.pack(pady=1)

label_operacion = tk.Label(root, text="Ingresa el nombre: ")
label_operacion.pack(side="top", pady=1)
entrada_operacion = tk.Entry(root)
entrada_operacion.pack(pady=1)

btn_guardar_datos = tk.Button(root, text="Generar Datos", command=guardar_datos)
btn_guardar_datos.pack(pady=5)






root.mainloop()
