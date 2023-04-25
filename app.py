from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizzes.db'
db = SQLAlchemy(app)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))

# Adding this block to set up an application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)

@app.route('/create', methods=['POST'])
def create_quiz():
    title = request.form['title']
    new_quiz = Quiz(title=title)
    db.session.add(new_quiz)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/quiz/<int:quiz_id>')
def quiz_page(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    return render_template('quiz.html', quiz=quiz)

@app.route('/create-quiz', methods=['GET', 'POST'])
def create_quiz_page():
    try:
        if request.method == 'POST':
            title = request.form['title']
            new_quiz = Quiz(title=title)
            db.session.add(new_quiz)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('create_quiz.html')
    except Exception as e:
        print(f"Error: {e}")
        return render_template('create_quiz.html', error=str(e))


@app.route('/edit/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if request.method == 'POST':
        quiz.title = request.form['title']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', quiz=quiz)

@app.route('/delete-quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('index'))

# In app.py
# In app.py
@app.route('/add-question/<int:quiz_id>', methods=['GET', 'POST'])
def add_question_page(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if request.method == 'POST':
        question_text = request.form['question']
        new_question = Question(question_text=question_text, quiz_id=quiz_id)
        db.session.add(new_question)
        db.session.commit()

        options = [
            request.form['option1'],
            request.form['option2'],
            request.form['option3'],
            request.form['option4']
        ]
        correct_option = int(request.form['correct_option'])

        for index, option in enumerate(options, start=1):
            is_correct = (index == correct_option)
            new_answer = Answer(answer_text=option, is_correct=is_correct, question_id=new_question.id)
            db.session.add(new_answer)
            db.session.commit()

        return redirect(url_for('add_question_page', quiz_id=quiz_id))
    return render_template('add_question.html', quiz=quiz)
