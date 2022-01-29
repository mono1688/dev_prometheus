FROM python:3.7.12
RUN pip3 install python-telegram-bot flask gunicorn python-dateutil flask_basicauth PyYAML requests
WORKDIR /code
ADD telegram_warn.py /code/telegram_warn.py
ENV TAG "vc2.0"
ENV CHATID xxx
ENV TOKEN xxx
CMD ["python3","/code/telegram_warn.py"]