FROM python:3.10
ARG DJANGO_PORT
ENV DOCKER_APP_LOCATION=/opt/app
WORKDIR $DOCKER_APP_LOCATION

# Update pip
RUN pip install --upgrade pip

# Install dependencies
COPY . $DOCKER_APP_LOCATION
RUN pip install -r requirements.txt

# Expose django port and run the dev server
EXPOSE ${DJANGO_PORT}
CMD python l8nite/manage.py runserver 0.0.0.0:${DJANGO_PORT}
