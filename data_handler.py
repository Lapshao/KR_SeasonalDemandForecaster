import pandas as pd
from datetime import datetime
from config import Config  # Импортируем конфигурацию


class DataHandler:
    def __init__(self):
        self.data = None
        self.forecast = None
        self.required_columns = Config.REQUIRED_COLUMNS  # Из конфига

    def load_data(self, file_path):
        """
        Загружает и валидирует данные с учетом конфигурации

        Args:
            file_path: Путь к файлу

        Returns:
            bool: True при успешной загрузке
        """
        try:
            # Определяем формат файла из конфига
            if not any(file_path.endswith(ext[1]) for ext in Config.SUPPORTED_FORMATS):
                raise ValueError("Неподдерживаемый формат файла")

            # Загрузка данных
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            else:
                return False

            # Валидация данных
            if not self.validate_data(df):
                return False

            # Обработка временного индекса
            if Config.DATE_COLUMN in df.columns:
                df[Config.DATE_COLUMN] = pd.to_datetime(df[Config.DATE_COLUMN], errors='coerce')
                df = df.dropna(subset=[Config.DATE_COLUMN, Config.VALUE_COLUMN])
                df = df.set_index(Config.DATE_COLUMN).sort_index()
                df.index.freq = Config.INFER_FREQ  # Установка частоты из конфига

            self.data = df[[Config.VALUE_COLUMN]].rename(columns={Config.VALUE_COLUMN: 'value'})
            return True

        except Exception as e:
            print(f"Ошибка загрузки: {str(e)}")
            return False

    def validate_data(self, df):
        """
        Проверяет данные согласно конфигурации

        Args:
            df: DataFrame для проверки

        Returns:
            bool: Результат валидации
        """
        # Проверка обязательных столбцов
        missing_cols = self.required_columns - set(df.columns)
        if missing_cols:
            raise ValueError(f"Отсутствуют обязательные столбцы: {', '.join(missing_cols)}")

        # Проверка пустых данных
        if df.empty:
            raise ValueError("Файл не содержит данных")

        # Проверка числовых значений
        if not pd.api.types.is_numeric_dtype(df[Config.VALUE_COLUMN]):
            raise TypeError(f"Столбец '{Config.VALUE_COLUMN}' должен содержать числовые значения")

        return True

    def save_data(self, file_path):
        """
        Сохраняет прогноз с учетом формата из конфига

        Args:
            file_path: Путь для сохранения

        Raises:
            ValueError: Если прогноз не сгенерирован
        """
        if self.forecast is None:
            raise ValueError("Нет данных для экспорта")

        # Определяем формат по расширению из конфига
        try:
            if file_path.endswith('.csv'):
                self.forecast.to_csv(file_path, index=False)
            elif file_path.endswith('.xlsx'):
                self.forecast.to_excel(file_path, index=False, engine='openpyxl')
            elif file_path.endswith('.png'):
                self.forecast.plot().get_figure().savefig(file_path)
            else:
                raise ValueError("Неподдерживаемый формат файла")
        except Exception as e:
            raise IOError(f"Ошибка сохранения: {str(e)}")

    def prepare_forecast_data(self, forecast_series):
        """
        Подготавливает прогнозные данные для сохранения

        Args:
            forecast_series: Series с прогнозом
        """
        self.forecast = forecast_series.reset_index()
        self.forecast.columns = [Config.DATE_COLUMN, Config.FORECAST_COLUMN]