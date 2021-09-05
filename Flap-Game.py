from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import turtle
import random

kv = '''
<Windmanage>:

    Screen:
        name: "first"
        orientation: "horizontal"
        Label:
            text: root.dis_text
            color: 0,1,0.9,1
            font_size: 200
            pos_hint: {"x": 0.01, "y": 0.04}
            size_hint_y: 1
        ProgressBar:
            color: 0.2,0.4,0.5,0.5
            max: 8
            min: 0
            value: root.vlv
            pos_hint: {"x": 0, "top": 0.7}
            size_hint_y: 1

    Screen:
        name: "second"
        FloatLayout:
            Image:
                source: "img_bg1.png"
                allow_stretch: True
                keep_ratio: False
            Button:
                background_normal: "img_bg1.png"
                background_color: [2,0,2,1]
                text: "Play"
                pos_hint: {"x": 0.03 , "y":root.sz_y}
                size_hint: root.siz
                font_size: root.fnt
                font_weight: "bold"
                color: root.clr
                on_press:
                    root.strt_game()

            Button:
                background_normal: "img_bg1.png"
                text: "Help"
                pos_hint: {"x": 0.35 , "y": root.sz_y}
                size_hint: root.siz
                font_size: root.fnt
                color: root.clr
                on_press:
                    root.current = "third"
                    root.transition.direction = "left"
            Button:
                background_normal: "img_bg1.png"
                text: "Quit"
                pos_hint: {"x": 0.65 , "y": root.sz_y}
                size_hint: root.siz
                font_size: root.fnt
                color: root.clr
                on_press:
                    root.op_pop()

    Screen:
        name: "third"
        FloatLayout:
            Label:
                pos_hint: { "x": 0.3 , "y": 0.41}
                size_hint: 0.4, 0.8
                text: "How to Play!"
                font_size: 100
                font_weight: "bold"
                color: 0.5,0,0.4,1
            Label:
                pos_hint: { "x": 0.4 , "y": 0.38}
                size_hint: 0.2, 0.4
                text: "Press: SpaceBar to make it fly"
                font_size: 30
                color: 0.5,0.8,0,1
            Button:
                pos_hint: { "x": 0.4 , "y": 0.2}
                size_hint: 0.2, 0.1
                text: "Go Back"
                background_color: (0.5,0.8,0.1,1)
                on_press:
                    root.current = "second"
                    root.transition.direction = "right"

'''
class Windmanage(ScreenManager):
    dis_text = StringProperty("")
    vlv = NumericProperty("0")
    # Button pos y
    sz_y = NumericProperty("0.4")
    # Button Size
    siz = (0.3,0.3)
    # font of btn
    fnt = NumericProperty("30")
    # Button color
    clr = [0.9,0,0.2,1]
    def strt_game(self):
        App.get_running_app().root_window.minimize()
        playing()
    def clicked_max(self):
        App.get_running_app().root_window.maximize()
    def op_pop(self):
        show = wind_pop()
        Popup(title="Exit", content=show, size_hint=(0.4,0.3)).open()

