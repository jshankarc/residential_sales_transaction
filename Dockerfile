FROM python:3.7-slim-buster	

WORKDIR /app

# managing logs
# TODO: mount this directory 
RUN mkdir logs

# local file storage directory to process data
RUN mkdir output

# TODO: analyze a short way to move file to the container
ADD aws_handler /app/aws_handler
ADD configs /app/configs
ADD css /app/css
ADD extract /app/extract
ADD load /app/load
ADD pytest /app/pytest
ADD templates /app/templates
ADD transform /app/transform


COPY configuration.py /app
COPY logconfig.py /app
COPY requirements.txt /app
COPY routes.py /app

RUN pip --no-cache-dir install -r requirements.txt
RUN pip install awscli

VOLUME /root/.aws/

EXPOSE 8088

ENTRYPOINT [ "python" ]
CMD [ "routes.py" ]