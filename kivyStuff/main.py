from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock

class MyApp(App):
    def build(self):
        layout = FloatLayout()

        # Create and add the label
        self.label = Label(text='Gesture Navigator!',
                           font_size='40sp',
                           size_hint=(.5, .5),
                            pos_hint={'center_x': .5, 'center_y': .5},
                            opacity=0)
        
        layout.add_widget(self.label)

        # Fade in the label
        Clock.schedule_once(self.fade_in_label, 2)

        # Fade out the label after 2 seconds
        Clock.schedule_once(self.fade_out_label, 2)

        return layout

    def fade_out_label(self, dt):
        # Animation to fade out the label
        anim = Animation(opacity=0, duration=1)
        anim.start(self.label)

        # Schedule the method to show the button after the animation finishes
        Clock.schedule_once(self.show_button, 1)

    def fade_in_label(self, dt):
        # Animation to fade in the label
        anim = Animation(opacity=1, duration=1)
        anim.start(self.label)

    def show_button(self, dt):
        layout = self.root

        # Create and add the button
        button = Button(text='Click me!',
                        size_hint=(.3, .15),
                        pos_hint={'center_x': .5, 'center_y': .4})
        layout.add_widget(button)

if __name__ == '__main__':
    MyApp().run()
