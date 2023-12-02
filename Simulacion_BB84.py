### Importamos y usamos las librerias que necesitamos
import pandas as pd
import random
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

### Recursos de la UI
ventana = tk.Tk()
ventana.geometry("1035x500")
ventana.title("Protocolo BB84")

image1 = Image.open("Ana.png")
image1 = image1.resize((200,200))
imgAna = ImageTk.PhotoImage(image1)
labelImageAna = tk.Label(ventana, image = imgAna)

image2 = Image.open("Bob.png")
image2 = image2.resize((200,200))
imgBob = ImageTk.PhotoImage(image2)
labelImageBob = tk.Label(ventana, image = imgBob)

image3 = Image.open("Eva.png")
image3 = image3.resize((200,200))
imgEva = ImageTk.PhotoImage(image3)
labelImageEva = tk.Label(ventana, image = imgEva)

frame1 = tk.Frame(master = ventana, width = 50)
frame2 = tk.Frame(master = ventana, width = 50)
frame3 = tk.Frame(master = ventana, width = 25)
frame4 = tk.Frame(master = ventana, width = 25)
frame5 = tk.Frame(master = ventana, width = 25)
label = tk.Label(ventana, text = "Tabla de Ana")
label2 = tk.Label(ventana, text = "Tabla de Bob")
label3 = tk.Label(ventana, text = "Tabla de Llave Privada")
label4 = tk.Label(ventana, text = "Tabla de Eva")

tabla = ttk.Treeview(ventana, columns = ("Col1", "Col2"))
tabla.heading("#0", text = "Bits Ana")
tabla.heading("Col1", text = "Bases Ana")
tabla.heading("Col2", text = "Qbits Ana")
tabla.column("#0", width = 100, anchor = "center")
tabla.column("Col1", width = 100, anchor = "center")
tabla.column("Col2", width = 100, anchor = "center")

tabla2 = ttk.Treeview(ventana, columns = ("Col1"))
tabla2.heading("#0", text = "Bases Bob")
tabla2.heading("Col1", text = "Qbits Bob")
tabla2.column("#0", width = 100, anchor = "center")
tabla2.column("Col1", width = 100, anchor = "center")

tabla3 = ttk.Treeview(ventana)
tabla3.heading("#0", text = "Llave Privada")
tabla3.column("#0", width = 150, anchor = "center")

tabla4 = ttk.Treeview(ventana)
tabla4.heading("#0", text = "Bases Eva")
tabla4.column("#0", width = 150, anchor = "center")

### Declaramos las variables que vamos a usar
bases = ["C", "D"]
bits_Ana = []
bases_Ana = []
bases_Bob = []
bases_Eva = []
qubits_Ana = []
qubits_Bob = []
llave_Privada = []

### En este primer for generamos aleatoriamente los bits de Ana y las bases de Ana, Bob, y Eva
for i in range(100):
    bits_1 = random.randint(0,1)
    bases_1 = random.choice(bases)
    bases_2 = random.choice(bases)
    bases_3 = random.choice(bases)
    bits_Ana.append(bits_1)
    bases_Ana.append(bases_1)
    bases_Bob.append(bases_2)
    bases_Eva.append(bases_3)

### En este segundo for simulamos las mediciones de Ana 
# y generamos sus Qbits con las reglas del Protocolo BB84
for i in range(100):
    qubit = ""
    if bits_Ana[i] == 0 and bases_Ana[i] == "C":
        qubit = "|0>"
    elif bits_Ana[i] == 1 and bases_Ana[i] == "C":
        qubit = "|1>"
    elif bits_Ana[i] == 0 and bases_Ana[i] == "D":
        qubit = "|+>"
    elif bits_Ana[i] == 1 and bases_Ana[i] == "D":
        qubit = "|->"
    qubits_Ana.append(qubit)

