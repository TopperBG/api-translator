import os
import glob
import requests
import sys

# Конфигурация за LibreTranslate
API_URL = "http://localhost:5000/translate"
SOURCE_LANG = "en"  # език на оригиналния текст
TARGET_LANG = "bg"  # език за превод
OUTPUT_FOLDER = "bg"  # Папка за преведените файлове

# Създаване на папката, ако не съществува
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def translate_text(text):
    """
    Превежда подадения текст чрез LibreTranslate API.
    """
    payload = {
        "q": text,
        "source": SOURCE_LANG,
        "target": TARGET_LANG,
        "format": "text"
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("translatedText", text)
    except Exception as e:
        print(f"\nГрешка при превода на текст: {e}")
        return text

def is_translatable_line(line):
    """
    Проверява дали дадения ред съдържа текст за превод.
    Пропуска редове с номера, времеви кодове или празни редове.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.isdigit():
        return False
    if "-->" in stripped:
        return False
    return True

def process_file(filename):
    print(f"\nОбработва се файл: {filename}")
    
    # Четене на всички редове от файла
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    new_lines = []

    # Обхождаме ред по ред
    for idx, line in enumerate(lines):
        if is_translatable_line(line):
            # Превеждаме само редовете, които съдържат текст
            translated = translate_text(line.strip())
            new_lines.append(translated + "\n")
        else:
            new_lines.append(line)
        
        # Изчисляване и показване на процента изпълнение
        progress = (idx + 1) / total_lines * 100
        sys.stdout.write(f"\r{filename} - {progress:.2f}%")
        sys.stdout.flush()

    # Генериране на име за изходния файл
    output_filename = os.path.splitext(filename)[0]
    output_filename = output_filename.replace(".en", "")  # Премахване на ".en"
    output_filename = os.path.join(OUTPUT_FOLDER, output_filename + ".bg.srt")
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"\nГотово: {filename} е преведен и запазен като {output_filename}\n")

def main():
    # Намиране на всички .srt файлове в текущата директория
    srt_files = glob.glob("*.srt")
    if not srt_files:
        print("Няма намерени .srt файлове в текущата директория.")
        return

    for srt_file in srt_files:
        process_file(srt_file)

if __name__ == "__main__":
    main()
