import math
import time
import os
import matplotlib.pyplot as plt

plt.ion()
fig, ax = plt.subplots()
scatter = None

UNIVERSAL_GRAVITATIONAL_CONSTANT = 6.67e-11
G = UNIVERSAL_GRAVITATIONAL_CONSTANT
delta_t = 0.1  # 1 Second


class Vector2D:
    def __init__(self, pos_x: float = 0, pos_y: float = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def distance(self, other: "Vector2D"):
        x_squared = (self.pos_x - other.pos_x) ** 2
        y_squared = (self.pos_y - other.pos_y) ** 2
        return math.sqrt(x_squared + y_squared)

    def __sub__(self, other: "Vector2D"):
        temp = Vector2D()
        temp.pos_x = self.pos_x - other.pos_x
        temp.pos_y = self.pos_y - other.pos_y
        return temp

    def __add__(self, other: "Vector2D"):
        temp = Vector2D()
        temp.pos_x = self.pos_x + other.pos_x
        temp.pos_y = self.pos_y + other.pos_y
        return temp

    def __str__(self) -> str:
        return f"({self.pos_x},{self.pos_y})"

    def __iadd__(self, other: "Vector2D"):
        self.pos_x += other.pos_x
        self.pos_y += other.pos_y
        return self

    def __mul__(self, scalar: float):
        return Vector2D(self.pos_x * scalar, self.pos_y * scalar)


class Body:
    numberOfBodies = 0
    bodydict: dict[str, "Body"] = {}

    def __init__(
        self,
        name: str,
        position: "Vector2D",
        mass: float = 1,
        velocity: "Vector2D" = Vector2D(),
    ):
        # Let's assume that the body is circular
        self.name = name
        self.position = position  # Meters
        assert mass > 0, "Mass must be greater than 0"
        self.mass = mass  # KGS
        self.velocity = velocity if velocity else Vector2D(0, 0)
        # self.angle = math.atan(self.position.pos_y / self.position.pos_x)
        Body.numberOfBodies += 1
        Body.bodydict[self.name] = self

    def __str__(self) -> str:
        retstring = f"""Body {self.name}\n
                        Mass: {self.mass} KG\n
                        Velocity: {self.velocity} m/s\n
                        Position: {self.position}\n"""

        return retstring


def compute_gravitational_force(body: Body) -> "Vector2D":
    force = Vector2D()
    for other in Body.bodydict.values():
        if other.name == body.name:
            continue
        r_vector = other.position - body.position
        distance = body.position.distance(other.position)
        if distance == 0:
            continue  # Avoid divide by zero
        force_magnitude = (G * body.mass * other.mass) / (distance**2)
        # Normalize direction
        force.pos_x += force_magnitude * (r_vector.pos_x / distance)
        force.pos_y += force_magnitude * (r_vector.pos_y / distance)
    return force


def update_position(body: Body):
    force = compute_gravitational_force(body)
    acceleration = Vector2D(force.pos_x / body.mass, force.pos_y / body.mass)

    # s = vt + 0.5at^2
    displacement = Vector2D()
    displacement.pos_x = (
        body.velocity.pos_x * delta_t + 0.5 * acceleration.pos_x * delta_t**2
    )
    displacement.pos_y = (
        body.velocity.pos_y * delta_t + 0.5 * acceleration.pos_y * delta_t**2
    )

    # Update position
    body.position += displacement

    # Update velocity: v = v + at
    body.velocity.pos_x += acceleration.pos_x * delta_t
    body.velocity.pos_y += acceleration.pos_y * delta_t


count = 0
mass = 1e24
distance = 1e9  # meters between bodies

# Place them in an equilateral triangle
B1 = Body(
    name="B1",
    mass=mass,
    velocity=Vector2D(0, 1000),  # upward
    position=Vector2D(-distance / 2, -distance * math.sqrt(3) / 6),
)

B2 = Body(
    name="B2",
    mass=mass,
    velocity=Vector2D(866, -500),  # down-right
    position=Vector2D(distance / 2, -distance * math.sqrt(3) / 6),
)

B3 = Body(
    name="B3",
    mass=mass,
    velocity=Vector2D(-866, -500),  # down-left
    position=Vector2D(0, distance * math.sqrt(3) / 3),
)


def visualize_bodies():
    global scatter
    ax.clear()
    ax.set_title("3-Body Simulation")
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")

    positions = [
        (body.position.pos_x, body.position.pos_y) for body in Body.bodydict.values()
    ]
    xs, ys = zip(*positions)

    # Auto-scale view with margin
    margin = 0.1
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    range_x = max_x - min_x
    range_y = max_y - min_y

    ax.set_xlim(min_x - range_x * margin, max_x + range_x * margin)
    ax.set_ylim(min_y - range_y * margin, max_y + range_y * margin)

    scatter = ax.scatter(xs, ys, c=["r", "g", "b"], s=100)

    plt.draw()
    plt.pause(0.001)


def mainloop() -> None:
    os.system("cls")
    for body in Body.bodydict.values():
        update_position(body)
        print(body)
    visualize_bodies()
    global count
    count += delta_t
    print(f"{count} Seconds passed.")
    time.sleep(delta_t)


for body in Body.bodydict.values():
    print(body)
input("Press Enter to Start Newtonian Simulation.")


while True:
    mainloop()
