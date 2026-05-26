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

# Import plyer for Android-specific functionalities
try:
    from plyer import tts, filechooser, permissions
    from plyer.utils import platform as plyer_platform
except ImportError:
    # Fallback for desktop development without plyer
    tts = None
    filechooser = None
    permissions = None
    plyer_platform = 'desktop'
    print("Plyer not found. Some functionalities (TTS, FileChooser, Permissions) will be disabled.")

# Kivy Builder String for UI layout and styling
KV = """
<RootWidget>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.498, 1, 0.831, 1  # Aquamarine color #7FFFD4
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
                    background_color: 1, 0, 0, 1  # Red color #FF0000
                    color: 1, 1, 1, 1
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
                    text_validate_unfocus: False # Keep focus on Android keyboard

                Button:
                    text: 'Confirmar y Convertir'
                    id: confirm_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1  # Red color #FF0000
                    color: 1, 1, 1, 1
                    on_release: app.on_button_press(self, 'Confirmar y convertir', app.confirm_convert)

                Button:
                    text: 'Efectos'
                    id: effects_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1  # Red color #FF0000
                    color: 1, 1, 1, 1
                    on_release: app.on_button_press(self, 'Efectos de audio', app.open_effects_menu)

                Button:
                    text: 'Reproducir'
                    id: play_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1  # Red color #FF0000
                    color: 1, 1, 1, 1
                    on_release: app.on_button_press(self, 'Reproducir audio', app.play_audio)

                Button:
                    text: 'Descargar Audio Generado'
                    id: download_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1  # Red color #FF0000
                    color: 1, 1, 1, 1
                    on_release: app.on_button_press(self, 'Descargar audio generado', app.download_audio)

                Button:
                    text: 'Menú de Configuración'
                    id: config_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1  # Red color #FF0000
                    color: 1, 1, 1, 1
                    on_release: app.on_button_press(self, 'Menú de configuración', app.open_config_menu)

                Button:
                    text: 'Salir'
                    id: exit_button
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ''
                    background_color: 1, 0, 0, 1  # Red color #FF0000
                    color: 1, 1, 1, 1
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
        # Initial TTS announcement for accessibility
        self.speak_action("Aplicación de Conversión de Texto a Audio iniciada.")

    def speak_action(self, text):
        """Emits a voice feedback using TTS."""
        if tts:
            try:
                tts.speak(text)
            except Exception as e:
                print(f"Error al usar TTS: {e}")
                # Fallback to print if TTS fails
                print(f"TTS Fallback: {text}")
        else:
            print(f"TTS (plyer) no disponible. Mensaje: {text}")

        """Generic callback for button presses to provide TTS feedback and then trigger the action."""
        action_callback()

    def request_android_permissions(self):
        """Requests necessary Android permissions."""
        if plyer_platform == 'android' and permissions:
            perms = [
                permissions.READ_EXTERNAL_STORAGE,
                permissions.WRITE_EXTERNAL_STORAGE
            ]
            permissions.request_permissions(perms, self._on_permission_callback)
        else:
            print("No se requieren permisos de Android o plyer.permissions no está disponible.")

    def _on_permission_callback(self, results):
        """Callback for permission requests."""
        for perm, status in results.items():
            if status == 'granted':
                print(f"Permiso {perm} concedido.")
                self.speak_action(f"Permiso {perm.split('.')[-1].replace('_', ' ').lower()} concedido.")
            else:
                print(f"Permiso {perm} denegado.")
                self.speak_action(f"Permiso {perm.split('.')[-1].replace('_', ' ').lower()} denegado. Algunas funciones podrían no estar disponibles.")

    def attach_file(self):
        """Opens a file chooser to select text or audio files."""
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
        """Callback for file chooser selection."""
        if selection:
            file_path = selection[0]
            self.speak_action(f"Archivo seleccionado: {file_path.split('/')[-1]}")
            print(f"Selected file: {file_path}")
            if file_path.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.root_widget.ids.text_input.text = content[:5000] # Limit to 5000 chars
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
        """Placeholder for text processing and conversion."""
        text_to_process = self.root_widget.ids.text_input.text
        if text_to_process:
            self.speak_action("Texto confirmado y en proceso de conversión. Esto es una simulación.")
            print(f"Processing text: {text_to_process[:50]}...")
            # Here would be the actual logic to send text to Gemini API or similar
        else:
            self.speak_action("No hay texto para confirmar y convertir. Por favor, introduce o adjunta un archivo.")

    def open_effects_menu(self):
        """Opens a popup menu for audio effects."""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text='Selecciona un efecto:', size_hint_y=None, height=dp(40)))

        effects = ['Música de Fondo', 'Sonidos de Naturaleza', 'Eco', 'Reverb', 'Ninguno']
        for effect in effects:
            btn = Button(
                text=effect,
                size_hint_y=None,
                height=dp(50),
                background_normal='',
                background_color=(1, 0, 0, 1), # Red
                color=(1, 1, 1, 1),
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
        """Handles selection of an audio effect."""
        self.speak_action(f"Efecto '{effect_name}' seleccionado. Esto es una simulación.")
        print(f"Selected effect: {effect_name}")
        popup_instance.dismiss()

    def play_audio(self):
        """Placeholder for playing the generated audio."""
        self.speak_action("Reproduciendo audio generado. Esto es una simulación.")
        print("Playing generated audio...")
        # Here would be the actual logic to play audio

    def download_audio(self):
        """Placeholder for downloading the generated audio."""
        self.speak_action("Descargando audio generado. Esto es una simulación.")
        print("Downloading generated audio...")
        # Here would be the actual logic to save the audio file

    def open_config_menu(self):
        """Opens a popup menu for configuration, including Gemini voices."""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text='Configuración de Voz y Parámetros:', size_hint_y=None, height=dp(40)))

        # Voice selection (simulated Gemini voices)
        content.add_widget(voice_label)

        dropdown = DropDown()
        voices = ['Es-ES-Standard-A', 'Es-ES-Wavenet-B', 'Es-US-Standard-C', 'Es-US-Wavenet-D']
        for voice in voices:
            btn = Button(
                text=voice,
                size_hint_y=None,
                height=dp(44),
                background_normal='',
                background_color=(1, 0, 0, 1), # Red
                color=(1, 1, 1, 1),
            )
            btn.bind(on_release=lambda btn_instance, voice_name=voice: self.select_voice(voice_name, dropdown, popup))
            dropdown.add_widget(btn)

        main_button = Button(
            text='Voz Actual: Es-ES-Standard-A',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(1, 0, 0, 1), # Red
            color=(1, 1, 1, 1),
        )
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', f'Voz Actual: {x}'))
        content.add_widget(main_button)

        # Placeholder for other settings
        content.add_widget(other_settings_label)
        
        # Example: Pitch control
        pitch_button = Button(
            text='Ajustar Tono',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(1, 0, 0, 1), # Red
            color=(1, 1, 1, 1),
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
        """Handles selection of a voice."""
        self.speak_action(f"Voz '{voice_name}' seleccionada. Esto es una simulación.")
        print(f"Selected voice: {voice_name}")
        dropdown_instance.select(voice_name) # Update the main button text
        # popup_instance.dismiss() # Keep popup open for other settings

    def exit_app(self):
        """Closes the application."""
        self.speak_action("Cerrando la aplicación. Adiós.")
        App.get_running_app().stop()

if __name__ == '__main__':
    MyKivyApp().run()

# IMPORTANT: For Android compilation with Buildozer, add the following to your buildozer.spec file:
#
# requirements = python3,kivy,plyer
# android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET
#
# INTERNET permission is good practice if you plan to integrate with actual APIs like Gemini.
#
# To build:
# buildozer init
# (edit buildozer.spec as above)
# buildozer android debug deploy run
#