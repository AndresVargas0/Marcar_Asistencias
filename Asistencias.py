# Librerias Usadas
import sqlite3
import datetime
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, Label
import sqlite3

# Variable de proceso Creada sin ningun valor asignado aun
proceso = None

recognizer = sr.Recognizer()

# Funcion para insertar la Asistencia
def agregar_asistencia(code,nombre):
    # Conexion a la BD
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    # Variables
    fecha = datetime.date.today()
    hora = datetime.datetime.now().time()
    # Consulta para seleccionar la Fila
    cursor.execute("SELECT * FROM asistencias WHERE id = ? AND Nombre = ? AND fecha = ?",
                   (code,nombre, fecha))
    # Obtiene la primera fila si existe
    fila = cursor.fetchone()
    #Inserta la asistencia correspondiente
    if fila:
        print("Asistencia ya registrada")
    
    else:
        # Establece el límite de tiempo para la asistencia puntual
        puntual = datetime.datetime.strptime("07:15:00", "%H:%M:%S").time()

        # Establece el límite de tiempo para la asistencia con tardanza
        tardanza = datetime.datetime.strptime("12:00:00", "%H:%M:%S").time()

        # Compara la hora actual con los límites de tiempo
        if hora <= puntual:
            asistencia = "Puntual"
            cursor.execute("INSERT INTO asistencias (id, nombre, fecha, hora, asistencia) VALUES (?, ?, ?, ?, ?)",
                       (code, nombre, fecha, hora.strftime('%H:%M:%S'), asistencia))
        elif puntual < hora <= tardanza:
            asistencia = "Tardanza"
            cursor.execute("INSERT INTO asistencias (id, nombre, fecha, hora, asistencia) VALUES (?, ?, ?, ?, ?)",
                       (code, nombre, fecha, hora.strftime('%H:%M:%S'), asistencia))
        else:
            asistencia = "No asistió"
            cursor.execute("INSERT INTO asistencias (id, nombre, fecha, hora, asistencia) VALUES (?, ?, ?, ?, ?)",
                       (code, nombre, fecha, hora.strftime('%H:%M:%S'), asistencia))

        print(f"Asistencia marcada como {asistencia}")
    #Cerrar la Conexion
    conexion.commit()
    conexion.close()

def agregar_asistencia_voz(code, nombre):
    # Conexion a la BD
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    # Variables
    nombre = nombre
    fecha = datetime.date.today()
    hora = datetime.datetime.now().time()
    # Consulta para seleccionar la Fila
    cursor.execute("SELECT * FROM asistencias WHERE id = ? AND Nombre = ? AND fecha = ?",
                   (code,nombre, fecha))
    # Obtiene la primera fila si existe
    fila = cursor.fetchone()
    if fila:
        print("Asistencia ya registrada")
    #Si llego a la Hora Marcada colocara "Puntual"
    else:
         # Establece el límite de tiempo para la asistencia puntual
        puntual = datetime.datetime.strptime("07:15:00", "%H:%M:%S").time()

        # Establece el límite de tiempo para la asistencia con tardanza
        tardanza = datetime.datetime.strptime("12:00:00", "%H:%M:%S").time()

        # Compara la hora actual con los límites de tiempo
        if hora <= puntual:
            asistencia = "Puntual"
            cursor.execute("INSERT INTO asistencias (id, nombre, fecha, hora, asistencia) VALUES (?, ?, ?, ?, ?)",
                       (code, nombre, fecha, hora.strftime('%H:%M:%S'), asistencia))
        elif puntual < hora <= tardanza:
            asistencia = "Tardanza"
            cursor.execute("INSERT INTO asistencias (id, nombre, fecha, hora, asistencia) VALUES (?, ?, ?, ?, ?)",
                       (code, nombre, fecha, hora.strftime('%H:%M:%S'), asistencia))
        else:
            asistencia = "No asistió"
            cursor.execute("INSERT INTO asistencias (id, nombre, fecha, hora, asistencia) VALUES (?, ?, ?, ?, ?)",
                       (code, nombre, fecha, hora.strftime('%H:%M:%S'), asistencia))

        print(f"Asistencia marcada como {asistencia}")
    #Cerrar la Conexion
    conexion.commit()
    conexion.close()

def eliminar_asistencias():
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM asistencias;")
    conexion.commit()
    conexion.close()

