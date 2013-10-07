from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from sqrl import *

class SQRLApp(App):
    def build(self):
        layout = BoxLayout(padding=10)
        layout.add_widget(TextInput(text='Hello world'))
        layout.add_widget(Button(text="Submit"))
        return layout

if __name__ == '__main__':
    SQRLApp().run()