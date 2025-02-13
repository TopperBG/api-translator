import pysrt, os, sys, subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")  # API deepseek
APP_VERSION = "1.0.0"

print(f"Running {os.path.basename(__file__)} version {APP_VERSION}")

if not API_KEY:
    print("❌ ERROR: OPENAI_API_KEY is missing in the .env file!")
    sys.exit(1)

# Configure OpenAI API
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def list_files_in_directory(directory="/app/data"):
    try:
        result = subprocess.run(['ls', '-al', directory], capture_output=True, text=True)
        print(f"Target files: {result.stdout}")
    except Exception as e:
        print(f"Error occurred: {e}")

def translate_text(text, target_lang="bg"):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"Translate the following text to {target_lang}:"},
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return response.choices[0].message.content.strip()

def translate_srt(input_srt, target_lang="bg"):
    subs = pysrt.open(input_srt)
    translated_subs = pysrt.SubRipFile()

    for sub in subs:
        translated_text = translate_text(sub.text, target_lang)
        new_sub = pysrt.SubRipItem(index=sub.index, start=sub.start, end=sub.end, text=translated_text)
        translated_subs.append(new_sub)

    output_srt = f"{os.path.splitext(input_srt)[0]}_{target_lang}.srt"
    translated_subs.save(output_srt, encoding='utf-8')
    print(f"✅ Translated: {input_srt} → {output_srt}")

def process_directory(directory="/app/data", target_lang="bg"):
    print(f"Checking directory: {directory}")

    if not os.path.exists(directory):
        print(f"⚠️ Directory {directory} not found!")
        return

    srt_files = [f for f in os.listdir(directory) if f.endswith(".srt")]
    print(f"📁 Found {len(srt_files)} .srt files in {directory}")

    if not srt_files:
        print("⚠️ No .srt files found!")
        return

    for srt_file in srt_files:
        translate_srt(os.path.join(directory, srt_file), target_lang)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translate_srt.py <target_language>")
        sys.exit(1)

    target_lang = sys.argv[1]
    process_directory("/app/data", target_lang)
