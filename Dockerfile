FROM alpine
COPY main.py ./main.py
CMD ["python", "main.py"]

