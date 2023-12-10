FROM python:3

ENV FLASK_APP=server
ENV FLASK_DEBUG=1
 
# Create app directory
WORKDIR /app
 
COPY requirements.txt ./
 
RUN pip install -r requirements.txt
 
COPY . .
 
EXPOSE 5000

CMD [ "flask", "run","--host","0.0.0.0","--port","5000", "--cert", "server_config/cert/certificate.crt", "--key", "server_config/cert/private_key.key"]