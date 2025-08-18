FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
COPY . .
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-k", "gevent", "-w", "2"]