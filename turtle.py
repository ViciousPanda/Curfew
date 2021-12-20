import turtle

""" Game Settings """
win = turtle.Screen()
win.title("Curfew")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

P_SPEED = 10

# Player
player = turtle.Turtle()
player.speed(0)
player.shape("circle")
player.color("white")
player.penup()
player.goto(-350, -250)


"""

# Environment
wall = turtle.Turtle()
wall.speed(0)
wall.shape("square")
wall.color("white")
# wall.shapesize(stretch_wid=20, stretch_len=1)
wall.penup()
wall.goto(-375, -275)

# Camera cones
camera = turtle.Turtle()
camera.speed(0)
camera.shape("triangle")
camera.color("white")
camera.penup()
camera.goto(350, -250)

"""

""" Player Movement Controls"""

def move(dir1, dir2)
    x = player.xcor()
    y = player.ycor()

    if dir1 and not dir2:

    dir

    player.setx(x)
    player.sety(y)


def move_up():
    y = player.ycor()
    y += P_SPEED
    player.sety(y)


def move_down():
    y = player.ycor()
    y -= P_SPEED
    player.sety(y)


def move_right():
    x = player.xcor()
    x += P_SPEED
    player.setx(x)


def move_left():
    x = player.xcor()
    x -= P_SPEED
    player.setx(x)


""" Keyboard Bindings """
win.listen()

# WASD
win.onkeypress(move_up, "w")
win.onkeypress(move_down, "s")
win.onkeypress(move_left, "a")
win.onkeypress(move_right, "d")

""" primary gameplay loop """
while True:
    win.update()
