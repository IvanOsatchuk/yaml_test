FROM alpine
COPY main.py ./main.py
RUN chmod 755 main
CMD ["python", "main.py"]

