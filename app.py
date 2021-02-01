from flask import Flask, render_template, request
from flaskext.markdown import Markdown
import frontmatter, os
app = Flask(__name__)

post_list = {}

@app.route('/')
def home():
    path_dir = 'static/post'
    file_list = os.listdir(path_dir)
    post_list.clear()
    for file in file_list:
        ft = frontmatter.load(path_dir + '/' + file)
        post_list[(ft['title'])] = ft
    return render_template('home.html', post_list=post_list)

@app.route('/post/<post_id>/')
def post(post_id):
    return render_template('post.html', post=post_list[post_id])

if __name__ == '__main__':
    Markdown(app, extensions=['nl2br', 'fenced_code'])
    app.run(host = '0.0.0.0', port = 80)