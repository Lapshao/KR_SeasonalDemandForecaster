import tkinter as tk
from gui import App

if __name__ == "__main__":
    # Создаем корневое окно Tkinter
    root = tk.Tk()
    root.title("Прогнозирование спроса v0.1")
    root.geometry("1200x800")  # Начальный размер окна

    # Инициализируем главное приложение
    app = App(root)

    # Запуск основного цикла событий
    root.mainloop()