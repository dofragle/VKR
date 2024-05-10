import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QDialog, QComboBox, QCheckBox
import os
from analyze import *
from syntax_tree import *
from test_lasuas import * 

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

        self.start_button = QPushButton('Начать работу')
        self.start_button.clicked.connect(self.show_mode_selection_screen)
        layout.addWidget(self.start_button)

    def show_mode_selection_screen(self):
        self.next_screen = ModeSelectionScreen()
        self.next_screen.show()
        self.close()


class ModeSelectionScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Выбор режима работы')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        self.label = QLabel('Выберите режим работы:')
        layout.addWidget(self.label)

        self.individual_sentences_button = QPushButton('Работа с отдельными предложениями')
        self.individual_sentences_button.clicked.connect(self.show_individual_sentences_screen)
        layout.addWidget(self.individual_sentences_button)

        self.text_work_button = QPushButton('Работа с текстом')
        self.text_work_button.clicked.connect(self.show_text_work_screen)
        layout.addWidget(self.text_work_button)

        self.dataset_work_button = QPushButton('Работа с датасетом: подсчет метрик UAS/LAS')
        self.dataset_work_button.clicked.connect(self.show_dataset_work_screen)
        layout.addWidget(self.dataset_work_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def show_individual_sentences_screen(self):
        self.next_screen = FileInputScreen()
        self.next_screen.show()
        self.close()

    def show_text_work_screen(self):
        self.next_screen = TextWorkScreen()
        self.next_screen.show()
        self.close()

    def show_dataset_work_screen(self):
        self.next_screen = DatasetWorkScreen()
        self.next_screen.show()
        self.close()

    def go_back(self):
        self.prev_screen = WelcomeScreen()
        self.prev_screen.show()
        self.close()

#Первый режим работы

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
        self.analysis_method_combo.addItem("DeepPavlov")
        self.analysis_method_combo.addItem("Stanza")
        layout.addWidget(self.analysis_method_combo)

        self.save_conllu_checkbox = QCheckBox('Сохранить файл .conllu')
        layout.addWidget(self.save_conllu_checkbox)

        self.conllu_file_path_label = QLabel('')
        layout.addWidget(self.conllu_file_path_label)

        self.conllu_file_path_button = QPushButton('Выбрать место сохранения')
        self.conllu_file_path_button.clicked.connect(self.choose_conllu_file_path)
        layout.addWidget(self.conllu_file_path_button)

        self.analyze_button = QPushButton('Анализировать')
        self.analyze_button.clicked.connect(self.analyze_and_show_result)
        layout.addWidget(self.analyze_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def choose_conllu_file_path(self):
        conllu_file_path, _ = QFileDialog.getSaveFileName(self, 'Выберите место сохранения', '.', 'CONLLU files (*.conllu)')
        if conllu_file_path:
            self.conllu_file_path_label.setText(conllu_file_path)

    def analyze_and_show_result(self):
        content = self.text_edit.toPlainText()
        analysis_method = self.analysis_method_combo.currentText()

        if content.strip():
            try:
                if analysis_method == "spacy_udpipe":
                    analyzed_content = analyze_sentences(content)
                elif analysis_method == "Natasha":
                    analyzed_content = analyze_with_natasha(content)
                elif analysis_method == "DeepPavlov":
                    analyzed_content = analyze_with_deeppavlov(content)
                elif analysis_method == "Stanza":
                    analyzed_content = analyze_with_stanza(content)
                else:
                    raise ValueError("Неверный метод анализа выбран")
                
                if self.save_conllu_checkbox.isChecked():
                    conllu_file_path = self.conllu_file_path_label.text()
                    self.save_to_conllu(analyzed_content, conllu_file_path)


            except Exception as e:
                print("Ошибка при анализе предложений:", e)
        else:
            print("Пустой текст для анализа.")
        show_result(analyzed_content)

    def go_back(self):
        self.prev_screen = FileInputScreen()
        self.prev_screen.show()
        self.close()
        
    def save_to_conllu(self, analyzed_content, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as conllu_file:
                for sentence in analyzed_content:
                     conllu_file.write(sentence)
                     conllu_file.write('\n')
                     
        except Exception as e:
            print("Ошибка при сохранении в формат .conllu:", e)

#Второй режим работы

class TextWorkScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Работа с текстом')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        self.label = QLabel('Выберите текстовый файл:')
        layout.addWidget(self.label)

        self.file_path_label = QLabel('')
        layout.addWidget(self.file_path_label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.browse_button = QPushButton('Обзор')
        self.browse_button.clicked.connect(self.load_file_and_show_content)
        layout.addWidget(self.browse_button)

        self.next_button = QPushButton('Далее')
        self.next_button.clicked.connect(self.show_save_conllu_screen)
        layout.addWidget(self.next_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def load_file_and_show_content(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '.', 'Text files (*.txt)')
        if file_path:
            self.file_path_label.setText(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setPlainText(content)

    def show_save_conllu_screen(self):
        file_path = self.file_path_label.text()
        content = self.text_edit.toPlainText()
        if not file_path:
            print("Файл не выбран.")
            return
        if not content:
            print("Файл пуст.")
            return

        self.next_screen = SaveConlluScreen(file_path, content)
        self.next_screen.show()
        self.close()

    def go_back(self):
        self.prev_screen = ModeSelectionScreen()
        self.prev_screen.show()
        self.close()


class SaveConlluScreen(QWidget):
    def __init__(self, file_path, content):
        super().__init__()
        self.file_path = file_path
        self.content = content
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Сохранение файла CONLLU')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        self.label = QLabel('Выберите место сохранения файла CONLLU:')
        layout.addWidget(self.label)

        self.conllu_file_path_label = QLabel('')
        layout.addWidget(self.conllu_file_path_label)

        self.conllu_file_path_button = QPushButton('Обзор')
        self.conllu_file_path_button.clicked.connect(self.choose_conllu_file_path)
        layout.addWidget(self.conllu_file_path_button)

        self.next_button = QPushButton('Далее')
        self.next_button.clicked.connect(self.show_analyzer_screen)
        layout.addWidget(self.next_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def choose_conllu_file_path(self):
        conllu_file_path, _ = QFileDialog.getSaveFileName(self, 'Выберите место сохранения', '.', 'CONLLU files (*.conllu)')
        if conllu_file_path:
            self.conllu_file_path_label.setText(conllu_file_path)

    def show_analyzer_screen(self):
        conllu_file_path = self.conllu_file_path_label.text()
        if not conllu_file_path:
            print("Путь для сохранения файла CONLLU не выбран.")
            return

        self.next_screen = AnalyzerSelectionScreen(self.file_path, self.content, conllu_file_path)
        self.next_screen.show()
        self.close()

    def go_back(self):
        self.prev_screen = TextWorkScreen()
        self.prev_screen.show()
        self.close()


class AnalyzerSelectionScreen(QWidget):
    def __init__(self, file_path, content, conllu_file_path):
        super().__init__()
        self.file_path = file_path
        self.content = content
        self.conllu_file_path = conllu_file_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Выбор анализатора')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        self.label = QLabel('Выберите метод анализа:')
        layout.addWidget(self.label)

        self.analysis_method_combo = QComboBox()
        self.analysis_method_combo.addItem("spacy_udpipe")
        self.analysis_method_combo.addItem("Natasha")
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
        content = self.content
        analysis_method = self.analysis_method_combo.currentText()

        try:
            if analysis_method == "spacy_udpipe":
                analyzed_content = [analyze_sentences(sentence) for sentence in content.split('\n') if sentence.strip()]
            elif analysis_method == "Natasha":
                analyzed_content = [analyze_with_natasha(sentence) for sentence in content.split('\n') if sentence.strip()]
            elif analysis_method == "DeepPavlov":
                analyzed_content = [analyze_with_deeppavlov(sentence) for sentence in content.split('\n') if sentence.strip()]
            elif analysis_method == "Stanza":
                analyzed_content = [analyze_with_stanza(sentence) for sentence in content.split('\n') if sentence.strip()]
            else:
                raise ValueError("Неверный метод анализа выбран")
            
            conll_file_path = self.conllu_file_path
            self.save_to_conllu(analyzed_content, conll_file_path)

        except Exception as e:
            print("Ошибка при анализе текста:", e)

    def save_to_conllu(self, analyzed_content, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as conllu_file:
                for sentence in analyzed_content:
                    conllu_file.write(sentence[0])
                    conllu_file.write('\n')
        except Exception as e:
            print("Ошибка при сохранении в формат .conllu:", e)

    def go_back(self):
        self.prev_screen = SaveConlluScreen(self.file_path, self.content)
        self.prev_screen.show()
        self.close()

#3 режим работы
import matplotlib.pyplot as plt
import seaborn as sns

class VisualizationScreen(QDialog):
    def __init__(self, uas, las):
        super().__init__()
        self.setWindowTitle('График метрик UAS/LAS')
        self.initUI(uas, las)

    def initUI(self, uas, las):
        layout = QVBoxLayout()

        # Create figure and axes
        fig, ax = plt.subplots()

        # Make a separate list for each metric
        x1 = las
        x2 = uas

        # Assign colors for each metric and the names
        colors = ['#E69F00', '#56B4E9']
        names = ['LAS', 'UAS']

        # Make the histogram using a list of lists
        # Normalize the metrics and assign colors and names
        ax.hist([x1, x2], color=colors, label=names)

        # Plot formatting
        ax.legend()
        ax.set_xlabel('Оценка')
        ax.set_ylabel('Количество предложений')

        # Add the plot to the layout
        layout.addWidget(ax.figure.canvas)

        # Set layout for the window
        self.setLayout(layout)

class DatasetWorkScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Работа с датасетом: подсчет метрик UAS/LAS')
        self.setFixedSize(800, 600)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        # Экран загрузки тестового датасета и эталонного датасета
        self.label = QLabel('Выберите файлы тестового и эталонного датасетов в формате CONLLU:')
        layout.addWidget(self.label)

        self.test_dataset_path_label = QLabel('')
        layout.addWidget(self.test_dataset_path_label)

        self.test_dataset_browse_button = QPushButton('Обзор тестового датасета')
        self.test_dataset_browse_button.clicked.connect(self.browse_test_dataset)
        layout.addWidget(self.test_dataset_browse_button)

        self.reference_dataset_path_label = QLabel('')
        layout.addWidget(self.reference_dataset_path_label)

        self.reference_dataset_browse_button = QPushButton('Обзор эталонного датасета')
        self.reference_dataset_browse_button.clicked.connect(self.browse_reference_dataset)
        layout.addWidget(self.reference_dataset_browse_button)

        self.next_button = QPushButton('Далее')
        self.next_button.clicked.connect(self.calculate_metrics)
        layout.addWidget(self.next_button)

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def browse_test_dataset(self):
        test_dataset_path, _ = QFileDialog.getOpenFileName(self, 'Выберите тестовый датасет', '.', 'CONLLU files (*.conllu)')
        if test_dataset_path:
            self.test_dataset_path_label.setText(test_dataset_path)

    def browse_reference_dataset(self):
        reference_dataset_path, _ = QFileDialog.getOpenFileName(self, 'Выберите эталонный датасет', '.', 'CONLLU files (*.conllu)')
        if reference_dataset_path:
            self.reference_dataset_path_label.setText(reference_dataset_path)

    def calculate_metrics(self):
        test_dataset_path = self.test_dataset_path_label.text()
        reference_dataset_path = self.reference_dataset_path_label.text()

        if test_dataset_path and reference_dataset_path:
            try:
                # Получаем путь для сохранения файла
                save_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить результат', '.', 'Text files (*.txt)')
                if save_path:
                    # Здесь вычисляются метрики UAS и LAS для тестового и эталонного датасетов
                    uas, las = calculate_uas_las(test_dataset_path, reference_dataset_path, save_path)

                    # Открываем окно с визуализацией графика
                    self.show_visualization(uas, las)

            except Exception as e:
                print("Ошибка при вычислении метрик:", e)
        else:
            print("Не выбраны файлы тестового или эталонного датасета.")

    def show_visualization(self, uas, las):
        vis_screen = VisualizationScreen(uas, las)
        vis_screen.exec_()

    def go_back(self):
        self.prev_screen = WelcomeScreen() 
        self.prev_screen.show()
        self.close()
class ResultScreen(QDialog):
    def __init__(self, uas, las):
        super().__init__()
        self.setWindowTitle('Результаты подсчета метрик')
        self.setFixedSize(400, 300)  # Установка фиксированного размера
        layout = QVBoxLayout(self)

        self.uas_label = QLabel(f'UAS: {uas}')
        layout.addWidget(self.uas_label)

        self.las_label = QLabel(f'LAS: {las}')
        layout.addWidget(self.las_label)

        self.ok_button = QPushButton('ОК')
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
