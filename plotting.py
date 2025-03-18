import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

plt.style.use('ggplot')  # Устанавливаем стиль графиков


class Plotter:
    def __init__(self):
        self.figsize = (12, 4)  # Размер графиков для окна приложения

    def plot_original(self, data):
        """
        Строит график исходных данных

        Args:
            data: Временной ряд (pd.Series)

        Returns:
            matplotlib.figure.Figure
        """
        fig = Figure(figsize=self.figsize)
        ax = fig.add_subplot(111)

        data.plot(ax=ax, marker='o', markersize=4, linestyle='-', linewidth=1)
        ax.set_title("Исходные данные")
        ax.set_ylabel("Значение")
        ax.grid(True, linestyle='--', alpha=0.7)

        return fig

    def plot_averages(self, data, window=3):
        """
        Строит график со скользящим средним

        Args:
            data: Временной ряд (pd.Series)
            window: Размер окна

        Returns:
            matplotlib.figure.Figure
        """
        fig = Figure(figsize=self.figsize)
        ax = fig.add_subplot(111)

        # Исходные данные
        data.plot(ax=ax, alpha=0.3, label='Исходные данные')
        # Скользящее среднее
        data.rolling(window=window).mean().plot(
            ax=ax,
            color='red',
            linewidth=2,
            label=f'Среднее ({window} периода)'
        )

        ax.set_title("Скользящее среднее")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)

        return fig

    def plot_forecast(self, historical, forecast):
        """
        Строит комбинированный график с прогнозом

        Args:
            historical: Исторические данные (pd.Series)
            forecast: Прогнозные данные (pd.Series)

        Returns:
            matplotlib.figure.Figure
        """
        fig = Figure(figsize=self.figsize)
        ax = fig.add_subplot(111)

        # Исторические данные
        historical.plot(
            ax=ax,
            marker='o',
            markersize=4,
            linestyle='-',
            linewidth=1,
            label='История'
        )

        # Прогноз
        forecast.plot(
            ax=ax,
            marker='s',
            markersize=4,
            linestyle='--',
            linewidth=2,
            color='red',
            label='Прогноз'
        )

        # Заливка доверительного интервала (пример)
        ax.fill_between(
            forecast.index,
            forecast * 0.9,
            forecast * 1.1,
            color='pink',
            alpha=0.3,
            label='Доверительный интервал'
        )

        ax.set_title("Прогноз спроса")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)

        # Вертикальная линия раздела данных
        ax.axvline(
            historical.index[-1],
            color='gray',
            linestyle='--',
            linewidth=1,
            label='_nolegend_'
        )

        return fig