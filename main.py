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

    app.mainloop()