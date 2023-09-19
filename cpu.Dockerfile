FROM ubuntu:focal

# installing packages required for installation
RUN echo "downloading basic packages for installation"
RUN apt-get update
RUN apt-get install -y tmux wget curl git
RUN apt-get install -y libstdc++6 gcc

RUN gcc --version

# install conda
RUN wget -q -P . https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash ./Miniconda3-latest-Linux-x86_64.sh -b -p /conda
RUN rm Miniconda3-latest-Linux-x86_64.sh
RUN . "/conda/etc/profile.d/conda.sh"
ENV PATH="/conda/condabin:${PATH}"

RUN mkdir lab-equibind
COPY environment_cpuonly.yml /lab-equibind/.
RUN conda env create -f lab-equibind/environment_cpuonly.yml

# Switch to the new environment:
SHELL ["conda", "run", "-n", "equibind", "/bin/bash", "-c"] 
RUN conda update -n base conda -y
COPY . /lab-equibind/.
WORKDIR /lab-equibind

CMD ["conda", "activate", "equibind-conda"]

