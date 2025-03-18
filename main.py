import tkinter as tk
from gui import App
from config import Config

if __name__ == "__main__":
    # Создаем корневое окно Tkinter
    root = tk.Tk()
    root.title("Прогнозирование спроса v0.1")
    root.geometry(Config.WINDOW_SIZE)  # Используем из конфига

    # Инициализируем главное приложение
    app = App(root)

    # Запуск основного цикла событий
    root.mainloop()