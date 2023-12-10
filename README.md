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
    <pre>flask run --cert server_config/cert/certificate.crt --key server_config/cert/private_key.key</pre>

4. Visite the Website on
    <pre>https://127.0.0.1:5000</pre>

5. Trust our selfsigned Certificate


### Optional (run a proxy server)

1. Install nginx
    <pre>sudo apt update</pre>
    <pre>sudo apt install nginx</pre>

2. Navigate to the Repo Folder
    <pre>cd security_by_design/</pre>

3. Add your local path to the Repo in the site.conf for the certificate and the private key
    <pre>nano nginx-config/site.conf</pre>
    
4. Copy site.conf in the nginx-sites
    <pre>sudo cp nginx-config/site.conf /etc/nginx/sites-available/flask_app</pre>

5. Enable the site
    <pre>sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled</pre>

6. Restart nginx
    <pre>sudo service nginx restart</pre>

7. Visit the site (just type in localhost in the url you will get redirected to our website with https)
    <pre>localhost</pre>

8. Trust our selfsigned Certificate

## User Accounts (with smartmeters)

1. email: k.stroetmann@example.org  pw: secbydesign
2. email: s.claus@christmas.org     pw: secbydesign

Actions:    
1. Change Password
2. Delete Account
3. Add new 2FA Token
4. Remove 2FA Token
5. View your Smartmeters
6. View your Contract Details (Contract Model 1 or 2)


## Admin Account (you will need an 2F-Authenticator App)

1. email: admin@admin pw: admin 2fa setup key:
2. Setup Key for 2FA: (You can simply add this code in e.g. Google Authenticator App)
    <pre>FJMXJNVZSYV5A4PFOIWC5MXQO5KSMUOT</pre>
3. Has access to the hidden site /admin/dashboard

Actions on Admin Dashboard:    
1. Reset the password of an User Account
2. Delete an User Account
3. Unlock an Account (Reset the failed Login tries)
4. Manage Rights
5. Manage Contract details
6. View Logs of permission changes (green mac signals that its valid)
