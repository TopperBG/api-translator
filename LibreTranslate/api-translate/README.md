# api-translator
Use of AI API for .srt translation
Fill your AI API Key in .env file

### Build container
```
docker build -t api-translator .
```

### Run API translator with source directory and target language
```
docker run --rm --env-file .env -v "/home/my movie dir/my new movie/:/app/data" api-translator bg
```
