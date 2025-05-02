from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.config import Config
from kivy.core.text import Label as CoreLabel
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import os
import requests
import json
import pytesseract
from PIL import Image
import PyPDF2
import io

# Configure keyboard shortcuts
Config.set('kivy', 'exit_on_escape', '0')

class CustomTitleBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)  # Fixed height for title bar
        self.padding = [10, 5]
        self.spacing = 10
        
        # Create a container for the language controls that will center them vertically
        self.language_container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),  # Fixed size
            height=dp(40),  # Fixed height for controls
            width=dp(300),  # Fixed width for the container
            spacing=10,
            pos_hint={'center_y': 0.5}  # Center vertically
        )
        
        # Source language spinner with fixed size
        self.source_lang = Spinner(
            text='English',
            values=('English', 'Spanish', 'French', 'German', 'Russian', 'Chinese', 'Italian'),
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        
        # Swap languages button with fixed size
        self.swap_btn = Button(
            text='⇄',
            size_hint=(None, None),
            size=(dp(44), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        
        # Target language spinner with fixed size
        self.target_lang = Spinner(
            text='Spanish',
            values=('English', 'Spanish', 'French', 'German', 'Russian', 'Chinese', 'Italian'),
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        
        # Add widgets to language container
        self.language_container.add_widget(self.source_lang)
        self.language_container.add_widget(self.swap_btn)
        self.language_container.add_widget(self.target_lang)
        
        # Create a container that will center the language_container horizontally
        center_container = BoxLayout(orientation='horizontal')
        center_container.add_widget(Widget())  # Flexible space on the left
        center_container.add_widget(self.language_container)
        center_container.add_widget(Widget())  # Flexible space on the right
        
        # Add the centered container to the title bar
        self.add_widget(center_container)

class TranslationApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_path = self._find_font()
        self.file_chooser = None
        self.popup = None
    
    def _find_font(self):
        """Find a suitable font for Chinese characters"""
        # Common font paths on Linux
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # WenQuanYi Zen Hei
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # WenQuanYi Micro Hei
            '/usr/share/fonts/truetype/droid/DroidSansFallback.ttf',  # Droid Sans Fallback
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # Liberation Sans
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # DejaVu Sans
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        
        # If no font found, return None to use system default
        return None
    
    def show_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.png', '*.jpg', '*.jpeg', '*.pdf']
        )
        content.add_widget(self.file_chooser)
        
        buttons = BoxLayout(size_hint_y=None, height=dp(44))
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        
        select_btn.bind(on_press=self.process_selected_file)
        cancel_btn.bind(on_press=self.dismiss_popup)
        
        buttons.add_widget(select_btn)
        buttons.add_widget(cancel_btn)
        content.add_widget(buttons)
        
        self.popup = Popup(title='Select File', content=content, size_hint=(0.9, 0.9))
        self.popup.open()
    
    def dismiss_popup(self, instance):
        if self.popup:
            self.popup.dismiss()
    
    def process_selected_file(self, instance):
        if self.file_chooser and self.file_chooser.selection:
            file_path = self.file_chooser.selection[0]
            self.dismiss_popup(instance)
            
            try:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    text = self.extract_text_from_image(file_path)
                elif file_path.lower().endswith('.pdf'):
                    text = self.extract_text_from_pdf(file_path)
                else:
                    self.result_text.text = "Unsupported file format"
                    return
                
                self.input_text.text = text
            except Exception as e:
                self.result_text.text = f"Error processing file: {str(e)}"
    
    def extract_text_from_image(self, image_path):
        try:
            image = Image.open(image_path)
            
            # Determine the language for OCR based on source language
            lang_codes = {
                'English': 'eng',
                'Chinese': 'chi_sim+chi_tra',  # Use both simplified and traditional Chinese
                'Russian': 'rus',
                'German': 'deu',
                'French': 'fra',
                'Spanish': 'spa',
                'Italian': 'ita'
            }
            
            # Get the source language from the spinner
            source_lang = self.title_bar.source_lang.text
            lang = lang_codes.get(source_lang, 'eng')
            
            # Configure tesseract parameters for better accuracy
            custom_config = f'-l {lang} --psm 3'
            
            # Preprocess image for better OCR
            # Convert to RGB if image is in RGBA
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            text = pytesseract.image_to_string(image, config=custom_config)
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path):
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def build(self):
        # Set minimum window size
        Window.minimum_width = dp(600)
        Window.minimum_height = dp(400)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=5)
        
        # Custom title bar with language selection
        self.title_bar = CustomTitleBar()
        main_layout.add_widget(self.title_bar)
        
        # Text input area
        self.input_text = TextInput(
            multiline=True,
            hint_text='Enter text to translate...',
            size_hint_y=0.4,  # Take 40% of available height
            font_name=self.font_path if self.font_path else '',
            font_size=14,
            allow_copy=True
        )
        
        # Translation engine selection and buttons
        engine_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=10,
            padding=[10, 5]
        )
        
        # Engine spinner with fixed size
        self.engine = Spinner(
            text='Google',
            values=('Google', 'DuckDuckGo', 'Yandex', 'DeepL'),
            size_hint=(None, None),
            size=(dp(150), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        
        # File selection button with fixed size
        file_btn = Button(
            text='Select Image/PDF',
            size_hint=(None, None),
            size=(dp(150), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        file_btn.bind(on_press=self.show_file_chooser)
        
        # Translate button with fixed size
        translate_btn = Button(
            text='Translate',
            size_hint=(None, None),
            size=(dp(150), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        translate_btn.bind(on_press=self.translate_text)
        
        # Copy button with fixed size
        copy_btn = Button(
            text='Copy Translation',
            size_hint=(None, None),
            size=(dp(150), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        copy_btn.bind(on_press=self.copy_translation)
        
        # Add buttons to engine layout with flexible space between them
        engine_layout.add_widget(self.engine)
        engine_layout.add_widget(Widget(size_hint_x=0.1))  # Flexible space
        engine_layout.add_widget(file_btn)
        engine_layout.add_widget(Widget(size_hint_x=0.1))  # Flexible space
        engine_layout.add_widget(translate_btn)
        engine_layout.add_widget(Widget(size_hint_x=0.1))  # Flexible space
        engine_layout.add_widget(copy_btn)
        engine_layout.add_widget(Widget(size_hint_x=0.1))  # Flexible space
        
        # Result text area
        self.result_text = TextInput(
            multiline=True,
            readonly=True,
            hint_text='Translation will appear here...',
            size_hint_y=0.4,  # Take 40% of available height
            font_name=self.font_path if self.font_path else '',
            font_size=14,
            allow_copy=True
        )
        
        # Add all widgets to main layout
        main_layout.add_widget(self.input_text)
        main_layout.add_widget(engine_layout)
        main_layout.add_widget(self.result_text)
        
        # Bind swap button
        self.title_bar.swap_btn.bind(on_press=self.swap_languages)
        
        return main_layout
    
    def swap_languages(self, instance):
        # Swap source and target languages
        current_source = self.title_bar.source_lang.text
        self.title_bar.source_lang.text = self.title_bar.target_lang.text
        self.title_bar.target_lang.text = current_source
    
    def translate_text(self, instance):
        text = self.input_text.text
        if not text:
            return
            
        # Map language names to their correct API codes
        language_codes = {
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'russian': 'ru',
            'chinese': 'zh',
            'italian': 'it'
        }
        
        # Map engine names to their API identifiers
        engine_codes = {
            'google': 'google',
            'duckduckgo': 'duckduckgo',
            'yandex': 'yandex',
            'deepl': 'deepl'
        }
        
        source_lang = language_codes.get(self.title_bar.source_lang.text.lower(), 'en')
        target_lang = language_codes.get(self.title_bar.target_lang.text.lower(), 'es')
        engine = engine_codes.get(self.engine.text.lower(), 'google')
        
        try:
            # API endpoint with query parameters
            url = f"https://translate.librenode.com/api/translate?from={source_lang}&to={target_lang}&engine={engine}&text={requests.utils.quote(text)}"
            
            # Print debug information
            print(f"Making request to: {url}")
            
            # Make API request with proper headers
            headers = {
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            
            # Print response details for debugging
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response content: {response.text[:500]}")  # Print first 500 chars of response
            
            response.raise_for_status()
            
            try:
                result = response.json()
                if 'translated-text' in result:
                    self.result_text.text = result['translated-text']
                else:
                    self.result_text.text = f"Translation failed: Unexpected response format. Response: {response.text[:100]}"
            except json.JSONDecodeError as json_err:
                self.result_text.text = f"Error parsing response: {str(json_err)}. Response: {response.text[:100]}"
            
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 400:
                try:
                    error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                    self.result_text.text = f"Error: {error_detail}"
                except json.JSONDecodeError:
                    self.result_text.text = f"Error: {response.text[:100]}"
            else:
                self.result_text.text = f"HTTP Error: {str(http_err)}"
        except requests.exceptions.RequestException as req_err:
            self.result_text.text = f"Request Error: {str(req_err)}"
        except Exception as e:
            self.result_text.text = f"Unexpected Error: {str(e)}"
    
    def copy_translation(self, instance):
        if self.result_text.text:
            Clipboard.copy(self.result_text.text)

if __name__ == '__main__':
    TranslationApp().run()
