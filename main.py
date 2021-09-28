from tkinter import *

if __name__ == '__main__':
    app = Tk()
    app.title('Proyecto2 - 201901421')
    icono = PhotoImage(file = 'Icono.png')
    app.iconphoto(True, icono)
    app.config(bg = '#08AEF5')  
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

    #Frame
    frame = Frame(app)
    frame.pack(expand = 1)
    frame.config(width = '950', height = '550')

    #Barra de Menú
    menuBar = Menu(frame)
    app.config(menu=menuBar)

    #Menú Archvio
    archivoMenu = Menu(menuBar, tearoff=0)
    archivoMenu.add_command(label='Cargar')
    archivoMenu.add_separator()
    archivoMenu.add_command(label='Salir')

    #Menú Analizar
    analisisMenu = Menu(menuBar, tearoff=0)
    analisisMenu.add_command(label='Analizar Archivo')

    #Menú Reportes
    reporteMenu = Menu(menuBar, tearoff=0)
    reporteMenu.add_command(label='Tokens')
    reporteMenu.add_command(label='Errores')
    reporteMenu.add_command(label='Árbol de Derivación')

    #Añadiendo las opciones a la barra del menú.
    menuBar.add_cascade(label='Archivo', menu=archivoMenu)
    menuBar.add_cascade(label='Análisis', menu=analisisMenu)
    menuBar.add_cascade(label='Generar Reporte', menu=reporteMenu)

    app.mainloop()