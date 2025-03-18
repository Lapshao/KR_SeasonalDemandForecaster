class Config:
    # Основные настройки приложения
    WINDOW_SIZE = "1200x800"  # Размер окна приложения
    APP_TITLE = "Прогнозирование спроса"  # Заголовок окна
    MIN_SIZE = (800, 600)  # Минимальный размер окна

    # Настройки данных
    REQUIRED_COLUMNS = {'date', 'value'}  # Обязательные столбцы
    DATE_COLUMN = 'date'  # Название столбца с датой
    VALUE_COLUMN = 'value'  # Название столбца со значениями
    FORECAST_COLUMN = 'forecast_value'  # Название столбца прогноза
    INFER_FREQ = 'MS'  # Ежемесячная частота ('MS' - начало месяца)

    # Поддерживаемые форматы
    SUPPORTED_FORMATS = [
        ('CSV', '.csv'),
        ('Excel', '.xlsx')
    ]
    EXPORT_FILETYPES = [
        ('CSV', '.csv'),
        ('Excel', '.xlsx'),
        ('PNG', '.png')
    ]

    # Параметры анализа
    MOVING_AVERAGE_WINDOW = 3  # Размер окна скользящего среднего
    SEASONAL_PERIOD = 12  # Сезонный период (месяцев)
    FORECAST_PERIODS = 12  # Количество периодов прогноза

    # Визуализация
    PLOT_STYLE = 'ggplot'  # Стиль графиков matplotlib
    PLOT_DPI = 100  # Качество сохраняемых изображений
    FONT_SIZE = 10  # Размер шрифта
    GRID_STYLE = '--'  # Стиль сетки
    GRID_ALPHA = 0.7  # Прозрачность сетки
    LINE_WIDTH = 2  # Толщина линий
    MARKER_SIZE = 4  # Размер маркеров
    PLOT_MARKER = 'o'  # Маркер для исходных данных
    PLOT_LINESTYLE = '-'  # Стиль линии
    COLOR_PRIMARY = '#2c7bb6'  # Основной цвет
    COLOR_SECONDARY = '#d7191c'  # Второстепенный цвет
    COLOR_FORECAST = '#fdae61'  # Цвет прогноза
    COLOR_CONFIDENCE = '#abdda4'  # Цвет доверительного интервала
    COLOR_SEPARATOR = '#5e5e5e'  # Цвет разделителя
    FORECAST_MARKER = 's'  # Маркер прогноза
    FORECAST_LINESTYLE = '--'  # Стиль линии прогноза
    SHOW_CONFIDENCE = True  # Показывать доверительный интервал
    CONFIDENCE_LOWER = 0.9  # Нижняя граница интервала
    CONFIDENCE_UPPER = 1.1  # Верхняя граница интервала
    CONFIDENCE_ALPHA = 0.3  # Прозрачность интервала
    ALPHA_SECONDARY = 0.3 # Прозрачность второстепенных элементов
    SEPARATOR_STYLE = '--' # Разделитель


    # Системные настройки
    BASE_DIR = '.'  # Базовая директория проекта
    DATA_DIR = 'data'  # Папка с данными
    EXPORT_DIR = 'exports'  # Папка для экспорта
    LOG_FILE = 'app.log'  # Файл логов