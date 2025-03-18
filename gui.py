import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from config import Config

from data_handler import DataHandler
from analysis import DemandAnalyzer
from plotting import Plotter


class App:
    def __init__(self, root):
        self.root = root
        self.root.minsize(*map(int, Config.WINDOW_SIZE.split('x')))
        self.root.title("Прогнозирование спроса")

        self.data_handler = DataHandler()
        self.analyzer = DemandAnalyzer()
        self.plotter = Plotter()

        self.canvas = None
        self.scrollbar = None
        self.current_figures = []
        self.toolbar = None
        self.btn_import = None
        self.btn_analyze = None
        self.btn_export = None
        self.status_var = None
        self.status_bar = None

        self.create_widgets()
        self.create_status_bar()

    def create_widgets(self):
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

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

        self.plot_container = tk.Frame(self.root)
        self.plot_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var,
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("Готово")

    def load_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=Config.SUPPORTED_FORMATS
        )

        if not file_path:
            return

        try:
            if self.data_handler.load_data(file_path):
                self.update_status(f"Загружено: {file_path}")
                self.btn_analyze.config(state=tk.NORMAL)

                if not isinstance(self.data_handler.data.index, pd.DatetimeIndex):
                    self.data_handler.data.index = pd.to_datetime(self.data_handler.data.index)
            else:
                messagebox.showerror("Ошибка", "Неверный формат данных")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def run_analysis(self):
        try:
            self.update_status("Выполняется анализ...")
            self.btn_analyze.config(state=tk.DISABLED)

            if self.canvas:
                self.canvas.get_tk_widget().destroy()
                self.scrollbar.destroy()

            original_fig = self.plotter.plot_original(self.data_handler.data)
            moving_avg_fig = self.plotter.plot_averages(
                self.data_handler.data,
                window=Config.MOVING_AVERAGE_WINDOW
            )

            self.analyzer.decompose_seasonality(
                self.data_handler.data,
                period=Config.SEASONAL_PERIOD
            )
            forecast = self.analyzer.generate_forecast(
                self.data_handler.data,
                periods=Config.FORECAST_PERIODS
            )
            forecast_fig = self.plotter.plot_forecast(
                self.data_handler.data,
                forecast
            )

            self.display_plots([original_fig, moving_avg_fig, forecast_fig])

            self.data_handler.prepare_forecast_data(forecast)
            self.btn_export.config(state=tk.NORMAL)

            self.update_status("Анализ завершен")

        except Exception as e:
            messagebox.showerror("Ошибка анализа", str(e))
            self.update_status("Ошибка анализа")
        finally:
            self.btn_analyze.config(state=tk.NORMAL)

    def display_plots(self, figures):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.scrollbar.destroy()

        canvas = tk.Canvas(self.plot_container)
        scrollbar = tk.Scrollbar(
            self.plot_container,
            orient=tk.VERTICAL,
            command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all"),
                width=self.plot_container.winfo_width() - 20
            )
        )

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        min_width = 0
        for fig in figures:
            fig.set_size_inches(6, 3)
            fig.tight_layout()
            fig_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
            fig_canvas.draw()
            widget = fig_canvas.get_tk_widget()
            widget.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5, expand=True)
            min_width = max(min_width, widget.winfo_reqwidth())

        canvas.config(width=min_width + 40)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = canvas
        self.scrollbar = scrollbar
        self.current_figures = figures

    def export_results(self):
        if self.data_handler.forecast is None:
            return

        file_path = filedialog.asksaveasfilename(
            filetypes=Config.EXPORT_FILETYPES,
            initialdir=Config.EXPORT_DIR
        )

        if file_path:
            try:
                self.data_handler.save_data(file_path)
                self.update_status(f"Результаты сохранены в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def update_status(self, message):
        self.status_var.set(message)
        self.status_bar.update()