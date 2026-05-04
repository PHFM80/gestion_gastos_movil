from kivy.uix.spinner import SpinnerOption


PALETTE = {
    "navy": (11 / 255, 31 / 255, 58 / 255, 1),       # 0B1F3A
    "blue": (10 / 255, 102 / 255, 194 / 255, 1),     # 0A66C2
    "cyan": (34 / 255, 199 / 255, 242 / 255, 1),     # 22C7F2
    "white": (1, 1, 1, 1),                            # FFFFFF
    "soft": (244 / 255, 247 / 255, 250 / 255, 1),    # F4F7FA
    "slate": (31 / 255, 41 / 255, 55 / 255, 1),      # 1F2937
}


class StyledSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = PALETTE["white"]
        self.color = PALETTE["slate"]
        self.font_size = 16


def style_primary_button(button):
    button.background_normal = ""
    button.background_down = ""
    button.background_color = PALETTE["blue"]
    button.color = PALETTE["white"]
    button.font_size = 18


def style_secondary_button(button):
    button.background_normal = ""
    button.background_down = ""
    button.background_color = PALETTE["navy"]
    button.color = PALETTE["white"]
    button.font_size = 16


def style_input(widget):
    widget.background_normal = ""
    widget.background_active = ""
    widget.background_color = PALETTE["white"]
    widget.foreground_color = PALETTE["slate"]
    widget.cursor_color = PALETTE["blue"]
    widget.font_size = 16


def style_spinner(spinner):
    spinner.background_normal = ""
    spinner.background_color = PALETTE["white"]
    spinner.color = PALETTE["slate"]
    spinner.option_cls = StyledSpinnerOption
    spinner.sync_height = True


def style_title(label):
    label.color = PALETTE["navy"]
    label.bold = True


def style_text(label):
    label.color = PALETTE["slate"]
