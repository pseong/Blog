from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
from flask_disqus import Disqus
import frontmatter, os
from collections import Counter
import markdown
import logging
from bs4 import BeautifulSoup

app = Flask(__name__)

post_list = {}
category_list = Counter()

def sortPostList():
    global post_list
    post_list = dict(sorted(post_list.items(), key=lambda x : x[1]['date'], reverse=True))


def loadPost(category_id=''):
    global post_list
    path_dir = '/home/coder/blog/static/post'
    file_list = os.listdir(path_dir)
    post_list.clear()
    category_list.clear()
    for file in file_list:
        ft = frontmatter.load(path_dir + '/' + file)
        category_list[ft['category']] += 1
        if(category_id) : 
            if(ft['category'] == category_id) : 
                post_list[ft['title']] = ft
        else : post_list[ft['title']] = ft
    sortPostList()

def searchPost(post_id):
    global post_list
    path_dir = '/home/coder/blog/static/post'
    file_list = os.listdir(path_dir)
    post_list.clear()
    category_list.clear()

    for file in file_list:
        ft = frontmatter.load(path_dir + '/' + file)
        category_list[ft['category']] += 1
        if(post_id in ft['title']) : 
            post_list[ft['title']] = ft
    sortPostList()

def get_posts(offset=0, per_page=10):
    return list(post_list.keys())[offset: offset + per_page]

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    loadPost()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(post_list)
    pagination_posts = get_posts(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('home.html', post_list=post_list, category_list=category_list, len=len,
                           BeautifulSoup=BeautifulSoup, markdown=markdown,
                           posts=pagination_posts,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route('/post/<post_id>/')
def post(post_id):
    loadPost()
    return render_template('post.html', post=post_list[post_id], category_list=category_list, len=len, markdown=markdown)

@app.route('/category/<category_id>/')
def category(category_id):
    loadPost(category_id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(post_list)
    pagination_posts = get_posts(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('home.html', post_list=post_list, category_list=category_list, len=len, category_id=category_id,
                           posts=pagination_posts,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route('/search/<search_id>')
def search(search_id):
    searchPost(search_id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(post_list)
    pagination_posts = get_posts(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('home.html', post_list=post_list, category_list=category_list, len=len, search_id=search_id,
                           posts=pagination_posts,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route('/search/')
def notsearch():
    return redirect(url_for('home'))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', category_list=category_list), 404

@app.errorhandler(401)
def custom_401(e):
    return render_template('401.html', category_list=category_list), 401

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', category_list=category_list), 500

if __name__ == '__main__':
    disq = Disqus(app)
    app.run(host = '0.0.0.0', port = 7273)