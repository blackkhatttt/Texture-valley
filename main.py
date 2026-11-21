from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.graphics.texture import Texture

from core.generator import generate_texture
from core.exporter import export_texture


class TextureValleyApp(App):
    title = "Texture Valley"

    def build(self):
        self.current_image = None
        self.material = "concrete"
        self.resolution = 512
        Window.clearcolor = (0.055, 0.067, 0.075, 1)

        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(9))
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(48))
        header.add_widget(Label(
            text="[b]TEXTURE VALLEY[/b]", markup=True, font_size="21sp",
            color=(0.91, 0.95, 0.94, 1), halign="left"
        ))
        header.add_widget(Label(
            text="PROCEDURAL TEXTURE STUDIO  •  VERSION 0.1",
            font_size="9sp", color=(0.48, 0.68, 0.65, 1), halign="left"
        ))
        root.add_widget(header)

        self.preview = Image(allow_stretch=True, keep_ratio=True, size_hint_y=0.58)
        with self.preview.canvas.before:
            Color(0.10, 0.12, 0.13, 1)
            self.preview_bg = RoundedRectangle(pos=self.preview.pos, size=self.preview.size, radius=[dp(10)])
        self.preview.bind(pos=self._update_preview_bg, size=self._update_preview_bg)
        root.add_widget(self.preview)

        controls = BoxLayout(orientation="vertical", spacing=dp(7), size_hint_y=None)
        controls.bind(minimum_height=controls.setter("height"))
        selectors = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(7))
        self.material_spinner = Spinner(
            text="Concrete", values=("Concrete", "Wood", "Metal", "Wallpaper"),
            background_normal="", background_color=(0.14, 0.25, 0.25, 1),
            color=(0.94, 0.97, 0.96, 1)
        )
        self.material_spinner.bind(text=self._on_material)
        self.res_spinner = Spinner(
            text="512 × 512",
            values=("256 × 256", "512 × 512", "1024 × 1024", "2048 × 2048"),
            background_normal="", background_color=(0.14, 0.25, 0.25, 1),
            color=(0.94, 0.97, 0.96, 1)
        )
        self.res_spinner.bind(text=self._on_resolution)
        selectors.add_widget(self.material_spinner)
        selectors.add_widget(self.res_spinner)
        controls.add_widget(selectors)

        self.scale_slider = self._add_slider(controls, "SCALE", 0.55)
        self.noise_slider = self._add_slider(controls, "NOISE", 0.45)
        self.detail_slider = self._add_slider(controls, "DETAIL", 0.55)

        actions = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        generate_btn = Button(text="GENERATE", bold=True, background_normal="",
                              background_color=(0.13, 0.48, 0.42, 1))
        generate_btn.bind(on_release=self.generate)
        export_btn = Button(text="EXPORT PNG", bold=True, background_normal="",
                            background_color=(0.20, 0.25, 0.27, 1))
        export_btn.bind(on_release=self.export)
        actions.add_widget(generate_btn)
        actions.add_widget(export_btn)
        controls.add_widget(actions)
        root.add_widget(controls)

        self.status = Label(
            text="Ready • Choose a material and generate your first texture.",
            size_hint_y=None, height=dp(30), font_size="11sp",
            color=(0.60, 0.72, 0.70, 1), halign="left"
        )
        root.add_widget(self.status)
        Clock.schedule_once(self.generate, 0.25)
        return root

    def _update_preview_bg(self, *_):
        self.preview_bg.pos = self.preview.pos
        self.preview_bg.size = self.preview.size

    def _add_slider(self, parent, label_text, initial):
        row = BoxLayout(size_hint_y=None, height=dp(37), spacing=dp(8))
        row.add_widget(Label(text=label_text, size_hint_x=0.20, font_size="10sp",
                             color=(0.67, 0.78, 0.76, 1)))
        slider = Slider(min=0, max=1, value=initial, step=0.01)
        value_label = Label(text=f"{initial:.2f}", size_hint_x=0.13, font_size="10sp")
        slider.bind(value=lambda _obj, value: setattr(value_label, "text", f"{value:.2f}"))
        row.add_widget(slider)
        row.add_widget(value_label)
        parent.add_widget(row)
        return slider

    def _on_material(self, _instance, value):
        self.material = value.lower()

    def _on_resolution(self, _instance, value):
        self.resolution = int(value.split()[0])

    def generate(self, *_):
        self.status.text = "Generating texture..."
        try:
            self.current_image = generate_texture(
                material=self.material, size=self.resolution,
                scale=self.scale_slider.value, noise=self.noise_slider.value,
                detail=self.detail_slider.value
            )
            texture = Texture.create(size=self.current_image.size, colorfmt="rgb")
            texture.blit_buffer(self.current_image.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
            texture.flip_vertical()
            self.preview.texture = texture
            self.status.text = f"{self.material.title()} • {self.resolution} × {self.resolution} • Generated"
        except Exception as exc:
            self._message("Generation error", str(exc))

    def export(self, *_):
        if self.current_image is None:
            self._message("Nothing to export", "Generate a texture first.")
            return
        try:
            path = export_texture(self.current_image, self.material)
            self.status.text = f"Saved: {path}"
            self._message("Texture exported", f"PNG saved successfully:\n{path}")
        except Exception as exc:
            self._message("Export error", str(exc))

    def _message(self, title, message):
        content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        content.add_widget(Label(text=message, halign="center"))
        close = Button(text="OK", size_hint_y=None, height=dp(42))
        popup = Popup(title=title, content=content, size_hint=(0.88, 0.42))
        close.bind(on_release=popup.dismiss)
        content.add_widget(close)
        popup.open()


if __name__ == "__main__":
    TextureValleyApp().run()
