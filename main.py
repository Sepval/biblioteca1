import tkinter as tk
from tkinter import messagebox
import datetime
from sqlalchemy import func
from models import Autor, Libro, Usuario, Prestamo, Session

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.session = Session()
        self.menu_principal()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def menu_principal(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Gestión Biblioteca", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Ver autores con libros", command=self.ver_autores_con_libros).pack(pady=5)
        tk.Button(self.root, text="Autores", command=self.menu_autores).pack(pady=5)
        tk.Button(self.root, text="Libros", command=self.menu_libros).pack(pady=5)
        tk.Button(self.root, text="Usuarios", command=self.menu_usuarios).pack(pady=5)
        tk.Button(self.root, text="Préstamos", command=self.menu_prestamos).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=5)

    def menu_autores(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Autores", font=("Arial", 14)).pack(pady=10)
        
        # Frame para agregar autores
        frame_agregar = tk.Frame(self.root)
        frame_agregar.pack(pady=5)
        
        entry = tk.Entry(frame_agregar)
        entry.pack(side=tk.LEFT, padx=5)
        
        def agregar_autor():
            nombre = entry.get()
            if nombre:
                nuevo = Autor(nombre=nombre)
                self.session.add(nuevo)
                self.session.commit()
                messagebox.showinfo("OK", "Autor guardado.")
                self.menu_autores()

        tk.Button(frame_agregar, text="Añadir Autor", command=agregar_autor).pack(side=tk.LEFT, padx=5)
        
        # Lista de autores con botón de eliminar
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10)
        
        lista = tk.Listbox(frame_lista, width=40, height=10)
        lista.pack(side=tk.LEFT, padx=5)
        
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical")
        scrollbar.config(command=lista.yview)
        scrollbar.pack(side=tk.LEFT, fill="y")
        
        lista.config(yscrollcommand=scrollbar.set)
        
        for a in self.session.query(Autor).all():
            lista.insert(tk.END, f"{a.id} - {a.nombre}")
            
        def eliminar_autor():
            seleccion = lista.curselection()
            if seleccion:
                autor_id = int(lista.get(seleccion).split(" - ")[0])
                autor = self.session.get(Autor, autor_id)
                if autor:
                    # Verificar si el autor tiene libros asociados
                    if len(autor.libros) > 0:
                        messagebox.showerror("Error", "No se puede eliminar un autor que tiene libros asociados.")
                    else:
                        self.session.delete(autor)
                        self.session.commit()
                        messagebox.showinfo("OK", "Autor eliminado.")
                        self.menu_autores()
        
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=5)
        
        tk.Button(frame_botones, text="Eliminar Autor", command=eliminar_autor).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Volver", command=self.menu_principal).pack(side=tk.LEFT, padx=5)

    def menu_libros(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Libros", font=("Arial", 14)).pack(pady=10)

        # Frame para agregar libros
        frame_agregar = tk.Frame(self.root)
        frame_agregar.pack(pady=5)
        
        tk.Label(frame_agregar, text="Título:").pack()
        entry_titulo = tk.Entry(frame_agregar)
        entry_titulo.pack()
        
        tk.Label(frame_agregar, text="Autor ID:").pack()
        entry_autor_id = tk.Entry(frame_agregar)
        entry_autor_id.pack()

        def agregar_libro():
            titulo = entry_titulo.get()
            autor_id = entry_autor_id.get()
            if titulo and autor_id.isdigit():
                autor = self.session.get(Autor, int(autor_id))
                if autor:
                    libro = Libro(titulo=titulo, autor_id=int(autor_id))
                    self.session.add(libro)
                    self.session.commit()
                    messagebox.showinfo("OK", "Libro guardado.")
                    self.menu_libros()
                else:
                    messagebox.showerror("Error", "ID de autor no válido.")

        tk.Button(frame_agregar, text="Añadir Libro", command=agregar_libro).pack(pady=5)
        
        # Lista de libros con botón de eliminar
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10)
        
        lista = tk.Listbox(frame_lista, width=60, height=10)
        lista.pack(side=tk.LEFT, padx=5)
        
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical")
        scrollbar.config(command=lista.yview)
        scrollbar.pack(side=tk.LEFT, fill="y")
        
        lista.config(yscrollcommand=scrollbar.set)
        
        for l in self.session.query(Libro).all():
            autor = self.session.get(Autor, l.autor_id)
            estado = " (Prestado)" if l.prestado else ""
            lista.insert(tk.END, f"{l.id} - {l.titulo} ({autor.nombre}){estado}")
            
        def eliminar_libro():
            seleccion = lista.curselection()
            if seleccion:
                libro_id = int(lista.get(seleccion).split(" - ")[0])
                libro = self.session.get(Libro, libro_id)
                if libro:
                    if libro.prestado:
                        messagebox.showerror("Error", "No se puede eliminar un libro que está prestado.")
                    else:
                        self.session.delete(libro)
                        self.session.commit()
                        messagebox.showinfo("OK", "Libro eliminado.")
                        self.menu_libros()
        
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=5)
        
        tk.Button(frame_botones, text="Eliminar Libro", command=eliminar_libro).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Volver", command=self.menu_principal).pack(side=tk.LEFT, padx=5)

    def menu_usuarios(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Usuarios", font=("Arial", 14)).pack(pady=10)
        entry = tk.Entry(self.root)
        entry.pack()

        def agregar_usuario():
            nombre = entry.get()
            if nombre:
                usuario = Usuario(nombre=nombre)
                self.session.add(usuario)
                self.session.commit()
                messagebox.showinfo("OK", "Usuario añadido.")
                self.menu_usuarios()

        tk.Button(self.root, text="Añadir Usuario", command=agregar_usuario).pack()
        tk.Button(self.root, text="Volver", command=self.menu_principal).pack(pady=10)

        lista = tk.Listbox(self.root)
        for u in self.session.query(Usuario).all():
            lista.insert(tk.END, f"{u.id} - {u.nombre}")
        lista.pack()

    def menu_prestamos(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Gestión de Préstamos", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="ID Libro:").pack()
        entry_libro = tk.Entry(self.root)
        entry_libro.pack()
        tk.Label(self.root, text="ID Usuario:").pack()
        entry_usuario = tk.Entry(self.root)
        entry_usuario.pack()

        def prestar():
            libro_id = entry_libro.get()
            usuario_id = entry_usuario.get()
            if libro_id.isdigit() and usuario_id.isdigit():
                libro = self.session.get(Libro, int(libro_id))
                usuario = self.session.get(Usuario, int(usuario_id))
                if libro and usuario and libro.prestado == 0:
                    prestamo = Prestamo(libro_id=libro.id, usuario_id=usuario.id)
                    libro.prestado = 1
                    self.session.add(prestamo)
                    self.session.commit()
                    messagebox.showinfo("Éxito", "Préstamo registrado.")
                    self.menu_prestamos()
                else:
                    messagebox.showerror("Error", "Libro no disponible o datos inválidos.")

        tk.Button(self.root, text="Registrar préstamo", command=prestar).pack(pady=5)

        def devolver():
            seleccion = lista.curselection()
            if seleccion:
                prestamo_id = int(lista.get(seleccion).split(" - ")[0])
                prestamo = self.session.get(Prestamo, prestamo_id)
                if prestamo and not prestamo.fecha_devolucion:
                    prestamo.fecha_devolucion = datetime.date.today()
                    prestamo.libro.prestado = 0
                    self.session.commit()
                    messagebox.showinfo("OK", "Libro devuelto.")
                    self.menu_prestamos()
                else:
                    messagebox.showerror("Error", "Ya devuelto o no válido.")

        tk.Button(self.root, text="Marcar como devuelto", command=devolver).pack()
        tk.Button(self.root, text="Volver", command=self.menu_principal).pack(pady=10)

        lista = tk.Listbox(self.root, width=70)
        prestamos = self.session.query(Prestamo).filter_by(fecha_devolucion=None).all()
        for p in prestamos:
            lista.insert(tk.END, f"{p.id} - {p.libro.titulo} a {p.usuario.nombre} el {p.fecha_prestamo}")
        lista.pack()

    def ver_autores_con_libros(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Autores con sus libros", font=("Arial", 14)).pack(pady=10)
        autores = self.session.query(Autor).all()
        texto = ""
        for autor in autores:
            total = len(autor.libros)
            texto += f"{autor.nombre} ({total} libro(s)):\n"
            for libro in autor.libros:
                estado = " (Prestado)" if libro.prestado else ""
                texto += f"  - {libro.titulo}{estado}\n"
            texto += "\n"
        text_widget = tk.Text(self.root, width=60, height=25)
        text_widget.insert(tk.END, texto)
        text_widget.config(state="disabled")
        text_widget.pack()
        tk.Button(self.root, text="Volver", command=self.menu_principal).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()