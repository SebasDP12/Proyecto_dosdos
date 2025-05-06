import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pygame
import os


class NodoCancion:
    def __init__(self, nombre, artista, duracion, ruta):
        self.nombre = nombre
        self.artista = artista
        self.duracion = duracion
        self.ruta = ruta
        self.siguiente = None
        self.anterior = None


class ListaReproduccion:
    def __init__(self):
        self.head = None
        self.current = None  

    def agregar_cancion(self, nodo):
        if self.head is None:
        
            self.head = nodo
            nodo.siguiente = nodo
            nodo.anterior = nodo
            self.current = nodo
        else:
           
            tail = self.head.anterior  
            tail.siguiente = nodo
            nodo.anterior = tail
            nodo.siguiente = self.head
            self.head.anterior = nodo

    def eliminar_cancion(self, nombre):
        if self.head is None:
            return False
        actual = self.head
        encontrado = False
        
        while True:
            if actual.nombre == nombre:
                encontrado = True
                break
            actual = actual.siguiente
            if actual == self.head:
                break
        if not encontrado:
            return False
    
        if actual.siguiente == actual:
            self.head = None
            self.current = None
        else:
            actual.anterior.siguiente = actual.siguiente
            actual.siguiente.anterior = actual.anterior
            
            if actual == self.head:
                self.head = actual.siguiente
            if actual == self.current:
                self.current = actual.siguiente
        return True

    def mostrar_playlist(self):
        canciones = []
        if self.head is None:
            return canciones
        actual = self.head
        i = 1
        while True:
            canciones.append(f"{i}. {actual.nombre} - {actual.artista} ({actual.duracion})")
            actual = actual.siguiente
            i += 1
            if actual == self.head:
                break
        return canciones

    def siguiente_cancion(self):
        if self.current is not None:
            self.current = self.current.siguiente
        return self.current

    def anterior_cancion(self):
        if self.current is not None:
            self.current = self.current.anterior
        return self.current


def reproducir_cancion(cancion):
    try:
        pygame.mixer.music.load(cancion.ruta)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reproducir la canción: {e}")

def pausar_cancion():
    pygame.mixer.music.pause()

def reanudar_cancion():
    pygame.mixer.music.unpause()

def detener_cancion():
    pygame.mixer.music.stop()


pygame.init()
pygame.mixer.init()


class MusicPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Música")
        self.lista_reproduccion = ListaReproduccion()

        
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        
        self.btn_cargar = tk.Button(root, text="Cargar Canción", command=self.cargar_cancion)
        self.btn_cargar.pack(pady=5)

       
        self.btn_reproducir = tk.Button(root, text="Reproducir", command=self.reproducir)
        self.btn_reproducir.pack(pady=5)

        self.btn_pausar = tk.Button(root, text="Pausar", command=pausar_cancion)
        self.btn_pausar.pack(pady=5)

        self.btn_reanudar = tk.Button(root, text="Reanudar", command=reanudar_cancion)
        self.btn_reanudar.pack(pady=5)

        self.btn_detener = tk.Button(root, text="Detener", command=detener_cancion)
        self.btn_detener.pack(pady=5)

        self.btn_siguiente = tk.Button(root, text="Siguiente", command=self.siguiente)
        self.btn_siguiente.pack(pady=5)

        self.btn_anterior = tk.Button(root, text="Anterior", command=self.anterior)
        self.btn_anterior.pack(pady=5)

    
        self.btn_eliminar = tk.Button(root, text="Eliminar Canción", command=self.eliminar)
        self.btn_eliminar.pack(pady=5)

    def cargar_cancion(self):
     
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.mp3;*.wav")])
        if ruta:
            # Pedir información adicional sobre la canción
            nombre = simpledialog.askstring("Nombre de la Canción", "Ingrese el nombre de la canción:")
            if not nombre:
                nombre = os.path.basename(ruta)
            artista = simpledialog.askstring("Artista", "Ingrese el nombre del artista:")
            if not artista:
                artista = "Desconocido"
            duracion = simpledialog.askstring("Duración", "Ingrese la duración de la canción:")
            if not duracion:
                duracion = "Desconocido"

            nodo = NodoCancion(nombre, artista, duracion, ruta)
            self.lista_reproduccion.agregar_cancion(nodo)
            self.actualizar_lista()

    def actualizar_lista(self):
        self.listbox.delete(0, tk.END)
        canciones = self.lista_reproduccion.mostrar_playlist()
        for cancion in canciones:
            self.listbox.insert(tk.END, cancion)

    def reproducir(self):
        if self.lista_reproduccion.current is None:
            messagebox.showinfo("Información", "No hay canciones en la lista.")
        else:
            reproducir_cancion(self.lista_reproduccion.current)
            self.resaltar_cancion()

    def siguiente(self):
        if self.lista_reproduccion.current is not None:
            detener_cancion()
            self.lista_reproduccion.siguiente_cancion()
            reproducir_cancion(self.lista_reproduccion.current)
            self.resaltar_cancion()

    def anterior(self):
        if self.lista_reproduccion.current is not None:
            detener_cancion()
            self.lista_reproduccion.anterior_cancion()
            reproducir_cancion(self.lista_reproduccion.current)
            self.resaltar_cancion()

    def eliminar(self):
        
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una canción para eliminar.")
            return
        indice = seleccion[0]
        canciones = self.lista_reproduccion.mostrar_playlist()
        
        nombre = canciones[indice].split(". ", 1)[1].split(" - ")[0]
        eliminado = self.lista_reproduccion.eliminar_cancion(nombre)
        if eliminado:
            messagebox.showinfo("Información", "Canción eliminada.")
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la canción.")

    def resaltar_cancion(self):
      
        canciones = self.lista_reproduccion.mostrar_playlist()
        if self.lista_reproduccion.current is not None:
            actual_nombre = self.lista_reproduccion.current.nombre
            for i, cancion in enumerate(canciones):
                if actual_nombre in cancion:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(i)
                    self.listbox.activate(i)
                    break


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerGUI(root)
    root.mainloop()
