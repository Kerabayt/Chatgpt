import sys
import typing
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from ui import Ui_MainWindow
import openai
chat_model='gpt-3.5-turbo'
max_tokens=3000
temperature=0.7
KEY = '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'
openai.api_key = KEY
print(chat_model)
# Зберігання попередніх запитань і відповідей
conversation = []
def generate_response():#генерування відповіді
    prompt=ex.ui.lineEdit.text()
    messages = []

    # Додаємо попередні запитання і відповіді до контексту
    for i in range(0, len(conversation), 2):
        messages.append({"role": "system", "content": f"You: {conversation[i]}"})
        messages.append({"role": "user", "content": f"chat gpt: {conversation[i + 1]}"})
    messages.append({"role": "system", "content": "You:"})
    messages.append({"role": "user", "content": prompt})
    api_key = KEY
    temperature = ex.ui.doubleSpinBox.value()
    res = None
    if chat_model != 'text-davinci-003' or 'gpt-4' or 'gpt-4-32k':
        ex.ui.plainTextEdit.appendPlainText('Користувач: '+ str(ex.ui.lineEdit.text()))
        response = openai.ChatCompletion.create(
            model=chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "\n".join(f"{m['role']}: {m['content']}" for m in messages)}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        if response and response.choices:
            ex.ui.plainTextEdit.appendPlainText('ChatGPT: '+ str(response.choices[0].message['content']))
            reset()
            current_response = response.choices[0].message['content']
            # Зберігаємо поточне запитання і відповідь
            conversation.append(prompt)
            conversation.append(current_response)

        
        else:
            ex.ui.plainTextEdit.appendPlainText('помилка, спробуйте ще раз')

        reset()
def reset():
    ex.ui.lineEdit.setText(None)
def resetchat():
    ex.ui.plainTextEdit.setPlainText(None)
#вибір язикової моделі
def td003():
    global chat_model
    global max_tokens
    chat_model = 'text-davinci-003'
    max_tokens=4000
def gpt4():
    global chat_model
    global max_tokens
    chat_model = ''
    max_tokens=8000
def gpt432k():
    global chat_model
    global max_tokens
    chat_model = 'gpt-4-32k'
    max_tokens=32500
def gpt35t():
    global chat_model
    global max_tokens
    max_tokens=3000
    chat_model = 'gpt-3.5-turbo'
def gpt35t16k():
    global chat_model
    global max_tokens
    chat_model = 'gpt-3.5-turbo-16k'
    max_tokens=15000
def save_file(window):
    # Відкриваємо діалог вибору папки та файлу
    file_path, _ = QFileDialog.getSaveFileName(window, 'Зберегти файл', '', 'Text Files (*.txt)')
    if file_path:
        text = ex.ui.plainTextEdit.toPlainText()
        with open(file_path, 'w') as file:
            file.write(text)
        print(f"Значення перемінної збережено в файлі: {file_path}")
def onChange():
    Text = ex.ui.lineEdit.text()
class Widjet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(resetchat)
        self.ui.lineEdit.textChanged.connect(onChange)
        self.ui.pushButton.clicked.connect(generate_response)
        self.ui.gpt35t.clicked.connect(gpt35t)
        self.ui.gpt35t16k.clicked.connect(gpt35t16k)
        self.ui.gpt4.clicked.connect(gpt4)
        self.ui.gpt432k.clicked.connect(gpt432k)
        self.ui.pushButton_2.clicked.connect(lambda: save_file(self))
        self.ui.gpt35t16k_2.clicked.connect(td003)
app = QApplication(sys.argv)
ex = Widjet()
ex.show()
sys.exit(app.exec_())
