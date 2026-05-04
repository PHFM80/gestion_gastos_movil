from datetime import date
from decimal import Decimal, InvalidOperation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from app.models.tipo_movimiento import TipoMovimiento
from app.repositories.medio_pago_repository import MedioPagoRepository
from app.service.categoria_service import CategoriaService
from app.service.movimiento_service import MovimientoService, ValidationError
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


class CargarEgresoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._categoria_service = CategoriaService()
        self._movimiento_service = MovimientoService()
        self._medio_pago_repository = MedioPagoRepository()
        self._categorias_por_nombre = {}
        self._medios_por_nombre = {}

        layout = BoxLayout(orientation="vertical", spacing=16, padding=24)
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*PALETTE["soft"])
            self._bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self._update_bg, size=self._update_bg)

        titulo = Label(text="Cargar egreso", font_size=32, size_hint_y=None, height=56)
        style_title(titulo)
        layout.add_widget(titulo)

        fecha_row = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=46)
        self.fecha_input = TextInput(
            text=date.today().isoformat(),
            multiline=False,
            hint_text="Fecha (YYYY-MM-DD)",
            readonly=True,
            size_hint_x=0.75,
        )
        style_input(self.fecha_input)
        fecha_row.add_widget(self.fecha_input)
        boton_cal = Button(text="Calendario", size_hint_x=0.25)
        style_secondary_button(boton_cal)
        boton_cal.bind(on_release=self.abrir_calendario)
        fecha_row.add_widget(boton_cal)
        layout.add_widget(fecha_row)

        self.monto_input = TextInput(
            multiline=False,
            hint_text="Monto",
            input_filter="float",
            size_hint_y=None,
            height=46,
        )
        style_input(self.monto_input)
        layout.add_widget(self.monto_input)

        self.categoria_spinner = Spinner(
            text="Seleccionar categoria",
            values=[],
            size_hint_y=None,
            height=46,
        )
        style_spinner(self.categoria_spinner)
        layout.add_widget(self.categoria_spinner)

        self.medio_pago_spinner = Spinner(
            text="Seleccionar medio de pago",
            values=[],
            size_hint_y=None,
            height=46,
        )
        style_spinner(self.medio_pago_spinner)
        layout.add_widget(self.medio_pago_spinner)

        self.detalle_input = TextInput(
            multiline=False,
            hint_text="Detalle (opcional)",
            size_hint_y=None,
            height=46,
        )
        style_input(self.detalle_input)
        layout.add_widget(self.detalle_input)

        boton_guardar = Button(text="Guardar egreso", size_hint_y=None, height=48)
        style_primary_button(boton_guardar)
        boton_guardar.bind(on_release=self.guardar_egreso)
        layout.add_widget(boton_guardar)

        self.mensaje_label = Label(text="", size_hint_y=None, height=32)
        style_text(self.mensaje_label)
        layout.add_widget(self.mensaje_label)

        boton_volver = Button(text="Volver", size_hint_y=None, height=48)
        style_secondary_button(boton_volver)
        boton_volver.bind(on_release=self.volver_a_inicio)
        layout.add_widget(boton_volver)
        self.add_widget(layout)

    def _update_bg(self, instance, _value):
        self._bg_rect.pos = instance.pos
        self._bg_rect.size = instance.size

    def on_pre_enter(self, *args):
        self._cargar_opciones()
        return super().on_pre_enter(*args)

    def abrir_calendario(self, _instance):
        popup = DatePickerPopup(
            initial_date=date.fromisoformat(self.fecha_input.text),
            on_date_selected=lambda selected: setattr(
                self.fecha_input, "text", selected.isoformat()
            ),
        )
        popup.open()

    def _cargar_opciones(self):
        categorias = self._categoria_service.listar_por_tipo(TipoMovimiento.EGRESO)
        self._categorias_por_nombre = {categoria.nombre: categoria.id for categoria in categorias}
        self.categoria_spinner.values = tuple(self._categorias_por_nombre.keys())
        self.categoria_spinner.text = "Seleccionar categoria"

        medios_pago = self._medio_pago_repository.list_all()
        self._medios_por_nombre = {medio.nombre: medio.id for medio in medios_pago}
        self.medio_pago_spinner.values = tuple(self._medios_por_nombre.keys())
        self.medio_pago_spinner.text = "Seleccionar medio de pago"

        if not categorias:
            self.mensaje_label.text = "No hay categorias de egreso disponibles"
        elif not medios_pago:
            self.mensaje_label.text = "No hay medios de pago disponibles"
        else:
            self.mensaje_label.text = ""

    def guardar_egreso(self, _instance):
        try:
            fecha_valor = date.fromisoformat(self.fecha_input.text.strip())
        except ValueError:
            self.mensaje_label.text = "Fecha invalida. Use YYYY-MM-DD"
            return

        monto_texto = self.monto_input.text.strip().replace(",", ".")
        try:
            monto_valor = Decimal(monto_texto)
        except (InvalidOperation, ValueError):
            self.mensaje_label.text = "Monto invalido"
            return

        categoria_id = self._categorias_por_nombre.get(self.categoria_spinner.text)
        if categoria_id is None:
            self.mensaje_label.text = "Seleccione una categoria"
            return

        medio_pago_id = self._medios_por_nombre.get(self.medio_pago_spinner.text)
        if medio_pago_id is None:
            self.mensaje_label.text = "Seleccione un medio de pago"
            return

        try:
            self._movimiento_service.crear_movimiento(
                tipo=TipoMovimiento.EGRESO,
                fecha=fecha_valor,
                monto=monto_valor,
                categoria_id=categoria_id,
                medio_pago_id=medio_pago_id,
                detalle=self.detalle_input.text,
            )
        except ValidationError as error:
            self.mensaje_label.text = str(error)
            return

        self.mensaje_label.text = "Egreso guardado correctamente"
        self.monto_input.text = ""
        self.detalle_input.text = ""
        self.fecha_input.text = date.today().isoformat()
        self.categoria_spinner.text = "Seleccionar categoria"
        self.medio_pago_spinner.text = "Seleccionar medio de pago"

    def volver_a_inicio(self, _instance):
        self.manager.current = "home"
