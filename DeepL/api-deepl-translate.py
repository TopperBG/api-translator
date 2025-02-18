import os
import argparse
import pysubparser.parser as psp
import deepl

def translate_text(text, target_lang, api_key):
    """
    Tanslate text with DeepL API, handling missing API key and limit reached.
    """
    if not api_key:
        raise ValueError("API ключът не е предоставен.")

    translator = deepl.Translator(api_key)
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"Грешка при превод: {e}")
        return text

def process_srt_file(input_file, target_lang, api_key):
    """
    Parse SRT file, clean HI subtitles, translate and save.
    """
    try:
        subs = list(psp.parse(input_file))
    except Exception as e:
        print(f"Грешка при четене на файла {input_file}: {e}")
        return

    translated_subs = []
    for sub in subs:
        try:
            translated_text = translate_text(sub.text, target_lang, api_key)
            translated_subs.append((sub.index, sub.start, sub.end, translated_text))
        except Exception as e:
            print(f"Грешка при превод във файл {input_file}: {e} реда:\n{sub}")

    output_filename = f"{os.path.splitext(input_file)[0]}_{target_lang}.srt"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for index, start, end, text in translated_subs:
                f.write(f"{index}\n{start} --> {end}\n{text}\n\n")
        print(f"Файлът е запазен като {output_filename}")
    except Exception as e:
        print(f"Грешка при запис на файла {output_filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Превод на SRT субтитри с DeepL API')
    parser.add_argument('input_dir', nargs='?', default=os.getcwd(), help='Директория с входни SRT файлове')
    parser.add_argument('--target_lang', default='BG', help='Целевият език (по подразбиране "BG")')
    parser.add_argument('--api_key', required=True, help='API ключ за DeepL')

    args = parser.parse_args()

    for filename in os.listdir(args.input_dir):
        if filename.endswith('.srt'):
            input_file = os.path.join(args.input_dir, filename)
            process_srt_file(input_file, args.target_lang, args.api_key)

if __name__ == "__main__":
    main()
