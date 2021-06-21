from app import webApp
from database import db
from flask import render_template
from flask import redirect
from flask import request


@webApp.route('/')
def index():
    return 'Hello, World!!'


@webApp.route('/site/<url>')
@webApp.route('/site')
@db.site
def render(page=None):

    print(page.__dict__)

    if not page.__dict__:
        error = {
            'title': "Error 404!",
            'body': "Page not found."
        }
        return render_template("pattern.html", page=error)

    return render_template("pattern.html", page=page.__dict__)

    if request.values.get('raw'):
        return page

    print("view site:", page)
    if not page:
        return "Page not found"

    body = page['body']
    side_bar = page['side_bar']

    data = {
        'style': page['style'],
        'title': page['title'],
        'head': page['head'],
        'body': body,
        'side': side_bar,
        'photo1': page['photo1'],
        'photo2': page['photo2']
    }

    print(data)
    # return render_template("pattern.html", page=data)


    out = ''
    for i in site.items():
        key, val = i
        out += f"<p> {key} : {val} </p>"
    return out
