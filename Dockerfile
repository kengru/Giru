FROM python:3.8-slim
RUN pip install pipenv

WORKDIR /src
COPY . .

VOLUME /home/GiruData
ENV GIRU_DATA_PATH /home/GiruData

RUN pipenv install --system --deploy --ignore-pipfile
ENTRYPOINT [ "python", "-m", "giru" ]
