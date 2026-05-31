from PIL import Image, ImageSequence

def prepare_for_steam(input_path, output_path):
    gif = Image.open(input_path)
    frames = [f.copy().convert("P", palette=Image.ADAPTIVE, colors=256, dither=0) for f in ImageSequence.Iterator(gif)]
    
    # 30мс - это стандарт, который Steam чаще всего оставляет как есть
    # Убедись, что оба файла (большой и маленький) прогнаны через этот скрипт
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=30, # СТАВИМ ВЕЗДЕ ОДИНАКОВО
        loop=0,
        optimize=True,
        disposal=1   # ВАЖНО: 1 - наложение слоев
    )
    print(f"Готово для Steam: {output_path}")

# Запусти для обоих файлов
prepare_for_steam("Большая_часть.gif", "Steam_Large.gif")
prepare_for_steam("Маленькая_часть.gif", "Steam_Small.gif")