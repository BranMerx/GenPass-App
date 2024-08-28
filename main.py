import random
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

# Password generation function
def gen_password(length=12, upper_include=True, digits_include=True, specialChars_include=True):
    if length < 6:
        raise ValueError("Password must be at least six characters")

    characters = list(string.ascii_lowercase)  # Always include lowercase letters
    if upper_include:
        characters += list(string.ascii_uppercase)
    if digits_include:
        characters += list(string.digits)
    if specialChars_include:
        characters += list(string.punctuation)

    password = []
    if upper_include:
        password.append(random.choice(string.ascii_uppercase))
    if digits_include:
        password.append(random.choice(string.digits))
    if specialChars_include:
        password.append(random.choice(string.punctuation))
    password += [random.choice(characters) for _ in range(length - len(password))]

    random.shuffle(password)
    return ''.join(password)

# Main application class
class PasswordGeneratorApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Password Length Input
        self.root.add_widget(Label(text="Password Length:"))
        self.length_input = TextInput(text='12', multiline=False, input_filter='int')
        self.root.add_widget(self.length_input)

        # Include Upper Case Letters
        upper_layout = BoxLayout(orientation ='horizontal', spacing = 10)
        self.upper_checkbox = CheckBox(active = True)
        upper_layout.add_widget(Label(text = "Include Upper Case Letters:"))
        upper_layout.add_widget(self.upper_checkbox)
        self.root.add_widget(upper_layout)

        # Include Numerical Digits
        digits_layout = BoxLayout(orientation ='horizontal', spacing = 10)
        self.digits_checkbox = CheckBox(active = True)
        digits_layout.add_widget(Label(text = "Include Numerical Digits:"))
        digits_layout.add_widget(self.digits_checkbox)
        self.root.add_widget(digits_layout)

        # Include Special Characters
        special_layout = BoxLayout(orientation ='horizontal', spacing = 10)
        self.special_checkbox = CheckBox(active = True)
        special_layout.add_widget(Label(text = "Include Special Characters:"))
        special_layout.add_widget(self.special_checkbox)
        self.root.add_widget(special_layout)

        # Generate Button
        self.generate_button = Button(text="Generate Password")
        self.generate_button.bind(on_press=self.generate_password)
        self.root.add_widget(self.generate_button)

        # Display the Generated Password
        self.root.add_widget(Label(text="Generated Password:"))
        self.password_output = TextInput(readonly=True, multiline=False)
        self.root.add_widget(self.password_output)

        return self.root

    def generate_password(self, instance):
        try:
            length = int(self.length_input.text)
            upper = self.upper_checkbox.active
            digits = self.digits_checkbox.active
            special_chars = self.special_checkbox.active

            password = gen_password(length, upper, digits, special_chars)
            self.password_output.text = password

        except ValueError as e:
            self.show_error(str(e))

    def show_error(self, message):
        popup = Popup(title='Input Error',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__":
    PasswordGeneratorApp().run()
