import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from data_handler import DataHandler
from analysis import DemandAnalyzer
from plotting import Plotter


class App:
    def __init__(self, root):
        self.root = root
        self.root.minsize(800, 600)  # Минимальный размер окна

        # Инициализация компонентов
        self.data_handler = DataHandler()
        self.analyzer = DemandAnalyzer()
        self.plotter = Plotter()

        # Переменные GUI
        self.canvas = None
        self.scrollbar = None
        self.current_figures = []

        # Создание интерфейса
        self.create_widgets()
        self.create_status_bar()

    def create_widgets(self):
        """Создает все элементы интерфейса"""
        # Панель инструментов
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки управления
        btn_style = {'padx': 10, 'pady': 5}
        self.btn_import = tk.Button(self.toolbar, text="Импорт данных",
                                    command=self.load_data, **btn_style)
        self.btn_analyze = tk.Button(self.toolbar, text="Провести анализ",
                                     command=self.run_analysis, state=tk.DISABLED, **btn_style)
        self.btn_export = tk.Button(self.toolbar, text="Экспорт",
                                    command=self.export_results, state=tk.DISABLED, **btn_style)

        self.btn_import.pack(side=tk.LEFT)
        self.btn_analyze.pack(side=tk.LEFT)
        self.btn_export.pack(side=tk.LEFT)

        # Контейнер для графиков с прокруткой
        self.plot_container = tk.Frame(self.root)
        self.plot_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_status_bar(self):
        """Создает статус-бар"""
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var,
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("Готово")

    def load_data(self):
        """Загружает данные из файла"""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])

        if not file_path:
            return

        try:
            if self.data_handler.load_data(file_path):
                self.update_status(f"Загружено: {file_path}")
                self.btn_analyze.config(state=tk.NORMAL)

                # Проверка временного индекса
                if not isinstance(self.data_handler.data.index, pd.DatetimeIndex):
                    self.data_handler.data.index = pd.to_datetime(self.data_handler.data.index)
            else:
                messagebox.showerror("Ошибка", "Неверный формат данных")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def run_analysis(self):
        """Выполняет анализ и обновляет графики"""
        try:
            self.update_status("Выполняется анализ...")
            self.btn_analyze.config(state=tk.DISABLED)

            # Очистка предыдущих графиков
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
                self.scrollbar.destroy()

            # 1. Исходные данные
            original_fig = self.plotter.plot_original(self.data_handler.data)

            # 2. Скользящее среднее
            moving_avg_fig = self.plotter.plot_averages(self.data_handler.data, window=3)

            # 3. Прогноз
            self.analyzer.decompose_seasonality(self.data_handler.data, period=12)
            forecast = self.analyzer.generate_forecast(self.data_handler.data)
            forecast_fig = self.plotter.plot_forecast(self.data_handler.data, forecast)

            # Отображение графиков с прокруткой
            self.display_plots([original_fig, moving_avg_fig, forecast_fig])

            # Сохранение прогноза
            self.data_handler.prepare_forecast_data(forecast)
            self.btn_export.config(state=tk.NORMAL)

            self.update_status("Анализ завершен")

        except Exception as e:
            messagebox.showerror("Ошибка анализа", str(e))
            self.update_status("Ошибка анализа")
        finally:
            self.btn_analyze.config(state=tk.NORMAL)

    def display_plots(self, figures):
        """Отображает графики с горизонтальной прокруткой"""
        # Создаем Canvas и Scrollbar
        canvas = tk.Canvas(self.plot_container)
        scrollbar = tk.Scrollbar(self.plot_container, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollable_frame = tk.Frame(canvas)

        # Настройка прокрутки
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all"),
                width=self.plot_container.winfo_width()
            )
        )

        # Обработка прокрутки колесом мыши
        def on_mousewheel(event):
            if event.state == 1:  # Horizontal scroll
                canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Создаем окно внутри Canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        # Добавляем графики
        min_height = 0
        for fig in figures:
            fig.set_size_inches(8, 4)  # Фиксированный размер
            fig.tight_layout()
            fig_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
            fig_canvas.draw()
            fig_canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
            min_height = max(min_height, fig_canvas.get_tk_widget().winfo_reqheight())

        # Устанавливаем минимальную высоту
        canvas.config(height=min_height + 40)

        # Размещаем элементы
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Сохраняем ссылки
        self.canvas = canvas
        self.scrollbar = scrollbar
        self.current_figures = figures

    def export_results(self):
        """Экспортирует результаты"""
        if self.data_handler.forecast is None:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])

        if file_path:
            try:
                self.data_handler.save_data(file_path)
                self.update_status(f"Результаты сохранены в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def update_status(self, message):
        """Обновляет статус-бар"""
        self.status_var.set(message)
        self.status_bar.update()