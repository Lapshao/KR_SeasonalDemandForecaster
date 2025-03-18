import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tools.sm_exceptions import MissingDataError


class DemandAnalyzer:
    def __init__(self):
        self.decomposition = None
        self.seasonal_pattern = None

    def calculate_moving_average(self, data, window=3):
        """
        Рассчитывает скользящее среднее

        Args:
            data: Временной ряд (pd.Series)
            window: Размер окна

        Returns:
            pd.Series со скользящим средним
        """
        if len(data) < window:
            raise ValueError("Размер окна превышает длину данных")

        return data.rolling(window=window, center=True).mean()

    def decompose_seasonality(self, data, period=12):
        """
        Выполняет декомпозицию временного ряда

        Args:
            data: Временной ряд (pd.Series)
            period: Сезонный период (по умолчанию 12 месяцев)

        Returns:
            statsmodels DecomposeResult
        """
        if not isinstance(data.index, pd.DatetimeIndex):
            raise TypeError("Данные должны иметь временной индекс")

        try:
            self.decomposition = seasonal_decompose(data, model='additive', period=period)
            self.seasonal_pattern = self.decomposition.seasonal
            return self.decomposition

        except MissingDataError as e:
            raise ValueError("Недостаточно данных для декомпозиции") from e

    def generate_forecast(self, data, periods=12):
        """
        Генерирует прогноз на основе сезонной компоненты

        Args:
            data: Исторические данные (pd.Series)
            periods: Количество периодов для прогноза

        Returns:
            pd.Series с прогнозными значениями

        Raises:
            RuntimeError: Если декомпозиция не выполнена
        """
        if self.seasonal_pattern is None:
            raise RuntimeError("Необходимо сначала выполнить декомпозицию")

        # Создаем индекс для прогноза
        last_date = data.index[-1]
        freq = pd.infer_freq(data.index)
        forecast_index = pd.date_range(start=last_date, periods=periods + 1, freq=freq)[1:]

        # Берем сезонные компоненты последнего года
        recent_seasonal = self.seasonal_pattern[-periods:]

        # Повторяем паттерн для прогноза
        forecast_values = []
        for i in range(periods):
            forecast_values.append(recent_seasonal.iloc[i % len(recent_seasonal)])

        return pd.Series(forecast_values, index=forecast_index, name='forecast')