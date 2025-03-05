from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
posts = {0: {"post_id": 0, "title": "Hello", "content": "This is the first post"}}

@app.route('/')
def home():
    return render_template('home.jinja2', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = posts.get(post_id)
    if not post:
        return render_template('404.jinja2', message=f"Post with id {post_id} was not found")
    return render_template('post.jinja2', post=post)

@app.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post_id = len(posts)  # Auto-increment post ID

        # Store new post
        posts[post_id] = {'post_id': post_id, 'title': title, 'content': content}

        return redirect(url_for('post', post_id=post_id))  # Redirect to the new post

    return render_template('create.jinja2')

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if post_id in posts:
        del posts[post_id]
    return redirect(url_for('home'))  # Redirect to homepage after deletion

# Route for editing a post
@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = posts.get(post_id)
    if not post:
        return render_template('404.jinja2', message=f'Post with id {post_id} was not found')
    
    if request.method == 'POST':
        # Get updated title and content from form
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        return redirect(url_for('post', post_id=post_id))  # Redirect back to the post page after editing
    
    return render_template('edit.jinja2', post=post)


if __name__ == '__main__':
    app.run(debug=True)
