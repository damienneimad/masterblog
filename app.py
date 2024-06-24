import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    try:
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
        except FileNotFoundError:
        return []


def save_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_posts()
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
