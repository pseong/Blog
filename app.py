from flask import Flask, render_template, request
from flaskext.markdown import Markdown
from flask_disqus import Disqus
import frontmatter, os

app = Flask(__name__)

post_list = {}
category_list = set()
    
def loadPost(category_id=''):
    path_dir = 'static/post'
    file_list = os.listdir(path_dir)
    post_list.clear()
    for file in file_list:
        ft = frontmatter.load(path_dir + '/' + file)
        category_list.add(ft['category'])
        if(category_id) : 
            if(ft['category'] == category_id) : 
                post_list[(ft['title'])] = ft
        else : post_list[(ft['title'])] = ft

@app.route('/')
def home():
    loadPost()
    return render_template('home.html', post_list=post_list, category_list=list(category_list), len=len)

@app.route('/post/<post_id>/')
def post(post_id):
    loadPost()
    return render_template('post.html', post=post_list[post_id], category_list=list(category_list), len=len)

@app.route('/category/<category_id>/')
def category(category_id):
    loadPost(category_id)
    return render_template('home.html', post_list=post_list, category_list=list(category_list), len=len)

if __name__ == '__main__':
    Markdown(app, extensions=['nl2br', 'fenced_code'])
    disq = Disqus(app)
    app.run(host = '0.0.0.0', port = 7273)