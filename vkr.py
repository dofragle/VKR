import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QDialog
import spacy_udpipe
import os

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Приветствие')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)
        
        self.label = QLabel('Добро пожаловать!')
        layout.addWidget(self.label)

        self.how_to_button = QPushButton('Как пользоваться этой программой?')
        self.how_to_button.clicked.connect(self.show_instructions)
        layout.addWidget(self.how_to_button)

        self.start_button = QPushButton('Начать работу')
        self.start_button.clicked.connect(self.show_next_screen)
        layout.addWidget(self.start_button)

    def show_instructions(self):
        instructions = "Инструкции: ...\n" 
        self.label.setText(instructions)

    def show_next_screen(self):
        self.next_screen = FileInputScreen()
        self.next_screen.show()
        self.close()


class FileInputScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Выбор файла')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        self.label = QLabel('Выберите текстовый файл:')
        layout.addWidget(self.label)

        self.file_path_label = QLabel('')
        layout.addWidget(self.file_path_label)

        self.browse_button = QPushButton('Обзор')
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.next_button = QPushButton('Далее')
        self.next_button.clicked.connect(self.show_file_content)
        layout.addWidget(self.next_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '.', 'Text files (*.txt)')
        if file_path:
            self.file_path_label.setText(file_path)

    def show_file_content(self):
        file_path = self.file_path_label.text()
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.next_screen = FileContentScreen(content)
                self.next_screen.show()
                self.close()

    def go_back(self):
        self.prev_screen = WelcomeScreen()
        self.prev_screen.show()
        self.close()


class FileContentScreen(QWidget):
    def __init__(self, content):
        super().__init__()
        self.content = content
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Содержимое файла')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)
        
        self.text_edit = QTextEdit()
        self.text_edit.setText(self.content)
        layout.addWidget(self.text_edit)

        self.analyze_button = QPushButton('Анализировать')
        self.analyze_button.clicked.connect(self.analyze_and_show_result)
        layout.addWidget(self.analyze_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def analyze_and_show_result(self):
        content = self.text_edit.toPlainText()
        if content.strip():  # Проверяем, что текст не пустой
            try:
                analyzed_content = analyze_sentences(content)
                result_dialog = ResultDialog(analyzed_content)
                result_dialog.exec_()  # Вместо result_dialog.exec_()
            except Exception as e:
                print("Ошибка при анализе предложений:", e)
        else:
            print("Пустой текст для анализа.")


    def go_back(self):
        self.prev_screen = FileInputScreen()
        self.prev_screen.show()
        self.close()


class ResultDialog(QDialog):
    def __init__(self, result):
        super().__init__()
        self.result = result
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Результат анализа')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        # Преобразуем список результатов в строку
        result_str = "\n".join([f"Токен: {token}, Тип связи: {dep_type}, Слово-родитель: {parent_word}" for token, dep_type, parent_word in self.result])

        self.result_label = QLabel(result_str)
        layout.addWidget(self.result_label)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.close)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)



def analyze_sentences(text):
    udpipe_model = spacy_udpipe.load("ru")
    parsed = udpipe_model(text)

    # Создаем список для хранения результатов
    parsed_result = []

    # Проходимся по каждому токену в предложении
    for token in parsed:
        # Извлекаем тип связи и слово-родитель
        dep_type = token.dep_
        parent_word = token.head.text

        # Добавляем информацию о токене в список результатов
        parsed_result.append((token.text, dep_type, parent_word))

    return parsed_result



if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome_screen = WelcomeScreen()
    welcome_screen.show()
    sys.exit(app.exec_())

