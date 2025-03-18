import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tools.sm_exceptions import MissingDataError
from config import Config  # Импортируем конфигурацию


class DemandAnalyzer:
    def __init__(self):
        self.decomposition = None
        self.seasonal_pattern = None

    def calculate_moving_average(self, data, window=None):
        """
        Рассчитывает скользящее среднее с настраиваемым окном

        Args:
            data: pd.Series временной ряд
            window: Размер окна (берется из конфига если не указано)

        Returns:
            pd.Series со скользящим средним
        """
        window = window or Config.MOVING_AVERAGE_WINDOW
        if len(data) < window:
            raise ValueError(f"Размер окна ({window}) превышает длину данных ({len(data)})")

        return data.rolling(window=window, center=True).mean()

    def decompose_seasonality(self, data, period=None):
        """
        Выполняет декомпозицию временного ряда

        Args:
            data: pd.Series временной ряд
            period: Сезонный период (берется из конфига если не указан)

        Returns:
            statsmodels DecomposeResult
        """
        period = period or Config.SEASONAL_PERIOD
        if not isinstance(data.index, pd.DatetimeIndex):
            raise TypeError("Данные должны иметь временной индекс")

        try:
            self.decomposition = seasonal_decompose(data, model='additive', period=period)
            self.seasonal_pattern = self.decomposition.seasonal
            return self.decomposition

        except MissingDataError as e:
            raise ValueError("Недостаточно данных для декомпозиции") from e

    def generate_forecast(self, data, periods=None):
        """
        Генерирует прогноз на основе сезонной компоненты

        Args:
            data: pd.Series исторические данные
            periods: Количество периодов прогноза (из конфига если не указано)

        Returns:
            pd.Series с прогнозными значениями

        Raises:
            RuntimeError: Если декомпозиция не выполнена
        """
        periods = periods or Config.FORECAST_PERIODS
        if self.seasonal_pattern is None:
            raise RuntimeError("Необходимо сначала выполнить декомпозицию")

        # Создаем индекс для прогноза
        last_date = data.index[-1]
        freq = pd.infer_freq(data.index)
        forecast_index = pd.date_range(start=last_date, periods=periods + 1, freq=freq)[1:]

        # Берем сезонные компоненты последнего периода
        recent_seasonal = self.seasonal_pattern[-periods:]

        # Генерируем прогнозные значения
        forecast_values = []
        for i in range(periods):
            forecast_values.append(recent_seasonal.iloc[i % len(recent_seasonal)])

        return pd.Series(forecast_values, index=forecast_index, name='forecast')

    def sarima_forecast(self, data, periods=None):
        """
        Прогноз с использованием SARIMA (опционально)

        Args:
            data: pd.Series временной ряд
            periods: Количество периодов прогноза

        Returns:
            pd.Series прогнозных значений
        """
        periods = periods or Config.FORECAST_PERIODS
        try:
            from statsmodels.tsa.statespace.sarimax import SARIMAX
            model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, Config.SEASONAL_PERIOD))
            results = model.fit(disp=False)
            return results.get_forecast(steps=periods).predicted_mean
        except Exception as e:
            raise RuntimeError(f"SARIMA ошибка: {str(e)}")

    def calculate_mape(self, actual, forecast):
        """
        Рассчитывает MAPE (Mean Absolute Percentage Error)

        Args:
            actual: Фактические значения
            forecast: Прогнозные значения

        Returns:
            float: MAPE в процентах
        """
        return np.mean(np.abs((actual - forecast) / actual)) * 100