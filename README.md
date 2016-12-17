# ~Good~Vibes~

**Relaxing music loops from /f/**

This project houses a selection of flash videos with atmospheric music and images.
Flash is no longer a popular media format, but I think that it offers a certain lo-fi charm that adds to the experience.
Minimal navigation controls are provided to switch between songs.

This project is hosted @ https://chill-out.herokuapp.com/

## Setup
To run your own server using gunicorn (recommended)

```bash
$ git clone https://github.com/michael-lazar/goodvibes
$ cd goodvibes
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ gevent goodvibes.server:app
```