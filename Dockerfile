FROM python:3.10

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --verbose --timeout 1000 -i https://pypi.python.org/simple

COPY . .

CMD [ "uvicorn", "App.main:app", "--host" , "0.0.0.0","--port","8000" ]