FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt update -y
RUN apt install tesseract-ocr -y
RUN apt install tesseract-ocr-fra -y
EXPOSE 5000
CMD ["python", "main.py"]
