from flask import render_template, request, Blueprint, redirect
from app.models import Post, Todo
from app import db


main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        if len(task_content) < 1 or str(task_content).isdigit():
            return redirect('/error')

        else:
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'Adding error'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, posts=posts)


@main.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Deleting error'


@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Updating error'
    else:
        return render_template('update.html', task=task)


