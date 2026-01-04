import pygame
import math
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Logo Épico - Animación Extendida")
clock = pygame.time.Clock()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
PURPLE = (138, 43, 226)
BLUE = (0, 150, 255)

# Partículas mejoradas
class Particle:
    def __init__(self, x, y, color=WHITE):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 255
        self.size = random.randint(2, 6)
        self.color = color
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        self.life -= 2
        self.size = max(1, self.size - 0.03)
        
    def draw(self, surf):
        if self.life > 0:
            alpha = max(0, self.life)
            s = pygame.Surface((int(self.size * 2 + 4), int(self.size * 2 + 4)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, int(alpha * 0.3)), (int(self.size + 2), int(self.size + 2)), int(self.size + 2))
            pygame.draw.circle(s, (*self.color, int(alpha)), (int(self.size + 2), int(self.size + 2)), int(self.size))
            surf.blit(s, (int(self.x - self.size - 2), int(self.y - self.size - 2)))

# Líneas del logo con animación
class LogoLine:
    def __init__(self, start, end, delay=0, width=45):
        self.start_x, self.start_y = start
        self.end_x, self.end_y = end
        self.delay = delay
        self.progress = 0
        self.width = width
        self.current_width = 0
        self.particles = []
        self.glow_intensity = 0
        
    def update(self, time):
        if time > self.delay:
            elapsed = time - self.delay
            self.progress = min(1.0, elapsed / 2.0)
            self.current_width = self.width * min(1.0, elapsed / 0.8)
            self.glow_intensity = 255 * (1.0 - abs(self.progress - 0.5) * 2) if self.progress < 1 else 50
            
            # Generar más partículas
            if self.progress < 1.0 and random.random() < 0.5:
                curr_x = self.start_x + (self.end_x - self.start_x) * self.progress
                curr_y = self.start_y + (self.end_y - self.start_y) * self.progress
                for _ in range(3):
                    self.particles.append(Particle(curr_x, curr_y, CYAN))
        
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
    
    def draw(self, surf):
        if self.progress > 0:
            curr_x = self.start_x + (self.end_x - self.start_x) * self.progress
            curr_y = self.start_y + (self.end_y - self.start_y) * self.progress
            
            # Efecto de brillo múltiple
            glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for i in range(3):
                alpha = int(self.glow_intensity / (i + 1))
                width = int(self.current_width + (i + 1) * 15)
                color = CYAN if i == 0 else BLUE
                pygame.draw.line(glow_surf, (*color, alpha), (self.start_x, self.start_y), 
                               (curr_x, curr_y), width)
            surf.blit(glow_surf, (0, 0))
            
            # Línea principal
            pygame.draw.line(surf, WHITE, (self.start_x, self.start_y), 
                           (curr_x, curr_y), int(self.current_width))
        
        for p in self.particles:
            p.draw(surf)

# Centro del logo
center_x, center_y = WIDTH // 2, HEIGHT // 2
size = 200

# Definir las líneas exactas de tu logo (6 líneas formando el símbolo)
lines = [
    # Diagonal superior izquierda (de arriba-izquierda hacia el centro)
    LogoLine((center_x - size, center_y - size), (center_x + 20, center_y + 20), 0.5, 45),
    
    # Línea horizontal superior (de izquierda a derecha)
    LogoLine((center_x - size + 100, center_y - 40), (center_x + size, center_y - 40), 1.5, 45),
    
    # Diagonal superior derecha (de arriba-derecha hacia abajo-izquierda)
    LogoLine((center_x + size, center_y - size), (center_x - 80, center_y + 80), 2.5, 45),
    
    # Línea horizontal inferior (de izquierda a derecha)
    LogoLine((center_x - size, center_y + 40), (center_x + size - 100, center_y + 40), 3.5, 45),
    
    # Diagonal inferior izquierda (de abajo-izquierda hacia arriba-derecha)
    LogoLine((center_x - size, center_y + size), (center_x + 80, center_y - 80), 4.5, 45),
    
    # Diagonal inferior derecha (de abajo-derecha hacia el centro)
    LogoLine((center_x + size, center_y + size), (center_x - 20, center_y - 20), 5.5, 45),
]

