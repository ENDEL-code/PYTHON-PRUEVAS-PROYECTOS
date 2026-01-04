import pandas as pd
import random
import string
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class RegistroTrabajos:
    def __init__(self, archivo='registro-trabajos-escolares.xlsx'):
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
                'Codigo', 'Materia', 'Titulo Trabajo', 'Estudiante', 'Grado',
                'Profesor', 'Fecha Asignacion', 'Fecha Entrega', 'Calificacion',
                'Estado', 'Descripcion', 'Observaciones'
            ])
    
    def generar_codigo(self):
        while True:
            codigo = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8
                
            ))
            if codigo not in self.codigos_usados:
                self.codigos_usados.add(codigo)
                return codigo
    
    def agregar_registro(self, materia, titulo, estudiante, grado, profesor, 
                        fecha_asignacion, fecha_entrega, calificacion, 
                        estado, descripcion, observaciones=''):
        codigo = self.generar_codigo()
        
        nuevo_registro = {
            'Codigo': codigo,
            'Materia': materia,
            'Titulo Trabajo': titulo,
            'Estudiante': estudiante,
            'Grado': grado,
            'Profesor': profesor,
            'Fecha Asignacion': fecha_asignacion,
            'Fecha Entrega': fecha_entrega,
            'Calificacion': calificacion,
            'Estado': estado,
            'Descripcion': descripcion,
            'Observaciones': observaciones
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
    
    def actualizar_calificacion(self, codigo, calificacion):
        indice = self.df[self.df['Codigo'] == codigo].index
        if len(indice) == 0:
            return False
        
        self.df.loc[indice, 'Calificacion'] = calificacion
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
    
    def filtrar_por_materia(self, materia):
        return self.df[self.df['Materia'] == materia]
    
    def filtrar_por_estudiante(self, estudiante):
        return self.df[self.df['Estudiante'] == estudiante]
    
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
        self.root.title("Sistema de Registro - Trabajos Escolares")
        self.root.geometry("1100x700")
        
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
        
        self.sistema = RegistroTrabajos()
        
        self.crear_interfaz()
        self.actualizar_tabla()
    
    def crear_interfaz(self):
        # Frame principal con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Nuevo registro
        self.frame_nuevo = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_nuevo, text='Nuevo Trabajo')
        self.crear_formulario_nuevo()
        
        # Pestaña 2: Gestionar registros
        self.frame_gestionar = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_gestionar, text='Gestionar Trabajos')
        self.crear_vista_gestion()
    
    def crear_formulario_nuevo(self):
        canvas = tk.Canvas(self.frame_nuevo, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_nuevo, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = ttk.LabelFrame(scrollable_frame, text="Registrar Nuevo Trabajo", padding=20, style='Blue.TLabelframe')
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Materia
        ttk.Label(frame, text="Materia:", font=('Arial', 10, 'bold'), style='Blue.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.combo_materia = ttk.Combobox(frame, 
                           values=['Matemáticas', 'Español', 'Inglés', 'Ciencias', 
                                  'Historia', 'Geografía', 'Educación Física', 'Arte', 'Informática', 'Otra'],
                                       width=45, state='readonly',
                                       font=('Arial', 10))
        self.combo_materia.set('Matemáticas')
        self.combo_materia.grid(row=0, column=1, pady=5, padx=10)
        
        # Título del trabajo
        ttk.Label(frame, text="Título del Trabajo:", style='Blue.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.entry_titulo = ttk.Entry(frame, width=48)
        self.entry_titulo.grid(row=1, column=1, pady=5, padx=10)
        
        # Estudiante
        ttk.Label(frame, text="Nombre del Estudiante:", style='Blue.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.entry_estudiante = ttk.Entry(frame, width=48)
        self.entry_estudiante.grid(row=2, column=1, pady=5, padx=10)
        
        # Grado
        ttk.Label(frame, text="Grado/Curso:", style='Blue.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        self.combo_grado = ttk.Combobox(frame, 
                           values=['1°', '2°', '3°', '4°', '5°', '6°', '7°', '8°', '9°', '10°', '11°', 'Otro'],
                                       width=45, state='readonly')
        self.combo_grado.set('1°')
        self.combo_grado.grid(row=3, column=1, pady=5, padx=10)
        
        # Profesor
        ttk.Label(frame, text="Profesor Responsable:", style='Blue.TLabel').grid(row=4, column=0, sticky='w', pady=5)
        self.entry_profesor = ttk.Entry(frame, width=48)
        self.entry_profesor.grid(row=4, column=1, pady=5, padx=10)
        
        # Fecha de Asignación
        ttk.Label(frame, text="Fecha de Asignación:", style='Blue.TLabel').grid(row=5, column=0, sticky='w', pady=5)
        self.entry_fecha_asignacion = DateEntry(frame, width=45, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='dd/mm/yyyy', locale='es_ES')
        self.entry_fecha_asignacion.grid(row=5, column=1, pady=5, padx=10)
        
        # Fecha de Entrega
        ttk.Label(frame, text="Fecha de Entrega:", style='Blue.TLabel').grid(row=6, column=0, sticky='w', pady=5)
        self.entry_fecha_entrega = DateEntry(frame, width=45, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='dd/mm/yyyy', locale='es_ES')
        self.entry_fecha_entrega.grid(row=6, column=1, pady=5, padx=10)
        
        # Calificación
        ttk.Label(frame, text="Calificación Inicial:", style='Blue.TLabel').grid(row=7, column=0, sticky='w', pady=5)
        self.entry_calificacion = ttk.Combobox(frame, 
                                               values=['N/A', 'Excelente', 'Bueno', 'Satisfactorio', 'Deficiente', 'Por Calificar'],
                                               width=45, state='readonly')
        self.entry_calificacion.set('Por Calificar')
        self.entry_calificacion.grid(row=7, column=1, pady=5, padx=10)
        
        # Estado inicial
        ttk.Label(frame, text="Estado Inicial:", style='Blue.TLabel').grid(row=8, column=0, sticky='w', pady=5)
        self.combo_estado_inicial = ttk.Combobox(frame, 
                                                 values=['No echo', 'En Progreso', 'Echo', 'Entregado', 'Revisado', 'Calificado'],
                                                 width=45, state='readonly')
        self.combo_estado_inicial.set('No echo')
        self.combo_estado_inicial.grid(row=8, column=1, pady=5, padx=10)
        
        # Descripción del trabajo
        ttk.Label(frame, text="Descripción del Trabajo:", style='Blue.TLabel').grid(row=9, column=0, sticky='nw', pady=5)
        self.text_descripcion = tk.Text(frame, width=48, height=4)
        self.text_descripcion.grid(row=9, column=1, pady=5, padx=10)
        
        # Observaciones
        ttk.Label(frame, text="Observaciones (opcional):", style='Blue.TLabel').grid(row=10, column=0, sticky='nw', pady=5)
        self.text_observaciones = tk.Text(frame, width=48, height=3)
        self.text_observaciones.grid(row=10, column=1, pady=5, padx=10)
        
        # Botón registrar
        btn_registrar = ttk.Button(frame, text="📝 Registrar Trabajo", 
                       command=self.registrar_nuevo, style='Blue.TButton')
        btn_registrar.grid(row=11, column=1, pady=20)
        
        # Label para código generado
        self.label_codigo = ttk.Label(frame, text="", font=('Arial', 12, 'bold'),
                                     foreground='green')
        self.label_codigo.grid(row=12, column=1, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
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
        ttk.Button(fila1, text="🔍 Buscar", 
                  command=self.buscar_registro).pack(side='left', padx=5)
        
        ttk.Button(fila1, text="📋 Mostrar Todo", 
                  command=self.actualizar_tabla).pack(side='left', padx=20)
        
        # Fila 2
        fila2 = ttk.Frame(frame_filtros)
        fila2.pack(fill='x', pady=5)
        
        ttk.Label(fila2, text="Materia:").pack(side='left', padx=5)
        self.combo_filtro_materia = ttk.Combobox(fila2, 
                             values=['Todas', 'Matemáticas', 'Español', 'Inglés', 'Ciencias', 
                                    'Historia', 'Geografía', 'Educación Física', 'Arte', 'Informática', 'Otra'],
                                             width=12, state='readonly')
        self.combo_filtro_materia.set('Todas')
        self.combo_filtro_materia.pack(side='left', padx=5)
        
        ttk.Label(fila2, text="Estado:").pack(side='left', padx=5)
        self.combo_filtro_estado = ttk.Combobox(fila2, 
                                               values=['Todos', 'No echo', 'En Progreso', 'Echo', 'Entregado', 'Revisado', 'Calificado'],
                                               width=12, state='readonly')
        self.combo_filtro_estado.set('Todos')
        self.combo_filtro_estado.pack(side='left', padx=5)
        
        ttk.Label(fila2, text="Estudiante:").pack(side='left', padx=5)
        self.entry_filtro_estudiante = ttk.Entry(fila2, width=12)
        self.entry_filtro_estudiante.pack(side='left', padx=5)
        
        ttk.Button(fila2, text="🔎 Aplicar Filtros", 
                  command=self.aplicar_filtros).pack(side='left', padx=5)
        
        # Tabla
        frame_tabla = ttk.Frame(self.frame_gestionar)
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabla, orient='vertical')
        scroll_x = ttk.Scrollbar(frame_tabla, orient='horizontal')
        
        # Treeview
        self.tree = ttk.Treeview(frame_tabla, 
                                 columns=('Codigo', 'Materia', 'Titulo', 'Estudiante', 'Grado',
                                         'Profesor', 'F_Asignacion', 'F_Entrega', 'Calificacion', 'Estado'),
                                 show='headings',
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading('Codigo', text='Código')
        self.tree.heading('Materia', text='Materia')
        self.tree.heading('Titulo', text='Título')
        self.tree.heading('Estudiante', text='Estudiante')
        self.tree.heading('Grado', text='Grado')
        self.tree.heading('Profesor', text='Profesor')
        self.tree.heading('F_Asignacion', text='F. Asignación')
        self.tree.heading('F_Entrega', text='F. Entrega')
        self.tree.heading('Calificacion', text='Calificación')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('Codigo', width=70)
        self.tree.column('Materia', width=80, anchor='center')
        self.tree.column('Titulo', width=120)
        self.tree.column('Estudiante', width=110)
        self.tree.column('Grado', width=50, anchor='center')
        self.tree.column('Profesor', width=110)
        self.tree.column('F_Asignacion', width=90, anchor='center')
        self.tree.column('F_Entrega', width=90, anchor='center')
        self.tree.column('Calificacion', width=100, anchor='center')
        self.tree.column('Estado', width=100, anchor='center')
        
        # Tags para colores
        self.tree.tag_configure('no_echo', background='#ffe6e6', foreground='#8b0000')
        self.tree.tag_configure('en_progreso', background='#ffffcc', foreground='#ff8800')
        self.tree.tag_configure('echo', background='#cfeedd', foreground='#072a19')
        self.tree.tag_configure('entregado', background='#e3f2fd', foreground='#01579b')
        self.tree.tag_configure('calificado', background='#f3e5f5', foreground='#4a148c')
        
        # Posicionar elementos
        self.tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')
        
        # Frame de acciones
        frame_acciones = ttk.LabelFrame(self.frame_gestionar, text="Acciones", padding=10, style='Blue.TLabelframe')
        frame_acciones.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_acciones, text="Selecciona un registro y elige una acción:").pack(anchor='w', pady=5)
        
        frame_botones = ttk.Frame(frame_acciones)
        frame_botones.pack(fill='x', pady=5)
        
        ttk.Label(frame_botones, text="Cambiar estado a:").pack(side='left', padx=5)
        
        self.combo_nuevo_estado = ttk.Combobox(frame_botones, 
                                              values=['No echo', 'En Progreso', 'Echo', 'Entregado', 'Revisado', 'Calificado'],
                                              width=15)
        self.combo_nuevo_estado.set('Entregado')
        self.combo_nuevo_estado.pack(side='left', padx=5)
        
        ttk.Button(frame_botones, text="✓ Cambiar Estado", 
                  command=self.cambiar_estado_seleccionado).pack(side='left', padx=10)
        
        ttk.Label(frame_botones, text="Calificación:").pack(side='left', padx=5)
        
        self.combo_nueva_calificacion = ttk.Combobox(frame_botones, 
                                                     values=['N/A', 'Excelente', 'Bueno', 'Satisfactorio', 'Deficiente', 'Por Calificar'],
                                                     width=15)
        self.combo_nueva_calificacion.set('Por Calificar')
        self.combo_nueva_calificacion.pack(side='left', padx=5)
        
        ttk.Button(frame_botones, text="⭐ Calificar", 
                  command=self.calificar_seleccionado).pack(side='left', padx=10)
        
        ttk.Button(frame_botones, text="Eliminar", 
                  command=self.eliminar_seleccionado).pack(side='left', padx=10)
        
        ttk.Button(frame_botones, text="✏️ Editar", 
                  command=self.editar_seleccionado).pack(side='left', padx=10)
    
    def registrar_nuevo(self):
        materia = self.combo_materia.get()
        titulo = self.entry_titulo.get().strip()
        estudiante = self.entry_estudiante.get().strip()
        grado = self.combo_grado.get()
        profesor = self.entry_profesor.get().strip()
        fecha_asignacion = self.entry_fecha_asignacion.get()
        fecha_entrega = self.entry_fecha_entrega.get()
        calificacion = self.entry_calificacion.get()
        estado = self.combo_estado_inicial.get()
        descripcion = self.text_descripcion.get('1.0', 'end-1c').strip()
        observaciones = self.text_observaciones.get('1.0', 'end-1c').strip()
        
        if not titulo or not estudiante or not profesor:
            messagebox.showerror("Error", "Título, Estudiante y Profesor son obligatorios")
            return
        
        codigo = self.sistema.agregar_registro(materia, titulo, estudiante, grado, profesor, 
                                              fecha_asignacion, fecha_entrega, calificacion, 
                                              estado, descripcion, observaciones)
        
        self.label_codigo.config(text=f"✓ Trabajo registrado con código: {codigo}")
        
        # Limpiar campos
        self.entry_titulo.delete(0, 'end')
        self.entry_estudiante.delete(0, 'end')
        self.entry_profesor.delete(0, 'end')
        self.text_descripcion.delete('1.0', 'end')
        self.text_observaciones.delete('1.0', 'end')
        self.entry_fecha_asignacion.set_date(datetime.now())
        self.entry_fecha_entrega.set_date(datetime.now())
        
        self.actualizar_tabla()
        
        messagebox.showinfo("Éxito", f"Trabajo registrado con código:\n{codigo}")
    
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
            tag = self.obtener_tag_estado(row['Estado'])
            self.tree.insert('', 'end', values=(
                row['Codigo'], row['Materia'], row['Titulo Trabajo'], row['Estudiante'],
                row['Grado'], row['Profesor'], row['Fecha Asignacion'], row['Fecha Entrega'],
                row['Calificacion'], row['Estado']
            ), tags=(tag,))
    
    def obtener_tag_estado(self, estado):
        if estado == 'No echo':
            return 'no_echo'
        elif estado == 'En Progreso':
            return 'en_progreso'
        elif estado == 'Echo':
            return 'echo'
        elif estado == 'Entregado':
            return 'entregado'
        else:
            return 'calificado'
    
    def aplicar_filtros(self):
        materia = self.combo_filtro_materia.get()
        estado = self.combo_filtro_estado.get()
        estudiante = self.entry_filtro_estudiante.get().strip()
        
        df = self.sistema.obtener_todos()
        
        if materia != 'Todas':
            df = df[df['Materia'] == materia]
        
        if estado != 'Todos':
            df = df[df['Estado'] == estado]
        
        if estudiante:
            df = df[df['Estudiante'].str.contains(estudiante, case=False, na=False)]
        
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            tag = self.obtener_tag_estado(row['Estado'])
            self.tree.insert('', 'end', values=(
                row['Codigo'], row['Materia'], row['Titulo Trabajo'], row['Estudiante'],
                row['Grado'], row['Profesor'], row['Fecha Asignacion'], row['Fecha Entrega'],
                row['Calificacion'], row['Estado']
            ), tags=(tag,))
    
    def actualizar_tabla(self):
        df = self.sistema.obtener_todos()
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            tag = self.obtener_tag_estado(row['Estado'])
            self.tree.insert('', 'end', values=(
                row['Codigo'], row['Materia'], row['Titulo Trabajo'], row['Estudiante'],
                row['Grado'], row['Profesor'], row['Fecha Asignacion'], row['Fecha Entrega'],
                row['Calificacion'], row['Estado']
            ), tags=(tag,))
        
        # Resetear filtros
        self.combo_filtro_materia.set('Todas')
        self.combo_filtro_estado.set('Todos')
        self.entry_filtro_estudiante.delete(0, 'end')
    
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
    
    def calificar_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        nueva_calificacion = self.combo_nueva_calificacion.get()
        
        if self.sistema.actualizar_calificacion(codigo, nueva_calificacion):
            messagebox.showinfo("Éxito", f"Calificación actualizada a: {nueva_calificacion}")
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la calificación")
    
    def eliminar_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        titulo = item['values'][2]
        estudiante = item['values'][3]
        
        confirmar = messagebox.askyesno("Confirmar Eliminación", 
                                        f"¿Estás seguro de eliminar este registro?\n\n"
                                        f"Código: {codigo}\n"
                                        f"Título: {titulo}\n"
                                        f"Estudiante: {estudiante}")
        
        if confirmar:
            if self.sistema.eliminar(codigo):
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro")
    
    def editar_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        
        # Obtener datos del dataframe
        fila = self.sistema.df[self.sistema.df['Codigo'] == codigo].iloc[0]
        
        # Crear ventana de edición
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title(f"Editar Trabajo - {codigo}")
        ventana_editar.geometry("550x700")
        ventana_editar.resizable(False, False)
        
        frame = ttk.LabelFrame(ventana_editar, text=f"Código: {codigo}", padding=20, style='Blue.TLabelframe')
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Materia
        ttk.Label(frame, text="Materia:", style='Blue.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        combo_materia_edit = ttk.Combobox(frame, 
                                          values=['Matemáticas', 'Español', 'Inglés', 'Ciencias', 
                                                 'Historia', 'Geografía', 'Educación Física', 'Arte', 'Informática', 'Otra'],
                                          width=45, state='readonly')
        combo_materia_edit.set(fila['Materia'])
        combo_materia_edit.grid(row=0, column=1, pady=5, padx=10)
        
        # Título
        ttk.Label(frame, text="Título:", style='Blue.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        entry_titulo_edit = ttk.Entry(frame, width=48)
        entry_titulo_edit.insert(0, fila['Titulo Trabajo'])
        entry_titulo_edit.grid(row=1, column=1, pady=5, padx=10)
        
        # Estudiante
        ttk.Label(frame, text="Estudiante:", style='Blue.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        entry_estudiante_edit = ttk.Entry(frame, width=48)
        entry_estudiante_edit.insert(0, fila['Estudiante'])
        entry_estudiante_edit.grid(row=2, column=1, pady=5, padx=10)
        
        # Profesor
        ttk.Label(frame, text="Profesor:", style='Blue.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        entry_profesor_edit = ttk.Entry(frame, width=48)
        entry_profesor_edit.insert(0, fila['Profesor'])
        entry_profesor_edit.grid(row=3, column=1, pady=5, padx=10)
        
        # Estado
        ttk.Label(frame, text="Estado:", style='Blue.TLabel').grid(row=4, column=0, sticky='w', pady=5)
        combo_estado_edit = ttk.Combobox(frame, 
                                         values=['No echo', 'En Progreso', 'Echo', 'Entregado', 'Revisado', 'Calificado'],
                                         width=45, state='readonly')
        combo_estado_edit.set(fila['Estado'])
        combo_estado_edit.grid(row=4, column=1, pady=5, padx=10)
        
        # Calificación
        ttk.Label(frame, text="Calificación:", style='Blue.TLabel').grid(row=5, column=0, sticky='w', pady=5)
        combo_calificacion_edit = ttk.Combobox(frame, 
                                               values=['N/A', 'Excelente', 'Bueno', 'Satisfactorio', 'Deficiente', 'Por Calificar'],
                                               width=45, state='readonly')
        combo_calificacion_edit.set(fila['Calificacion'])
        combo_calificacion_edit.grid(row=5, column=1, pady=5, padx=10)
        
        # Descripción
        ttk.Label(frame, text="Descripción:", style='Blue.TLabel').grid(row=6, column=0, sticky='nw', pady=5)
        text_descripcion_edit = tk.Text(frame, width=48, height=3)
        text_descripcion_edit.insert('1.0', fila['Descripcion'])
        text_descripcion_edit.grid(row=6, column=1, pady=5, padx=10)
        
        # Observaciones
        ttk.Label(frame, text="Observaciones:", style='Blue.TLabel').grid(row=7, column=0, sticky='nw', pady=5)
        text_observaciones_edit = tk.Text(frame, width=48, height=3)
        text_observaciones_edit.insert('1.0', fila['Observaciones'])
        text_observaciones_edit.grid(row=7, column=1, pady=5, padx=10)
        
        # Función para guardar cambios
        def guardar_cambios():
            nueva_materia = combo_materia_edit.get()
            nuevo_titulo = entry_titulo_edit.get().strip()
            nuevo_estudiante = entry_estudiante_edit.get().strip()
            nuevo_profesor = entry_profesor_edit.get().strip()
            nuevo_estado = combo_estado_edit.get()
            nueva_calificacion = combo_calificacion_edit.get()
            nueva_descripcion = text_descripcion_edit.get('1.0', 'end-1c').strip()
            nuevas_observaciones = text_observaciones_edit.get('1.0', 'end-1c').strip()
            
            if not nuevo_titulo or not nuevo_estudiante or not nuevo_profesor:
                messagebox.showerror("Error", "Título, Estudiante y Profesor son obligatorios")
                return
            
            # Actualizar el registro
            indice = self.sistema.df[self.sistema.df['Codigo'] == codigo].index[0]
            self.sistema.df.loc[indice, 'Materia'] = nueva_materia
            self.sistema.df.loc[indice, 'Titulo Trabajo'] = nuevo_titulo
            self.sistema.df.loc[indice, 'Estudiante'] = nuevo_estudiante
            self.sistema.df.loc[indice, 'Profesor'] = nuevo_profesor
            self.sistema.df.loc[indice, 'Estado'] = nuevo_estado
            self.sistema.df.loc[indice, 'Calificacion'] = nueva_calificacion
            self.sistema.df.loc[indice, 'Descripcion'] = nueva_descripcion
            self.sistema.df.loc[indice, 'Observaciones'] = nuevas_observaciones
            self.sistema.guardar()
            
            messagebox.showinfo("Éxito", "Trabajo actualizado correctamente")
            ventana_editar.destroy()
            self.actualizar_tabla()
        
        # Botones
        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=8, column=1, pady=20)
        
        ttk.Button(frame_botones, text="💾 Guardar Cambios", 
              command=guardar_cambios, style='Blue.TButton').pack(side='left', padx=5)
        ttk.Button(frame_botones, text="❌ Cancelar", 
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