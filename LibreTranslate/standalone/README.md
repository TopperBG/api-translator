Build and run LibreTranslate container
```
docker-compose up -d
```

Before first run and only then:
```
pip3 install -r requirements.txt
```

Run translating scripts:
- Default: current dir is srt source, target language is BG
- Options:
```
Running translate_srt_sa.py version 1.1.0
usage: translate_srt_sa.py [-h] [--src SRC] [--lang LANG] [--out OUT]

python3 translate_srt_sa.py -src /path/to/srt --lang bg
```
- Default: current dir is srt source, target language is BG
```
python3 libre-translateV3-sa.py
```
