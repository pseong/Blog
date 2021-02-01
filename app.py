from flask import Flask, render_template, request
import frontmatter, os
app = Flask(__name__)

@app.route('/')
def home():
    path_dir = 'static/post'
    file_list = os.listdir(path_dir)
    post_list = []
    for file in file_list:
        post_list.append(frontmatter.load(path_dir + '/' + file))
    return render_template('home.html', post_list=post_list)

@app.route('/post')
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)