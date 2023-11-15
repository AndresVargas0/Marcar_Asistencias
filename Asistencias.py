# Librerias Usadas
import sqlite3
import datetime
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, Label, PhotoImage
import sqlite3

# Variable de proceso Creada sin ningun valor asignado aun
proceso = None

# Funcion para insertar la Asistencia
def agregar_asistencia(code, nombre, fecha, hora, asistencia):
    # Conexion a la BD
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    # Variable para sacar la hora actual
    hora_str = hora.strftime('%H:%M:%S')
    # Consulta para seleccionar la Fila
    cursor.execute("SELECT id, asistencia FROM asistencias WHERE nombre = ? AND fecha = ? AND hora = ?",
                   (nombre, fecha, hora_str))
    
    row = cursor.fetchone()
    if row:
        asistencia_actual = row[4]
        nueva_asistencia = asistencia_actual + 1

        cursor.execute("UPDATE asistencias SET asistencia = ? WHERE id = ?",
                       (nueva_asistencia, row[4]))
    else:
        asistencia = 1
        cursor.execute("INSERT INTO asistencias (id, nombre, fecha, hora, asistencia) VALUES (?, ?, ?, ?, ?)",
                       (code, nombre, fecha, hora_str, asistencia))
        
    conexion.commit()
    conexion.close()

def eliminar_asistencias():
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM asistencias;")
    conexion.commit()
    conexion.close()

recognizer = sr.Recognizer()

def ejecutar_comando(comando):
    if "marcar asistencia de Juan" in comando:
        code = 1001
        nombre = "Juan Rojas"
        fecha = datetime.date.today()
        hora = datetime.datetime.now().time()
        asistencia = 1 
        agregar_asistencia(code, nombre, fecha, hora, asistencia)
        print("Asistencia Agregada")
    elif "marcar asistencia de José" in comando:
        code = 1002
        nombre = "Jose Paredes"
        fecha = datetime.date.today()
        hora = datetime.datetime.now().time()
        asistencia = 1
        agregar_asistencia(code, nombre, fecha, hora, asistencia)
        print("Asistencia Agregada")
    elif "marcar asistencia de Andrés" in comando:
        code = 1003
        nombre = "Andres Vargas"
        fecha = datetime.date.today()
        hora = datetime.datetime.now().time()
        asistencia = 1
        agregar_asistencia(code, nombre, fecha, hora, asistencia)
        print("Asistencia Agregada")
    elif "marcar asistencia de Miguel" in comando:
        code = 1004
        nombre = "Miguel"
        fecha = datetime.date.today()
        hora = datetime.datetime.now().time()
        asistencia = 1 
        agregar_asistencia(code, nombre, fecha, hora, asistencia)
        print("Asistencia Agregada")
    elif "marcar asistencia de Jose" in comando:
        code = 1005
        nombre = "Jose"
        fecha = datetime.date.today()
        hora = datetime.datetime.now().time()
        asistencia = 1 
        agregar_asistencia(code, nombre, fecha, hora, asistencia)
        print("Asistencia Agregada")
    elif "eliminar asistencias" in comando:
        eliminar_asistencias()
        print("Asistencias Eliminadas")
    elif "cierra el programa" in comando:
        proceso.terminate()

