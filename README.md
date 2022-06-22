# Grape Chat App
---
Grape is a website for chatting and join rooms.

## this app made with:
- Django
- Djanog-channels (for websockets)

## Get app running on your local machine
First, clone this repo and navigate to it.
```cmd
git clone https://github.com/HazemLenin/grape-chat-app.git
cd grape-chat-app
```

Then, you should check if you have python, virtualenv and redis installed by typing thoose commands:

```cmd
python -v
virtualenv -v
redis-server -v
```

You should now make virtual environment. Let's call it venv and install all required packages:

```cmd
virtualenv venv
"./venv/Scripts/activate.bat"
pip install -r requirements.txt
```

Migration filed are already exist in core app. Just migrate the whole project:

```cmd
python manage.py migrate
```

You can now run the app on localhost and start redis server

```cmd
python manage.py runserver
```

```cmd
redis-server
```

Open http://localhost:8000 and voilla!
