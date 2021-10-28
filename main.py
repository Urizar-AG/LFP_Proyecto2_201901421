from tkinter import *
from tkinter import filedialog, messagebox
from os import system, startfile
from tabulate import tabulate
from analisis import automata, getReporteria, getListados, generarReporteTokens, generarReporteErrores
doc ='' #Variable que almacena 
editor = '' #El área de edición de la ventana principal.
consola = '' #Consola del programa.
existenTokens = False
existenErrores = False


def abrirFile():
    global doc
    archivo = filedialog.askopenfilename(
        title = "Seleccionar un archivo ",
        #indica el directorio donde se abre el "navegador"
        initialdir = "../",
        filetypes = (
            ("Archivos LFP", "*.lfp"),
            ("Todos los archivos", "*.*")
        )
    )
    if archivo is None or archivo == "" or archivo == '':
        #En caso no se seleccione ningún archivo
        messagebox.showinfo(message="No se cargo ningún archivo.", title="Carga de Archivo")
        doc = None
    else:
        f = open(archivo, mode = "r", encoding = "UTF-8")
        contenido = f.read()
        f.close()
        doc = contenido
        global editor
        #Borra el contenido que ya tiene
        editor.delete(1.0, END)
        messagebox.showinfo(message="El archivo se cargó correctamente.", title="Carga de Archivo")  
        #Agrega el cotenido del archivo nuevo.
        editor.insert(1.0, doc)

#El contenido del editor lo manda al autómata
def getCodigo():
    global editor
    global existenTokens
    global existenErrores
    global consola

    consola.config(state='normal')
    consola.delete(1.0, END)
    doc = editor.get(1.0, END)
    if len(doc)>0 and doc != '' and doc != '\n' and doc != '\t' and doc is not None:
        resultado = automata(doc)
        if resultado == True:
            existenTokens = True
            existenErrores = False
            messagebox.showinfo(message='Análisis exitoso', title='Analizar Archivo')
            mostrarEnConsola()
        else:
            existenTokens = True
            existenErrores = True
            messagebox.showwarning(message='Se encontraron algunos errores, corrige el archivo de entrada.', title='Analizar Archivo')
            #mostrarEnConsola()
    else:
        messagebox.showwarning(message='No hay datos para analizar', title='Analizar Archivo')

def mostrarEnConsola():
    global consola
    consola.config(state='normal')#Se habilita la edición para poder editar y borrar el contenido que ya tiene.
    consola.delete(1.0, END)
    
    lista = getReporteria()
    for elemento in lista:
        if elemento[0] == '01':
            consola.insert(END, str(elemento[1]))
        elif elemento[0] == '02':
            consola.insert(END, str(elemento[1]))
            consola.insert(END,'\n')
        elif elemento[0] == '03':
            consola.insert(END, str(elemento[1]))
            consola.insert(END,'\n')
        elif elemento[0] == '04':
            consola.insert(END, str(elemento[1]))
            consola.insert(END,'\n')
        elif elemento[0] == '05':
            consola.insert(END, str(elemento[1]))
            consola.insert(END,'\n')
        elif elemento[0] == '06':
            lista1, lista2 = getListados()
            consola.insert(END,'\n')
            consola.insert(END,tabulate(lista2, headers = lista1))
            consola.insert(END,'\n')
        elif elemento[0] == '07':
            consola.insert(END, str(elemento[1]))
            consola.insert(END,'\n')
        elif elemento[0] == '08':
            consola.insert(END, str(elemento[1]))
            consola.insert(END,'\n')  
        elif elemento[0] == '09':
            consola.insert(END, str(elemento[1]))
            consola.insert(END,'\n')
        elif elemento[0] == '10':
            consola.insert(END, str(elemento[1]))
            consola.insert(END, '\n')
            startfile('Reportes\\ReporteDatos.html')         

    consola.config(state="disabled")#Se deshabilita la escritura de la consola y queda como solo lectura.

def getReporteTokens():
    global existenTokens
    if existenTokens == True:
        generarReporteTokens()
        messagebox.showinfo(message='Reporte de Tokens generado exitosamente.', title='Reporte Tokens')
        startfile('Reportes\\ReporteTokens.html')
    else:
        messagebox.showerror(message='No hay datos que reportar', title='Reporte Tokens')

def getReporteErrores():
    global existenErrores
    if existenErrores == True:
        generarReporteErrores()
        messagebox.showinfo(message='Reporte de Errores generado exitosamente', title='Reporte Errores')
        startfile('Reportes\\ReporteErrores.html')
    else:
        messagebox.showerror(message='No hay errores que reportar', title='Reporte Errores')

