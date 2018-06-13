import subprocess

subprocess.call(["sudo", "apt-get", "-y", "install", "virtualenv"])
subprocess.call(["virtualenv", "-p", "python3", ".env"])
subprocess.call([".env/bin/pip", "install", "-r", "requirements.txt"])
subprocess.call([".env/bin/python", "catalog_image/manage.py", "migrate"])
subprocess.call([".env/bin/python", "catalog_image/manage.py", "runserver", "8001"])
