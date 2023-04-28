<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from flask import render_template, redirect, url_for, request, flash
=======
from flask import render_template, redirect, url_for, request
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
from flask import render_template, redirect, url_for, request
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
from flask import render_template, redirect, url_for, request
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
from flask_login import login_user, logout_user, login_required, current_user
from myapp.auth.models import User
from myapp.database.models import Quiz, Question, Answer
from myapp.database.db import db


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
def init_auth_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user_id = request.form['username']
            password = request.form['password']
            user = User.authenticate(user_id, password)
            if user:
                login_user(user)
                return redirect(url_for('index'))
        return render_template('login.html')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            school = request.form['school']
            username = request.form['username']
            password = request.form['password']

            existing_user = User.query.filter_by(id=username).first()
            if existing_user is None:
                user = User(id=username, password_hash=User.hash_password(password), user_type='student')
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

            flash('A user with that username already exists. Please choose a different username.')
        return render_template('register.html')
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/protected')
    @login_required
    def protected():
        return f'Logged in as: {current_user.id}'


    @app.route('/')
    @login_required
    def index():
        quizzes = Quiz.query.all()
        return render_template('index.html', quizzes=quizzes)


    @app.route('/create', methods=['POST'])
    @login_required
    def create_quiz():
        title = request.form['title']
        new_quiz = Quiz(title=title)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('index'))


    @app.route('/quiz/<int:quiz_id>')
    @login_required
    def quiz_page(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        return render_template('quiz.html', quiz=quiz)


    @app.route('/create-quiz', methods=['GET', 'POST'])
    @login_required
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
    @login_required
    def edit_quiz(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if request.method == 'POST':
            quiz.title = request.form['title']
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('edit.html', quiz=quiz)


    @app.route('/delete-quiz/<int:quiz_id>', methods=['POST'])
    @login_required
    def delete_quiz(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        return redirect(url_for('index'))
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
    @app.route('/category/<category>')
    @login_required
    def category_page(category):
        # Replace this with your own logic to filter quizzes based on the category
        quizzes = Quiz.query.filter_by(category=category).all()
        return render_template('category.html', quizzes=quizzes, category=category)
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671


    # In app.py
    # In app.py
    @app.route('/add-question/<int:quiz_id>', methods=['GET', 'POST'])
    @login_required
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