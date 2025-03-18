import pandas as pd
from datetime import datetime


class DataHandler:
    def __init__(self):
        self.data = None
        self.forecast = None
        self.required_columns = {'date', 'value'}  # Обязательные столбцы

    def load_data(self, file_path):
        """
        Загружает данные из файла с валидацией

        Args:
            file_path: Путь к файлу (CSV/Excel)

        Returns:
            bool: True при успешной загрузке, иначе False
        """
        try:
            # Определение типа файла
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            else:
                return False

            # Валидация данных
            if not self.validate_data(df):
                return False

            # Преобразование даты
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date', 'value'])
            df = df.set_index('date').sort_index()

            self.data = df
            return True

        except Exception as e:
            print(f"Ошибка загрузки: {str(e)}")
            return False

    def validate_data(self, df):
        """
        Проверяет корректность структуры данных

        Args:
            df: DataFrame для проверки

        Returns:
            bool: Результат валидации
        """
        # Проверка наличия обязательных столбцов
        if not self.required_columns.issubset(df.columns):
            missing = self.required_columns - set(df.columns)
            raise ValueError(f"Отсутствуют обязательные столбцы: {missing}")

        # Проверка наличия данных
        if df.empty:
            raise ValueError("Файл не содержит данных")

        # Проверка числовых значений
        if not pd.api.types.is_numeric_dtype(df['value']):
            raise TypeError("Столбец 'value' должен содержать числовые значения")

        return True

    def save_data(self, file_path):
        """
        Сохраняет прогноз в файл

        Args:
            file_path: Путь для сохранения

        Raises:
            ValueError: Если прогноз не сгенерирован
        """
        if self.forecast is None:
            raise ValueError("Нет данных для экспорта")

        # Определение формата файла
        if file_path.endswith('.csv'):
            self.forecast.to_csv(file_path, index=False)
        elif file_path.endswith('.xlsx'):
            self.forecast.to_excel(file_path, index=False, engine='openpyxl')
        else:
            raise ValueError("Неподдерживаемый формат файла")

    def prepare_forecast_data(self, forecast_series):
        """
        Подготавливает прогнозные данные для сохранения

        Args:
            forecast_series: Series с прогнозом
        """
        self.forecast = forecast_series.reset_index()
        self.forecast.columns = ['date', 'forecast_value']