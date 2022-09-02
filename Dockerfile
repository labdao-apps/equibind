FROM python:3.8-slim 

WORKDIR /home/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash"]