def limpiarEditor():
    global editor
    #editor.config(state='normal')
    editor.delete(1.0, END)

def limpiarConsola():
    global consola
    consola.config(state = 'normal')
    consola.delete(1.0, END)
    consola.config(state = 'disabled')

def salir():
    respuesta = messagebox.askyesno(message="¿Está seguro de cerrar el programa?", title="Salir")
    if respuesta == YES:
        app.destroy()
    else:
        pass

if __name__ == '__main__':

    app = Tk()
    app.title('Proyecto2 - 201901421')
    icono = PhotoImage(file ='Icono.png')
    app.iconphoto(True, icono)  
    app.resizable(0,0)
    w = 1000 #Ancho de la ventana
    h = 600 #Alto de la ventana
    app.update_idletasks()#Geometría precisa
    # winfo_rootx() y winfo_rooty() -> Coordenana de la ventana sin el marco exterior.
    # winfo_x() y winfo_y() -> Coordenada del marco exterior de la ventana.    
    fw = app.winfo_rootx() - app.winfo_x() #Ancho del marco de la ventana.
    vw = w + 2 * fw #Ancho de la ventana + los marcos.
    th = app.winfo_rooty() - app.winfo_y() #Alto de la barrra de titulo de la ventana.
    vh = h + th + fw 
    x = app.winfo_screenwidth() // 2 - vw // 2
    y = app.winfo_screenheight() // 2 - vh // 2
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    app.deiconify()

#------------------------------------------------------------------- Barra de Menú ----------------------------------------------------------
    menuBar = Menu(app, bg='#333A3B')
    app.config(menu=menuBar)

    #Menú Archvio
    archivoMenu = Menu(menuBar, tearoff=0, bg='#333A3B', fg='#FFFFFF')
    archivoMenu.add_command(label='Abrir', command=lambda:abrirFile())
    archivoMenu.add_command(label='Limpiar editor', command=lambda: limpiarEditor())
    archivoMenu.add_command(label='Limpiar consola', command=lambda: limpiarConsola())
    archivoMenu.add_separator()
    archivoMenu.add_command(label='Salir', command=lambda:salir())

    #Menú Analizar
    analisisMenu = Menu(menuBar, tearoff=0, bg='#333A3B', fg='#FFFFFF')
    analisisMenu.add_command(label='Analizar Archivo', command=lambda:getCodigo())

    #Menú Reportes
    reporteMenu = Menu(menuBar, tearoff=0, bg='#333A3B', fg='#FFFFFF')
    reporteMenu.add_command(label='Tokens', command=lambda:getReporteTokens())
    reporteMenu.add_command(label='Errores', command=lambda:getReporteErrores())
    reporteMenu.add_command(label='Árbol de Derivación')

    #Añadiendo las opciones a la barra del menú.
    menuBar.add_cascade(label='Archivo', menu=archivoMenu)
    menuBar.add_cascade(label='Análisis', menu=analisisMenu)
    menuBar.add_cascade(label='Generar Reporte', menu=reporteMenu)

#------------------------------------------------------------------------ Frame -----------------------------------------------------------
    #Frame Principal
    frame = Frame(app)
    frame.config(bg='#333A3B', padx=25)
    frame.pack(fill='both', expand = True)
    frame.pack_propagate(False)#Para que no se adapte al tamaño de los hijos.

    #Frames Contenedores
    frame1 = Frame(frame, width=460, height=550)
    frame2 = Frame(frame, width=460, height=550)
    frame1.pack_propagate(False)
    frame2.pack_propagate(False)
    frame1.pack(side = LEFT)
    frame2.pack(side = RIGHT)

    #Área de edición
    seccion1 = Label(frame1, text='EDITOR')
    seccion1.pack()
    #global editor
    editor = Text(frame1, width=50, height=30)
    editor.config(padx=10, pady=10, bd=0, bg='#000000', fg='#FFFFFF', selectbackground="#333A3B", insertbackground="#FFFFFF", font=("Consolas", 12))
    editor.pack_propagate(False)
    editor.pack()

    #Consola
    seccion2 = Label(frame2, text='CONSOLA')
    seccion2.pack()
    consola = Text(frame2, width=50, height=30)
    consola.config(state='disabled', padx=10, pady=10, bd=0, bg='#000000', fg ='#08AEF5', selectbackground="#333A3B", font=("Consolas", 12))
    #consola.config(padx=10, pady=10, bd=0, bg='#000000', fg ='#08AEF5', selectbackground="#333A3B", font=("Consolas", 12))
    consola.pack_propagate(False)
    consola.pack()

    app.mainloop()