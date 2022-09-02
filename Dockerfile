FROM python:3.8-slim 

WORKDIR /home/

COPY requirements_docker.txt ./

RUN pip install --no-cache-dir -r requirements_docker.txt

COPY . .

CMD ["bash"]
