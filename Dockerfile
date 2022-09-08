FROM python:3.8-slim 

# installing packages required for installation
RUN echo "downloading basic packages for installation"
RUN apt-get update
RUN apt-get install -y tmux wget curl nano less

WORKDIR /home/

COPY requirements_docker.txt ./

RUN pip install --no-cache-dir -r requirements_docker.txt
RUN curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
RUN chmod +x /usr/local/bin/cog
COPY . .

#CMD ["bash"]
# run a test
RUN python predict.py
CMD ["bash"]
