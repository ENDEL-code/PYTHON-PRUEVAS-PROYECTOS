import tkinter as tk
from tkinter import messagebox
import random
import math
from datetime import datetime
import colorsys

class NavidadTecnologica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎄 NAVIDAD TECH 2024 🎅")
        
        # Configurar ventana
        self.root.attributes('-fullscreen', False)
        self.root.geometry('1400x900')
        self.root.configure(bg='#000000')
        
        # Variables de animación
        self.copos_nieve = []
        self.estrellas = []
        self.particulas = []
        self.rayos_laser = []
        self.circulos_neon = []
        self.ondas = []
        self.fuegos_artificiales = []
        self.time = 0
        self.hue = 0
        self.titulo_colores = []
        
        # Canvas con antialiasing
        self.canvas = tk.Canvas(
            self.root, 
            bg='#000000', 
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind de teclas
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.root.bind('<space>', lambda e: self.crear_explosion_particulas(700, 450))
        
        # Crear elementos
        self.crear_grid_tecnologico()
        self.crear_estrellas_avanzadas()
        self.crear_interfaz_tech()
        self.crear_particulas_flotantes()
        self.crear_arbol_holografico()
        self.crear_circulos_neon()
        
        # Iniciar animaciones
        self.animacion_principal()
        self.actualizar_countdown()
        self.pulso_titulo()
        self.animar_grid()
        self.crear_rayos_laser()
        self.ondas_expansion()
        
    def toggle_fullscreen(self, event=None):
        estado = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not estado)
        
    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
    
    def rgb_to_hex(self, r, g, b):
        """Convertir RGB a hexadecimal"""
        return f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    
    def hsv_to_rgb_hex(self, h, s, v):
        """Convertir HSV a RGB hexadecimal"""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return self.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def crear_grid_tecnologico(self):
        """Crear grid de fondo estilo cyberpunk"""
        self.lineas_grid = []
        
        # Líneas verticales
        for x in range(0, 1400, 50):
            linea = self.canvas.create_line(
                x, 0, x, 900,
                fill='#00ff41', width=1, stipple='gray25'
            )
            self.lineas_grid.append({'id': linea, 'tipo': 'v', 'x': x})
        
        # Líneas horizontales
        for y in range(0, 900, 50):
            linea = self.canvas.create_line(
                0, y, 1400, y,
                fill='#00ff41', width=1, stipple='gray25'
            )
            self.lineas_grid.append({'id': linea, 'tipo': 'h', 'y': y})
    
    def animar_grid(self):
        """Animar el grid de fondo"""
        for linea in self.lineas_grid:
            if linea['tipo'] == 'v':
                # Efecto de pulso en líneas verticales
                if random.random() < 0.01:
                    color = random.choice(['#00ff41', '#00ffff', '#ff00ff'])
                    self.canvas.itemconfig(linea['id'], fill=color, width=2)
                    self.root.after(100, lambda l=linea: self.canvas.itemconfig(
                        l['id'], fill='#00ff41', width=1
                    ))
        
        self.root.after(50, self.animar_grid)
    
    def crear_estrellas_avanzadas(self):
        """Crear estrellas con efecto digital"""
        for _ in range(150):
            x = random.randint(0, 1400)
            y = random.randint(0, 400)
            size = random.randint(1, 4)
            
            # Crear estrella con glow
            estrella = self.canvas.create_oval(
                x-size, y-size, x+size, y+size,
                fill='#ffffff', outline='#00ffff', width=1
            )
            
            self.estrellas.append({
                'id': estrella,
                'x': x,
                'y': y,
                'brillo': random.random(),
                'velocidad': random.uniform(0.1, 0.3),
                'size': size
            })
    
    def crear_particulas_flotantes(self):
        """Crear partículas flotantes estilo Matrix"""
        for _ in range(100):
            x = random.randint(0, 1400)
            y = random.randint(0, 900)
            size = random.randint(2, 6)
            color = random.choice(['#00ff41', '#00ffff', '#ff00ff', '#ffff00'])
            
            particula = self.canvas.create_oval(
                x-size//2, y-size//2, x+size//2, y+size//2,
                fill=color, outline=color
            )
            
            self.particulas.append({
                'id': particula,
                'x': x,
                'y': y,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'color': color,
                'size': size
            })
    
    def crear_interfaz_tech(self):
        """Crear interfaz tecnológica"""
        # Título con efecto neón
        self.titulo = self.canvas.create_text(
            700, 80,
            text="🎄 NAVIDAD TECH 2024 🎄",
            font=('Courier New', 52, 'bold'),
            fill='#00ffff'
        )
        
        # Subtítulo con efecto glitch
        self.subtitulo = self.canvas.create_text(
            700, 140,
            text="[[ SISTEMA NAVIDEÑO ACTIVADO ]]",
            font=('Courier New', 16, 'bold'),
            fill='#00ff41'
        )
        
        # HUD elementos
        self.crear_hud()
        
        # Mensaje holográfico
        self.mensaje = self.canvas.create_text(
            700, 750,
            text=">>> INICIANDO PROTOCOLO DE CELEBRACIÓN <<<",
            font=('Courier New', 14, 'bold'),
            fill='#ff00ff'
        )
        
        # Countdown
        self.countdown_text = self.canvas.create_text(
            700, 700,
            text="",
            font=('Courier New', 20, 'bold'),
            fill='#ffff00'
        )
        
        # Panel de control
        self.crear_panel_control()
    
    def crear_hud(self):
        """Crear HUD (Head-Up Display)"""
        # Esquinas del HUD
        esquinas = [
            [(50, 50), (150, 50), (150, 70)],  # Superior izquierda
            [(1250, 50), (1350, 50), (1350, 70)],  # Superior derecha
            [(50, 850), (50, 830), (150, 830)],  # Inferior izquierda
            [(1350, 850), (1350, 830), (1250, 830)]  # Inferior derecha
        ]
        
        for puntos in esquinas:
            for i in range(len(puntos)-1):
                self.canvas.create_line(
                    puntos[i][0], puntos[i][1],
                    puntos[i+1][0], puntos[i+1][1],
                    fill='#00ffff', width=3
                )
        
        # Indicadores
        self.canvas.create_text(
            100, 100,
            text="[ONLINE]",
            font=('Courier New', 12, 'bold'),
            fill='#00ff41',
            anchor='w'
        )
        
        self.canvas.create_text(
            1300, 100,
            text="[ACTIVE]",
            font=('Courier New', 12, 'bold'),
            fill='#00ff41',
            anchor='e'
        )
    
    def crear_circulos_neon(self):
        """Crear círculos neón pulsantes"""
        centros = [(200, 450), (1200, 450), (700, 250)]
        
        for cx, cy in centros:
            for i in range(3):
                radio = 30 + i * 20
                circulo = self.canvas.create_oval(
                    cx-radio, cy-radio, cx+radio, cy+radio,
                    outline='#00ffff', width=2, stipple='gray25'
                )
                self.circulos_neon.append({
                    'id': circulo,
                    'cx': cx,
                    'cy': cy,
                    'radio_base': radio,
                    'fase': i * 0.5
                })
    
    def crear_arbol_holografico(self):
        """Crear árbol de Navidad holográfico"""
        cx = 700
        base_y = 600
        
        # Tronco holográfico
        self.canvas.create_rectangle(
            cx-15, base_y, cx+15, base_y+40,
            fill='', outline='#00ffff', width=3
        )
        
        # Triángulos del árbol con efecto wireframe
        niveles = [
            (80, base_y-30),
            (110, base_y-90),
            (140, base_y-150),
            (170, base_y-210)
        ]
        
        self.triangulos_arbol = []
        for ancho, y in niveles:
            triangulo = self.canvas.create_polygon(
                cx, y-50,
                cx-ancho, y,
                cx+ancho, y,
                fill='', outline='#00ff41', width=3
            )
            self.triangulos_arbol.append(triangulo)
        
        # Estrella holográfica
        self.crear_estrella_holografica(cx, base_y-260, 30)
        
        # Luces LED del árbol
        self.luces_led = []
        for nivel in range(4):
            y = base_y - 30 - (nivel * 60)
            num_luces = 3 + nivel
            for i in range(num_luces):
                x = cx + (i - num_luces//2) * 40
                color = random.choice(['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'])
                luz = self.canvas.create_oval(
                    x-5, y-5, x+5, y+5,
                    fill=color, outline=color, width=2
                )
                self.luces_led.append({
                    'id': luz,
                    'color': color,
                    'fase': random.random() * math.pi * 2
                })
    
    def crear_estrella_holografica(self, cx, cy, radio):
        """Crear estrella con efecto holográfico"""
        puntos = []
        for i in range(10):
            angulo = (i * math.pi / 5) - math.pi / 2
            r = radio if i % 2 == 0 else radio / 2
            x = cx + r * math.cos(angulo)
            y = cy + r * math.sin(angulo)
            puntos.extend([x, y])
        
        self.estrella_arbol = self.canvas.create_polygon(
            puntos,
            fill='#ffff00', outline='#ffff00', width=2
        )
    
    def crear_rayos_laser(self):
        """Crear rayos láser animados"""
        for _ in range(5):
            y = random.randint(200, 700)
            rayo = self.canvas.create_line(
                0, y, 1400, y,
                fill='#ff00ff', width=2, stipple='gray50'
            )
            self.rayos_laser.append({
                'id': rayo,
                'y': y,
                'velocidad': random.uniform(2, 5),
                'visible': True
            })
    
    def ondas_expansion(self):
        """Crear ondas de expansión"""
        if random.random() < 0.05:
            x = random.randint(200, 1200)
            y = random.randint(200, 700)
            
            for i in range(3):
                onda = self.canvas.create_oval(
                    x-5, y-5, x+5, y+5,
                    outline=random.choice(['#00ffff', '#ff00ff', '#ffff00']),
                    width=2
                )
                self.ondas.append({
                    'id': onda,
                    'x': x,
                    'y': y,
                    'radio': 5,
                    'velocidad': 3 + i,
                    'vida': 50
                })
        
        self.root.after(100, self.ondas_expansion)
    
    def crear_panel_control(self):
        """Crear panel de control tecnológico"""
        panel = tk.Frame(self.root, bg='#000000')
        panel.place(relx=0.5, rely=0.93, anchor='center')
        
        botones = [
            ("⚡ EXPLOSIÓN", lambda: self.crear_explosion_particulas(700, 450), '#ff00ff'),
            ("🎵 MÚSICA", self.reproducir_musica, '#00ffff'),
            ("🚀 LÁSER", self.activar_laser_show, '#ffff00'),
            ("⛶ FULLSCREEN", self.toggle_fullscreen, '#00ff41'),
            ("❌ SALIR", self.root.quit, '#ff0000')
        ]
        
        for texto, comando, color in botones:
            btn = tk.Button(
                panel,
                text=texto,
                command=comando,
                font=('Courier New', 11, 'bold'),
                bg='#000000',
                fg=color,
                padx=15,
                pady=8,
                relief=tk.FLAT,
                bd=2,
                highlightthickness=2,
                highlightbackground=color,
                cursor='hand2',
                activebackground='#111111',
                activeforeground=color
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Instrucciones
        self.canvas.create_text(
            700, 870,
            text="[F11] Pantalla Completa | [ESC] Salir | [ESPACIO] Explosión",
            font=('Courier New', 10),
            fill='#00ff41'
        )
    
    def animacion_principal(self):
        """Animación principal del sistema"""
        self.time += 0.05
        self.hue = (self.hue + 0.003) % 1.0
        
        # Animar estrellas
        for estrella in self.estrellas:
            estrella['brillo'] = (math.sin(self.time * 2 + estrella['x'] * 0.01) + 1) / 2
            color = self.hsv_to_rgb_hex(self.hue, 0.8, estrella['brillo'])
            self.canvas.itemconfig(estrella['id'], fill=color, outline=color)
        
        # Animar partículas flotantes
        for particula in self.particulas:
            particula['x'] += particula['vx']
            particula['y'] += particula['vy']
            
            # Rebotar en bordes
            if particula['x'] < 0 or particula['x'] > 1400:
                particula['vx'] *= -1
            if particula['y'] < 0 or particula['y'] > 900:
                particula['vy'] *= -1
            
            self.canvas.coords(
                particula['id'],
                particula['x']-particula['size']//2,
                particula['y']-particula['size']//2,
                particula['x']+particula['size']//2,
                particula['y']+particula['size']//2
            )
        
        # Animar círculos neón
        for circulo in self.circulos_neon:
            radio = circulo['radio_base'] + math.sin(self.time * 2 + circulo['fase']) * 10
            self.canvas.coords(
                circulo['id'],
                circulo['cx']-radio, circulo['cy']-radio,
                circulo['cx']+radio, circulo['cy']+radio
            )
        
        # Animar luces LED
        for luz in self.luces_led:
            luz['fase'] += 0.1
            brillo = (math.sin(luz['fase']) + 1) / 2
            # Convertir color hex a RGB y ajustar brillo
            color_base = luz['color']
            self.canvas.itemconfig(luz['id'], fill=color_base if brillo > 0.5 else '#333333')
        
        # Animar rayos láser
        for rayo in self.rayos_laser:
            coords = self.canvas.coords(rayo['id'])
            if coords:
                rayo['y'] += rayo['velocidad']
                if rayo['y'] > 900:
                    rayo['y'] = 0
                self.canvas.coords(rayo['id'], 0, rayo['y'], 1400, rayo['y'])
        
        # Animar ondas
        ondas_activas = []
        for onda in self.ondas:
            onda['radio'] += onda['velocidad']
            onda['vida'] -= 1
            
            if onda['vida'] > 0:
                self.canvas.coords(
                    onda['id'],
                    onda['x']-onda['radio'], onda['y']-onda['radio'],
                    onda['x']+onda['radio'], onda['y']+onda['radio']
                )
                ondas_activas.append(onda)
            else:
                self.canvas.delete(onda['id'])
        self.ondas = ondas_activas
        
        # Animar fuegos artificiales
        self.animar_fuegos_artificiales()
        
        self.root.after(30, self.animacion_principal)
    
    def pulso_titulo(self):
        """Efecto de pulso en el título"""
        color = self.hsv_to_rgb_hex((self.time * 0.5) % 1.0, 1.0, 1.0)
        self.canvas.itemconfig(self.titulo, fill=color)
        
        # Efecto glitch aleatorio
        if random.random() < 0.05:
            offset = random.randint(-5, 5)
            coords = self.canvas.coords(self.titulo)
            self.canvas.coords(self.titulo, coords[0] + offset, coords[1])
            self.root.after(50, lambda: self.canvas.coords(self.titulo, 700, 80))
        
        self.root.after(100, self.pulso_titulo)
    
    def actualizar_countdown(self):
        """Actualizar cuenta regresiva"""
        now = datetime.now()
        christmas = datetime(now.year, 12, 25)
        
        if now > christmas:
            christmas = datetime(now.year + 1, 12, 25)
        
        diff = christmas - now
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60
        
        if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
            texto = "[[ 🎉 NAVIDAD INICIADA 🎉 ]]"
        elif days == 0:
            texto = f"[[ TIEMPO: {hours:02d}:{minutes:02d}:{seconds:02d} ]]"
        else:
            texto = f"[[ DÍAS: {days} | HORAS: {hours:02d}:{minutes:02d}:{seconds:02d} ]]"
        
        self.canvas.itemconfig(self.countdown_text, text=texto)
        self.root.after(1000, self.actualizar_countdown)
    
    def crear_explosion_particulas(self, cx, cy):
        """Crear explosión de partículas"""
        for i in range(50):
            angulo = (i / 50) * 2 * math.pi
            velocidad = random.uniform(5, 15)
            color = random.choice(['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'])
            
            particula = self.canvas.create_oval(
                cx-3, cy-3, cx+3, cy+3,
                fill=color, outline=color
            )
            
            self.fuegos_artificiales.append({
                'id': particula,
                'x': cx,
                'y': cy,
                'dx': math.cos(angulo) * velocidad,
                'dy': math.sin(angulo) * velocidad,
                'vida': 60,
                'gravedad': 0.3
            })
    
    def animar_fuegos_artificiales(self):
        """Animar fuegos artificiales"""
        fuegos_activos = []
        
        for fuego in self.fuegos_artificiales:
            fuego['x'] += fuego['dx']
            fuego['y'] += fuego['dy']
            fuego['dy'] += fuego['gravedad']
            fuego['vida'] -= 1
            
            if fuego['vida'] > 0:
                self.canvas.coords(
                    fuego['id'],
                    fuego['x']-3, fuego['y']-3,
                    fuego['x']+3, fuego['y']+3
                )
                fuegos_activos.append(fuego)
            else:
                self.canvas.delete(fuego['id'])
        
        self.fuegos_artificiales = fuegos_activos
    
    def activar_laser_show(self):
        """Activar show de láser"""
        for _ in range(10):
            x1, y1 = random.randint(0, 1400), random.randint(0, 900)
            x2, y2 = random.randint(0, 1400), random.randint(0, 900)
            color = random.choice(['#ff0000', '#00ff00', '#0000ff', '#ff00ff', '#ffff00'])
            
            laser = self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color, width=3
            )
            
            self.root.after(500, lambda l=laser: self.canvas.delete(l))
        
        self.crear_explosion_particulas(700, 450)
    
    def reproducir_musica(self):
        """Reproducir música"""
        messagebox.showinfo(
            "🎵 SISTEMA DE AUDIO",
            ">>> REPRODUCIENDO VILLANCICOS TECNOLÓGICOS <<<\n\n" +
            "🎵 JINGLE BELLS [REMIX ELECTRÓNICO] 🎵\n\n" +
            "VOLUMEN: ████████████ 100%\n" +
            "ESTADO: [ACTIVO]"
        )
        
        # Explosión múltiple
        for i in range(5):
            self.root.after(i * 200, lambda: self.crear_explosion_particulas(
                random.randint(200, 1200),
                random.randint(200, 700)
            ))
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = NavidadTecnologica()
    app.ejecutar()