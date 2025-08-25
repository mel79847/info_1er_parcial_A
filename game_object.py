import math
import arcade
import pymunk
from game_logic import ImpulseVector


class Bird(arcade.Sprite):
    """
    Bird class. This represents an angry bird. All the physics is handled by Pymunk,
    the init method only set some initial properties
    """
    def __init__(
        self,
        image_path: str,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 5,
        radius: float = 12,
        max_impulse: float = 100,
        power_multiplier: float = 50,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)
        # body
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)

        impulse = min(max_impulse, impulse_vector.impulse) * power_multiplier
        impulse_pymunk = impulse * pymunk.Vec2d(1, 0)
        # apply impulse
        body.apply_impulse_at_local_point(impulse_pymunk.rotated(impulse_vector.angle))
        # shape
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer

        space.add(body, shape)

        self.body = body
        self.shape = shape

    def update(self, delta_time):
        """
        Update the position of the bird sprite based on the physics body position
        """
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class Pig(arcade.Sprite):
    def __init__(
        self,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 0.4,
        collision_layer: int = 0,
    ):
        super().__init__("assets/img/pig_failed.png", 0.1)
        moment = pymunk.moment_for_circle(mass, 0, self.width / 2 - 3)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, self.width / 2 - 3)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self`, delta_time):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class PassiveObject(arcade.Sprite):
    """
    Passive object that can interact with other objects.
    """
    def __init__(
        self,
        image_path: str,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)

        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self, delta_time):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class Column(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/column.png", x, y, space)


class StaticObject(arcade.Sprite):
    def __init__(
            self,
            image_path: str,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 2,
            elasticity: float = 0.8,
            friction: float = 1,
            collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)

class YellowBird(Bird):
    """ un clic izquierdo mientras vuela añade impulso extra en la dirección en la que se mueve. 
    Asi el multiplicador se aplica sobre el impulso inicial solamente una vez"""
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        image_path: str = "assets/img/chuck.png",
        radius: float = 12,
        mass: float = 5,
        max_impulse: float = 100,
        power_multiplier: float = 35,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
        boost_multiplier: float = 2.0,
    ):
        # guardamos cuánto “valía” el impulso aplicado al inicio y lo multiplicamos por el poder
        self._applied_initial_impulse = min(max_impulse, abs(impulse_vector.impulse)) * power_multiplier 
        self._boost_used = False
        self._boost_multiplier = boost_multiplier
        super().__init__(
            image_path=image_path,
            impulse_vector=impulse_vector,
            x=x, y=y, space=space,
            radius=radius, mass=mass,
            max_impulse=max_impulse, power_multiplier=power_multiplier,
            elasticity=elasticity, friction=friction, collision_layer=collision_layer
        )
        # normaliza el tamaño de este sprite para que coincida con el ancho del rojo, ya que las texturas son de distintos tamaños
        try:
            ref_w = arcade.load_texture("assets/img/red-bird3.png").width  # ancho “ideal”
            cur_w = self.texture.width                                    # ancho de esta textura
            if cur_w > 0:
                self.scale = ref_w / cur_w
        except Exception:
            pass

    def boost(self):
        if self._boost_used:
            return
        # impulso extra = (mult - 1) * impulso_inicial_aplicado
        extra = (self._boost_multiplier - 1.0) * self._applied_initial_impulse
        # dirección actual de movimiento
        vel = self.body.velocity
        if vel.length < 1e-3:
            # si está casi quieto, usamos el ángulo del cuerpo (podría estar girando)
            direction = self.body.angle
        else:
            direction = vel.angle

        impulse_vec = extra * pymunk.Vec2d(1, 0)
        self.body.apply_impulse_at_local_point(impulse_vec.rotated(direction))
        self._boost_used = True


class BlueBird(Bird):
    """un clic izquierdo mientras vuela crea 2 pájaros extras con la MISMA velocidad, separados ±30 grados del pájaro original.
    Esto igual que el pajaro amarillo, solo se puede usar una vez por pájaro"""
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        image_path: str = "assets/img/blue.png",
        radius: float = 12,
        mass: float = 5,
        max_impulse: float = 100,
        power_multiplier: float = 35,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(
            image_path=image_path,
            impulse_vector=impulse_vector,
            x=x, y=y, space=space,
            radius=radius, mass=mass,
            max_impulse=max_impulse, power_multiplier=power_multiplier,
            elasticity=elasticity, friction=friction, collision_layer=collision_layer
        )
        self._split_used = False
        # normaliza el tamaño de este sprite para que coincida con el ancho del rojo ya que las texturas son de distintos tamaños
        try:
            ref_w = arcade.load_texture("assets/img/red-bird3.png").width  # ancho “ideal”
            cur_w = self.texture.width                                    # ancho de esta textura
            if cur_w > 0:
                self.scale = ref_w / cur_w # la escala es el factor por el cual se multiplica el tamaño original
        except Exception:
            pass

    def split(self, app):
        """ Esta funcion crea 2 pajaros azules extras, pero el pajaro original conserva su velocidad y dirección. 
        Los nuevos salen a ±30 grados con la MISMA rapidez, `app` se usa para agregarlos a sprites y a la lista de aves."""
        if self._split_used:
            return

        base_vel = self.body.velocity
        speed = base_vel.length

        # si está demasiado lento, no vale la pena dividir al pajaro 
        if speed < 1e-3:
            self._split_used = True
            return

        base_angle = base_vel.angle
        offsets_deg = (+30, -30) # grados de separación entre los nuevos pájaros y el original

        for off in offsets_deg:
            ang = base_angle + math.radians(off)
            # creamos con impulso 0 y luego asignamos la velocidad que querramos
            iv = ImpulseVector(angle=ang, impulse=0.0)
            b = BlueBird(
                impulse_vector=iv,
                x=self.center_x,
                y=self.center_y,
                space=app.space,
            )
            # asignamos la MISMA rapidez pero en el nuevo ángulo
            b.body.velocity = pymunk.Vec2d(speed, 0).rotated(ang)
            app.sprites.append(b) # para que se dibuje
            app.birds.append(b) # para que se actualice y se limpie igual que los demás

        self._split_used = True