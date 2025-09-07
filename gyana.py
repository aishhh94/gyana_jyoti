from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen , FadeTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color

from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.uix.gridlayout import GridLayout
from quiz import QUIZ_DATA
from kivy.app import App
from kivy.uix.slider import Slider

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout

import random



LabelBase.register(name="ComicNeue", fn_regular="ComicNeue-Bold.ttf")


Config.set('kivy', 'default_font', ['ComicNeue'])


TRIBE_IMAGES = {
    "Santali": "santali_bg.jpg",
    "Ho": "ho_bg.jpg",
    "Kui": "kui_bg.jpg",
    "Munda": "munda_bg.jpg"
}

def blink_button(self, button, color1, color2, times=4, interval=0.2):
    def toggle_color(dt):
        nonlocal times
        if times > 0:
            button.background_color = color1 if times % 2 == 0 else color2
            times -= 1
            Clock.schedule_once(toggle_color, interval)
        else:
            button.background_color = color1
    toggle_color(0)

# for tribe_group_selection

class BackgroundBoxLayout(BoxLayout):
    def __init__(self, tribe=None, **kwargs):
        super().__init__(**kwargs)
        self.tribe = tribe
        with self.canvas.before:
            self.color = Color(1, 1, 1, 0.3)
            img_source = TRIBE_IMAGES.get(tribe, "OdishaTribes.jpg")
            self.bg = Rectangle(source=img_source, pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        img_source = TRIBE_IMAGES.get(self.tribe, "OdishaTribes.jpg")
        self.bg.source = img_source
        self.bg.size = self.size
        self.bg.pos = self.pos
         
class HoverBehavior(object):
    """Simple desktop hover detection (ignored on touch devices)."""
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self._on_mouse_pos)

    def _on_mouse_pos(self, _window, pos):
        if not self.get_root_window():
            return
        # translate global -> local coords and test collision
        self.hovered = self.collide_point(*self.to_widget(*pos))


class TribeButton(Button, HoverBehavior):
    """Button with hover color + bounce animation on press."""
    # default colors; you can overwrite per-button
    normal_color = ListProperty([0.13, 0.36, 0.48, 1])  # dark teal
    hover_color  = ListProperty([0.18, 0.55, 0.75, 1])  # lighter teal

    def __init__(self, **kwargs):
        # ensure background_color is visible (no image skin)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_color", self.normal_color)
        kwargs.setdefault("size_hint", (1, 0.2))
        super().__init__(**kwargs)

        # hover -> swap colors (desktop)
        self.bind(hovered=self._on_hover)

        # press/release -> bounce
        self.bind(on_press=self._bounce_in)
        self.bind(on_release=self._bounce_out)

    # --- interactions ---
    def _on_hover(self, _inst, value):
        # only matters when there is a mouse
        self.background_color = self.hover_color if value else self.normal_color

    def _bounce_in(self, *_):
        Animation.cancel_all(self)
        # quick grow
        Animation(size_hint=(1.03, 0.22), duration=0.12).start(self)

    def _bounce_out(self, *_):
        Animation.cancel_all(self)
        # snap back
        Animation(size_hint=(1.00, 0.20), duration=0.12).start(self)



class TribeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.bg = Rectangle(source="coverpage.jpg", size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        title = Label(text="Welcome, Pick Your Tribe!",
                       font_size=36, 
                       color=(1, 1, 1, 1),
                       font_name="ComicNeue-Bold.ttf",
                       bold=True
                       )
        layout.add_widget(title)

        self.name_input = TextInput(
            hint_text="Enter your name",
            size_hint=(1, 0.15),
            multiline=False,
            font_name="ComicNeue-Bold.ttf",
            font_size=22,
            foreground_color=(0, 0, 0, 1),  # Black text
            background_color=(1, 1, 1, 0.7)  # White with transparency
        )
        layout.add_widget(self.name_input)
        tribes = ["Santali", "Ho", "Kui", "Munda"]

        


       
        tribes_layout = GridLayout(cols=2, spacing=15, size_hint=(1, 0.6))

        TRIBE_BUTTON_COLORS = {
            "Santali": ([0.85, 0.40, 0.20, 1], [0.95, 0.55, 0.30, 1]),
            "Ho":      ([0.20, 0.50, 0.80, 1], [0.30, 0.70, 0.95, 1]),
            "Kui":     ([0.20, 0.70, 0.45, 1], [0.35, 0.85, 0.60, 1]),
            "Munda":   ([0.55, 0.35, 0.80, 1], [0.70, 0.50, 0.95, 1])
        }
        
        for tribe in tribes:
            normal, hover = TRIBE_BUTTON_COLORS.get(
                tribe, ([1, 1, 1, 0.25], [1, 1, 1, 0.45])
            )
            btn = TribeButton(
                text=tribe,
                font_name="ComicNeue-Bold.ttf",
                font_size=24,
                color=(1, 1, 1, 1),       # White text for contrast
                background_normal='',
                background_down=''      
            )
            btn.normal_color = normal
            btn.hover_color = hover
            # btn.background_color = normal


            with btn.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                btn._bg_color = Color(*normal)
                btn._bg_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[25])

    # Keep updating size/pos
            def update_rect(instance, value,b=btn):
                b._bg_rect.size = instance.size
                b._bg_rect.pos = instance.pos
            btn.bind(size=update_rect, pos=update_rect)
        
            def on_hover(instance, value,b=btn):
                b._bg_color.rgba = b.hover_color if value else b.normal_color
            btn.bind(on_hover=on_hover)

            btn.bind(on_release=lambda inst, t=tribe: self.select_tribe(t))
            tribes_layout.add_widget(btn)

        layout.add_widget(tribes_layout)
        self.add_widget(layout)
    
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def select_tribe(self, tribe):
        app = App.get_running_app()
        app.selected_tribe = tribe
        app.username = self.name_input.text if self.name_input.text.strip() else "Friend"
        self.manager.current = "home"

# Home Screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)


        with self.layout.canvas.before:
            self.bg = Rectangle(source="coverpage.jpg", pos=self.pos, size=self.size)

        self.layout.bind(size=self._update_bg, pos=self._update_bg)

        self.title = Label(text="", font_size=28, color=(0.902, 0.905, 0.145, 0.87),font_name="ComicNeue-Bold.ttf")
        self.layout.add_widget(self.title)


        lesson_btn = Button(text="Start Video Lesson", size_hint=(1, 0.2))
        quiz_btn = Button(text="Take Quiz", size_hint=(1, 0.2))
        exit_btn = Button(text="Exit", size_hint=(1, 0.2))

        lesson_btn.bind(on_press=self.go_to_lessons)
        quiz_btn.bind(on_press=self.go_to_topic_selection)
        exit_btn.bind(on_press=lambda x: App.get_running_app().stop())

        self.layout.add_widget(lesson_btn)
        self.layout.add_widget(quiz_btn)
        self.layout.add_widget(exit_btn)

        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size
    
    def go_to_topic_selection(self, instance):
        self.manager.current = "topic_selection"
        
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.title.text = f"Welcome {app.username}!\nTribe: {app.selected_tribe}"
        self.layout.tribe=app.selected_tribe
        self.layout._update_bg()

    def go_to_lessons(self, instance):
        self.manager.current = "lessons"

    def go_to_quiz(self, instance):
        self.manager.current = "quiz"


# Lessons Screen
# from kivy.uix.video import Video

