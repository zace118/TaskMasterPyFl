from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This just references line 1
app = Flask(__name__)

# Telling our app where our DB is located
    # Three slashes is a relative path
    # Four slashes is a absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initalizing our Database
db = SQLAlchemy(app)


# Create a model
class Todo(db.Model):
    # Set up columns
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # A function that returns a string every time we create a new element
    def __repr__(self):
        # Every time we make a new element it'll return the Task with the ID that has just been created. (That's what the %r is?)
        return '<Task %r>' % self.id




# ------------- CREATE & READ -------------

# Index route
    # Now we've added our methods of what we can do with this route
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method== "POST":
        # This pulls the 'content' from the name attribute on the input in the index.html file
        task_content = request.form['content']

        # Creating a model for this
        new_task = Todo(content=task_content)

        # Push to DB
        try:
            # Create a new task from the input
            db.session.add(new_task)

            # Commit it to our database
            db.session.commit()

            # Redirect after commit
            return redirect('/')

        except:
            return 'There was an issue adding your task.'

    else:
        # This looks at all the DB content in order of creation and grabs ALL of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        # render_template will automatically go into a templates file. The parameter is the file it's searching for
        return render_template('index.html', tasks=tasks)


# ------------- UPDATE -------------

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        # Setting the current task's content to the content in the Update Task page's form's input box
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was in issue updating this task'
    else:
        # Setting task to task_to_update
        return render_template('update.html', task=task_to_update)


# ------------- DELETE -------------

# Setting up delete route. The route is built similarly to MYSQL where we do '/delete/:id' this does '<dataType:variableName>'
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was an issue deleting that task.'
            
            
if __name__ == "__main__":
    # Setting debug to True so it'll give us an error if it bugs out
    app.run(debug=True)