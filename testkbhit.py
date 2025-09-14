import msvcrt

while True:
    if msvcrt.kbhit():  # detecta si hay una tecla presionada
        tecla = msvcrt.getch()  # obtiene la tecla
        print("Tecla presionada:", tecla.decode())

