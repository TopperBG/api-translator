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
```
python3 translate_srt_sa.py [/path/to/srt] [bg]
```
- Default: current dir is srt source, target language is BG
```
python3 libre-translateV3-sa.py
```
