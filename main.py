from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.app import App
from kivy.config import Config
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from random import sample
from random import random
from random import randint
from kivy.clock import Clock
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget


Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '634')

sm = ScreenManager(transition=FadeTransition(duration=0.04))

Builder.load_file("my.kv")


def letras(palavra):
    l = ["Primeira", "Segunda", "Terceira", "Quarta", "Quinta",
         "Sexta", "Sétima", "Oitava", "Nona", "Décima"]
    x = randint(0, len(palavra) - 1)
    return str(l[x] + " letra: " + palavra[x])




def transformar(decimal):
    a = int(decimal * 1000)
    return a/1000


ultimo_score = 0

class Touch(Widget):
    def on_touch_down(self, touch):
        print(touch)

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        pass

class ButtonL(ButtonBehavior, Image):
    pass


class CircularButtonE(ButtonBehavior, Label):
    pass


class CircularButtonC(ButtonBehavior, Label):
    pass


class Inicio(Screen):


    pass



class GameOver(Screen):
    us = NumericProperty(0)
    pont = "Pontuação: "
    def on_pre_enter(self, *args):
        self.us = ultimo_score
        if ultimo_score > 6:
            self.ids.letra.text = "Décimo dígito:\n2"
        elif ultimo_score > 4:
            self.ids.letra.text = "Nono dígito:\nR"
        elif ultimo_score > 2:
            self.ids.letra.text = "Oitavo dígito:\nY"
        else:
            self.ids.letra.text = "Nenhum dígito\nconquistado"
    pass

class Player(Image):
    source = "Hgame2.png"
    speed = NumericProperty(0)
    pass

class Obstaculo(Image):
    source = "gordura.png"
    scored = False
    gameScreen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = Animation(x= -self.width, duration=3)
        self.anim.bind(on_complete= self.vanish)
        self.anim.start(self)
        self.gameScreen = App.get_running_app().root.get_screen("game")

    def on_x(self, *args):
        if self.gameScreen:
            if self.x < self.gameScreen.ids.player.x and not self.scored:
                self.gameScreen.score += 0.5
                self.scored = True

    def vanish(self, *args):
        self.gameScreen.remove_widget(self)
        self.gameScreen.obstaculos.remove(self)


class Game(Screen):
    obstaculos = []
    score = NumericProperty(0)

    def on_enter(self, *args):
        Clock.schedule_interval(self.update,1/30)
        Clock.schedule_interval(self.putObstaculo, 1.4)

    def on_pre_enter(self, *args):
        self.ids.player.y = self.height/2
        self.ids.player.speed = 0
        self.score = 0

    def update(self, *args):
        global ultimo_score
        self.ids.player.speed += -self.height * 2 * 1/30
        self.ids.player.y += self.ids.player.speed * 1/30
        if self.ids.player.y > self.height or self.ids.player.y < 0:
            ultimo_score = self.score
            self.game0ver()
        elif self.playerCollided():
            ultimo_score = self.score
            self.game0ver()

    def putObstaculo(self, *args):
        gap = self.height*0.3
        position = (self.height-gap) * random()
        width = self.width*0.1
        obstaculoLow = Obstaculo(x = self.width, height=position, width= width)
        obstaculoHigh = Obstaculo(x=self.width, y=position + gap, height=self.height -position - gap, width= width)
        self.add_widget(obstaculoLow, 3)
        self.obstaculos.append(obstaculoLow)
        self.add_widget(obstaculoHigh, 3)
        self.obstaculos.append(obstaculoHigh)

    def game0ver(self):
        Clock.unschedule(self.update, 1/30)
        Clock.unschedule(self.putObstaculo, 1)
        App.get_running_app().root.current = "go"
        for ob in self.obstaculos:
            ob.anim.cancel(ob)
            self.remove_widget(ob)
        self.obstaculos = []

    def collided(self, wid1, wid2):
        if wid2.x <= wid1.x + wid1.width and \
            wid2.x + wid2.width >= wid1.x and \
            wid2.y <= wid1.y + wid1.height and \
            wid2.y + wid2.height >= wid1.y:
            return True
        return False

    def playerCollided(self):
        collided = False
        for obstacle in self.obstaculos:
            if self.collided(self.ids.player, obstacle):
                collided = True
                break
        return collided


    def on_touch_down(self, touch):
        self.ids.player.speed = self.height*0.7
    pass





sm.add_widget(Inicio(name='inicio'))
sm.add_widget(Game(name='game'))
sm.add_widget(GameOver(name='go'))


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()