class LessonScreen(Screen):
    def __init__(self, **kwargs):
        super(LessonScreen, self).__init__(**kwargs)

        # ---- MAIN LAYOUT (added only ONCE) ----
        self.layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)

        with self.layout.canvas.before:
            self.bg = Rectangle(source="coverpage.jpg", pos=self.pos, size=self.size)

        self.layout.bind(size=self._update_bg, pos=self._update_bg)
        # Title
        self.label = Label(text="Lesson Content", font_size=28, bold=True, size_hint=(1, 0.2))
        self.layout.add_widget(self.label)

        # Video widget
        self.video = Video(source="lesson.mp4", state="stop", options={'eos': 'loop'})
        self.video.size_hint = (1, 0.6)
        self.layout.add_widget(self.video)

        # Controls (Play, Pause, Stop)
        controls = BoxLayout(size_hint=(1, 0.2), spacing=10)
        play_btn = Button(text="Play")
        pause_btn = Button(text="Pause")
        stop_btn = Button(text="Stop")

        play_btn.bind(on_press=lambda x: setattr(self.video, "state", "play"))
        pause_btn.bind(on_press=lambda x: setattr(self.video, "state", "pause"))
        stop_btn.bind(on_press=lambda x: setattr(self.video, "state", "stop"))

        controls.add_widget(play_btn)
        controls.add_widget(pause_btn)
        controls.add_widget(stop_btn)
        self.layout.add_widget(controls)

        # Timeline Slider
        self.timeline = Slider(min=0, max=10, value=0, size_hint=(1, 0.1))
        self.timeline.bind(on_touch_up=self.seek_video)
        self.layout.add_widget(self.timeline)

        # Update timeline dynamically
        Clock.schedule_interval(self.update_timeline, 0.25)

        # Back button
        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        # ✅ Add layout only once
        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.layout.tribe = app.selected_tribe
        self.layout._update_bg()

    def update_timeline(self, dt):
        """Update slider with current video position"""
        if self.video.duration and self.video.position is not None:
            self.timeline.max = self.video.duration
            self.timeline.value = self.video.position

    def seek_video(self, instance, touch):
        """Allow dragging slider to seek video"""
        if instance.collide_point(*touch.pos) and self.video.duration:
            self.video.position = self.timeline.value

    def go_back(self, instance):
        self.manager.current = "tribe"