# Ondas de impacto mejoradas
class ShockWave:
    def __init__(self, x, y, delay, max_radius=300):
        self.x = x
        self.y = y
        self.delay = delay
        self.radius = 0
        self.alpha = 255
        self.max_radius = max_radius
        
    def update(self, time):
        if time > self.delay:
            self.radius += 6
            progress = self.radius / self.max_radius
            self.alpha = max(0, int(255 * (1 - progress)))
    
    def draw(self, surf):
        if self.alpha > 0 and self.radius < self.max_radius:
            wave_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(wave_surf, (*PURPLE, int(self.alpha * 0.6)), 
                             (self.x, self.y), int(self.radius), 4)
            pygame.draw.circle(wave_surf, (*CYAN, int(self.alpha * 0.4)), 
                             (self.x, self.y), int(self.radius - 10), 2)
            surf.blit(wave_surf, (0, 0))

# Múltiples ondas en diferentes momentos
waves = []
for i in range(10):
    waves.append(ShockWave(center_x, center_y, i * 0.7, 300 + i * 20))

# Explosión de partículas central
class CentralExplosion:
    def __init__(self, x, y, delay):
        self.x = x
        self.y = y
        self.delay = delay
        self.particles = []
        self.triggered = False
        
    def update(self, time):
        if time > self.delay and not self.triggered:
            self.triggered = True
            for _ in range(100):
                self.particles.append(Particle(self.x, self.y, random.choice([WHITE, CYAN, PURPLE])))
        
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
    
    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)

explosions = [
    CentralExplosion(center_x, center_y, 7.0),
    CentralExplosion(center_x, center_y, 7.3),
]

# Estrellas de fondo
stars = []
for _ in range(150):
    stars.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': random.uniform(0.3, 1.5),
        'size': random.randint(1, 3),
        'brightness': random.randint(100, 255),
        'twinkle_speed': random.uniform(0.05, 0.15)
    })

# Flash de pantalla
class ScreenFlash:
    def __init__(self, delay, duration=0.3):
        self.delay = delay
        self.duration = duration
        self.alpha = 0
        
    def update(self, time):
        if time > self.delay and time < self.delay + self.duration:
            progress = (time - self.delay) / self.duration
            self.alpha = int(255 * math.sin(progress * math.pi))
        else:
            self.alpha = 0
    
    def draw(self, surf):
        if self.alpha > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((*WHITE, self.alpha))
            surf.blit(flash_surf, (0, 0))

flashes = [
    ScreenFlash(0.5, 0.2),
    ScreenFlash(7.0, 0.4),
]

# Loop principal
running = True
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()
                for line in lines:
                    line.progress = 0
                    line.particles = []
                for wave in waves:
                    wave.radius = 0
                    wave.alpha = 255
                for explosion in explosions:
                    explosion.triggered = False
                    explosion.particles = []
    
    current_time = (pygame.time.get_ticks() - start_time) / 1000.0
    
    screen.fill(BLACK)
    
    # Estrellas parpadeantes
    for star in stars:
        star['y'] += star['speed']
        if star['y'] > HEIGHT:
            star['y'] = 0
            star['x'] = random.randint(0, WIDTH)
        star['brightness'] += star['twinkle_speed'] * random.choice([-1, 1])
        star['brightness'] = max(50, min(255, star['brightness']))
        color = (star['brightness'], star['brightness'], star['brightness'])
        pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])
    
    # Flashes
    for flash in flashes:
        flash.update(current_time)
        flash.draw(screen)
    
    # Ondas
    for wave in waves:
        wave.update(current_time)
        wave.draw(screen)
    
    # Explosiones
    for explosion in explosions:
        explosion.update(current_time)
        explosion.draw(screen)
    
    # Líneas del logo
    for line in lines:
        line.update(current_time)
        line.draw(screen)
    
    # Pulso central continuo
    if current_time > 7.5:
        pulse = abs(math.sin(current_time * 2)) * 40 + 30
        pulse_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(pulse_surf, (*CYAN, 80), (center_x, center_y), int(pulse))
        pygame.draw.circle(pulse_surf, (*PURPLE, 60), (center_x, center_y), int(pulse * 0.7))
        screen.blit(pulse_surf, (0, 0))
    
    # Texto informativo
    font = pygame.font.Font(None, 32)
    if current_time > 8:
        alpha = min(255, int((current_time - 8) * 200))
        text_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        text = font.render("Presiona ESPACIO para reiniciar | ESC para salir", True, (*WHITE, alpha))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        text_surf.blit(text, text_rect)
        screen.blit(text_surf, (0, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()