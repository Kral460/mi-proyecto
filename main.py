import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.utils import platform

try:
    from plyer import tts, filechooser, permissions
    from plyer.utils import platform as plyer_platform
except ImportError:
    tts = None
    filechooser = None
    permissions = None
    plyer_platform = 'desktop'
    print("Plyer not found. Some functionalities (TTS, FileChooser, Permissions) will be disabled.")

KV = """
<RootWidget>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.498, 1, 0.831, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        ScrollView:
            size_hint_y: 0.7
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)

                Button:
                    text: 'Adjuntar Archivo'
                    id: attach_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1
                    color: 1, 1, 1, 1
                    accessibility_text: 'Adjuntar archivo, abre el selector de archivos para seleccionar un documento de texto o audio.'
                    on_release: app.on_button_press(self, 'Adjuntar archivo', app.attach_file)

                TextInput:
                    id: text_input
                    hint_text: 'Pega o escribe tu texto aquí (hasta 5000 caracteres)'
                    multiline: True
                    size_hint_y: None
                    height: dp(300)
                    font_size: dp(18)
                    padding: dp(10)
                    background_color: 1, 1, 1, 0.9
                    foreground_color: 0, 0, 0, 1
                    cursor_color: 0, 0, 0, 1
                    accessibility_text: 'Campo de edición de texto, introduce o pega tu texto aquí.'
                    text_validate_unfocus: False

                Button:
                    text: 'Confirmar y Convertir'
                    id: confirm_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1
                    color: 1, 1, 1, 1
                    accessibility_text: 'Confirmar y convertir, procesa el texto introducido o el archivo adjunto.'
                    on_release: app.on_button_press(self, 'Confirmar y convertir', app.confirm_convert)

                Button:
                    text: 'Efectos'
                    id: effects_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1
                    color: 1, 1, 1, 1
                    accessibility_text: 'Efectos de audio, abre un menú para añadir música de fondo o sonidos a la nota de audio.'
                    on_release: app.on_button_press(self, 'Efectos de audio', app.open_effects_menu)

                Button:
                    text: 'Reproducir'
                    id: play_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1
                    color: 1, 1, 1, 1
                    accessibility_text: 'Reproducir, escucha el resultado de audio previo.'
                    on_release: app.on_button_press(self, 'Reproducir audio', app.play_audio)

                Button:
                    text: 'Descargar Audio Generado'
                    id: download_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1
                    color: 1, 1, 1, 1
                    accessibility_text: 'Descargar audio generado, guarda el archivo de audio en tu almacenamiento local.'
                    on_release: app.on_button_press(self, 'Descargar audio generado', app.download_audio)

                Button:
                    text: 'Menú de Configuración'
                    id: config_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1
                    color: 1, 1, 1, 1
                    accessibility_text: 'Menú de configuración, ajusta parámetros adicionales y selecciona voces.'
                    on_release: app.on_button_press(self, 'Menú de configuración', app.open_config_menu)

                Button:
                    text: 'Salir'
                    id: exit_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1
                    color: 1, 1, 1, 1
                    accessibility_text: 'Salir de la aplicación, cierra la aplicación de forma segura.'
                    on_release: app.on_button_press(self, 'Salir de la aplicación', app.exit_app)
"""

class RootWidget(BoxLayout):
    pass