# Topic Selection Screen
class TopicSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ✅ self.layout define karna zaroori hai
        self.layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)

        with self.layout.canvas.before:
            self.bg = Rectangle(source="coverpage.jpg", pos=self.pos, size=self.size)

        self.layout.bind(size=self._update_bg, pos=self._update_bg)



        title = Label(text="Choose Topic", font_size=36, color=(0.9, 0.6, 0.2, 1))
        self.layout.add_widget(title)

        topics = ["Math", "General"]
        for topic in topics:
            btn = Button(
                text=topic,
                font_size=24,
                background_color=(0.2, 0.7, 0.9, 1)
            )
            btn.bind(on_press=lambda instance, t=topic: self.select_topic(t))
            self.layout.add_widget(btn)   # ✅ self.layout use kiya

        back_btn = Button(text="Back to Home", size_hint=(1, 0.15))
        back_btn.bind(on_press=self.go_back_home)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)  # ✅ ek hi baar add kiya

    def _update_bg(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.layout.tribe = app.selected_tribe
        self.layout._update_bg()

    def select_topic(self, topic):
        app = App.get_running_app()
        app.selected_topic = topic
        self.manager.current = "quiz"

    def go_back_home(self, instance):
        self.manager.current = "home"




# # Quiz Screen
# from kivy.app import App
# from kivy.uix.screenmanager import Screen
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.clock import Clock

# # 👇 quiz.py se data import
# from quiz import QUIZ_DATA  

# # 👇 BackgroundBoxLayout tum already bana chuki ho
# from background_layout import BackgroundBoxLayout  


class QuizScreen(Screen):
    COLORS = [
        (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1),
        (1, 0.5, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1), (1, 1, 0, 1)
    ]
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)

        # Main layout with background
        self.layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)

        with self.layout.canvas.before:
            self.bg = Rectangle(source="coverpage.jpg", pos=self.pos, size=self.size)

        self.layout.bind(size=self._update_bg, pos=self._update_bg)

        # Question label
        self.question_label = Label(text="", font_size=26, color=(0, 0, 0, 1))
        self.layout.add_widget(self.question_label)
        
        

        # Option buttons
        self.option_buttons = []
        for i in range(3):  # max 3 options
            btn = Button(size_hint=(1, None), height=80, font_size=20, background_color=(1, 1, 1, 1))
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            self.layout.add_widget(btn)

        # Feedback label
        self.feedback_label = Label(text="", font_size=20, color=(0.2, 0.5, 0.9, 1))
        self.layout.add_widget(self.feedback_label)

        # Next button
        self.next_btn = Button(text="Next", size_hint=(1, 0.2), font_size=22)
        self.next_btn.bind(on_press=self.next_question)
        self.layout.add_widget(self.next_btn)

        # Back button
        self.back_btn = Button(text="Back to Topic Selection", size_hint=(1, 0.2), font_size=22)
        self.back_btn.bind(on_press=self.go_topic_selection)
        self.layout.add_widget(self.back_btn)

        self.add_widget(self.layout)

        # State
        self.questions = []
        self.current_index = 0
        self.score = 0
        

    
    


    def _update_bg(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size
    

    # --- Load quiz when screen opens ---
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.layout.tribe = app.selected_tribe
        self.layout._update_bg()
        tribe = app.selected_tribe
        topic = getattr(app, "selected_topic", "General")
        self.questions = QUIZ_DATA.get(tribe, {}).get(topic, [])
        self.current_index = 0
        self.score = 0
        if self.questions:
            self.show_question()
        else:
            self.question_label.text = "No quiz available for this tribe/topic."
            self.feedback_label.text = ""
            for btn in self.option_buttons:
                btn.text = ""
                btn.disabled = True
            self.next_btn.disabled = True

     # --- Show current question with random color ---
    def show_question(self):
        q = self.questions[self.current_index]
        self.question_label.color = random.choice(self.COLORS)
        self.question_label.text = f"Q: {q['q_en']}\n{q['q_local']}"
        for i, btn in enumerate(self.option_buttons):
            if i < len(q["options_en"]):  # option available
                option = q["options_en"][i]
                local_option = q["options_local"][i]
                btn.text = f"{option}\n({local_option})"
                btn.answer_value = option   # ⭐ yeh zaroori hai
                btn.background_color = (1, 1, 1, 1)
                btn.disabled = False
            else:
                btn.text = ""
                btn.answer_value = None     # ⭐ clear value
                btn.disabled = True

        self.feedback_label.text = ""
        self.next_btn.text = "Next"
        self.next_btn.disabled = True

    # --- Answer check ---
    def check_answer(self, instance):
        q = self.questions[self.current_index]
        if instance.answer_value == q["answer"]:
            self.score += 1
            self.feedback_label.text = "Correct!"
            self.blink_button(instance, (0, 1, 0, 1), (1, 1, 1, 1))  # green blink
        else:
            self.feedback_label.text = "Wrong!"
            self.blink_button(instance, (1, 0, 0, 1), (1, 1, 1, 1))  # red blink

        for btn in self.option_buttons:
            btn.disabled = True
        self.next_btn.disabled = False


    # --- Blink effect on button ---

    def blink_button(self, button, color1, color2, times=4, interval=0.2):
        def toggle_color(dt):
            nonlocal times
            if times > 0:
                button.background_color = color1 if times % 2 == 0 else color2
                times -= 1
                Clock.schedule_once(toggle_color, interval)
            else:
                button.background_color = (1, 1, 1, 1)  # reset to white
        toggle_color(0)

    # --- Next question ---
    def next_question(self, instance):
        if self.current_index + 1 < len(self.questions):
            self.current_index += 1
            self.show_question()
        else:
        # Quiz finished
            self.question_label.text = f"Quiz Finished!\nYour Score: {self.score}/{len(self.questions)}"
            self.feedback_label.text = "Great Job!" if self.score > 0 else "Keep Practicing!"
        for btn in self.option_buttons:
            btn.text = ""
            btn.disabled = True

        # Change Next button to "Choose Another Topic"
        self.next_btn.text = "Choose Another Topic"

        # 🔥 FIX: unbind old and bind new action
        self.next_btn.unbind(on_press=self.next_question)
        self.next_btn.bind(on_press=self.go_topic_selection)

            # self.next_btn.unbind(on_press=self.next_question)
            # self.next_btn.bind(on_press=self.go_topic_selection)


    # --- Go back to home ---
    # def go_back(self, instance):
        # self.manager.current = "topic_selection"


    def go_topic_selection(self, *args):
        self.manager.current = "topic_selection"
    def go_back(self, instance):
        self.manager.current = "home"



# Screen Manager
class TribalApp(App):
    def build(self):
        self.selected_tribe = None
        self.username = "Friend"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(TribeSelectionScreen(name="tribe"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LessonScreen(name="lessons"))
        sm.add_widget(TopicSelectionScreen(name="topic_selection"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.current = "tribe"   # ✅ Start from tribe selection
        return sm


if __name__ == "__main__":
    TribalApp().run()