### En este cuarto for simulamos las mediciones de Bob, 
# estas dependen de las bases de Bob y de las bases de Eva para generar sus Qbits
for i in range(100):
    qubit = ""
    if bases_Ana[i] == bases_Bob[i] and bases_Eva[i] != bases_Ana[i]:
        if bases_Bob[i] == "C":
            qubits = ["|0>", "|1>"]
            qubit = random.choice(qubits)
        elif bases_Bob[i] == "D":
            qubits = ["|+>", "|->"]
            qubit = random.choice(qubits)
    elif bases_Ana[i] == bases_Bob[i] and bases_Eva[i] == bases_Ana[i]:
        qubit = qubits_Ana[i]
    elif bases_Bob[i] == "C":
        qubits = ["|0>", "|1>"]
        qubit = random.choice(qubits)
    elif bases_Bob[i] == "D":
        qubits = ["|+>", "|->"]
        qubit = random.choice(qubits)
    qubits_Bob.append(qubit)

### En este quinto for simulamos la comparacion de las mediciones, aqui detectamos si Eva fue detectada o no
for i in range(100):
    llave = ""
    if bases_Ana[i] == bases_Bob[i]:
        if qubits_Ana[i] == qubits_Bob[i]:
            llave = bits_Ana[i]
        elif qubits_Ana[i] != qubits_Bob[i]:
            llave = "Eva detectada"
    elif bases_Ana[i] != bases_Bob[i]:
        llave = "Se cancela"
    llave_Privada.append(llave)

### Generamos la tabla a mostrar del Protocolo BB84
data = {
    "Bits Ana": bits_Ana,
    "Bases Ana": bases_Ana,
    "Qubits Ana": qubits_Ana,
    "Bases Eva": bases_Eva,
    "Bases Bob": bases_Bob,
    "Qubits Bob": qubits_Bob,
    "Llave Privada": llave_Privada
}

df = pd.DataFrame(data)

### Imprimimos el Protocolo BB84 completo
print(df.to_string())
print("\n")

### Aqui simulamos la deteccion de Eva y cancelamos el mensaje
for i in range(100):
    if llave_Privada[i] == "Eva detectada":
        print(df.iloc[0:i+1,0:8])
        print("Mensaje cancelado")
        break

###Procedimiento para llenar la UI
for i in range(100):
    if llave_Privada[i] != "Eva detectada":
        tabla.insert("", "end", text = bits_Ana[i], values = (bases_Ana[i], qubits_Ana[i]))
        tabla2.insert("", "end", text = bases_Bob[i], values = (qubits_Bob[i]))
        tabla3.insert("", "end", text = llave_Privada[i])
        tabla4.insert("", "end", text = bases_Eva[i])
    elif llave_Privada[i] == "Eva detectada":
        tabla.insert("", "end", text = bits_Ana[i], values = (bases_Ana[i], qubits_Ana[i]))
        tabla2.insert("", "end", text = bases_Bob[i], values = (qubits_Bob[i]))
        tabla3.insert("", "end", text = llave_Privada[i])
        tabla4.insert("", "end", text = bases_Eva[i])
        tabla3.insert("", "end", text = "Mensaje Cancelado")
        break

frame1.grid(row = 0, column = 0)

labelImageAna.grid(row = 0, column = 1)
label.grid(row = 1, column = 1)
tabla.grid(row = 2, column = 1)

frame3.grid(row = 0, column = 2)

labelImageEva.grid(row = 0, column = 3)
label4.grid(row = 1, column = 3)
tabla4.grid(row = 2, column = 3)

frame4.grid(row = 0, column = 4)

labelImageBob.grid(row = 0, column = 5)
label2.grid(row = 1, column = 5)
tabla2.grid(row = 2, column = 5)

frame5.grid(row = 0, column = 6)

label3.grid(row = 1, column = 7)
tabla3.grid(row = 2, column = 7)

frame2.grid(row = 0, column = 8)

ventana.mainloop()
