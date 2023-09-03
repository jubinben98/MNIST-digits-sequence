# Build and test stage
FROM python:3.10-slim AS test
COPY . technical_assignment
WORKDIR technical_assignment

# Creating and activating a virtual environment
RUN python -m venv vir_env
ENV PATH="/technical_assignment/vir_env/bin:$PATH"

# Installing the packages
RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    && pip install -e .\
    && python -m pytest

# Final image
FROM python:3.10-slim
# Copying the virtual environment
COPY --from=test technical_assignment/vir_env  technical_assignment/vir_env/
# Copy the files required for running the main CLIs
COPY --from=test technical_assignment/src technical_assignment/src/
COPY --from=test technical_assignment/resources technical_assignment/resources/

# Activating the virtual environment
ENV PATH="/technical_assignment/vir_env/bin:$PATH"
RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y

# Final entrypoint
ENTRYPOINT ["python", "-m", "number-generator-script"]
CMD ["--help"]