import glob
import pysrt
import os
import sys
import requests

# Конфигурация за LibreTranslate
API_URL = "http://localhost:5000/translate"
SOURCE_LANG = "en"  # език на оригиналния текст
TARGET_LANG = "bg"  # език за превод
OUTPUT_FOLDER = f"/app/data/{sys.argv[1]}" if len(sys.argv) > 1 else "/app/data"
APP_VERSION = "1.0.0"

print(f"Running {os.path.basename(__file__)} version {APP_VERSION}")


def translate_text(text,target_lang=TARGET_LANG):
    """
    Превежда подадения текст чрез LibreTranslate API.

    :param text: текстът, който ще бъде преведен.
    :param target_lang: езикът на превода. По подразбиране е "bg".
    :return: преведеният текст, или подадения текст, ако се появи грешка.
    """
    payload = {
        "q": text,
        "source": SOURCE_LANG,
        "target": target_lang,
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

def translate_srt(input_srt, target_lang=TARGET_LANG):
    """
    Превежда SRT файл, използвайки LibreTranslate API.

    :param input_srt: Пътят до SRT файла, който ще бъде преведен.
    :param target_lang: Езикът на превода. По подразбиране е "bg".
    :return: Нe връща стойност. Изходният преведен файл се запазва като {input_srt}.{target_lang}.srt.
    """
    subs = pysrt.open(input_srt)
    translated_subs = pysrt.SubRipFile()

    total_subs = len(subs)
    for idx, sub in enumerate(subs):
        translated_text = translate_text(sub.text, target_lang)
        new_sub = pysrt.SubRipItem(index=sub.index, start=sub.start, end=sub.end, text=translated_text)
        translated_subs.append(new_sub)

        progress = (idx + 1) / total_subs * 100
        sys.stdout.write(f"\r{input_srt} - {progress:.2f}%")
        sys.stdout.flush()

    output_srt = f"{os.path.splitext(input_srt)[0]}.{target_lang}.srt"
    translated_subs.save(output_srt, encoding='utf-8')
    print(f"\n✅ Translated: {input_srt} → {output_srt}")

def process_directory(directory="/app/data", target_lang=TARGET_LANG):
    print(f"Проверявам директория с файлове: {directory}")

    if not os.path.exists(directory):
        print(f"⚠️ Директорията {directory} не е намерена!")
        return

    srt_files = [f for f in os.listdir(directory) if f.endswith(".srt")]
    print(f"📁 Намерих {len(srt_files)} .srt файлове в {directory}")

    if not srt_files:
        print("⚠️ Няма намерени .srt файлове!")
        return

    for srt_file in srt_files:
        translate_srt(os.path.join(directory, srt_file), target_lang)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print("Използване: python translate_srt.py <папка_за_изход> <език_на_превода>")
        print("  <папка_за_изход> - папката, където ще бъдат запазени преведените файлове.")
        print("  <език_на_превода> - езикът, на който ще бъде направен преводът. По подразбиране е 'bg'.")
        sys.exit(0)
    target_lang = sys.argv[2] if len(sys.argv) > 2 else TARGET_LANG
    process_directory("/app/data")
