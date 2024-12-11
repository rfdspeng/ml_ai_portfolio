FROM python:3.12-slim

# Set Miniconda path
ENV PATH="/root/miniconda3/bin:${PATH}"

# Install system dependencies and Miniconda
RUN apt update && apt upgrade -y && apt install wget -y && \
    cd /root && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3 && \
    /root/miniconda3/bin/conda --version

# Copy application files
WORKDIR /root/app
COPY book_rec_app.py .
COPY environment.yml .
COPY .streamlit ./.streamlit

# Create conda environment
RUN conda env create -n myenv --file environment.yml

# Expose port for Streamlit
EXPOSE 8501

# Start Streamlit using activated conda environment
ENTRYPOINT ["bash", "-c", "source activate myenv && streamlit run book_rec_app.py"]