FROM python:3.8-slim 

# installing packages required for installation
RUN echo "downloading basic packages for installation"
RUN apt-get update
RUN apt-get install -y tmux wget curl nano less git

WORKDIR /home/

COPY requirements_docker.txt ./

RUN pip install --no-cache-dir -r requirements_docker.txt
RUN git clone https://github.com/NiklasTR/petri.git
RUN pip install petri/python

COPY . .


# run a test
RUN python predict.py
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
#CMD ["bash"]