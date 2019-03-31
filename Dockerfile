FROM python:3

CMD sudo apt-get update && apt-get upgrade

# Install requirements
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Flask app
COPY api /api
ENV secrets .secrets-dev
WORKDIR /api/src
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5555", "-w", "3"]
