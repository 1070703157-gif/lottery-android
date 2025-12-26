from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import random, time, os

PRICE = {
    "超级大乐透": 2,
    "双色球": 2,
    "排列三": 2,
    "排列五": 2,
    "福彩3D": 2
}

def hot_pool(start, end):
    pool = []
    for i in range(start, end + 1):
        pool += [i] * random.randint(1, 10)
    return pool

def pick(pool, n):
    s = set()
    while len(s) < n:
        s.add(random.choice(pool))
    return sorted(s)

def 大乐透():
    return f"前区 {pick(hot_pool(1,35),5)} 后区 {pick(hot_pool(1,12),2)}"

def 双色球():
    return f"红 {pick(hot_pool(1,33),6)} 蓝 {pick(hot_pool(1,16),1)}"

def 排列三():
    return ''.join(str(random.randint(0,9)) for _ in range(3))

def 排列五():
    return ''.join(str(random.randint(0,9)) for _ in range(5))

def 福彩3D():
    return ''.join(str(random.randint(0,9)) for _ in range(3))

class LotteryUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.play = "超级大乐透"

        self.input = TextInput(
            hint_text="生成注数",
            multiline=False,
            size_hint_y=None,
            height=80
        )
        self.add_widget(self.input)

        btns = BoxLayout(size_hint_y=None, height=100)
        for name in ["超级大乐透", "双色球", "排列三", "排列五", "福彩3D"]:
            b = Button(text=name)
            b.bind(on_press=lambda x, n=name: self.set_play(n))
            btns.add_widget(b)
        self.add_widget(btns)

        gen = Button(text="生成号码", size_hint_y=None, height=100)
        gen.bind(on_press=self.generate)
        self.add_widget(gen)

        save = Button(text="保存投注单", size_hint_y=None, height=100)
        save.bind(on_press=self.save)
        self.add_widget(save)

        self.label = Label(text="", size_hint_y=None)
        self.label.bind(texture_size=self.label.setter('size'))

        scroll = ScrollView()
        scroll.add_widget(self.label)
        self.add_widget(scroll)

    def set_play(self, name):
        self.play = name

    def generate(self, instance):
        try:
            count = int(self.input.text)
        except:
            count = 1

        result = []
        for i in range(count):
            if self.play == "超级大乐透":
                num = 大乐透()
            elif self.play == "双色球":
                num = 双色球()
            elif self.play == "排列三":
                num = 排列三()
            elif self.play == "排列五":
                num = 排列五()
            else:
                num = 福彩3D()
            result.append(f"{i+1:02d} {self.play} {num}")

        money = count * PRICE.get(self.play, 2)
        result.append(f"\n共 {count} 注，金额 {money} 元")

        self.label.text = "\n".join(result)

    def save(self, instance):
        path = os.path.join(
            App.get_running_app().user_data_dir,
            f"lottery_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.label.text)
        self.label.text += "\n\n已保存到本地"

class LotteryApp(App):
    def build(self):
        return LotteryUI()

LotteryApp().run()
