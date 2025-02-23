from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont
from googletrans import Translator
import speech_recognition as sr
from languages import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.unitUI()
        self.connects()

    def settings(self):
        # Setting up the basics
        # window title, width, height
        self.setWindowTitle("Transly")
        self.setGeometry(250, 250, 600, 500)

    def unitUI(self):
        # All widgets app will need
        self.input_box = QTextEdit()
        self.output_box = QTextEdit()
        self.reverse = QPushButton("Reversed")
        self.reset = QPushButton("Reset")
        self.submit = QPushButton("Submit")
        self.speak_btn = QPushButton("Speak")
        self.input_option = QComboBox()
        self.output_option = QComboBox()
        self.title = QLabel("Transly")
        self.title.setFont(QFont("Arial", 55))

        self.input_option.addItems(values)
        self.output_option.addItems(values)

        parent = QHBoxLayout(self)
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(self.title)
        col1.addWidget(self.input_option)
        col1.addWidget(self.output_option)
        col1.addWidget(self.submit)
        col1.addWidget(self.speak_btn)
        col1.addWidget(self.reset)

        col2.addWidget(self.input_box)
        col2.addWidget(self.reverse)
        col2.addWidget(self.output_box)

        parent.addLayout(col1, 20)
        parent.addLayout(col2, 80)

        self.setStyleSheet("""
            QWidget {
                background-color: #2a576f;
                color: #e3e8ec;
            }
            QPushButton {
                background-color: #84a98c;
                color: #fff;
                border: 1px solid #84a98c;
                border-radius: 5px;
                padding: 10px 10px;
            }
            QTextEdit {
                background-color: #84a98c;
                color: #333;
            }
            QComboBox {
                background-color: #84a98c;
                color: #333;
                border-radius: 5px;
                padding: 10px 10px;
            }
            QLabel {
                color: #fff;
            }
            QPushButton:hover {
                background-color: #6e8f72;
            }
        """)

    def translate_click(self):
        try:
            value_to_key1 = self.output_option.currentText()
            key_to_value1 = [k for k, v in LANGUAGES.items() if v == value_to_key1]

            value_to_key2 = self.input_option.currentText()
            key_to_value2 = [k for k, v in LANGUAGES.items() if v == value_to_key2]

            self.script = self.translate_text(self.input_box.toPlainText(), key_to_value1[0], key_to_value2[0])

            self.output_box.setText(self.script)

        except Exception as e:
            print("Exception", e)
            self.input_box.setText("You must enter text to translate here...")

    def translate_text(self, text, d_lang, s_lang):
        speaker = Translator()
        translation = speaker.translate(text, dest=d_lang, src=s_lang)
        return translation.text

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5)
                recognized_text = recognizer.recognize_google(audio)
                return recognized_text
            except sr.UnknownValueError:
                self.output_box.setText("Could not understand audio")
            except sr.RequestError as e:
                self.output_box.setText(f"Error requesting speech results: {e}")
            except Exception as e:
                self.output_box.setText(f"Error recognizing speech: {e}")

    def recognize_and_translate(self):
        text = self.recognize_speech()
        if text:
            self.input_box.setText(text)
            self.translate_click()

    def reverse_text(self):
        input_text = self.input_box.toPlainText()
        output_text = self.output_box.toPlainText()
        input_lang = self.input_option.currentText()
        output_lang = self.output_option.currentText()

        self.input_box.setText(output_text)
        self.output_box.setText(input_text)
        self.input_option.setCurrentText(output_lang)
        self.output_option.setCurrentText(input_lang)

    def clear_boxes(self):
        self.input_box.clear()
        self.output_box.clear()

    def connects(self):
        self.submit.clicked.connect(self.translate_click)  # Fixed this line
        self.reverse.clicked.connect(self.reverse_text)
        self.reset.clicked.connect(self.clear_boxes)
        self.speak_btn.clicked.connect(self.recognize_and_translate)


if __name__ == "__main__":
    app = QApplication([])
    main = Main()
    main.show()
    app.exec_()