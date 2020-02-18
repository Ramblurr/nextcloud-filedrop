FROM python:3.8-slim AS build-image
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

FROM python:3.8-slim AS runtime-image
COPY --from=build-image /opt/venv /opt/venv
RUN useradd --create-home app -d /app
WORKDIR /app
USER app
COPY ncfd/ /app/ncfd
COPY setup.py /app/setup.py
ENV PATH="/opt/venv/bin:$PATH"
CMD ["python", "-u", "-m" , "ncfd"]
