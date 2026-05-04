from calendar import month_name, monthrange
from datetime import date

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from app.ui.theme import PALETTE, style_primary_button, style_secondary_button, style_text


class DatePickerPopup(Popup):
    def __init__(self, initial_date: date, on_date_selected, **kwargs):
        super().__init__(**kwargs)
        self.title = "Seleccionar fecha"
        self.size_hint = (0.95, 0.75)
        self.auto_dismiss = True
        self._selected_date = initial_date
        self._year = initial_date.year
        self._month = initial_date.month
        self._on_date_selected = on_date_selected
        self.background = ""
        self.background_color = PALETTE["soft"]

        container = BoxLayout(orientation="vertical", spacing=8, padding=10)
        header = BoxLayout(size_hint_y=None, height=44, spacing=8)
        self.month_label = Label()
        style_text(self.month_label)
        prev_button = Button(text="<", size_hint_x=0.2)
        style_secondary_button(prev_button)
        prev_button.bind(on_release=self._prev_month)
        next_button = Button(text=">", size_hint_x=0.2)
        style_secondary_button(next_button)
        next_button.bind(on_release=self._next_month)
        header.add_widget(prev_button)
        header.add_widget(self.month_label)
        header.add_widget(next_button)
        container.add_widget(header)

        self.days_grid = BoxLayout(orientation="vertical", spacing=4)
        container.add_widget(self.days_grid)

        self.content = container
        self._render_calendar()

    def _prev_month(self, _instance):
        if self._month == 1:
            self._month = 12
            self._year -= 1
        else:
            self._month -= 1
        self._render_calendar()

    def _next_month(self, _instance):
        if self._month == 12:
            self._month = 1
            self._year += 1
        else:
            self._month += 1
        self._render_calendar()

    def _render_calendar(self):
        self.days_grid.clear_widgets()
        self.month_label.text = f"{month_name[self._month]} {self._year}"

        week_labels = BoxLayout(size_hint_y=None, height=28, spacing=4)
        for d in ("L", "M", "X", "J", "V", "S", "D"):
            lbl = Label(text=d)
            style_text(lbl)
            week_labels.add_widget(lbl)
        self.days_grid.add_widget(week_labels)

        first_weekday, total_days = monthrange(self._year, self._month)
        start_col = (first_weekday + 1) % 7  # lunes=0
        day = 1
        for week in range(6):
            row = BoxLayout(size_hint_y=None, height=44, spacing=4)
            for col in range(7):
                if (week == 0 and col < start_col) or day > total_days:
                    row.add_widget(Label(text=""))
                    continue
                current = date(self._year, self._month, day)
                day_btn = Button(text=str(day))
                if current == self._selected_date:
                    style_primary_button(day_btn)
                else:
                    style_secondary_button(day_btn)
                    day_btn.background_color = PALETTE["white"]
                    day_btn.color = PALETTE["slate"]
                day_btn.bind(on_release=lambda _i, dt=current: self._select_date(dt))
                row.add_widget(day_btn)
                day += 1
            self.days_grid.add_widget(row)
            if day > total_days:
                break

    def _select_date(self, selected: date):
        self._selected_date = selected
        self._on_date_selected(selected)
        self.dismiss()
