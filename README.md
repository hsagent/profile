import os
import glob
import math
from PIL import Image, ImageDraw, ImageFont

def assemble_with_sequential_text(frames_folder, patch_path, output_gif_path, text_letters):
    # Находим все распакованные кадры
    frame_files = sorted(glob.glob(os.path.join(frames_folder, "*.png"))) + \
                  sorted(glob.glob(os.path.join(frames_folder, "*.gif")))
    
    if not frame_files:
        print(f"Ошибка: В папке '{frames_folder}' не найдено кадров!")
        return
        
    if not os.path.exists(patch_path):
        print(f"Ошибка: Файл заплатки '{patch_path}' не найден!")
        return

    print("Сборка анимации: поочередное появление букв + медленное мерцание...")
    patch = Image.open(patch_path).convert("RGBA")
    
    processed_frames = []
    total_frames = len(frame_files)
    
    # Твои идеальные скорректированные координаты
    target_x, target_y = 20, 68
    text_position = (33, 66)
    
    for idx, file_path in enumerate(frame_files):
        img = Image.open(file_path).convert("RGBA")
        
        # 1. Накладываем чистую заплатку фона на левую сторону
        img.paste(patch, (target_x, target_y), patch)
        
        # 2. Создаем слой для текста
        text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # --- ЛОГИКА ПООЧЕРЕДНОГО ПОЯВЛЕНИЯ ---
        # Считаем, сколько букв должно отображаться на текущем кадре
        # Разделяем всю гифку на равные отрезки для каждой из 4-х букв
        progress = idx / total_frames
        if progress < 0.25:
            current_text = text_letters[0]          # Только "m"
        elif progress < 0.50:
            current_text = "\n".join(text_letters[:2])  # "m\n9"
        elif progress < 0.75:
            current_text = "\n".join(text_letters[:3])  # "m\n9\ns"
        else:
            current_text = "\n".join(text_letters)     # Вся строка "m\n9\ns\n0"
            
        # --- МЕДЛЕННОЕ МЕРЦАНИЕ ---
        # Уменьшили множитель до 0.15, чтобы сделать затухание/разгорание плавным
        wave = abs(math.cos(idx * 0.15))
        color_val = int(50 + wave * 145)
        current_color = (color_val, color_val, color_val, 255)
        
        try:
            font = ImageFont.truetype("impact.ttf", size=58)
        except IOError:
            font = ImageFont.load_default()
            
        # Рисуем текущий набор букв
        draw.text(text_position, current_text, fill=current_color, font=font, spacing=15)
        
        # Склеиваем слои
        final_frame = Image.alpha_composite(img, text_layer)
        processed_frames.append(final_frame.convert("P", palette=Image.ADAPTIVE))
        
    print("Сохранение новой версии GIF...")
    processed_frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=processed_frames[1:],
        duration=40,
        loop=0,
        optimize=False
    )
    print(f"Готово! Анимация появления создана: {output_gif_path}")

if __name__ == "__main__":
    SOURCE_DIR = "C:/gif_frames/"  # Папка с кадрами из архива ezgif
    PATCH_FILE = "patch.png"       # Твой чистый кусочек фона из Paint
    OUTPUT_FILE = "Появление_m9s0.gif"
    
    # Передаем буквы списком для удобства посимвольного отсчета
    LETTERS_LIST = ["m", "9", "s", "0"]
    
    assemble_with_sequential_text(SOURCE_DIR, PATCH_FILE, OUTPUT_FILE, LETTERS_LIST)
