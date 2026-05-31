# profile

Bash
pip install Pillow

import os
from PIL import Image, ImageDraw, ImageFont, ImageSequence

def replace_text_in_gif(input_path, output_path, new_text_str):
    if not os.path.exists(input_path):
        print(f"Ошибка: Файл '{input_path}' не найден в текущей папке!")
        print("Пожалуйста, убедитесь, что имя файла совпадает.")
        return

    print(f"Открываем файл {input_path}...")
    gif_img = Image.open(input_path)
    
    # Сохраняем параметры анимации (задержку между кадрами и метод удаления кадров)
    durations = []
    disposals = []
    frames = []
    
    # Координаты прямоугольника, который перекроет старые буквы EXS
    # Подобрано точно под левый верхний угол (x1, y1, x2, y2)
    box_coords = [30, 70, 160, 310]
    
    # Позиция для начала ввода нового текста
    text_position = (50, 75)
    
    print("Начинаем покадровую обработку анимации...")
    
    for i, frame in enumerate(ImageSequence.Iterator(gif_img)):
        # Получаем метаданные текущего кадра
        durations.append(frame.info.get('duration', 40))
        disposals.append(frame.info.get('disposal', 2))
        
        # Конвертируем кадр в RGBA, чтобы рисовать без потери качества цвета
        rgba_frame = frame.convert("RGBA")
        draw = ImageDraw.Draw(rgba_frame)
        
        # 1. Замазываем буквы EXS темным цветом заднего фона (почти черный)
        draw.rectangle(box_coords, fill=(12, 12, 12, 255))
        
        # 2. Пытаемся загрузить красивый шрифт, если его нет — берем стандартный
        try:
            # Если у вас есть свой файл шрифта (.ttf), укажите его имя вместо "arial.ttf"
            font = ImageFont.truetype("arial.ttf", size=54)
        except IOError:
            font = ImageFont.load_default()
            
        # 3. Рисуем новый текст m9s0 со смещением (spacing) между строками
        draw.text(text_position, new_text_str, fill=(220, 220, 220, 240), font=font, spacing=18)
        
        # Конвертируем кадр обратно в формат палитры (P) с адаптивными цветами для GIF
        processed_frame = rgba_frame.convert("P", palette=Image.ADAPTIVE)
        frames.append(processed_frame)
        
    print(f"Всего обработано кадров: {len(frames)}")
    print("Собираем кадры обратно в анимированный GIF...")
    
    # Сохраняем итоговый файл со всеми кадрами и оригинальной скоростью
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=gif_img.info.get('loop', 0),
        disposal=disposals,
        optimize=True
    )
    
    print(f"Успешно! Новый файл сохранен как: {output_path}")

if __name__ == "__main__":
    # Настройки имен файлов
    SOURCE_GIF = "Большая часть.gif"
    RESULT_GIF = "Большая часть_m9s0.gif"
    
    # Текст в столбик, разделенный переносом строки \n
    TEXT_TO_WRITE = "m\n9\ns\n0"
    
    replace_text_in_gif(SOURCE_GIF, RESULT_GIF, TEXT_TO_WRITE)
