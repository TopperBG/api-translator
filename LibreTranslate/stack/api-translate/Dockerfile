FROM python:3.10
WORKDIR /app
COPY . .
RUN pip3 install pysrt requests
ENTRYPOINT ["python"]
CMD ["translate_srt.py"]