def playing():
    # screen
    global wn
    wn = turtle.Screen()
    rootwindow = wn.getcanvas().winfo_toplevel()
    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
    wn.setup(1000, 700)
    wn.title("Flap-Flap")
    wn.bgcolor("#25f46a")

    # border
    brd = turtle.Turtle()
    brd.hideturtle()
    brd.speed(0)
    brd.pensize(4)
    brd.color("white")
    brd.pu()
    brd.setpos(-232, -230)
    brd.pd()
    brd.color("cyan")
    brd.begin_fill()
    brd.fd(460)
    brd.lt(90)
    brd.fd(520)
    brd.lt(90)
    brd.fd(460)
    brd.lt(90)
    brd.fd(520)
    brd.lt(90)
    brd.end_fill()
    # player
    player = turtle.Turtle()
    player.pu()
    player.setpos(-150, 0)
    player.color("white")
    player.shape("square")
    player.speed(10)
    playermovey = -5
    playermovex = 35
    life = 1
    # pillars
    p1 = turtle.Turtle()
    p1.ht()
    p1.pu()
    p1.color("#25f46a")
    p1.shape("square")
    p1.resizemode("user")
    p1.setpos(0, 250)
    p1.shapesize(20, 2)
    p1.st()

    p2 = turtle.Turtle()
    p2.ht()
    p2.pu()
    p2.shape("square")
    p2.color("#25f46a")
    p2.resizemode("user")
    p2.setpos(0, -250)
    p2.shapesize(20, 2)
    p2.st()
    p3 = turtle.Turtle()
    p3.ht()
    p3.pu()
    p3.color("#25f46a")
    p3.shape("square")
    p3.resizemode("user")
    p3.setpos(180, 350)
    p3.shapesize(20, 2)
    p3.st()

    p4 = turtle.Turtle()
    p4.ht()
    p4.pu()
    p4.shape("square")
    p4.color("#25f46a")
    p4.resizemode("user")
    p4.setpos(180, -150)
    p4.shapesize(20, 2)
    p4.st()

    global score
    score = 0

    # player movements
    def fly():
        x = player.ycor()
        x += playermovex
        player.sety(x)

    while life != 0:
        wn.onkey(fly, "space")
        wn.listen()
        # collision
        if (player.xcor() + 10 > p1.xcor() - 25) and (player.xcor() - 10 < p1.xcor() + 25):
            if (player.ycor() + 10 > p1.ycor() - 210) or (player.ycor() - 10 < p2.ycor() + 210):
                life -= 1
        if (player.xcor() + 10 > p3.xcor() - 25) and (player.xcor() - 10 < p3.xcor() + 25):
            if (player.ycor() + 10 > p3.ycor() - 210) or (player.ycor() - 10 < p4.ycor() + 210):
                life -= 1
        if player.ycor() <= -220:
            life -= 1

        p1.backward(3)
        p2.backward(3)
        p3.backward(3)
        p4.backward(3)

        y = player.ycor()
        y += playermovey
        player.sety(y)

        hght1 = random.randrange(90, 450, 20)
        hght2 = hght1 - 500
        if p1.xcor() - 15 < -220:
            p1.speed(0)
            p2.speed(0)
            p1.ht()
            p2.ht()
            score += 1
            p1.setpos(160, hght1)
            p2.setpos(160, hght2)
            p2.st()
            p1.st()

        hght1 = random.randrange(90, 450, 20)
        hght2 = hght1 - 500
        if p3.xcor() - 15 < -220:
            p3.speed(0)
            p4.speed(0)
            p3.ht()
            p4.ht()
            score += 1
            p3.setpos(160, hght1)
            p4.setpos(160, hght2)
            p3.st()
            p4.st()
    if life == 0:
        wn.setup(0,0)
        App.get_running_app().root_window.maximize()
        displ = dis_turt_pop()
        Popup(title = "Well done!", content = displ, size_hint=(0.4,0.4)).open()
class dis_turt_pop(GridLayout):
    def __init__(self):
        super(dis_turt_pop, self).__init__()
        self.cols = 2
        self.lba = Label(text = "Pillars Crossed: ", font_size=30)
        self.add_widget(self.lba)
        self.lba2 = Label(text = str(score), font_size=30)
        self.add_widget(self.lba2)



class wind_pop(GridLayout):
    def __init__(self, **kwargs):
        super(wind_pop, self).__init__(**kwargs)
        self.cols = 1
        self.lbl = Label(text="Are you sure?", font_size=20)
        self.add_widget(self.lbl)
        self.grd = GridLayout()
        self.grd.cols = 1
        self.grd.btn1 = Button(text = "Yes", on_press = lambda dt: self.clicked_close())
        self.grd.add_widget(self.grd.btn1)
        self.add_widget(self.grd)
    def clicked_close(self):
        App.get_running_app().stop()



Builder.load_string(kv)

class Runapp(App):
    def build(self):
        self.title = "Flap-Flap"
        Clock.schedule_once(lambda dt: self.open_max(), 0)
        # 2
        Clock.schedule_once(lambda dt: self.on_op(), 2)
        # 3
        Clock.schedule_once(lambda dt:self.on_st_clock(), 3)
        # 7.5
        Clock.schedule_once(lambda dt: self.ch_scr(), 7.5)
        return Windmanage()

    def open_max(self):
        App.get_running_app().root_window.maximize()

    def ch_scr(self):
        self.root.current = "second"

    def on_st_clock(self):
        # 1
        Clock.schedule_interval(lambda dt: self.in_pb(), 1)

    def on_op(self):
        self.root.dis_text = "Flap-Flap"
    def in_pb(self):
        self.root.vlv+=2
if __name__ == "__main__":
    Runapp().run()
