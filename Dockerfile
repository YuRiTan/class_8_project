FROM python:3

# Install requirements
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Flask app
COPY api /api
ENV secrets .secrets-dev
WORKDIR /api
# CMD ["gunicorn", "app:app"]
CMD ["python", "app.py"]
