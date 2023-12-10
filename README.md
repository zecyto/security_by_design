# security_by_design

## run the project

### Option 1 (docker)
1. Navigate to the Repo Folder
    <pre>cd security_by_design/</pre>

2. Build the docker container (try sudo if permission denied)
    <pre>docker build -t flask-app .</pre>

3. Run the container
    <pre>docker run -it -p 5000:5000 -d flask-app</pre>

4. Visite the Website on
    <pre>https://127.0.0.1:5000</pre>

5. Trust our selfsigned Certificate

### Option 2 (python)
You need to install certain python moduls with pip (requirements.txt)

1. Navigate to the Repo Folder
    <pre>cd security_by_design/</pre>

2. Set Up Config to run the Server
    <pre>export FLASK_APP=server</pre>

3. Run the Server
    <pre>flask run</pre>

4. Visite the Website on
    <pre>https://127.0.0.1:5000</pre>

5. Trust our selfsigned Certificate


### Optional (run a proxy server)

1. Install nginx
    <pre>sudo apt update</pre>
    <pre>sudo apt install nginx</pre>

2. Navigate to your nginx sites
     <pre>cd /etc/nginx/sites-available/</pre>

3. Copy site.conf to nginx sites
    <pre>sudo cp nginx-config/site.conf /etc/nginx/sites-available/flask_app</pre>

4. Enable the site
    <pre>sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled</pre>

5. Restart nginx
    <pre>sudo service nginx restart</pre>

6. Visit the site (just type in localhost in the url you will get redirected to our website with https)
    <pre>localhost</pre>

7. Trust our selfsigned Certificate

## User Accounts (with smartmeters)

1. email: k.stroetmann@example.org  pw: secbydesign
2. email: s.claus@christmas.org     pw: secbydesign

## Admin Account (you will need an 2F-Authenticator App)

1. email: admin@admin pw: admin 2fa setup key:
2. Setup Key for 2FA: FJMXJNVZSYV5A4PFOIWC5MXQO5KSMUOT (You can simply add this code in e.g. Google Authenticator App)
3. Has access to the hidden site /admin/dashboard