
import pandas as pd
import random
import string
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class RegistroArticulos:
    def __init__(self, archivo='registro.xlsx'):
        self.archivo = archivo
        self.codigos_usados = set()
        self.cargar_datos()
    
    def cargar_datos(self):
        if os.path.exists(self.archivo):
            try:
                self.df = pd.read_excel(self.archivo)
                self.codigos_usados = set(self.df['Codigo'].tolist())
            except PermissionError:
                raise PermissionError(
                    f"El archivo '{self.archivo}' está abierto en otro programa.\n"
                    "Por favor ciérralo y vuelve a intentar."
                )
        else:
            self.df = pd.DataFrame(columns=[
                'Codigo', 'Tipo', 'Articulo', 'Persona', 'Fecha', 
                'Estado', 'Notas'
            ])
    
    def generar_codigo(self):
        while True:
            codigo = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8
            ))
            if codigo not in self.codigos_usados:
                self.codigos_usados.add(codigo)
                return codigo
    
    def agregar_registro(self, tipo, articulo, persona, fecha, estado, notas=''):
        codigo = self.generar_codigo()
        
        nuevo_registro = {
            'Codigo': codigo,
            'Tipo': tipo,
            'Articulo': articulo,
            'Persona': persona,
            'Fecha': fecha,
            'Estado': estado,
            'Notas': notas
        }
        
        self.df = pd.concat([self.df, pd.DataFrame([nuevo_registro])], 
                           ignore_index=True)
        self.guardar()
        return codigo
    
    def cambiar_estado(self, codigo, nuevo_estado):
        indice = self.df[self.df['Codigo'] == codigo].index
        if len(indice) == 0:
            return False
        
        self.df.loc[indice, 'Estado'] = nuevo_estado
        self.guardar()
        return True
    
    def eliminar(self, codigo):
        indice = self.df[self.df['Codigo'] == codigo].index
        if len(indice) == 0:
            return False
        
        self.df = self.df.drop(indice)
        self.codigos_usados.discard(codigo)
        self.guardar()
        return True
    
    def buscar(self, codigo):
        resultado = self.df[self.df['Codigo'] == codigo]
        if len(resultado) == 0:
            return None
        return resultado
    
    def obtener_todos(self):
        return self.df
    
    def filtrar_por_estado(self, estado):
        return self.df[self.df['Estado'] == estado]
    
    def filtrar_por_tipo(self, tipo):
        return self.df[self.df['Tipo'] == tipo]
    
    def guardar(self):
        try:
            self.df.to_excel(self.archivo, index=False)
        except PermissionError:
            raise PermissionError(
                f"No se puede guardar '{self.archivo}'.\n"
                "El archivo está abierto en otro programa. Ciérralo e intenta de nuevo."
            )

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro - Préstamos y Encargos")
        self.root.geometry("1000x650")
        # Estilos personalizados (paleta azul oscura, profesional)
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass
        # LabelFrame oscuro
        self.style.configure('Blue.TLabelframe', background='#0b3d91')
        self.style.configure('Blue.TLabelframe.Label', background='#0b3d91', foreground='#ffffff', font=('Arial', 11, 'bold'))
        # Labels dentro de los frames
        self.style.configure('Blue.TLabel', background='#0b3d91', foreground='#ffffff', font=('Arial', 10))
        # Botones con azul más oscuro
        self.style.configure('Blue.TButton', background='#0b57d0', foreground='#ffffff', font=('Arial', 10, 'bold'))
        self.style.map('Blue.TButton', background=[('active', '#0844a8')], foreground=[('active', '#ffffff')])
        # Treeview encabezados
        self.style.configure('Treeview.Heading', background='#0b57d0', foreground='#ffffff', font=('Arial', 10, 'bold'))
        self.style.configure('Treeview', background='#ffffff', foreground='#000000', fieldbackground='#ffffff')
        self.sistema = RegistroArticulos()
        
        self.crear_interfaz()
        self.actualizar_tabla()
    
    def crear_interfaz(self):
        # Frame principal con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Nuevo registro
        self.frame_nuevo = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_nuevo, text='Nuevo Registro')
        self.crear_formulario_nuevo()
        
        # Pestaña 2: Gestionar registros
        self.frame_gestionar = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_gestionar, text='Gestionar Registros')
        self.crear_vista_gestion()
    
    def crear_formulario_nuevo(self):
        frame = ttk.LabelFrame(self.frame_nuevo, text="Registrar Nuevo", padding=20, style='Blue.TLabelframe')
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tipo
        ttk.Label(frame, text="Tipo:", font=('Arial', 10, 'bold'), style='Blue.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.combo_tipo = ttk.Combobox(frame, 
                           values=['Préstamo', 'Encargo', 'Proyecto', 'Otro'],
                                       width=37, state='readonly',
                                       font=('Arial', 10))
        self.combo_tipo.set('Préstamo')
        self.combo_tipo.grid(row=0, column=1, pady=5, padx=10)
        self.combo_tipo.bind('<<ComboboxSelected>>', self.actualizar_etiquetas_tipo)
        
        # Artículo
        self.label_articulo = ttk.Label(frame, text="Artículo/Cosa:", style='Blue.TLabel')
        self.label_articulo.grid(row=1, column=0, sticky='w', pady=5)
        self.entry_articulo = ttk.Entry(frame, width=40)
        self.entry_articulo.grid(row=1, column=1, pady=5, padx=10)
        
        # Persona
        self.label_persona = ttk.Label(frame, text="Prestado a:", style='Blue.TLabel')
        self.label_persona.grid(row=2, column=0, sticky='w', pady=5)
        self.entry_persona = ttk.Entry(frame, width=40)
        self.entry_persona.grid(row=2, column=1, pady=5, padx=10)
        
        # Fecha
        ttk.Label(frame, text="Fecha:", style='Blue.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        self.entry_fecha = DateEntry(frame, width=37, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='dd/mm/yyyy', locale='es_ES')
        self.entry_fecha.grid(row=3, column=1, pady=5, padx=10)
        
        # Estado inicial
        ttk.Label(frame, text="Estado inicial:", style='Blue.TLabel').grid(row=4, column=0, sticky='w', pady=5)
        self.combo_estado_inicial = ttk.Combobox(frame, 
                                                 values=['Prestado', 'Devuelto', 'No devuelto',
                                                        'Pendiente', 'En proceso', 'Completado', 'Cancelado'],
                                                 width=37, state='readonly')
        self.combo_estado_inicial.set('Prestado')
        self.combo_estado_inicial.grid(row=4, column=1, pady=5, padx=10)
        self.combo_tipo.bind('<<ComboboxSelected>>', self.actualizar_estado_sugerido)
        
        # Notas
        ttk.Label(frame, text="Notas (opcional):", style='Blue.TLabel').grid(row=5, column=0, sticky='nw', pady=5)
        self.text_notas = tk.Text(frame, width=40, height=5)
        self.text_notas.grid(row=5, column=1, pady=5, padx=10)
        
        # Botón registrar
        btn_registrar = ttk.Button(frame, text="Registrar", 
                       command=self.registrar_nuevo, style='Blue.TButton')
        btn_registrar.grid(row=6, column=1, pady=20)
        
        # Label para código generado
        self.label_codigo = ttk.Label(frame, text="", font=('Arial', 12, 'bold'),
                                     foreground='green')
        self.label_codigo.grid(row=7, column=1, pady=5)
    
    def actualizar_etiquetas_tipo(self, event=None):
        """Actualiza las etiquetas según el tipo seleccionado"""
        tipo = self.combo_tipo.get()
        
        if tipo == 'Préstamo':
            self.label_articulo.config(text="Artículo/Cosa:")
            self.label_persona.config(text="Prestado a:")
        elif tipo == 'Encargo':
            self.label_articulo.config(text="Encargo/Servicio:")
            self.label_persona.config(text="Encargado a:")
        elif tipo == 'Proyecto':
            self.label_articulo.config(text="Proyecto/Elemento:")
            self.label_persona.config(text="Responsable:")
        else:  # Otro u otros
            self.label_articulo.config(text="Artículo/Cosa:")
            self.label_persona.config(text="Persona:")
    
    def actualizar_estado_sugerido(self, event=None):
        """Sugiere un estado según el tipo seleccionado"""
        tipo = self.combo_tipo.get()
        
        if tipo == 'Préstamo':
            self.combo_estado_inicial.set('Prestado')
        elif tipo == 'Encargo':
            self.combo_estado_inicial.set('Pendiente')
        elif tipo == 'Proyecto':
            self.combo_estado_inicial.set('En proceso')
        else:
            self.combo_estado_inicial.set('Pendiente')
        
        self.actualizar_etiquetas_tipo()
    
    def crear_vista_gestion(self):
        # Frame de filtros
        frame_filtros = ttk.LabelFrame(self.frame_gestionar, text="Filtros y Búsqueda", padding=10, style='Blue.TLabelframe')
        frame_filtros.pack(fill='x', padx=20, pady=10)
        
        # Fila 1
        fila1 = ttk.Frame(frame_filtros)
        fila1.pack(fill='x', pady=5)
        
        ttk.Label(fila1, text="Buscar código:").pack(side='left', padx=5)
        self.entry_buscar = ttk.Entry(fila1, width=12)
        self.entry_buscar.pack(side='left', padx=5)
        ttk.Button(fila1, text="Buscar", 
                  command=self.buscar_registro).pack(side='left', padx=5)
        
        ttk.Button(fila1, text="Mostrar Todo", 
                  command=self.actualizar_tabla).pack(side='left', padx=20)
        
        # Fila 2
        fila2 = ttk.Frame(frame_filtros)
        fila2.pack(fill='x', pady=5)
        
        ttk.Label(fila2, text="Tipo:").pack(side='left', padx=5)
        self.combo_filtro_tipo = ttk.Combobox(fila2, 
                             values=['Todos', 'Préstamo', 'Encargo', 'Proyecto', 'Otro'],
                                             width=12, state='readonly')
        self.combo_filtro_tipo.set('Todos')
        self.combo_filtro_tipo.pack(side='left', padx=5)
        
        ttk.Label(fila2, text="Estado:").pack(side='left', padx=5)
        self.combo_filtro_estado = ttk.Combobox(fila2, 
                                               values=['Todos', 'Prestado', 'Devuelto', 
                                                      'No devuelto', 'Pendiente', 
                                                      'En proceso', 'Completado', 'Cancelado'],
                                               width=12, state='readonly')
        self.combo_filtro_estado.set('Todos')
        self.combo_filtro_estado.pack(side='left', padx=5)
        
        ttk.Button(fila2, text="Aplicar Filtros", 
                  command=self.aplicar_filtros).pack(side='left', padx=5)
        
        # Tabla
        frame_tabla = ttk.Frame(self.frame_gestionar)
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabla, orient='vertical')
        scroll_x = ttk.Scrollbar(frame_tabla, orient='horizontal')
        
        # Treeview
        self.tree = ttk.Treeview(frame_tabla, 
                                 columns=('Codigo', 'Tipo', 'Articulo', 'Persona', 
                                         'Fecha', 'Estado', 'Notas'),
                                 show='headings',
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading('Codigo', text='Código')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Articulo', text='Artículo')
        self.tree.heading('Persona', text='Persona')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Estado', text='Estado')
        self.tree.heading('Notas', text='Notas')
        
        self.tree.column('Codigo', width=90)
        self.tree.column('Tipo', width=90, anchor='center')
        self.tree.column('Articulo', width=130)
        self.tree.column('Persona', width=130)
        self.tree.column('Fecha', width=90, anchor='center')
        self.tree.column('Estado', width=100, anchor='center')
        self.tree.column('Notas', width=180)
        
        # Tags para colores (tonos formales, ligeramente más oscuros que antes)
        self.tree.tag_configure('prestamo', background='#cfe3ff', foreground='#02112a')
        self.tree.tag_configure('encargo', background='#ffe6cc', foreground='#2b1700')
        self.tree.tag_configure('proyecto', background='#cfeedd', foreground='#072a19')
        self.tree.tag_configure('otro', background='#e6dbff', foreground='#1a063a')
        
        # Posicionar elementos
        self.tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')
        
        # Frame de acciones
        frame_acciones = ttk.LabelFrame(self.frame_gestionar, text="Acciones", padding=10, style='Blue.TLabelframe')
        frame_acciones.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_acciones, text="Selecciona un registro en la tabla y elige una acción:").pack(anchor='w', pady=5)
        
        frame_botones = ttk.Frame(frame_acciones)
        frame_botones.pack(fill='x', pady=5)
        
        ttk.Label(frame_botones, text="Cambiar estado a:").pack(side='left', padx=5)
        
        self.combo_nuevo_estado = ttk.Combobox(frame_botones, 
                                              values=['Prestado', 'Devuelto', 'No devuelto',
                                                     'Pendiente', 'En proceso', 'Completado', 'Cancelado'],
                                              width=15)
        self.combo_nuevo_estado.set('Devuelto')
        self.combo_nuevo_estado.pack(side='left', padx=5)
        
        ttk.Button(frame_botones, text="✓ Cambiar Estado", 
                  command=self.cambiar_estado_seleccionado).pack(side='left', padx=10)
        
        ttk.Button(frame_botones, text="Eliminar Registro", 
                  command=self.eliminar_seleccionado,
                  style='Danger.TButton').pack(side='left', padx=10)
        
        ttk.Button(frame_botones, text="📋 Copiar Código", 
                  command=self.copiar_codigo_seleccionado).pack(side='left', padx=10)
        
        ttk.Button(frame_botones, text="✏️ Editar Registro", 
                  command=self.editar_seleccionado).pack(side='left', padx=10)
    
    def registrar_nuevo(self):
        tipo = self.combo_tipo.get()
        articulo = self.entry_articulo.get().strip()
        persona = self.entry_persona.get().strip()
        fecha = self.entry_fecha.get()
        estado = self.combo_estado_inicial.get()
        notas = self.text_notas.get('1.0', 'end-1c').strip()
        
        if not articulo or not persona:
            messagebox.showerror("Error", "Artículo y Persona son obligatorios")
            return
        
        codigo = self.sistema.agregar_registro(tipo, articulo, persona, fecha, estado, notas)
        
        self.label_codigo.config(text=f"✓ Registro creado con código: {codigo}")
        
        # Limpiar campos
        self.entry_articulo.delete(0, 'end')
        self.entry_persona.delete(0, 'end')
        self.text_notas.delete('1.0', 'end')
        self.entry_fecha.set_date(datetime.now())
        self.actualizar_estado_sugerido()
        
        self.actualizar_tabla()
        
        messagebox.showinfo("Éxito", f"Registro creado con código:\n{codigo}")
    
    def buscar_registro(self):
        codigo = self.entry_buscar.get().strip().upper()
        if not codigo:
            messagebox.showwarning("Advertencia", "Ingresa un código para buscar")
            return
        
        resultado = self.sistema.buscar(codigo)
        if resultado is None:
            messagebox.showerror("Error", f"No se encontró el código: {codigo}")
            return
        
        # Limpiar y mostrar resultado
        self.tree.delete(*self.tree.get_children())
        for _, row in resultado.iterrows():
            tipo_row = row['Tipo']
            if tipo_row == 'Préstamo':
                tag = 'prestamo'
            elif tipo_row == 'Encargo':
                tag = 'encargo'
            elif tipo_row == 'Proyecto':
                tag = 'proyecto'
            else:
                tag = 'otro'
            self.tree.insert('', 'end', values=(
                row['Codigo'], row['Tipo'], row['Articulo'], row['Persona'],
                row['Fecha'], row['Estado'], row['Notas']
            ), tags=(tag,))
    
    def aplicar_filtros(self):
        tipo = self.combo_filtro_tipo.get()
        estado = self.combo_filtro_estado.get()
        
        df = self.sistema.obtener_todos()
        
        if tipo != 'Todos':
            df = df[df['Tipo'] == tipo]
        
        if estado != 'Todos':
            df = df[df['Estado'] == estado]
        
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            tipo_row = row['Tipo']
            if tipo_row == 'Préstamo':
                tag = 'prestamo'
            elif tipo_row == 'Encargo':
                tag = 'encargo'
            elif tipo_row == 'Proyecto':
                tag = 'proyecto'
            else:
                tag = 'otro'
            self.tree.insert('', 'end', values=(
                row['Codigo'], row['Tipo'], row['Articulo'], row['Persona'],
                row['Fecha'], row['Estado'], row['Notas']
            ), tags=(tag,))
    
    def actualizar_tabla(self):
        df = self.sistema.obtener_todos()
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            # Asignar tag según el tipo
            tipo_row = row['Tipo']
            if tipo_row == 'Préstamo':
                tag = 'prestamo'
            elif tipo_row == 'Encargo':
                tag = 'encargo'
            elif tipo_row == 'Proyecto':
                tag = 'proyecto'
            else:
                tag = 'otro'
            self.tree.insert('', 'end', values=(
                row['Codigo'], row['Tipo'], row['Articulo'], row['Persona'],
                row['Fecha'], row['Estado'], row['Notas']
            ), tags=(tag,))
        
        # Resetear filtros
        self.combo_filtro_tipo.set('Todos')
        self.combo_filtro_estado.set('Todos')
    
    def cambiar_estado_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        nuevo_estado = self.combo_nuevo_estado.get()
        
        if self.sistema.cambiar_estado(codigo, nuevo_estado):
            messagebox.showinfo("Éxito", f"Estado actualizado a: {nuevo_estado}")
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo cambiar el estado")
    
    def eliminar_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        articulo = item['values'][2]
        
        confirmar = messagebox.askyesno("Confirmar Eliminación", 
                                        f"¿Estás seguro de eliminar este registro?\n\n"
                                        f"Código: {codigo}\n"
                                        f"Artículo: {articulo}")
        
        if confirmar:
            if self.sistema.eliminar(codigo):
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro")
    
    def copiar_codigo_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        
        # Copiar al portapapeles
        self.root.clipboard_clear()
        self.root.clipboard_append(codigo)
        self.root.update()
        
        messagebox.showinfo("Copiado", f"Código copiado al portapapeles:\n{codigo}")
    
    def editar_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        tipo_actual = item['values'][1]
        articulo_actual = item['values'][2]
        persona_actual = item['values'][3]
        fecha_actual = item['values'][4]
        estado_actual = item['values'][5]
        notas_actual = item['values'][6]
        
        # Crear ventana de edición
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title(f"Editar Registro - {codigo}")
        ventana_editar.geometry("500x550")
        ventana_editar.resizable(False, False)
        ventana_editar.configure(bg='#052a5f')
        
        frame = ttk.LabelFrame(ventana_editar, text=f"Código: {codigo}", padding=20, style='Blue.TLabelframe')
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tipo
        ttk.Label(frame, text="Tipo:", style='Blue.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        combo_tipo_edit = ttk.Combobox(frame, values=['Préstamo', 'Encargo', 'Proyecto', 'Otro'],
                                       width=37, state='readonly')
        combo_tipo_edit.set(tipo_actual)
        combo_tipo_edit.grid(row=0, column=1, pady=5, padx=10)
        
        # Artículo
        ttk.Label(frame, text="Artículo/Cosa:", style='Blue.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        entry_articulo_edit = ttk.Entry(frame, width=40)
        entry_articulo_edit.insert(0, articulo_actual)
        entry_articulo_edit.grid(row=1, column=1, pady=5, padx=10)
        
        # Persona
        ttk.Label(frame, text="Persona:", style='Blue.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        entry_persona_edit = ttk.Entry(frame, width=40)
        entry_persona_edit.insert(0, persona_actual)
        entry_persona_edit.grid(row=2, column=1, pady=5, padx=10)
        
        # Fecha
        ttk.Label(frame, text="Fecha:", style='Blue.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        entry_fecha_edit = ttk.Entry(frame, width=40)
        entry_fecha_edit.insert(0, fecha_actual)
        entry_fecha_edit.grid(row=3, column=1, pady=5, padx=10)
        
        # Estado
        ttk.Label(frame, text="Estado:", style='Blue.TLabel').grid(row=4, column=0, sticky='w', pady=5)
        combo_estado_edit = ttk.Combobox(frame, 
                                         values=['Prestado', 'Devuelto', 'No devuelto',
                                                'Pendiente', 'En proceso', 'Completado', 'Cancelado', 'No echo' , 'Echo' ],
                                         width=37, state='readonly')
        combo_estado_edit.set(estado_actual)
        combo_estado_edit.grid(row=4, column=1, pady=5, padx=10)
        
        # Notas
        ttk.Label(frame, text="Notas:", style='Blue.TLabel').grid(row=5, column=0, sticky='nw', pady=5)
        text_notas_edit = tk.Text(frame, width=40, height=5)
        text_notas_edit.insert('1.0', notas_actual)
        text_notas_edit.grid(row=5, column=1, pady=5, padx=10)
        
        # Función para guardar cambios
        def guardar_cambios():
            nuevo_tipo = combo_tipo_edit.get()
            nuevo_articulo = entry_articulo_edit.get().strip()
            nueva_persona = entry_persona_edit.get().strip()
            nueva_fecha = entry_fecha_edit.get().strip()
            nuevo_estado = combo_estado_edit.get()
            nuevas_notas = text_notas_edit.get('1.0', 'end-1c').strip()
            
            if not nuevo_articulo or not nueva_persona:
                messagebox.showerror("Error", "Artículo y Persona son obligatorios")
                return
            
            # Actualizar el registro
            indice = self.sistema.df[self.sistema.df['Codigo'] == codigo].index[0]
            self.sistema.df.loc[indice, 'Tipo'] = nuevo_tipo
            self.sistema.df.loc[indice, 'Articulo'] = nuevo_articulo
            self.sistema.df.loc[indice, 'Persona'] = nueva_persona
            self.sistema.df.loc[indice, 'Fecha'] = nueva_fecha
            self.sistema.df.loc[indice, 'Estado'] = nuevo_estado
            self.sistema.df.loc[indice, 'Notas'] = nuevas_notas
            self.sistema.guardar()
            
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
            ventana_editar.destroy()
            self.actualizar_tabla()
        
        # Botones
        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=6, column=1, pady=20)
        
        ttk.Button(frame_botones, text="Guardar Cambios", 
              command=guardar_cambios, style='Blue.TButton').pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", 
              command=ventana_editar.destroy, style='Blue.TButton').pack(side='left', padx=5)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VentanaPrincipal(root)
        root.mainloop()
    except PermissionError as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error de Acceso", str(e))
        root.destroy()