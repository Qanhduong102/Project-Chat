import pygame
import math
import random
import colorsys


class AdvancedVisualizer:
    def __init__(self):
        pygame.init()
        # Tạo cửa sổ lớn hơn cho hiệu ứng đẹp hơn
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Advanced Voice Assistant")

        # Khởi tạo màu sắc động
        self.hue = 0.6  # Bắt đầu với màu xanh
        self.colors = self.generate_colors()

        # Các thông số hiệu ứng
        self.orb_radius = 60
        self.is_listening = False
        self.particles = []
        self.waves = []
        self.energy_rings = []
        self.time = 0

        # Khởi tạo particles với nhiều hiệu ứng hơn
        self.init_particles()

        # Font chữ đẹp hơn
        try:
            self.font = pygame.font.SysFont('Segoe UI', 36)
        except pygame.error:  # Sửa lỗi quá chung chung
            self.font = pygame.font.Font(None, 36)

    def generate_colors(self):
        """Tạo bảng màu gradient động"""
        colors = []
        for i in range(360):
            rgb = colorsys.hsv_to_rgb((self.hue + i / 1000) % 1, 0.8, 1)
            colors.append([int(c * 255) for c in rgb])
        return colors

    def init_particles(self):
        """Khởi tạo các hạt với nhiều thuộc tính hơn"""
        for _ in range(30):
            self.particles.append({
                'x': self.width // 2,
                'y': self.height // 2,
                'angle': random.uniform(0, math.pi * 2),
                'speed': random.uniform(2, 6),
                'size': random.uniform(2, 5),
                'alpha': random.randint(100, 255),
                'orbit': random.uniform(80, 120),
                'phase': random.uniform(0, math.pi * 2)
            })

    def create_energy_ring(self):
        """Tạo vòng năng lượng mới"""
        self.energy_rings.append({
            'radius': self.orb_radius,
            'alpha': 255,
            'width': random.uniform(2, 4),
            'color_offset': random.uniform(0, 360)
        })

    def draw_orb(self):
        """Vẽ quả cầu chính với hiệu ứng gradient động"""
        center = (self.width // 2, self.height // 2)

        # Hiệu ứng glow
        max_radius = self.orb_radius + 30
        for radius in range(max_radius, self.orb_radius - 10, -2):
            alpha = int(100 * (1 - (radius - self.orb_radius) / 40))
            color = self.colors[int(self.time * 50) % 360]
            glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*color, alpha), (radius, radius), radius)
            self.screen.blit(glow_surface, (center[0] - radius, center[1] - radius))

        # Core của orb
        pygame.draw.circle(self.screen, self.colors[int(self.time * 50) % 360], center, self.orb_radius)

        # Hiệu ứng highlight
        highlight_pos = (center[0] - self.orb_radius // 3, center[1] - self.orb_radius // 3)
        highlight_surface = pygame.Surface((self.orb_radius // 2, self.orb_radius // 2), pygame.SRCALPHA)
        pygame.draw.circle(highlight_surface, (255, 255, 255, 100),
                           (self.orb_radius // 4, self.orb_radius // 4),
                           self.orb_radius // 4)
        self.screen.blit(highlight_surface, highlight_pos)

    def update_particles(self):
        """Cập nhật và vẽ các hạt với chuyển động phức tạp hơn"""
        center = (self.width // 2, self.height // 2)

        for particle in self.particles:
            if self.is_listening:
                # Chuyển động phức tạp
                orbit = particle['orbit'] * (1 + 0.2 * math.sin(self.time * 2 + particle['phase']))
                particle['x'] = center[0] + math.cos(particle['angle']) * orbit
                particle['y'] = center[1] + math.sin(particle['angle']) * orbit
                particle['angle'] += particle['speed'] / 50
                particle['alpha'] = 150 + 100 * math.sin(self.time * 3 + particle['phase'])

                # Vẽ particle với hiệu ứng glow
                size = particle['size'] * (1 + 0.2 * math.sin(self.time * 4 + particle['phase']))
                for r in range(int(size * 2), 0, -1):
                    alpha = int(particle['alpha'] * (r / (size * 2)))
                    color = self.colors[int((self.time * 100 + particle['phase'] * 50) % 360)]
                    surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface, (*color, alpha), (r, r), r)
                    self.screen.blit(surface, (particle['x'] - r, particle['y'] - r))

    def update_energy_rings(self):
        """Cập nhật và vẽ các vòng năng lượng"""
        center = (self.width // 2, self.height // 2)

        for ring in self.energy_rings[:]:
            if ring['alpha'] > 0:
                color = self.colors[int((self.time * 100 + ring['color_offset']) % 360)]
                surface = pygame.Surface((ring['radius'] * 2, ring['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*color, ring['alpha']),
                                   (ring['radius'], ring['radius']), ring['radius'],
                                   int(ring['width']))
                self.screen.blit(surface, (center[0] - ring['radius'], center[1] - ring['radius']))

                ring['radius'] += 4
                ring['alpha'] = max(0, ring['alpha'] - 3)
                ring['width'] *= 1.02
            else:
                self.energy_rings.remove(ring)

    def draw_status(self):
        """Vẽ text trạng thái với hiệu ứng gradient"""
        text = "I'm listening..." if self.is_listening else "Press the button"
        color = self.colors[int(self.time * 50) % 360]
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_listening = not self.is_listening
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Cập nhật thời gian và màu sắc
            self.time += 0.02
            self.hue = (self.hue + 0.001) % 1
            self.colors = self.generate_colors()

            # Xóa màn hình với hiệu ứng fade
            self.screen.fill((0, 0, 0))

            # Vẽ các thành phần
            self.draw_orb()
            self.update_particles()

            if self.is_listening:
                if random.random() < 0.1:
                    self.create_energy_ring()
            self.update_energy_rings()

            self.draw_status()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    visualizer = AdvancedVisualizer()
    visualizer.run()
