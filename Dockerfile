FROM jupyter/scipy-notebook:latest

USER root
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /home/$NB_USER/gift-framework
WORKDIR /home/$NB_USER/gift-framework

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
