# BUPT Passport

A Python module for [web VPN](http://webvpn.bupt.edu.cn) and [authentication](https://auth.bupt.edu.cn/).

### Features
 - Captcha recognition
 - Broswer simulation
 - Custom session support
 - Duplicate logins support

### Requirements
 - Python 3.6+
 - Packages in `requirements.txt`
 - [Tesseract](https://github.com/tesseract-ocr/tesseract)
 - [pyenv](https://github.com/pyenv/pyenv) (recommend)

### Usage
1. Create a pyenv enviroment (recommend) and install dependencies.
1. Copy `credentials.default.py` to `credentials.py` and edit it.
1. Edit `config.py` if necessary.
1. Run `python3 run.py`.

### Note
 - Login status is linked with cookies/sessions.
 - The VPN server is unstable.
