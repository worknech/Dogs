from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter.ttk import Progressbar

import requests
from PIL import Image, ImageTk
from io import BytesIO


def show_image():
    """Загрузка изображения в метку"""
    image_url: str | None = get_dog_image()
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img_size = (int(with_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail((img_size))
            img = ImageTk.PhotoImage(img)
            # new_window = Toplevel(root)
            # new_window.title('Случайное изображение')
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f'Картинка №{notebook.index('end') + 1}')
            lb = ttk.Label(tab, image=img)
            lb.pack(padx=10, pady=10)
            tab.image = img  # сохраняем изображение в объекте вкладки
        except Exception as e:
            progress.stop()  # Остановка прогресс-бара при возникновении ошибки
            mb.showerror("Ошибка", f'Возникла ошибка при запросе к API {e}')
    progress.stop()


def get_dog_image():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except Exception as e:
        mb.showerror("Ошибка", f'Возникла ошибка при загрузке изображения {e}')
        return None


def prog():
    progress['value'] = 0
    progress.start(30)
    progress.after(3000, show_image)


def clear_tabs():
    """Удаляет все вкладки из Notebook"""
    for tab in notebook.tabs():
        notebook.forget(tab)


root = Tk()
root.title('Картинки с собачками')
root.geometry('360x420')

label = ttk.Label()
label.pack(pady=10)

# Фрейм для размещения кнопок
button_frame = Frame(label)
button_frame.pack(side=TOP, pady=5)

# Кнопка загрузки
button = ttk.Button(button_frame, text='Загрузить изображение', command=prog)
button.pack(side=LEFT, padx=5)

# Кнопка очистки
clear_button = ttk.Button(button_frame, text='Очистить вкладки', command=clear_tabs)
clear_button.pack(side=TOP, pady=5)

progress = Progressbar(root, orient=HORIZONTAL, mode='determinate', length=300)
progress.pack(pady=10)

with_label = ttk.Label(text='Ширина:')
with_label.pack(side='left', padx=(10, 0))
with_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
with_spinbox.set(300)
with_spinbox.pack(side='left', padx=(0, 10))

height_label = ttk.Label(text='Высота:')
height_label.pack(side='left', padx=(10, 0))
height_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
height_spinbox.set(300)
height_spinbox.pack(side='left', padx=(0, 10))

top_level_window = Toplevel(root)
top_level_window.title('Изображения собачек')
notebook = ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()
