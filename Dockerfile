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
ADD extract /app/extract
ADD load /app/load
ADD pytest /app/pytest
ADD static /app/static
ADD templates /app/templates
ADD transform /app/transform
ADD schedule_handler /app/transform

COPY configuration.py /app
COPY exception.py /app
COPY logconfig.py /app
COPY requirements.txt /app
COPY routes.py /app

#Install Requirements
RUN pip --no-cache-dir install -r requirements.txt

# Instal AWS CLI 2
RUN pip install awscli

# Attach Volumn credentials volumn 
VOLUME /root/.aws/

EXPOSE 8088

ENTRYPOINT [ "python" ]
CMD [ "routes.py" ]