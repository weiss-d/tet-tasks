FROM python:3.8-alpine

WORKDIR /usr/src/presence_calculator

COPY src .
COPY requirements.txt .

RUN addgroup --system npuser \
    && adduser \
      --disabled-password \
      --home "$(pwd)" \
      --ingroup npuser \
      --no-create-home \
    npuser \
    && pip install --no-cache-dir -r requirements.txt

USER npuser

CMD ["python", "-m", "presence_calculator.api.app"]
