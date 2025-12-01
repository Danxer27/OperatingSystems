t1 = tk.LabelFrame(frame_memoria, text='No.Marco')
t1.grid(row=0, column=0)
t3 = tk.LabelFrame(frame_memoria, text='No.Marco')
t3.grid(row=0, column=6)

for i in range(24):
    x = tk.LabelFrame(frame_memoria, text=f'{i}')
    x.grid(row=i, column=0)
    for j in range(5):
        c = tk.LabelFrame(frame_memoria, text=f'{i}')
        c.grid(row=i, column=j+1)
        Elemem.append(c)
        
    x2 = tk.LabelFrame(frame_memoria, text=f'{i}')
    x2.grid(row=i, column=6)
    for j in range(5):
        c = tk.LabelFrame(frame_memoria, text=f'{i}')
        c.grid(row=i, column=j+6)
        Elemem.append(c)