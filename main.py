from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from app.database import close_connection, init_database
from app.screens.cargar_egreso_screen import CargarEgresoScreen
from app.screens.cargar_ingreso_screen import CargarIngresoScreen
from app.screens.home_screen import HomeScreen
from app.screens.movimientos_screen import MovimientosScreen
from app.ui.theme import PALETTE


class GestionGastosApp(App):
    icon = "assets/icons/app_icon.png"

    def build(self):
        Window.clearcolor = PALETTE["soft"]
        init_database()
        screen_manager = ScreenManager()
        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(CargarIngresoScreen(name="cargar_ingreso"))
        screen_manager.add_widget(CargarEgresoScreen(name="cargar_egreso"))
        screen_manager.add_widget(MovimientosScreen(name="movimientos"))
        return screen_manager

    def on_stop(self):
        close_connection()


if __name__ == "__main__":
    GestionGastosApp().run()
