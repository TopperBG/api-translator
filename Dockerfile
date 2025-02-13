FROM python:3.10
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
ENV OPENAI_API_KEY=""
ENV OPENAI_BASE_URL="https://api.deepseek.com"
ENTRYPOINT ["python", "translate_srt.py"]
