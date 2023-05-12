from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from myapp.auth.models import User
from myapp.database.models import Quiz, Question, Answer, QuizQuestion
from myapp.database.db import db
from myapp.utils.handler import Search, QuizManager
import os
from flask import jsonify



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
        quizzes = Quiz.query.all()
        return render_template('landing.html', quizzes=quizzes)

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

            flash(
                'A user with that username already exists. Please choose a different username.')
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

    @app.route('/index')
    @login_required
    def index():
        user_quizzes = Quiz.query.filter_by(user_id=current_user.user_id).all()
        quiz_manager = QuizManager()
        user_quizzes_questions = []

        for quiz in user_quizzes:
            questions = quiz_manager.get_questions_answers(quiz.quiz_id)
            user_quizzes_questions.append((quiz, questions))

        return render_template('index.html', user_quizzes=user_quizzes, user_quizzes_questions=user_quizzes_questions)

    @app.route('/create', methods=['POST'])
    @login_required
    def create_quiz():
        title = request.form['title']
        new_quiz = Quiz(title=title)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('quiz_page', quiz_id=new_quiz.quiz_id))

    @app.route('/create-quiz', methods=['GET', 'POST'])
    # @login_required
    def create_quiz_page():
        try:
            if request.method == 'POST':
                quiz_name = request.form['title']
                duration = 30
                course = request.form['course']
                topic = request.form['quiz-topic']
                num = int(request.form['total_questions'])

                # Create the Quiz instance
                quiz = Quiz(user_id=current_user.user_id,
                            quiz_name=quiz_name, duration=duration)
                db.session.add(quiz)
                # Flush the session to get the quiz_id before adding QuizQuestion instances
                db.session.flush()

                # Add QuizQuestions for each question_id in question_ids
                search = Search("us-central1-gcp", "quizzes")
                question_ids = search.get_question_ids(course, topic, num, 0.3)
                print(f"Question IDs: {question_ids}")

                for question_id in question_ids:
                    quiz_question = QuizQuestion(
                        quiz_id=quiz.quiz_id, question_id=question_id)
                    db.session.add(quiz_question)
                    print(f"Adding QuizQuestion: {quiz_question}")

                db.session.commit()
                return redirect(url_for('quiz_page', quiz_id=quiz.quiz_id))
            return render_template('create_quiz.html')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('create_quiz.html', error=str(e))

    @app.route('/quiz/<int:quiz_id>')
    @login_required
    def quiz_page(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        manger = QuizManager()
        questions = manger.get_questions_answers(quiz_id)
        return render_template('quiz.html', quiz=quiz, questions=questions)

    @app.route('/submit-quiz/<int:quiz_id>', methods=['POST'])
    @login_required
    def submit_quiz(quiz_id):
        # Retrieve submitted answers
        answers = {}
        for key, value in request.form.items():
            if key.startswith('question-'):
                question_id = int(key.split('-')[-1])
                answers[question_id] = int(value)

        # Check answers and calculate the score
        score = 0
        total_questions = len(answers)
        for question_id, answer_id in answers.items():
            answer = Answer.query.get(answer_id)
            if answer.is_correct:
                score += 1
        return render_template('results.html', score=score, total_questions=total_questions, quiz_id=quiz_id)

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
            return redirect(url_for('landing.html'))
        return render_template('edit.html', quiz=quiz)
    
    # @app.route('/delete-quiz/<int:quiz_id>', methods=['POST'])
    # @login_required
    # def delete_quiz(quiz_id):
    #     quiz = Quiz.query.get(quiz_id)
    #     db.session.delete(quiz)
    #     db.session.commit()
    #     return redirect(url_for('landing.html'))

    @app.route('/delete-quiz/<int:quiz_id>', methods=['POST'])
    @login_required
    def delete_quiz(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if quiz.user_id == current_user.user_id:
            db.session.delete(quiz)
            db.session.commit()
            print(f"Quiz with id {quiz_id} was deleted successfully")
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'})

    @app.route('/category/<category>')
    @login_required
    def category_page(category):
        # Replace this with your own logic to filter quizzes based on the category
        quizzes = Quiz.query.filter_by(category=category).all()
        return render_template('category.html', quizzes=quizzes, category=category)

    @app.route('/add_question', methods=['GET', 'POST'])
    @login_required
    def add_question():
        if request.method == 'POST':
            user_id = current_user.user_id
            question_text = request.form.get('question')
            course = request.form.get('course')

            question = Question(
                user_id=user_id, question=question_text, course=course)
            db.session.add(question)
            db.session.commit()

            # Add the answers
            for i in range(1, 5):
                answer_text = request.form.get(f'answer{i}')
                if answer_text:  # Add this conditional check
                    is_correct = request.form.get(f'is_correct{i}') == 'true'
                    answer = Answer(question_id=question.question_id,
                                    answer=answer_text, is_correct=is_correct)
                    db.session.add(answer)

            db.session.commit()
            flash('Question added successfully.', 'success')
            return redirect(url_for('index'))

        return render_template('add_question.html')
    @app.route('/get-quiz-details/<int:quiz_id>', methods=['GET'])
    @login_required
    def get_quiz_details(quiz_id):
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        questions = []

        for quiz_question in quiz_questions:
            question = Question.query.get(quiz_question.question_id)
            questions.append({
                'question_id': question.question_id,
                'question_text': question.question_text
            })

        return jsonify(questions)
    
    @app.route('/update-quiz/<int:quiz_id>', methods=['POST'])
    @login_required
    def update_quiz(quiz_id):
        data = request.get_json()
        new_question_ids = data['question_ids']

        # Delete existing QuizQuestion instances
        existing_quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        for quiz_question in existing_quiz_questions:
            db.session.delete(quiz_question)

        # Add new QuizQuestions for each question_id in new_question_ids
        for question_id in new_question_ids:
            quiz_question = QuizQuestion(quiz_id=quiz_id, question_id=question_id)
            db.session.add(quiz_question)

        db.session.commit()
        return jsonify({'status': 'success'})
    
    @app.route('/delete-question/<int:question_id>', methods=['POST'])
    @login_required
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question.user_id == current_user.user_id:
            db.session.delete(question)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'})




    @app.route("/streamer")
    def streamer():
        return render_template("streamer.html")