def ejecutar_comando(comando):
    if "Juan" in comando:
        code = 1001
        nombre = "Juan Rojas"
        lambda: agregar_asistencia(code, nombre)
        print("Asistencia Agregada")
    elif "José" in comando:
        code = 1002
        nombre = "Jose Paredes"
        agregar_asistencia(code, nombre)
        print("Asistencia Agregada")
    elif "Andrés" in comando:
        code = 1003
        nombre = "Andres Vargas"
        agregar_asistencia(code, nombre)
        print("Asistencia Agregada")
    elif "Gabriel" in comando:
        code = 1004
        nombre = "Gabriel Garcia"
        agregar_asistencia(code, nombre)
        print("Asistencia Agregada")
    elif "Luis" in comando:
        code = 1005
        nombre = "Luis Mendez"
        agregar_asistencia(code, nombre)
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

def actualizar_tabla_admin(tree): # Limpia la tabla y recarga los datos
    for row in tree.get_children():
        tree.delete(row)
    # Conectar a la base de datos y obtener datos de asistencias
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    cursor.execute("SELECT asistencias.*, estudiantes.carrera, estudiantes.semestre FROM asistencias CROSS JOIN estudiantes")
    datos = cursor.fetchall()

    # Carga los datos en el Treeview
    for dato in datos:
        tree.insert("", "end", values=dato)

    # Cierra la conexión con la BD
    conexion.close()

def ventana_admin():
    print("Bienvenido Admin")
    admin_id = "Admin"
    user = admin_id
    admin = tk.Tk()

    admin.title("Panel de Adminitrador")
    admin.geometry("650x350")
    admin.resizable(width=False, height=False)

    lbl_filtro = tk.Label(admin, text="Buscar")
    lbl_filtro.place(x=20,y=60)
    filtro = ttk.Entry(admin, width=32, font=("Arial",11))
    filtro.place(x=70,y=60)
    btn_filtro = ttk.Button(admin, text="Filtrar", command=lambda: filtrar(filtro))
    btn_filtro.place(x=350,y=60)
    

    lbl_name = ttk.Label(admin, text="User: " + user, font=("Arial",11))
    lbl_name.place(x=20, y=20)

    btn_eliminar_asistencias = ttk.Button(admin, text="Eliminar", command=eliminar_asistencias)
    btn_eliminar_asistencias.place(x=200,y=20)

    btn_agregar = ttk.Button(admin, text="Agregar", command=agregar_alumno)
    btn_agregar.place(x=120,y=20)

    boton_salir = ttk.Button(admin, text="Salir", command=lambda:admin.destroy())
    boton_salir.place(x=360,y=20)

    def cargar_datos(tree):
        # Conectar a la base de datos SQLite
        conexion = sqlite3.connect("database/BD.sqlite3")
        cursor = conexion.cursor()

        # Ejecutar la consulta para obtener los datos de la tabla
        cursor.execute("SELECT asistencias.*, estudiantes.carrera, estudiantes.semestre FROM asistencias JOIN estudiantes ON asistencias.id = estudiantes.id")
        datos_asistencias = cursor.fetchall()

        # Cargar datos de la tabla 'asistencias' en el Treeview
        for dato in datos_asistencias:
            tree.insert("", "end", values=dato)

        # Cerrar la conexión a la base de datos
        conexion.close()

    tree = ttk.Treeview(admin, columns=("ID", "Nombre", "Fecha", "Hora" , "Asistencia", "Carrera", "Semestre"), show="headings")

    # Configurar encabezados
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Hora", text="Hora")
    tree.heading("Asistencia", text="Asistencia")
    tree.heading("Carrera", text="Carrera")
    tree.heading("Semestre", text="Semestre")

    # Configurar columnas
    tree.column("ID", width=50)
    tree.column("Nombre", width=100)
    tree.column("Fecha", width=100)
    tree.column("Hora", width=80)
    tree.column("Asistencia", width=100)
    tree.column("Carrera", width=100)
    tree.column("Semestre", width=100)

    # Posicionar el Treeview en la ventana
    tree.place(x=10, y=100)

    # Cargar datos en el Treeview
    cargar_datos(tree)

    # Botón para Recargar Datos
    boton_recargar = ttk.Button(admin, text="Actualizar", command=lambda: cargar_datos(tree))
    boton_recargar.place(x=280, y=20)

