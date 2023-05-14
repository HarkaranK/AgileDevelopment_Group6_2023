from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from myapp.auth.models import User
from myapp.database.models import Quiz, Question, Answer, QuizQuestion, QuizParticipant, UserResponse
from myapp.database.db import db
from myapp.utils.handler import Search, QuizManager
import os
from datetime import datetime
from flask import jsonify


def init_auth_routes(app):
    quiz_manager = QuizManager(app)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user_id = request.form['username']
            password = request.form['password']
            user = User.authenticate(user_id, password)
            if user:
                login_user(user)
                return redirect(url_for('quizzes'))
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
        questions = quiz_manager.get_questions_answers(quiz_id)
        return render_template('quiz.html', quiz=quiz, questions=questions)

    # @app.route('/submit-quiz/<int:quiz_id>', methods=['POST'])
    # @login_required
    # def submit_quiz(quiz_id):
    #     # Retrieve submitted answers
    #     answers = {}
    #     for key, value in request.form.items():
    #         if key.startswith('question-'):
    #             question_id = int(key.split('-')[-1])
    #             answers[question_id] = int(value)

    #     # Check answers and calculate the score
    #     score = 0
    #     total_questions = len(answers)
    #     for question_id, answer_id in answers.items():
    #         answer = Answer.query.get(answer_id)
    #         if answer.is_correct:
    #             score += 1
    #     return render_template('results.html', score=score, total_questions=total_questions, quiz_id=quiz_id)

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
        # Get data from request
        updated_quiz_data = request.json

        # Get the quiz
        quiz = Quiz.query.get(quiz_id)

        # Check for valid quiz
        if not quiz:
            return jsonify({'success': False, 'error': 'Quiz not found'})

        # Remove any questions not included in the updated quiz data
        for quiz_question in quiz.quiz_questions:
            if quiz_question.question_id not in updated_quiz_data['questions']:
                db.session.delete(quiz_question)

        # Commit changes to database
        db.session.commit()

        # Send back a response
        return jsonify({'success': True})

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

    @app.route('/quizzes')
    @login_required
    def quizzes():
        user_id = current_user.user_id
        quizzes = quiz_manager.get_quizzes(user_id)
        first_quiz_id = quizzes[0].quiz_id if quizzes else None
        first_quiz_data = quiz_manager.get_questions_answers(
            first_quiz_id) if first_quiz_id else None
        return render_template('quizzes.html', quizzes=quizzes, first_quiz_data=first_quiz_data, disable_inputs=True)

    @app.route('/quiz-detail/<int:quiz_id>')
    @login_required
    def quiz_detail(quiz_id):
        questions_answers = quiz_manager.get_questions_answers(quiz_id)
        quiz = Quiz.query.get(quiz_id)
        return render_template('quiz_detail.html', questions_answers=questions_answers, quiz=quiz, disable_inputs=True)

    @app.route('/delete-quiz/<int:quiz_id>', methods=['DELETE'])
    @login_required
    def delete_quiz(quiz_id):
        try:
            quiz = Quiz.query.get(quiz_id)
            QuizQuestion.query.filter_by(quiz_id=quiz_id).delete()
            QuizParticipant.query.filter_by(quiz_id=quiz_id).delete()
            db.session.delete(quiz)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/take-quiz/<int:quiz_id>', methods=['GET'])
    @login_required
    def take_quiz(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        questions_answers = quiz_manager.get_questions_answers(quiz_id)
        return render_template('take_quiz.html', quiz=quiz, questions_answers=questions_answers, disable_inputs=False)

    @app.route('/submit-quiz/<int:quiz_id>', methods=['POST'])
    @login_required
    def submit_quiz(quiz_id):
        try:
            # Get start_time from request payload
            start_time = request.json['start_time']
            # Convert from milliseconds to seconds
            start_time = datetime.fromtimestamp(start_time / 1000)

            # Calculate end_time
            end_time = datetime.now()

            # Create a new QuizParticipant entry with start_time and end_time
            quiz_participant = QuizParticipant(
                quiz_id=quiz_id,
                participant_id=current_user.user_id,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(quiz_participant)
            db.session.commit()

            # Create UserResponse entries
            for response in request.json['responses']:
                user_response = UserResponse(participation_id=quiz_participant.participation_id,
                                             question_id=response['question_id'],
                                             answer_id=response['answer_id'])
                db.session.add(user_response)
            db.session.commit()

            # Return participation_id instead of a simple success message
            return jsonify({'success': True, 'participation_id': quiz_participant.participation_id})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/quiz-results/<int:participation_id>', methods=['GET'])
    @login_required
    def quiz_results(participation_id):
        # Retrieve user's participation and responses
        participation = QuizParticipant.query.get(participation_id)
        responses = quiz_manager.get_responses(participation.participation_id)
        return render_template('quiz_results.html', responses=responses)
