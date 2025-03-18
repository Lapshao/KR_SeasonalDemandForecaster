import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from config import Config  # Импортируем конфигурацию

plt.style.use(Config.PLOT_STYLE)  # Применяем стиль из конфига


class Plotter:
    def __init__(self):
        self.dpi = Config.PLOT_DPI  # Качество изображения из конфига

    def plot_original(self, data):
        """Строит график исходных данных"""
        fig = Figure(figsize=(8, 4), dpi=self.dpi)
        ax = fig.add_subplot(111)

        data.plot(
            ax=ax,
            marker=Config.PLOT_MARKER,  # Новая настройка из конфига
            linestyle=Config.PLOT_LINESTYLE,
            color=Config.COLOR_PRIMARY
        )

        ax.set_title("Исходные данные", fontsize=Config.FONT_SIZE)
        ax.set_ylabel("Значение", fontsize=Config.FONT_SIZE)
        ax.grid(True, linestyle=Config.GRID_STYLE, alpha=Config.GRID_ALPHA)
        ax.tick_params(axis='both', labelsize=Config.FONT_SIZE)

        return fig

    def plot_averages(self, data, window):
        """Строит график со скользящим средним"""
        fig = Figure(figsize=(8, 4), dpi=self.dpi)
        ax = fig.add_subplot(111)

        # Исходные данные
        data.plot(
            ax=ax,
            alpha=Config.ALPHA_SECONDARY,
            label='Исходные данные',
            color=Config.COLOR_SECONDARY
        )

        # Скользящее среднее
        data.rolling(window).mean().plot(
            ax=ax,
            color=Config.COLOR_PRIMARY,
            linewidth=Config.LINE_WIDTH,
            label=f'Скользящее среднее ({window} периодов)'
        )

        ax.set_title("Скользящее среднее", fontsize=Config.FONT_SIZE)
        ax.legend(fontsize=Config.FONT_SIZE)
        ax.grid(True, linestyle=Config.GRID_STYLE, alpha=Config.GRID_ALPHA)
        ax.tick_params(axis='both', labelsize=Config.FONT_SIZE)

        return fig

    def plot_forecast(self, historical, forecast):
        """Строит комбинированный график с прогнозом"""
        fig = Figure(figsize=(8, 4), dpi=self.dpi)
        ax = fig.add_subplot(111)

        # Исторические данные
        historical.plot(
            ax=ax,
            marker=Config.PLOT_MARKER,
            markersize=Config.MARKER_SIZE,
            linestyle=Config.PLOT_LINESTYLE,
            linewidth=Config.LINE_WIDTH,
            color=Config.COLOR_PRIMARY,
            label='Исторические данные'
        )

        # Прогноз
        forecast.plot(
            ax=ax,
            marker=Config.FORECAST_MARKER,
            markersize=Config.MARKER_SIZE,
            linestyle=Config.FORECAST_LINESTYLE,
            linewidth=Config.LINE_WIDTH,
            color=Config.COLOR_FORECAST,
            label='Прогноз'
        )

        # Доверительный интервал (пример)
        if Config.SHOW_CONFIDENCE:
            ax.fill_between(
                forecast.index,
                forecast * Config.CONFIDENCE_LOWER,
                forecast * Config.CONFIDENCE_UPPER,
                color=Config.COLOR_CONFIDENCE,
                alpha=Config.CONFIDENCE_ALPHA,
                label='Доверительный интервал'
            )

        # Вертикальная разделительная линия
        ax.axvline(
            historical.index[-1],
            color=Config.COLOR_SEPARATOR,
            linestyle=Config.SEPARATOR_STYLE,
            linewidth=Config.LINE_WIDTH,
            label='_nolegend_'
        )

        ax.set_title("Прогноз спроса", fontsize=Config.FONT_SIZE)
        ax.legend(fontsize=Config.FONT_SIZE)
        ax.grid(True, linestyle=Config.GRID_STYLE, alpha=Config.GRID_ALPHA)
        ax.tick_params(axis='both', labelsize=Config.FONT_SIZE)

        return fig