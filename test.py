import pyxel


class App:
    def __init__(self):
        self.window = MainMenu(self)
        pyxel.init(128, 128, caption="Simple Block Break!!")
        pyxel.sound(0).set(
            "g-2",
            "p",
            "2",
            "n",
            10
        )
        pyxel.sound(1).set(
            "b-2",
            "p",
            "2",
            "n",
            15
        )
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.window != None:
            self.window.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        if self.window != None:
            self.window.draw()

    def setWindow(self, window):
        self.window = None
        self.window = window


class Window:

    def __init__(self, app):
        self.app = app

    def update(self):
        pass

    def draw(self):
        pass


class MainMenu(Window):
    def __init__(self, app):
        self.select = 0
        self.select_max = 0
        super().__init__(app)
        pass

    def draw(self):
        pyxel.cls(0)
        #pyxel.rectb(20, 27, 100, 13, 6)
        pyxel.text(24, 32, "Simple Block Break!!", pyxel.frame_count % 8 + 8)

        pyxel.text(54, 80, "Play", 7)
        #pyxel.text(51, 90, "Normal", 7)
        #pyxel.text(54, 100, "Play", 7)

        cursor_x = 0
        cursor_y = 0
        if self.select == 0:
            cursor_x = 50
            cursor_y = 80
        elif self.select == 1:
            cursor_x = 47
            cursor_y = 90
        elif self.select == 2:
            cursor_x = 50
            cursor_y = 100
        pyxel.text(cursor_x, cursor_y, ">", 7)

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.select += 1
            pyxel.play(0, 0)
        elif pyxel.btnp(pyxel.KEY_UP):
            self.select -= 1
            pyxel.play(0, 0)
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.decision()

        if self.select_max < self.select:
            self.select = 0
        elif self.select < 0:
            self.select = self.select_max

    def decision(self):
        if self.select == 0:
            self.app.setWindow(GameWindow(self.app))
            pass
        pyxel.play(0, 1)


class GameWindow(Window):

    def __init__(self, app):
        super().__init__(app)
        self.objects = []
        for x in range(5):
            for y in range(5):
                self.objects.append(Block(6 + x * 24, 3 + y * 10))
        self.objects.append(Paddle())
        self.objects.append(Ball(self, 64, 64))

    def draw(self):
        pyxel.cls(0)
        for objectInstance in self.objects:
            objectInstance.draw()
            objectInstance.update()

    def getObjects(self):
        return self.objects


class Entity:

    def __init__(self, minx, maxx, miny, maxy):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def draw(self):
        pass

    def update(self):
        pass

    def isInside(self, x, y):
        return (self.minx <= x and x <= self.maxx) and (self.miny <= y and y <= self.maxy)


class Block(Entity):

    def __init__(self, x, y):
        height = 6
        width = 20
        self.color = 13
        super().__init__(x, x+width, y, y+height)

    def draw(self):
        pyxel.rect(self.minx, self.miny, self.maxx - self.minx, self.maxy - self.miny, self.color)


class Paddle(Entity):

    def __init__(self):
        self.width = 32
        self.height = 4
        self.color = 12
        super().__init__(0, 0, 100, 100 + self.height)

    def update(self):
        pyxel.text(0, 0, str(pyxel.mouse_x), 7)
        self.minx = pyxel.mouse_x
        self.maxx = pyxel.mouse_x + self.width

    def draw(self):
        pyxel.rect(self.minx, self.miny, self.maxx - self.minx, self.maxy - self.miny, self.color)

class Ball:

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.mx = 1
        self.my = 2
        pass

    def update(self):
        self.x += self.mx
        self.y += self.my
        if self.x > 126 or self.x < 8:
            self.mx *= -1
        if self.y > 126 or self.y < 8:
            self.my *= -1
        for gameObject in self.game.getObjects():
            if gameObject != self:
                if gameObject.isInside(self.x, self.y):
                    self.mx *= -1
                    self.my *= -1
                    break

        pass

    def draw(self):
        pyxel.circ(self.x - 4, self.y - 4, 4, 8)
        pass

App()