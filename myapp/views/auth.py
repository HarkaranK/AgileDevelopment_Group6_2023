from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from myapp.auth.models import User
from myapp.database.models import Quiz, Question, Answer, QuizQuestion
from myapp.database.db import db
from myapp.utils.handler import Search
import os


def init_auth_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user_id = request.form['username']
            password = request.form['password']
            user = User.authenticate(user_id, password)
            if user:
                login_user(user)
                return redirect(url_for('create_quiz_page'))
        return render_template('login.html')

    @app.route('/')
    def landing_page():
        return render_template('landing.html')

    # @app.route('/')
    # def index():
    #     quizzes = Quiz.query.all()
    #     return render_template('index.html', quizzes=quizzes)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            school = request.form['school']
            username = request.form['username']
            password = request.form['password']

            existing_user = User.query.filter_by(user_id=username).first()
            if existing_user is None:
                new_user = User(user_id=username)
                new_user.set_password(password)
                new_user.set_attr(name, school)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))

            flash('A user with that username already exists. Please choose a different username.')
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/protected')
    @login_required
    def protected():
        return f'Logged in as: {current_user.user_id}'


    # @app.route('/')
    # def index():
    #     quizzes = Quiz.query.all()
    #     return render_template('index.html', quizzes=quizzes)


    @app.route('/create', methods=['POST'])
    @login_required
    def create_quiz():
        title = request.form['title']
        new_quiz = Quiz(title=title)
        # new_quiz = Quiz(title=title, user_id=current_user.user_id)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('quiz_page', quiz_id=new_quiz.quiz_id))
        # return redirect(url_for('index'))

    @app.route('/create-quiz', methods=['GET', 'POST'])
    @login_required
    def create_quiz_page():
        try:
            if request.method == 'POST':
                quiz_name = request.form['title']
                duration = 30
                course = request.form['course']
                topic = request.form['quiz-topic']
                num = int(request.form['total_questions'])
                
                # Create the Quiz instance
                quiz = Quiz(user_id=current_user.user_id, quiz_name=quiz_name, duration=duration)
                db.session.add(quiz)
                db.session.flush()  # Flush the session to get the quiz_id before adding QuizQuestion instances
                
                # Add QuizQuestions for each question_id in question_ids
                search = Search("us-central1-gcp", "quizzes")
                question_ids = search.get_question_ids(course, topic, num, 0.3)
                print(f"Question IDs: {question_ids}")

                for question_id in question_ids:
                    quiz_question = QuizQuestion(quiz_id=quiz.quiz_id, question_id=question_id)
                    db.session.add(quiz_question)
                    print(f"Adding QuizQuestion: {quiz_question}")

                db.session.commit()
                # return redirect(url_for('index'))
                return redirect(url_for('quiz_page', quiz_id=quiz.quiz_id))
            return render_template('create_quiz.html')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('create_quiz.html', error=str(e))
        
    @app.route('/quiz/<int:quiz_id>')
    @login_required
    def quiz_page(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        print(f"Quiz questions: {quiz_questions}")
        questions = []
        for quiz_question in quiz_questions:
            question = Question.query.get(quiz_question.question_id)
            print(f"Question: {question}")
            answers = Answer.query.filter_by(question_id=question.question_id).all()
            print(f"Answers: {answers}")
            questions.append({
                'question': question,
                'answers': answers
            })
        return render_template('quiz.html', quiz=quiz, questions=questions)

        
    @app.route('/test_statistic')
    @login_required
    def test_statistic():
        return render_template('test_statistic.html')



    @app.route('/edit/<int:quiz_id>', methods=['GET', 'POST'])
    @login_required
    def edit_quiz(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if request.method == 'POST':
            quiz.title = request.form['title']
            db.session.commit()
            return redirect(url_for('index.html'))
        return render_template('edit.html', quiz=quiz)


    @app.route('/delete-quiz/<int:quiz_id>', methods=['POST'])
    @login_required
    def delete_quiz(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        return redirect(url_for('index.html'))
    
    @app.route('/category/<category>')
    @login_required
    def category_page(category):
        # Replace this with your own logic to filter quizzes based on the category
        quizzes = Quiz.query.filter_by(category=category).all()
        return render_template('category.html', quizzes=quizzes, category=category)
    
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