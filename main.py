import math
import logging
import arcade
import pymunk

from game_object import Bird, Column, Pig, YellowBird, BlueBird
from game_logic import get_impulse_vector, Point2D

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)

logger = logging.getLogger("main")

WIDTH = 1800
HEIGHT = 800
TITLE = "Angry birds"
GRAVITY = -900


class App(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/img/background3.png")
        # crear espacio de pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        # agregar piso
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 15], [WIDTH, 15], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.active_bird = None  # último pájaro lanzado (si está en vuelo)
        self.world = arcade.SpriteList()
        self.add_columns()
        self.add_pigs()

        self.score = 0
        self.level = 1

        self.start_point = Point2D()
        self.end_point = Point2D()
        self.distance = 0
        self.draw_line = False
        # colisiones (por fuerza de impacto)
        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length # fuerza del impacto, es arbiter porque puede haber varias colisiones
        if impulse_norm > 1200:
            for obj in self.world:
                if obj.shape in arbiter.shapes: 
                    # puntaje simple por destruir objetos
                    if isinstance(obj, Pig):
                        self.score += 100 # los cerdos valen más
                    elif isinstance(obj, Column):
                        self.score += 50 # las columnas valen menos

                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)

        return True

    def add_columns(self):
        for x in range(WIDTH // 2, WIDTH, 400):
            column = Column(x, 50, self.space)
            self.sprites.append(column)
            self.world.append(column)

    def add_pigs(self):
        pig1 = Pig(WIDTH / 2, 100, self.space)
        self.sprites.append(pig1)
        self.world.append(pig1)

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)  # actualiza la simulacion de las fisicas del jugo
        self.update_collisions()
        self.sprites.update(delta_time)
        # avanza de nivel si se alcanzo el puntaje
        if self.score >= 200 * self.level:
            self.level += 1
            # añade 2 columnas y UN cerdo sobre CADA columna nueva
            pig_tex_h = arcade.load_texture("assets/img/pig_failed.png").height
            pig_scale = 0.1
            pig_h = pig_tex_h * pig_scale # para que el pig quede justo arriba de la columna

            for i in range(2):
                x = WIDTH // 2 + 200 * i + 100 * self.level
                col = Column(x, 50, self.space)
                self.sprites.append(col) 
                self.world.append(col)
                # la parte superior de la columna + un margen 
                column_top_y = 50 + col.height / 2
                # coloca el cerdito centrado en X, arriba de la columna + un margen
                pig_y = column_top_y + pig_h / 2 + 6
                pig = Pig(x, pig_y, self.space)
                self.sprites.append(pig)
                self.world.append(pig)

    def update_collisions(self):
        # limpia pájaros fuera de la pantalla y el poder del pájaro que este en pantalla
        to_remove = []
        for b in self.birds:
            if b.center_x < -200 or b.center_x > WIDTH + 200 or b.center_y < -200 or b.center_y > HEIGHT + 200: # aqui se define que es "fuera de pantalla"
                to_remove.append(b)
        for b in to_remove:
            b.remove_from_sprite_lists()
            try: # la excepción puede darse si el pájaro ya fue eliminado
                self.space.remove(b.shape, b.body)
            except Exception:
                pass
            if self.active_bird is b:
                self.active_bird = None

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            triggered = False 

            # activa el poder especial del pájaro si se puede
            if not self.draw_line and self.active_bird is not None:
                if isinstance(self.active_bird, YellowBird) and not getattr(self.active_bird, "_boost_used", True):
                    self.active_bird.boost()
                    triggered = True
                elif isinstance(self.active_bird, BlueBird) and not getattr(self.active_bird, "_split_used", True):
                    self.active_bird.split(self)
                    triggered = True

            if triggered:
                return  # consumimos el click para el poder
            # si no hubo poder (o ya estaba gastado), se dibuja la línea de puntería
            self.start_point = Point2D(x, y) 
            self.end_point = Point2D(x, y)
            self.draw_line = True
            logger.debug(f"Start Point: {self.start_point}")

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT and self.draw_line: 
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if not self.draw_line: #si no apuntando, solo activa el poder con el click
                return
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            impulse_vector = get_impulse_vector(self.start_point, self.end_point)
            bird = Bird("assets/img/red-bird3.png", impulse_vector, x, y, self.space) #para escoger el pajaro rojo, este no tiene imagen por defecto como los otros
            #bird = YellowBird(impulse_vector, x, y, self.space) #para escoger el pajaro amarillo
            #bird = BlueBird(impulse_vector, x, y, self.space) #para escoger el pajaro azul
            self.sprites.append(bird)
            self.birds.append(bird)
            self.active_bird = bird # el último lanzado es el que puede usar su poder

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        self.sprites.draw()
        if self.draw_line:
            arcade.draw_line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y,
                             arcade.color.BLACK, 3)
        # dibuja el puntaje y nivel actual arriba a la izquierda (head up display)
        hud = f"Score: {self.score}   Level: {self.level}" 
        arcade.draw_text(hud, 16, HEIGHT - 32, arcade.color.WHITE, 18)

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = App()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()