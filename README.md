# Yatube
![Python](https://img.shields.io/badge/Python-3.11-%23254F72?style=flat-square&logo=python&logoColor=yellow&labelColor=254f72)
![Django](https://img.shields.io/badge/Django-4.2-0C4B33?style=flat-square&logo=django&logoColor=white&labelColor=0C4B33)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-712CF9?style=flat-square&logo=bootstrap&logoColor=white&labelColor=712CF9)

## The social network for creating blogs✨
- Yatube is a social network, where you can create blogs, to share your thoughts and view other people's posts.

---
![Yatube Demo](yatube_project/demo/yatube.gif)
---

## Features

- 📝 Commenting on other people's posts
- 🖼 Adding photos to your posts
- 📌 Ability to subscribe for other people

---
## Tech

- [HTML/CSS](https://developer.mozilla.org)
- [Bootstrap 5.3](https://getbootstrap.com/)
- [Python 3.11](https://www.python.org/)
- [Django 4.2](https://www.djangoproject.com/)
---

## Installation

Clone the repository to your computer:

```
git clone https://github.com/RolanIm/yatube_project.git
```

Install and create the virtual environment:

```
python3 -m venv venv
```

Activate a virtual environment:
- for windows:

  ```
  source venv/Scripts/activate
  ```
- for Unix/macOS:

  ```
  source venv/bin/activate
  ```

Install dependencies from the file requirements.txt: 

```
pip install -r requirements.txt
```
Go to the yatube_project directory:

```
cd yatube_project/
```

Make migrations

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Run the `manage.py` file: 

```
python manage.py runserver
```

Go to the site using the link http://127.0.0.1:8000/
---
## Author
### [_Rolan Imangulov_](https://github.com/RolanIm)

---
## License

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
