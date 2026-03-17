import string
import secrets
import pyperclip

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup


# =========================
# Password Logic (SECURE)
# =========================
def generate_password(length=12, use_upper=True, use_digits=True, use_special=True):
    if length < 6:
        raise ValueError("Password must be at least 6 characters")

    char_pool = list(string.ascii_lowercase)
    password = []

    if use_upper:
        char_pool += list(string.ascii_uppercase)
        password.append(secrets.choice(string.ascii_uppercase))

    if use_digits:
        char_pool += list(string.digits)
        password.append(secrets.choice(string.digits))

    if use_special:
        char_pool += list(string.punctuation)
        password.append(secrets.choice(string.punctuation))

    # Fill remaining characters
    while len(password) < length:
        password.append(secrets.choice(char_pool))

    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


def check_strength(password):
    score = 0
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 1:
        return "Weak"
    elif score == 2:
        return "Moderate"
    elif score == 3:
        return "Strong"
    else:
        return "Very Strong"


# =========================
# App UI
# =========================
class PasswordGeneratorApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=12, spacing=10)

        # Title
        self.root.add_widget(Label(text="GenPass 🔐", font_size=22))

        # Length Input
        self.root.add_widget(Label(text="Password Length"))
        self.length_input = TextInput(text='12', multiline=False, input_filter='int')
        self.root.add_widget(self.length_input)

        # Checkboxes
        self.upper_checkbox = CheckBox(active=True)
        self.digits_checkbox = CheckBox(active=True)
        self.special_checkbox = CheckBox(active=True)

        self.root.add_widget(self._build_row("Include Uppercase", self.upper_checkbox))
        self.root.add_widget(self._build_row("Include Digits", self.digits_checkbox))
        self.root.add_widget(self._build_row("Include Special Characters", self.special_checkbox))

        # Generate Button
        self.generate_button = Button(text="Generate Password")
        self.generate_button.bind(on_press=self.generate_password)
        self.root.add_widget(self.generate_button)

        # Output
        self.root.add_widget(Label(text="Generated Password"))
        self.password_output = TextInput(readonly=True, multiline=False)
        self.root.add_widget(self.password_output)

        # Strength Label
        self.strength_label = Label(text="Strength: ")
        self.root.add_widget(self.strength_label)

        # Copy Button
        self.copy_button = Button(text="Copy to Clipboard")
        self.copy_button.bind(on_press=self.copy_password)
        self.root.add_widget(self.copy_button)

        return self.root

    def _build_row(self, text, checkbox):
        layout = BoxLayout(orientation='horizontal', spacing=10)
        layout.add_widget(Label(text=text))
        layout.add_widget(checkbox)
        return layout

    def generate_password(self, instance):
        try:
            length = int(self.length_input.text)
            password = generate_password(
                length,
                self.upper_checkbox.active,
                self.digits_checkbox.active,
                self.special_checkbox.active
            )

            self.password_output.text = password
            self.strength_label.text = f"Strength: {check_strength(password)}"

        except ValueError as e:
            self.show_error(str(e))

    def copy_password(self, instance):
        if self.password_output.text:
            pyperclip.copy(self.password_output.text)

    def show_error(self, message):
        popup = Popup(
            title='Input Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()


if __name__ == "__main__":
    PasswordGeneratorApp().run()