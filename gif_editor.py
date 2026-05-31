import os
import glob
import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def assemble_final_synced_gif(frames_folder, patch_path, output_gif_path, text_letters):
    frame_files = sorted(glob.glob(os.path.join(frames_folder, "*.png"))) + \
                  sorted(glob.glob(os.path.join(frames_folder, "*.gif")))
    frame_files = frame_files[:41] # Строго 41 кадр
    
    patch = Image.open(patch_path).convert("RGBA")
    processed_frames = []
    
    # Твои координаты
    target_x, target_y = 20, 68
    text_position = (33, 66)
    
    for idx, file_path in enumerate(frame_files):
        img = Image.open(file_path).convert("RGBA")
        
        # 1. Возвращаем ПАТЧ
        img.paste(patch, (target_x, target_y), patch)
        
        # 2. Текст
        text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Логика 41 кадра
        progress = idx / 41
        if progress < 0.25: current_text = text_letters[0]
        elif progress < 0.50: current_text = "\n".join(text_letters[:2])
        elif progress < 0.75: current_text = "\n".join(text_letters[:3])
        else: current_text = "\n".join(text_letters)
            
        wave = abs(math.cos(idx * 0.15))
        color_val = int(60 + wave * 140)
        
        try: font = ImageFont.truetype("impact.ttf", size=58)
        except: font = ImageFont.load_default()
            
        draw.text(text_position, current_text, fill=(color_val, color_val, color_val, 255), font=font, spacing=15)
        
        final_frame = Image.alpha_composite(img, text_layer)
        
        # Конвертация
        gif_frame = final_frame.convert("P", palette=Image.ADAPTIVE, colors=256, dither=0)
        processed_frames.append(gif_frame)
        
    # Сохранение с жестким таймингом 30мс и disposal=1
    processed_frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=processed_frames[1:],
        duration=30, 
        loop=0,
        optimize=True,
        disposal=1 
    )
    print(f"Файл готов: {output_gif_path}")

# Запуск
assemble_final_synced_gif("C:/gif_frames/", "patch.png", "ФИНАЛ_СИНХРОН.gif", ["m", "9", "s", "0"])
