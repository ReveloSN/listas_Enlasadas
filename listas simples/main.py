import tkinter as tk
from tkinter import messagebox, ttk
# Importamos tu clase del archivo original
# (Asumiendo que tu código original se llama logic.py)
from linked_list import TaskList 

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - Linked List")
        self.root.geometry("500x550")
        
        # Instancia de tu lógica
        self.task_list = TaskList()

        # --- Componentes de la Interfaz ---
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Entradas de texto
        tk.Label(main_frame, text="Título de la Tarea:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.entry_title = tk.Entry(main_frame, width=50)
        self.entry_title.pack(pady=(0, 10))

        tk.Label(main_frame, text="Descripción:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.entry_desc = tk.Entry(main_frame, width=50)
        self.entry_desc.pack(pady=(0, 10))

        # Botones de Acción
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar Tarea", command=self.add_task, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Eliminar Seleccionada", command=self.delete_task, bg="#f44336", fg="white", width=15).grid(row=0, column=1, padx=5)

        # Lista Visual (Treeview)
        tk.Label(main_frame, text="Tareas Actuales:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(10, 0))
        
        self.tree = ttk.Treeview(main_frame, columns=("Pos", "Título", "Descripción"), show='headings', height=10)
        self.tree.heading("Pos", text="Pos")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Descripción", text="Descripción")
        
        self.tree.column("Pos", width=40, anchor="center")
        self.tree.column("Título", width=150)
        self.tree.column("Descripción", width=250)
        self.tree.pack(fill="both", expand=True, pady=10)

        # Botones de Movimiento
        move_frame = tk.Frame(main_frame)
        move_frame.pack()
        tk.Button(move_frame, text="Mover Arriba", command=lambda: self.move_task(-1)).pack(side="left", padx=5)
        tk.Button(move_frame, text="Mover Abajo", command=lambda: self.move_task(1)).pack(side="left", padx=5)

    def refresh_list(self):
        """Limpia y vuelve a llenar la tabla con los datos de la TaskList."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for index, title, desc in self.task_list.iter_tasks():
            self.tree.insert("", "end", values=(index, title, desc))

    def add_task(self):
        title = self.entry_title.get()
        desc = self.entry_desc.get()
        
        if title and desc:
            self.task_list.add_task(title, desc)
            self.entry_title.delete(0, tk.END)
            self.entry_desc.delete(0, tk.END)
            self.refresh_list()
        else:
            messagebox.showwarning("Error", "Por favor rellena ambos campos.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Selecciona una tarea de la lista.")
            return
        
        # Obtenemos la posición desde la primera columna de la fila seleccionada
        values = self.tree.item(selected_item)['values']
        pos = int(values[0])
        
        if self.task_list.delete_task(pos):
            self.refresh_list()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la tarea.")

    def move_task(self, direction):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        current_pos = int(self.tree.item(selected_item)['values'][0])
        new_pos = current_pos + direction
        
        if 0 <= new_pos < self.task_list.get_size():
            if self.task_list.move_task(current_pos, new_pos):
                self.refresh_list()
                # Re-seleccionar el item en su nueva posición
                for item in self.tree.get_children():
                    if int(self.tree.item(item)['values'][0]) == new_pos:
                        self.tree.selection_set(item)
                        break

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()