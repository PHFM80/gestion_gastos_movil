from datetime import date, timedelta

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

        filtros = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=46)
        self.periodo_spinner = Spinner(
            text="dia",
            values=("dia", "semana", "mes"),
            size_hint_x=0.35,
        )
        style_spinner(self.periodo_spinner)
        filtros.add_widget(self.periodo_spinner)

        self.fecha_input = TextInput(
            text=date.today().isoformat(),
            multiline=False,
            hint_text="Fecha referencia YYYY-MM-DD",
            readonly=True,
            size_hint_x=0.3,
        )
        style_input(self.fecha_input)
        filtros.add_widget(self.fecha_input)

        boton_cal = Button(text="Calendario", size_hint_x=0.2)
        style_secondary_button(boton_cal)
        boton_cal.bind(on_release=self.abrir_calendario)
        filtros.add_widget(boton_cal)

        boton_filtrar = Button(text="Filtrar", size_hint_x=0.15)
        style_primary_button(boton_filtrar)
        boton_filtrar.bind(on_release=self.refrescar_listado)
        filtros.add_widget(boton_filtrar)
        root.add_widget(filtros)

        self.mensaje_label = Label(text="", size_hint_y=None, height=28)
        style_text(self.mensaje_label)
        root.add_widget(self.mensaje_label)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.tabla_layout = GridLayout(
            cols=6,
            spacing=4,
            size_hint_y=None,
            row_default_height=38,
            row_force_default=True,
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

    def abrir_calendario(self, _instance):
        popup = DatePickerPopup(
            initial_date=date.fromisoformat(self.fecha_input.text),
            on_date_selected=lambda selected: setattr(
                self.fecha_input, "text", selected.isoformat()
            ),
        )
        popup.open()

    def _update_bg(self, instance, _value):
        self._bg_rect.pos = instance.pos
        self._bg_rect.size = instance.size

    def on_pre_enter(self, *args):
        self.refrescar_listado()
        return super().on_pre_enter(*args)

    def refrescar_listado(self, *_args):
        self.tabla_layout.clear_widgets()
        self._movimientos_filtrados = []

        try:
            fecha_referencia = date.fromisoformat(self.fecha_input.text.strip())
        except ValueError:
            self.mensaje_label.text = "Fecha invalida. Use YYYY-MM-DD"
            return

        periodo = self.periodo_spinner.text
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

        self._agregar_encabezados_tabla()
        self.mensaje_label.text = f"Movimientos encontrados: {len(filtrados)}"
        for movimiento in filtrados:
            categoria = categorias.get(movimiento.categoria_id, f"ID {movimiento.categoria_id}")
            medio_pago = medios_pago.get(movimiento.medio_pago_id, f"ID {movimiento.medio_pago_id}")
            detalle = movimiento.detalle or "-"
            self.tabla_layout.add_widget(self._crear_celda(movimiento.tipo.value))
            self.tabla_layout.add_widget(self._crear_celda(movimiento.fecha.isoformat()))
            self.tabla_layout.add_widget(self._crear_celda(str(movimiento.monto)))
            self.tabla_layout.add_widget(self._crear_celda(categoria))
            self.tabla_layout.add_widget(self._crear_celda(medio_pago))
            self.tabla_layout.add_widget(self._crear_celda(detalle))

    def _agregar_encabezados_tabla(self):
        encabezados = ("Tipo", "Fecha", "Monto", "Categoria", "Medio", "Detalle")
        for encabezado in encabezados:
            self.tabla_layout.add_widget(self._crear_celda(encabezado, negrita=True))

    @staticmethod
    def _crear_celda(texto: str, negrita: bool = False) -> Label:
        if negrita:
            texto = f"[b]{texto}[/b]"
        return Label(
            text=texto,
            markup=negrita,
            halign="left",
            valign="middle",
            color=PALETTE["slate"],
            text_size=(None, None),
        )

    def _coincide_periodo(self, fecha_movimiento: date, fecha_referencia: date, periodo: str) -> bool:
        if periodo == "dia":
            return fecha_movimiento == fecha_referencia
        if periodo == "semana":
            inicio_semana = fecha_referencia - timedelta(days=fecha_referencia.weekday())
            fin_semana = inicio_semana + timedelta(days=6)
            return inicio_semana <= fecha_movimiento <= fin_semana
        if periodo == "mes":
            return (
                fecha_movimiento.year == fecha_referencia.year
                and fecha_movimiento.month == fecha_referencia.month
            )
        return False

    def enviar_datos_seleccionados(self, _instance):
        self.mensaje_label.text = (
            f"Filtrados: {len(self._movimientos_filtrados)} (envio pendiente de implementar)"
        )

    def volver_a_inicio(self, _instance):
        self.manager.current = "home"
