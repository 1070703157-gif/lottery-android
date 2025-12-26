from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
import random, time, os

PRICE = {
    "超级大乐透": 2,
    "双色球": 2,
    "排列三": 2,
    "排列五": 2,
    "福彩3D": 2,
    "7星彩": 2,
    "七星彩": 2,
    "11选5": 2,
    "体彩快乐8": 2,
    "福彩快乐8": 2,
    "七乐彩": 2
}

def hot_pool(start, end):
    pool = []
    for i in range(start, end + 1):
        pool.extend([i] * random.randint(1, 10))
    return pool

def pick(pool, n):
    s = set()
    while len(s) < n:
        s.add(random.choice(pool))
    return sorted(s)

# ===== 玩法函数 =====
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

def 7星彩():
    return ''.join(str(random.randint(0,9)) for _ in range(7))

def 七星彩():
    return ''.join(str(random.randint(0,9)) for _ in range(7))

def 11选5():
    return pick(hot_pool(1,11),5)

def 体彩快乐8():
    return pick(hot_pool(1,80),20)

def 福彩快乐8():
    return pick(hot_pool(1,80),20)

def 七乐彩():
    return pick(hot_pool(1,30),7)

PLAY_FUNC = {
    "超级大乐透": 大乐透,
    "双色球": 双色球,
    "排列三": 排列三,
    "排列五": 排列五,
    "福彩3D": 福彩3D,
    "7星彩": 7星彩,
    "七星彩": 七星彩,
    "11选5": 11选5,
    "体彩快乐8": 体彩快乐8,
    "福彩快乐8": 福彩快乐8,
    "七乐彩": 七乐彩
}

class LotteryUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.spinner = Spinner(
            text="超级大乐透",
            values=list(PLAY_FUNC.keys()),
            size_hint_y=None,
            height=80
        )
        self.add_widget(self.spinner)

        self.input = TextInput(
            hint_text="生成注数（默认1）",
            multiline=False,
            size_hint_y=None,
            height=80
        )
        self.add_widget(self.input)

        gen = Button(text="生成号码", size_hint_y=None, height=90)
        gen.bind(on_press=self.generate)
        self.add_widget(gen)

        save = Button(text="保存投注单", size_hint_y=None, height=90)
        save.bind(on_press=self.save)
        self.add_widget(save)

        self.label = Label(text="", size_hint_y=None)
        self.label.bind(texture_size=self.label.setter('size'))

        scroll = ScrollView()
        scroll.add_widget(self.label)
        self.add_widget(scroll)

    def generate(self, instance):
        play = self.spinner.text
        func = PLAY_FUNC[play]

        try:
            count = int(self.input.text)
        except:
            count = 1

        lines = []
        for i in range(count):
            lines.append(f"{i+1:02d} {play} {func()}")

        money = count * PRICE.get(play, 2)
        lines.append(f"\n共 {count} 注  合计 {money} 元")

        self.label.text = "\n".join(lines)

    def save(self, instance):
        path = os.path.join(
            App.get_running_app().user_data_dir,
            f"lottery_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.label.text)
        self.label.text += "\n\n【已保存到本地】"

class LotteryApp(App):
    def build(self):
        self.title = "彩票选号助手"
        return LotteryUI()

LotteryApp().run()