class MyKivyApp(App):
    def build(self):
        self.title = 'Conversor de Texto a Audio'
        Builder.load_string(KV)
        self.root_widget = RootWidget()
        self.request_android_permissions()
        return self.root_widget

    def on_start(self):
        self.speak_action("Aplicación de Conversión de Texto a Audio iniciada.")

    def speak_action(self, text):
        if tts:
            try:
                tts.speak(text)
            except Exception as e:
                print(f"Error al usar TTS: {e}")
                print(f"TTS Fallback: {text}")
        else:
            print(f"TTS (plyer) no disponible. Mensaje: {text}")

    def on_button_press(self, instance, accessibility_text, action_callback):
        self.speak_action(accessibility_text)
        action_callback()

    def request_android_permissions(self):
        if plyer_platform == 'android' and permissions:
            perms = [
                permissions.READ_EXTERNAL_STORAGE,
                permissions.WRITE_EXTERNAL_STORAGE
            ]
            permissions.request_permissions(perms, self._on_permission_callback)
        else:
            print("No se requieren permisos de Android o plyer.permissions no está disponible.")

    def _on_permission_callback(self, results):
        for perm, status in results.items():
            if status == 'granted':
                print(f"Permiso {perm} concedido.")
                self.speak_action(f"Permiso {perm.split('.')[-1].replace('_', ' ').lower()} concedido.")
            else:
                print(f"Permiso {perm} denegado.")
                self.speak_action(f"Permiso {perm.split('.')[-1].replace('_', ' ').lower()} denegado. Algunas funciones podrían no estar disponibles.")

    def attach_file(self):
        if filechooser:
            try:
                filechooser.open_file(
                    filters=['*.txt', '*.mp3', '*.wav'],
                    on_selection=self.selected_file
                )
            except Exception as e:
                self.speak_action(f"Error al abrir el selector de archivos: {e}")
                print(f"Error opening file chooser: {e}")
        else:
            self.speak_action("El selector de archivos no está disponible en este dispositivo.")
            print("File chooser (plyer) not available.")

    def selected_file(self, selection):
        if selection:
            file_path = selection[0]
            self.speak_action(f"Archivo seleccionado: {file_path.split('/')[-1]}")
            print(f"Selected file: {file_path}")
            if file_path.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.root_widget.ids.text_input.text = content[:5000]
                        if len(content) > 5000:
                            self.speak_action("El archivo de texto es demasiado grande. Se han cargado los primeros 5000 caracteres.")
                        else:
                            self.speak_action("Contenido del archivo de texto cargado en el campo de edición.")
                except Exception as e:
                    self.speak_action(f"Error al leer el archivo de texto: {e}")
                    print(f"Error reading text file: {e}")
            else:
                self.speak_action("Archivo de audio seleccionado. No se puede cargar el contenido en el campo de texto.")
        else:
            self.speak_action("No se seleccionó ningún archivo.")

    def confirm_convert(self):
        text_to_process = self.root_widget.ids.text_input.text
        if text_to_process:
            self.speak_action("Texto confirmado y en proceso de conversión. Esto es una simulación.")
            print(f"Processing text: {text_to_process[:50]}...")
        else:
            self.speak_action("No hay texto para confirmar y convertir. Por favor, introduce o adjunta un archivo.")

    def open_effects_menu(self):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text='Selecciona un efecto:', size_hint_y=None, height=dp(40)))

        effects = ['Música de Fondo', 'Sonidos de Naturaleza', 'Eco', 'Reverb', 'Ninguno']
        for effect in effects:
            btn = Button(
                text=effect,
                size_hint_y=None,
                height=dp(50),
                background_normal='',
                background_color=(1, 0, 0, 1),
                color=(1, 1, 1, 1),
                accessibility_text=f'Seleccionar efecto: {effect}'
            )
            btn.bind(on_release=lambda btn_instance, effect_name=effect: self.select_effect(effect_name, popup))
            content.add_widget(btn)

        popup = Popup(
            title='Menú de Efectos de Audio',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=True
        )
        popup.open()
        self.speak_action("Menú de efectos de audio abierto.")

    def select_effect(self, effect_name, popup_instance):
        self.speak_action(f"Efecto '{effect_name}' seleccionado. Esto es una simulación.")
        print(f"Selected effect: {effect_name}")
        popup_instance.dismiss()

    def play_audio(self):
        self.speak_action("Reproduciendo audio generado. Esto es una simulación.")
        print("Playing generated audio...")

    def download_audio(self):
        self.speak_action("Descargando audio generado. Esto es una simulación.")
        print("Downloading generated audio...")

    def open_config_menu(self):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text='Configuración de Voz y Parámetros:', size_hint_y=None, height=dp(40)))

        voice_label = Label(text='Seleccionar Voz (Gemini API):', size_hint_y=None, height=dp(40), accessibility_text='Etiqueta para seleccionar voz.')
        content.add_widget(voice_label)

        dropdown = DropDown()
        voices = ['Es-ES-Standard-A', 'Es-ES-Wavenet-B', 'Es-US-Standard-C', 'Es-US-Wavenet-D']
        for voice in voices:
            btn = Button(
                text=voice,
                size_hint_y=None,
                height=dp(44),
                background_normal='',
                background_color=(1, 0, 0, 1),
                color=(1, 1, 1, 1),
                accessibility_text=f'Seleccionar voz: {voice}'
            )
            btn.bind(on_release=lambda btn_instance, voice_name=voice: self.select_voice(voice_name, dropdown, popup))
            dropdown.add_widget(btn)

        main_button = Button(
            text='Voz Actual: Es-ES-Standard-A',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            accessibility_text='Botón para seleccionar voz, la voz actual es Es-ES-Standard-A.'
        )
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', f'Voz Actual: {x}'))
        content.add_widget(main_button)

        other_settings_label = Label(text='Otros parámetros (simulación):', size_hint_y=None, height=dp(40), accessibility_text='Etiqueta para otros parámetros de configuración.')
        content.add_widget(other_settings_label)
        
        pitch_button = Button(
            text='Ajustar Tono',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            accessibility_text='Ajustar tono de la voz.'
        )
        pitch_button.bind(on_release=lambda x: self.speak_action("Ajustar tono, esto es una simulación."))
        content.add_widget(pitch_button)

        popup = Popup(
            title='Menú de Configuración',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=True
        )
        popup.open()
        self.speak_action("Menú de configuración abierto.")

    def select_voice(self, voice_name, dropdown_instance, popup_instance):
        self.speak_action(f"Voz '{voice_name}' seleccionada. Esto es una simulación.")
        print(f"Selected voice: {voice_name}")
        dropdown_instance.select(voice_name)

    def exit_app(self):
        self.speak_action("Cerrando la aplicación. Adiós.")
        App.get_running_app().stop()

if __name__ == '__main__':
    MyKivyApp().run()
