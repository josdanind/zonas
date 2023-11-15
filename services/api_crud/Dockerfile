FROM python:3.12

WORKDIR /api_crud
COPY . /api_crud/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./scripts/wait-for-it.sh
