from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.ui.theme import PALETTE, style_primary_button, style_title


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", spacing=16, padding=24)
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*PALETTE["soft"])
            self._bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self._update_bg, size=self._update_bg)

        titulo = Label(text="Inicio", font_size=36, size_hint_y=0.4)
        style_title(titulo)
        layout.add_widget(titulo)

        boton_ingreso = Button(text="Cargar ingreso", size_hint_y=0.3)
        style_primary_button(boton_ingreso)
        boton_ingreso.bind(on_release=self.ir_a_cargar_ingreso)
        layout.add_widget(boton_ingreso)

        boton_egreso = Button(text="Cargar egreso", size_hint_y=0.3)
        style_primary_button(boton_egreso)
        boton_egreso.bind(on_release=self.ir_a_cargar_egreso)
        layout.add_widget(boton_egreso)

        boton_movimientos = Button(text="Ver movimientos", size_hint_y=0.3)
        style_primary_button(boton_movimientos)
        boton_movimientos.bind(on_release=self.ir_a_movimientos)
        layout.add_widget(boton_movimientos)

        self.add_widget(layout)

    def _update_bg(self, instance, _value):
        self._bg_rect.pos = instance.pos
        self._bg_rect.size = instance.size

    def ir_a_cargar_ingreso(self, _instance):
        self.manager.current = "cargar_ingreso"

    def ir_a_cargar_egreso(self, _instance):
        self.manager.current = "cargar_egreso"

    def ir_a_movimientos(self, _instance):
        self.manager.current = "movimientos"
