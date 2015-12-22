# Dockerfile to inject app source code into Image
FROM maxsocl/courselets:dev
ADD . /code/
RUN pip install -r ../requirements.txt
