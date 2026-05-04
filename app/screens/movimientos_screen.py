from datetime import date, timedelta

from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.medio_pago_repository import MedioPagoRepository
from app.service.movimiento_service import MovimientoService
from app.ui.date_picker import DatePickerPopup
from app.ui.theme import (
    PALETTE,
    style_input,
    style_primary_button,
    style_secondary_button,
    style_spinner,
    style_text,
    style_title,
)


class MovimientosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._movimiento_service = MovimientoService()
        self._categoria_repository = CategoriaRepository()
        self._medio_pago_repository = MedioPagoRepository()
        self._movimientos_filtrados = []

        root = BoxLayout(orientation="vertical", spacing=12, padding=16)
        with root.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*PALETTE["soft"])
            self._bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        titulo = Label(text="Movimientos", font_size=30, size_hint_y=None, height=50)
        style_title(titulo)
        root.add_widget(titulo)

        self.filtros = BoxLayout(
            orientation="horizontal", spacing=8, size_hint_y=None, height=46
        )
        self.periodo_spinner = Spinner(
            text="Seleccionar periodo",
            values=("dia", "semana", "mes"),
            size_hint_x=0.35,
        )
        style_spinner(self.periodo_spinner)
        self.filtros.add_widget(self.periodo_spinner)

        self.fecha_input = TextInput(
            text="",
            multiline=False,
            hint_text="Fecha referencia YYYY-MM-DD",
            readonly=True,
            size_hint_x=0.3,
        )
        style_input(self.fecha_input)
        self.filtros.add_widget(self.fecha_input)

        self.boton_cal = Button(text="Calendario", size_hint_x=0.2)
        style_secondary_button(self.boton_cal)
        self.boton_cal.bind(on_release=self.abrir_calendario)
        self.filtros.add_widget(self.boton_cal)

        self.boton_filtrar = Button(text="Filtrar", size_hint_x=0.15)
        style_primary_button(self.boton_filtrar)
        self.boton_filtrar.bind(on_release=self.refrescar_listado)
        self.filtros.add_widget(self.boton_filtrar)
        root.add_widget(self.filtros)

        self.mensaje_label = Label(text="", size_hint_y=None, height=28)
        style_text(self.mensaje_label)
        root.add_widget(self.mensaje_label)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.tabla_layout = GridLayout(
            cols=1,
            spacing=4,
            size_hint_y=None,
            row_default_height=120,
            row_force_default=False,
            padding=(2, 2),
        )
        self.tabla_layout.bind(minimum_height=self.tabla_layout.setter("height"))
        self.scroll.add_widget(self.tabla_layout)
        root.add_widget(self.scroll)

        boton_enviar = Button(
            text="Enviar datos seleccionados", size_hint_y=None, height=48
        )
        style_primary_button(boton_enviar)
        boton_enviar.bind(on_release=self.enviar_datos_seleccionados)
        root.add_widget(boton_enviar)

        boton_volver = Button(text="Volver", size_hint_y=None, height=48)
        style_secondary_button(boton_volver)
        boton_volver.bind(on_release=self.volver_a_inicio)
        root.add_widget(boton_volver)

        self.add_widget(root)
        Window.bind(size=self._on_window_resize)
        self._actualizar_layout_responsivo()

    def abrir_calendario(self, _instance):
        fecha_inicial = date.today()
        if self.fecha_input.text.strip():
            try:
                fecha_inicial = date.fromisoformat(self.fecha_input.text.strip())
            except ValueError:
                fecha_inicial = date.today()

        popup = DatePickerPopup(
            initial_date=fecha_inicial,
            on_date_selected=lambda selected: setattr(
                self.fecha_input, "text", selected.isoformat()
            ),
        )
        popup.open()

    def _update_bg(self, instance, _value):
        self._bg_rect.pos = instance.pos
        self._bg_rect.size = instance.size

    def on_pre_enter(self, *args):
        self._actualizar_layout_responsivo()
        self.tabla_layout.clear_widgets()
        self.mensaje_label.text = "Seleccione periodo y fecha, luego presione Filtrar"
        return super().on_pre_enter(*args)

    def _on_window_resize(self, _window, _size):
        self._actualizar_layout_responsivo()

    def _actualizar_layout_responsivo(self):
        self.filtros.orientation = "vertical" if (platform == "android" or Window.width <= 900) else "horizontal"
        self.filtros.height = 188 if self.filtros.orientation == "vertical" else 46
        self.periodo_spinner.size_hint_x = 1 if self.filtros.orientation == "vertical" else 0.35
        self.fecha_input.size_hint_x = 1 if self.filtros.orientation == "vertical" else 0.3
        self.boton_cal.size_hint_x = 1 if self.filtros.orientation == "vertical" else 0.2
        self.boton_filtrar.size_hint_x = 1 if self.filtros.orientation == "vertical" else 0.15
        self.tabla_layout.cols = 1
        self.tabla_layout.row_force_default = False
        self.tabla_layout.row_default_height = 120
        self.tabla_layout.spacing = 10
        self.tabla_layout.padding = (4, 4)

    def refrescar_listado(self, *_args):
        self.tabla_layout.clear_widgets()
        self._movimientos_filtrados = []
        self._actualizar_layout_responsivo()

        periodo = self.periodo_spinner.text.strip().lower()
        if periodo not in {"dia", "semana", "mes"}:
            self.mensaje_label.text = "Falta seleccionar el periodo (dia, semana o mes)"
            return

        fecha_texto = self.fecha_input.text.strip()
        if not fecha_texto:
            self.mensaje_label.text = "Falta seleccionar una fecha"
            return

        try:
            fecha_referencia = date.fromisoformat(fecha_texto)
        except ValueError:
            self.mensaje_label.text = "Fecha invalida. Use YYYY-MM-DD"
            return

        movimientos = self._movimiento_service.listar_movimientos()
        categorias = {c.id: c.nombre for c in self._categoria_repository.list_all()}
        medios_pago = {m.id: m.nombre for m in self._medio_pago_repository.list_all()}

        filtrados = [
            m for m in movimientos if self._coincide_periodo(m.fecha, fecha_referencia, periodo)
        ]
        self._movimientos_filtrados = filtrados

        if not filtrados:
            self.mensaje_label.text = "No hay movimientos para el filtro seleccionado"
            return

        self.mensaje_label.text = f"Movimientos encontrados: {len(filtrados)}"

        for movimiento in filtrados:
            categoria = categorias.get(movimiento.categoria_id, f"ID {movimiento.categoria_id}")
            medio_pago = medios_pago.get(movimiento.medio_pago_id, f"ID {movimiento.medio_pago_id}")
            detalle = movimiento.detalle or "-"
            self.tabla_layout.add_widget(
                self._crear_card_movimiento(
                    movimiento.tipo.value,
                    movimiento.fecha.isoformat(),
                    str(movimiento.monto),
                    categoria,
                    medio_pago,
                    detalle,
                )
            )

    def _crear_card_movimiento(
        self,
        tipo: str,
        fecha_texto: str,
        monto_texto: str,
        categoria: str,
        medio_pago: str,
        detalle: str,
    ) -> BoxLayout:
        card = BoxLayout(
            orientation="vertical",
            spacing=4,
            padding=(10, 10),
            size_hint_y=None,
            height=132,
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle

            Color(*PALETTE["white"])
            card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
        card.bind(pos=self._update_card_bg, size=self._update_card_bg)

        card.add_widget(self._crear_fila_card("Tipo", tipo, resaltar=True))
        card.add_widget(self._crear_fila_card("Fecha", fecha_texto))
        card.add_widget(self._crear_fila_card("Monto", monto_texto))
        card.add_widget(self._crear_fila_card("Categoria", categoria))
        card.add_widget(self._crear_fila_card("Medio", medio_pago))
        card.add_widget(self._crear_fila_card("Detalle", detalle))
        return card

    def _update_card_bg(self, instance, _value):
        if hasattr(instance, "_bg"):
            instance._bg.pos = instance.pos
            instance._bg.size = instance.size

    @staticmethod
    def _crear_fila_card(etiqueta: str, valor: str, resaltar: bool = False) -> Label:
        prefijo = f"[b]{etiqueta}:[/b] "
        contenido = f"{prefijo}{valor}" if resaltar else f"{etiqueta}: {valor}"
        fila = Label(
            text=contenido,
            markup=resaltar,
            size_hint_y=None,
            height=18,
            halign="left",
            valign="middle",
            color=PALETTE["slate"],
            text_size=(0, None),
            shorten=True,
            shorten_from="right",
        )
        fila.bind(size=lambda instance, size: setattr(instance, "text_size", (size[0], None)))
        return fila

    def _coincide_periodo(self, fecha_movimiento: date, fecha_referencia: date, periodo: str) -> bool:
        if periodo == "dia":
            return fecha_movimiento == fecha_referencia
        if periodo == "semana":
            fin_semana = fecha_referencia + timedelta(days=6)
            return fecha_referencia <= fecha_movimiento <= fin_semana
        if periodo == "mes":
            fin_mes = self._sumar_un_mes(fecha_referencia) - timedelta(days=1)
            return fecha_referencia <= fecha_movimiento <= fin_mes
        return False

    @staticmethod
    def _sumar_un_mes(fecha_base: date) -> date:
        anio = fecha_base.year
        mes = fecha_base.month + 1
        if mes > 12:
            mes = 1
            anio += 1

        for dia in range(fecha_base.day, 0, -1):
            try:
                return date(anio, mes, dia)
            except ValueError:
                continue
        return date(anio, mes, 1)

    def enviar_datos_seleccionados(self, _instance):
        self.mensaje_label.text = (
            f"Filtrados: {len(self._movimientos_filtrados)} (envio pendiente de implementar)"
        )

    def volver_a_inicio(self, _instance):
        self.manager.current = "home"
