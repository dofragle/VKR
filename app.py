import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QDialog, QComboBox
import os
from analyze import *

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

        self.analysis_method_label = QLabel('Метод анализа:')
        layout.addWidget(self.analysis_method_label)

        self.analysis_method_combo = QComboBox()
        self.analysis_method_combo.addItem("spacy_udpipe")
        self.analysis_method_combo.addItem("Natasha")
        self.analysis_method_combo.addItem("MaltParser")
        self.analysis_method_combo.addItem("DeepPavlov")
        self.analysis_method_combo.addItem("Stanza")
        layout.addWidget(self.analysis_method_combo)

        self.analyze_button = QPushButton('Анализировать')
        self.analyze_button.clicked.connect(self.analyze_and_show_result)
        layout.addWidget(self.analyze_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def analyze_and_show_result(self):
        content = self.text_edit.toPlainText()
        analysis_method = self.analysis_method_combo.currentText()

        if content.strip():  
            try:
                if analysis_method == "spacy_udpipe":
                    analyzed_content = analyze_sentences(content)
                elif analysis_method == "Natasha":
                    analyzed_content = analyze_with_natasha(content)
                elif analysis_method == "MaltParser":
                    analyzed_content = analyze_with_maltparser(content)
                elif analysis_method == "DeepPavlov":
                    analyzed_content = analyze_with_deeppavlov(content)
                elif analysis_method == "Stanza":
                    analyzed_content = analyze_with_stanza(content)
                else:
                    raise ValueError("Неверный метод анализа выбран")
                
                result_dialog = ResultDialog(analyzed_content)
                result_dialog.exec_()
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
