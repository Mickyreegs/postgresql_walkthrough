from taskmanager import db


class Category(db.Model):
    #schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False) #nullable=False means it's a required field
    #Since we aren't using db.Column, this will not be visible on the database itself like
    #the other columns, as it's just to reference the one-to-many relationship.
    #To link them, we need to specify which table is being targeted, which is "Task" in quotes.
    #Then, we need to use something called 'backref' which establishes a bidirectional relationship
    #in this one-to-many connection, meaning it sort of reverses and becomes many-to-one.
    #It needs to back-reference itself, but in quotes and lowercase, so backref="category".
    #Also, it needs to have the 'cascade' parameter set to 'all, delete' which means it will find
    #all related tasks and delete them.
    #The last parameter here is lazy=True, which means that when we query the database for
    #categories, it can simultaneously identify any task linked to the categories.
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        #represents itself in the form of a string
        return self.category_name

class Task(db.Model):
    #schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    #ondelete="CASCADE" essentially means that once a category is deleted, 
    # it will perform a cascading effect and also delete any task linked to it.
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        #represents itself in the form of a string
        return "#{0} - Task: {1} | Urgent: {2}".format(
            self.id, self.task_name, self.is_urgent
        )