def escuchar_comando():
    with sr.Microphone() as source:
        print("En qué te puedo ayudar...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        comando = recognizer.recognize_google(audio, language="es-ES")
        print(f"Comando Reconocido: {comando}")
        ejecutar_comando(comando)
    except sr.UnknownValueError:
        print("No se pudo entender el Comando")
    except sr.RequestError as e:
        print(f"Error al realizar la solicitud {e}")

# cursor.execute("CREATE TABLE estudiantes (id INTEGER PRIMARY KEY, nombre TEXT, contraseña VARCHAR(4,10))")

def actualizar_tabla(tree, ide): # Limpia la tabla y recarga los datos
    for row in tree.get_children():
        tree.delete(row)

    # Conectar a la base de datos y obtener datos de asistencias
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM asistencias WHERE id = ?", (ide,))
    datos = cursor.fetchall()

    # Carga los datos en el Treeview
    for dato in datos:
        tree.insert("", "end", values=dato)

    # Cierra la conexión con la BD
    conexion.close()

def validar(ident, pwd):
    ide = ident.get()
    contra = pwd.get()
    admin_id = "Admin"
    admin_pwd = "admin"

    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM estudiantes WHERE id = ? AND contraseña = ?", (ide, contra))

    fila = cursor.fetchone()
    conexion.close()

    if ide == admin_id and contra == admin_pwd:
        print("Bienvenido Admin")
        root.destroy()
        user = admin_id
        admin = tk.Tk()

        admin.title("Panel de Adminitrador")
        admin.geometry("400x400")

        lbl_name = ttk.Label(admin, text="User: " + user)
        lbl_name.place(x=20, y=20)

        boton_salir = ttk.Button(admin, text="Salir", command=lambda:admin.destroy())
        boton_salir.place(x=300, y=20)
    elif fila:
        root.destroy()
        code = ide
        nombre = fila[1]
        print("Sesion Iniciada con Exito")
        cuenta = tk.Tk()

        cuenta.title("Cuenta de @" + nombre)
        cuenta.geometry("450x300")

        lbl_name = tk.Label(cuenta, text="Alumno: " + nombre)
        lbl_name.place(x=20, y=20)
        lbl_code = tk.Label(cuenta, text="ID: " + code)
        lbl_code.place(x=20, y=40)

        marcar = tk.Button(cuenta, text="Marcar Asistencia", command=escuchar_comando)
        marcar.place(x=300, y=10)

        boton_actualizar = tk.Button(cuenta, text="Actualizar", command=lambda:actualizar_tabla(tree, ide))
        boton_actualizar.place(x=300, y=40)

        boton_salir = tk.Button(cuenta, text="Salir", command=lambda:cuenta.destroy())
        boton_salir.place(x=370, y=40)

        tree = ttk.Treeview(cuenta, columns=("ID", "Nombre", "Fecha", "Hora", "Asistencia"), show="headings")

        # Configurar encabezados
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")
        tree.heading("Asistencia", text="Asistencia")

        # Configurar columnas
        tree.column("ID", width=50)
        tree.column("Nombre", width=100)
        tree.column("Fecha", width=100)
        tree.column("Hora", width=80)
        tree.column("Asistencia", width=100)

        # Conectar a la base de datos y obtener datos de asistencias
        conexion = sqlite3.connect("database/BD.sqlite3")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM asistencias WHERE id = ?", (ide,))
        datos = cursor.fetchall()

        # Cargar datos en el Treeview
        for dato in datos:
            tree.insert("", "end", values=dato)

        # Colocar el Treeview en la ventana
        tree.place(x=10, y=80)

        # Cerrar la conexión a la base de datos
        conexion.close()
        cuenta.mainloop()
    else:
        print('''Credenciales Incorrectas,
              Intentelo Nuevamente''')

root = tk.Tk()
root.title("Programa de Asistencias")
root.geometry("250x200")

lbl_id = Label(root, text="Ingrese su ID:", font=("Arial",11))
lbl_id.place(x=20, y=20)
ident = ttk.Entry(root, width=25, font=("Arial",11))
ident.place(x=20, y=50)

lbl_pwd = Label(root, text="Ingrese su Contraseña:", font=("Arial",11))
lbl_pwd.place(x=20, y=80)
pwd = ttk.Entry(root, width=25, show="*", font=("Arial",11))
pwd.place(x=20, y=110)

boton_validar = ttk.Button(root, text="Ingresar", command=lambda: validar(ident, pwd))
boton_validar.configure(padding=(10, 5))
boton_validar.place(x=20, y=150)

root.mainloop()

# import tkinter as tk
# from tkinter import ttk
# import sqlite3

# def cargar_datos(tree):
#     # Conectar a la base de datos SQLite
#     conexion = sqlite3.connect("database/BD.sqlite3")
#     cursor = conexion.cursor()

#     # Ejecutar la consulta para obtener los datos de la tabla
#     cursor.execute("SELECT * FROM asistencias")
#     datos = cursor.fetchall()

#     # Limpiar la tabla antes de cargar nuevos datos
#     for row in tree.get_children():
#         tree.delete(row)

#     # Cargar datos en la tabla
#     for dato in datos:
#         tree.insert("", "end", values=dato)

#     # Cerrar la conexión a la base de datos
#     conexion.close()

# # Crear la ventana principal
# ventana = tk.Tk()
# ventana.title("Tabla de Datos")

# # Crear el widget Treeview
# tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Fecha", "Hora" , "Asistencia"), show="headings")

# # Configurar encabezados
# tree.heading("ID", text="ID")
# tree.heading("Nombre", text="Nombre")
# tree.heading("Fecha", text="Fecha")
# tree.heading("Hora", text="Hora")
# tree.heading("Asistencia", text="Asistencia")

# # Configurar columnas
# tree.column("ID", width=30)
# tree.column("Nombre", width=100)
# tree.column("Fecha", width=100)
# tree.column("Hora", width=80)
# tree.column("Asistencia", width=100)

# # Cargar datos iniciales
# cargar_datos(tree)

# # Crear un botón para recargar datos
# boton_recargar = tk.Button(ventana, text="Recargar Datos", command=lambda: cargar_datos(tree))

# # Colocar widgets en la ventana
# tree.pack(pady=10)
# boton_recargar.pack(pady=10)

# # Iniciar el bucle principal
# ventana.mainloop()