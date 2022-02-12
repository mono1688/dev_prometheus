FROM python:3.7.12
RUN pip3 install python-telegram-bot flask gunicorn python-dateutil flask_basicauth PyYAML requests
WORKDIR /code
ADD telegram_warn.py /code/telegram_warn.py
ADD host.txt /code/host.txt
ENV TAG 'test1.0:-773160920,test2.0:-773160920'
ENV TOKEN xxx

CMD ["python3","/code/telegram_warn.py"]
