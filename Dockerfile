# Build and test stage
FROM python:3.10-slim AS test
COPY . MNIST-digits-sequence
WORKDIR MNIST-digits-sequence

# Creating and activating a virtual environment
RUN python -m venv vir_env
ENV PATH="/MNIST-digits-sequence/vir_env/bin:$PATH"

# Installing the packages
RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    && pip install -e .\
    && python -m pytest

# Final image
FROM python:3.10-slim
# Copying the virtual environment
COPY --from=test MNIST-digits-sequence/vir_env  MNIST-digits-sequence/vir_env/
# Copy the files required for running the main CLIs
COPY --from=test MNIST-digits-sequence/src MNIST-digits-sequence/src/
COPY --from=test MNIST-digits-sequence/resources MNIST-digits-sequence/resources/

# Activating the virtual environment
ENV PATH="/MNIST-digits-sequence/vir_env/bin:$PATH"
RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y

# Final entrypoint
ENTRYPOINT ["python", "-m", "number-generator-script"]
CMD ["--help"]