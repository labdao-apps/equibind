FROM python:3.8-slim 

# installing packages required for installation
RUN echo "downloading basic packages for installation"
RUN apt-get update
RUN apt-get install -y tmux wget curl git nano

WORKDIR /home/

COPY requirements_docker.txt ./

RUN pip install --no-cache-dir -r requirements_docker.txt

COPY . .

#CMD ["bash"]
CMD ["bash", "run.sh"]