def agregar_alumno():
    # Conecta a la base de datos
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()

    # Crear la ventana principal
    agregar = tk.Tk()
    agregar.title("Añadir Datos del Alumno")
    agregar.geometry("500x500")

    # Crear y empaquetar los widgets
    id_lbl = ttk.Label(agregar, text="ID: ")
    id_lbl.pack()
    ide = ttk.Entry(agregar, width=50)
    ide.pack()

    nombre_lbl = ttk.Label(agregar, text="Nombre: ")
    nombre_lbl.pack()
    nombre = ttk.Entry(agregar, width=50)
    nombre.pack()

    carrera_lbl = ttk.Label(agregar, text="Carrera: ")
    carrera_lbl.pack()
    opciones_carrera = ["Ing. de Software", "Diseño Grafico", "CiberSeguridad", "Mecanica Automotriz", "Diseño de Modas"]
    carrera = ttk.Combobox(agregar, values=opciones_carrera, width=47)
    carrera.pack()

    semestre_lbl = ttk.Label(agregar, text="Semestre: ")
    semestre_lbl.pack()
    semetres = ["I","II","III","IV","V","VI"]
    semestre = ttk.Combobox(agregar,values=semetres, width=50)
    semestre.pack()

    contraseña_lbl = ttk.Label(agregar, text="Contraseña: ")
    contraseña_lbl.pack()
    contra = ttk.Entry(agregar, width=50)
    contra.pack()

    def insertar_datos():
        # Obtiene los datos de las entradas
        ide_valor = ide.get()
        nombre_valor = nombre.get()
        carrera_valor = carrera.get()
        semestre_valor = semestre.get()
        contra_valor = contra.get()

        # Ejecuta la consulta de inserción
        cursor.execute("INSERT INTO estudiantes (id, nombre, carrera, semestre, contraseña) VALUES (?, ?, ?, ?, ?)",
                       (ide_valor, nombre_valor, carrera_valor, semestre_valor, contra_valor))

        # Hace commit para guardar los cambios
        conexion.commit()

        print("Alumno Agregado")
        agregar.destroy()  # Cierra la ventana después de agregar al alumno

    button_añadir = ttk.Button(agregar, text="Añadir", command=insertar_datos)
    button_añadir.pack()

    agregar.mainloop()

    # Cierra la conexión a la base de datos después de cerrar la ventana principal
    conexion.close()

def filtrar(filtro):
    box_filtro = filtro.get()
    conexion = sqlite3.connect("database/BD.sqlite3")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM asistencias WHERE nombre = ? OR id = ?", (box_filtro, box_filtro))
    
    resultados = cursor.fetchall()
    
    print("Los Datos son:")
    for fila in resultados:
        print(fila)

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
        ventana_admin()

    elif fila:
        code = ide
        nombre = fila[1]
        print("Sesion Iniciada con Exito")
        cuenta = tk.Tk()

        cuenta.title("Cuenta de @" + nombre)
        cuenta.geometry("450x320")
        cuenta.resizable(width=False, height=False)

        lbl_name = tk.Label(cuenta, text="Alumno: " + nombre)
        lbl_name.place(x=20, y=20)
        lbl_code = tk.Label(cuenta, text="ID: " + code)
        lbl_code.place(x=20, y=40)

        marcar = ttk.Button(cuenta, text="Marcar Asistencia", command=lambda:agregar_asistencia(code, nombre))
        marcar.place(x=330, y=10)

        boton_actualizar = ttk.Button(cuenta, text="Actualizar", command=lambda:actualizar_tabla(tree, ide))
        boton_actualizar.place(x=270, y=40)

        boton_salir = ttk.Button(cuenta, text="Salir", command=lambda:cuenta.destroy())
        boton_salir.place(x=358, y=40)

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

def inicio_sesion():
    root = tk.Tk()
    root.title("Programa de Asistencias")
    root.geometry("250x200")
    root.configure(bg="black")
    root.resizable(width=False, height=False)

    lbl_id = Label(root, text="Ingrese su ID:", font=("Arial",11), bg="black", fg="white")
    lbl_id.place(x=20, y=20)
    ident = ttk.Entry(root, width=25, font=("Arial",11), foreground="black")
    ident.place(x=20, y=50)

    lbl_pwd = Label(root, text="Ingrese su Contraseña:", font=("Arial",11), bg="black", fg="white")
    lbl_pwd.place(x=20, y=80)
    pwd = ttk.Entry(root, width=25, show="*", font=("Arial",11))
    pwd.place(x=20, y=110)

    boton_validar = ttk.Button(root, text="Ingresar", command=lambda: validar(ident, pwd))
    boton_validar.place(x=20, y=150)

    cancelar = ttk.Button(root, text="Salir", command=root.destroy)
    cancelar.place(x=150, y=150)

    root.mainloop()

def marcar_por_voz():
    marcar_por_voz = tk.Tk()
    marcar_por_voz.geometry("200x100")

    button = ttk.Button(marcar_por_voz, text="Registrar Asistencia", command=escuchar_comando)
    button.place(x=45,y=50)

    button_regis = ttk.Button(marcar_por_voz, text="Ingresar a tu Cuenta", command=inicio_sesion)
    button_regis.place(x=45,y=10)

    marcar_por_voz.mainloop()

marcar_por_voz()