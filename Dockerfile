# Dockerfile - Ejecución 100% reproducible en cualquier OS
# Uso: docker build -t storytelling-matcom . && docker run -p 8888:8888 storytelling-matcom

FROM continuumio/miniconda3:24.1.2-0

LABEL maintainer="MATCOM - Ciencia de Datos Avanzada"
LABEL description="Storytelling con Datos: 5 arquetipos, 5 historias"

WORKDIR /app

# Copiar archivo de entorno primero (cache de capas)
COPY environment.yml .

# Crear entorno conda
RUN conda env create -f environment.yml && \
    conda clean -afy

# Activar entorno por defecto
ENV PATH /opt/conda/envs/storytelling-matcom/bin:$PATH

# Copiar todo el proyecto
COPY . .

# Exponer puerto Jupyter
EXPOSE 8888

# Comando por defecto: JupyterLab sin token, accesible desde fuera
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]