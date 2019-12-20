FROM python:3.6

RUN echo "Asia/Shanghai" > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata

ENV PYTHONPATH=/app

COPY requirements.txt /app/
RUN pip install --upgrade pip \
 && pip install wheel \
 && pip install -r /app/requirements.txt \
 && rm -rf ~/.cache/pip

COPY . /app/

EXPOSE 1127

CMD ["gunicorn", "-b", "0.0.0.0:1127", "run"]
