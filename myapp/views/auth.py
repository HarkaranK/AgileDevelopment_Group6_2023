from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from myapp.auth.models import User
from myapp.database.models import Quiz, Question, Answer, QuizQuestion, QuizParticipant, UserResponse
from myapp.database.db import db
from myapp.utils.handler import Search, QuizManager, Ingest
import os
from datetime import datetime
from flask import jsonify


def init_auth_routes(app):
    """Initializes all routes for user authentication and quiz management.

        Args:
            app (Flask): The Flask application to add routes to.

        """
    quiz_manager = QuizManager(app)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Handles user login requests, and renders the login page.

        Returns:
            Werkzeug Response: The HTTP response.
        """
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
        """Renders the landing page.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        return render_template('landing.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Handles user registration requests, and renders the registration page.

        Returns:
            Werkzeug Response: The HTTP response.
        """
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
        """Logs out the current user and redirects them to the login page.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        logout_user()
        return redirect(url_for('login'))

    @app.route('/protected')
    @login_required
    def protected():
        """Protected route that displays the current user's ID.

        Returns:
            str: A string containing the user ID of the current user.
        """
        return f'Logged in as: {current_user.user_id}'

    @app.route('/index')
    @login_required
    def index():
        """Renders the index page with all the quizzes associated with the current user.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        user_quizzes = Quiz.query.filter_by(user_id=current_user.user_id).all()
        user_quizzes_questions = []

        for quiz in user_quizzes:
            questions = quiz_manager.get_questions_answers(quiz.quiz_id)
            user_quizzes_questions.append((quiz, questions))

        return render_template('index.html', user_quizzes=user_quizzes, user_quizzes_questions=user_quizzes_questions)

    @app.route('/create_quiz', methods=['GET', 'POST'])
    @login_required
    def create_quiz():
        """Handles quiz creation requests, and renders the quiz creation page.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        if request.method == 'POST':
            # Get form data
            quiz_name = request.form.get('quiz_name')
            course = request.form.get('course')
            quiz_topic = request.form.get('quiz_topic')
            num_questions = int(request.form.get('num_questions'))
            duration = int(request.form.get('duration'))

            # Get question ids
            search = Search("us-central1-gcp", "quizzes")
            question_ids = search.get_question_ids(
                course, quiz_topic, num_questions)

            # Create Quiz
            new_quiz = Quiz(user_id=current_user.user_id,
                            quiz_name=quiz_name, duration=duration)
            db.session.add(new_quiz)
            db.session.flush()  # So we can get the ID of the new_quiz

            # Create QuizQuestion entries
            for question_id in question_ids:
                quiz_question = QuizQuestion(
                    quiz_id=new_quiz.quiz_id, question_id=question_id)
                db.session.add(quiz_question)

            db.session.commit()

            return redirect(url_for('quizzes'))
        else:
            return render_template('create_quiz.html')

    @app.route('/quiz/<int:quiz_id>')
    @login_required
    def quiz_page(quiz_id):
        """Renders the page for a specific quiz.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        quiz = Quiz.query.get(quiz_id)
        questions = quiz_manager.get_questions_answers(quiz_id)
        return render_template('quiz.html', quiz=quiz, questions=questions)

    @app.route('/edit/<int:quiz_id>', methods=['GET', 'POST'])
    @login_required
    def edit_quiz(quiz_id):
        """Handles quiz editing requests, and renders the quiz editing page.

        Args:
            quiz_id (int): The ID of the quiz to edit.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        quiz = Quiz.query.get(quiz_id)
        if request.method == 'POST':
            quiz.title = request.form['title']
            db.session.commit()
            return redirect(url_for('landing.html'))
        return render_template('edit.html', quiz=quiz)

    @app.route('/category/<category>')
    @login_required
    def category_page(category):
        """Renders the page for a specific category of quizzes.

        Args:
            category (str): The category of quizzes.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        # Replace this with your own logic to filter quizzes based on the category
        quizzes = Quiz.query.filter_by(category=category).all()
        return render_template('category.html', quizzes=quizzes, category=category)

    @app.route('/add_question', methods=['GET', 'POST'])
    @login_required
    def add_question():
        """Handles question creation requests, and renders the question creation page.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        if request.method == 'POST':
            user_id = current_user.user_id
            question_text = request.form.get('question')
            course = request.form.get('course')

            question = Question(
                user_id=user_id, question=question_text, course=course)
            db.session.add(question)
            db.session.flush()

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
        """Gets the details for a specific quiz.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            JSON: The quiz details in JSON format.
        """
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
        """Updates a specific quiz with new details.

        Args:
            quiz_id (int): The ID of the quiz to update.

        Returns:
            JSON: The result of the update operation in JSON format.
        """
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
        """Deletes a specific question.

        Args:
            question_id (int): The ID of the question to delete.

        Returns:
            JSON: The result of the deletion operation in JSON format.
        """
        question = Question.query.get(question_id)
        if question.user_id == current_user.user_id:
            db.session.delete(question)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'})

    @app.route("/streamer")
    def streamer():
        """Renders the streamer page.

        Returns:
            Werkzeug Response: The HTTP response.
        """
        return render_template("streamer.html")

    @app.route('/quizzes')
    @login_required
    def quizzes():
        """Retrieve and display quizzes for the current user.

        Returns:
            render_template: Renders the 'quizzes.html' template with the quizzes 
                            related to the current user and the first quiz data.
        """

        user_id = current_user.user_id
        quizzes = quiz_manager.get_quizzes(user_id)
        first_quiz_id = quizzes[0].quiz_id if quizzes else None
        first_quiz_data = quiz_manager.get_questions_answers(
            first_quiz_id) if first_quiz_id else None
        return render_template('quizzes.html', quizzes=quizzes, first_quiz_data=first_quiz_data, disable_inputs=True)

    @app.route('/quiz-detail/<int:quiz_id>')
    @login_required
    def quiz_detail(quiz_id):
        """Displays detailed information about a specific quiz.

        Args:
            quiz_id (int): The ID of the quiz to retrieve details for.

        Returns:
            render_template: Renders the 'quiz_detail.html' template with the quiz 
                            details and the related questions and answers.
        """

        questions_answers = quiz_manager.get_questions_answers(quiz_id)
        quiz = Quiz.query.get(quiz_id)
        return render_template('quiz_detail.html', questions_answers=questions_answers, quiz=quiz, disable_inputs=True)

    @app.route('/delete-quiz/<int:quiz_id>', methods=['DELETE'])
    @login_required
    def delete_quiz(quiz_id):
        """Deletes a specific quiz and its related entries.

        Args:
            quiz_id (int): The ID of the quiz to delete.

        Returns:
            jsonify: JSON response indicating the success or failure of the operation.
        """
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
        """Prepares a specific quiz for the user to take.

        Args:
            quiz_id (int): The ID of the quiz to take.

        Returns:
            render_template: Renders the 'take_quiz.html' template with the quiz 
                            details and the related questions and answers.
        """
        quiz = Quiz.query.get(quiz_id)
        questions_answers = quiz_manager.get_questions_answers(quiz_id)
        return render_template('take_quiz.html', quiz=quiz, questions_answers=questions_answers, disable_inputs=False)

    @app.route('/submit-quiz/<int:quiz_id>', methods=['POST'])
    @login_required
    def submit_quiz(quiz_id):
        """Handles the submission of a taken quiz.

        Args:
            quiz_id (int): The ID of the submitted quiz.

        Returns:
            jsonify: JSON response indicating the success or failure of the operation 
                    and the ID of the participation.
        """
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
            db.session.flush()

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
        """Displays the results of a completed quiz.

        Args:
            participation_id (int): The ID of the participation whose results to retrieve.

        Returns:
            render_template: Renders the 'quiz_results.html' template with the responses 
                            and the participation details.
        """
        # Retrieve user's participation and responses
        participation = QuizParticipant.query.get(participation_id)
        responses = quiz_manager.get_responses(participation.participation_id)
        return render_template('quiz_results.html', responses=responses, participation=participation)

    @app.route('/past-attempts/<int:quiz_id>')
    @login_required
    def past_attempts(quiz_id):
        """Displays past attempts of a specific quiz.

        Args:
            quiz_id (int): The ID of the quiz to retrieve past attempts for.

        Returns:
            render_template: Renders the 'past_attempts.html' template with the past 
                            attempts and the first attempt data.
        """
        participations = quiz_manager.get_participation(quiz_id)
        first_attempt_data = None
        if participations:
            first_attempt_data = quiz_manager.get_responses(
                participations[0].participation_id)
        return render_template('past_attempts.html', participations=participations, quiz_id=quiz_id, first_attempt_data=first_attempt_data)

    @app.route('/attempt-detail/<int:participation_id>')
    @login_required
    def attempt_detail(participation_id):
        """Displays detailed information about a specific attempt.

        Args:
            participation_id (int): The ID of the attempt to retrieve details for.

        Returns:
            render_template: Renders the 'attempt_detail.html' template with the responses 
                            related to the attempt.
        """
        responses = quiz_manager.get_responses(participation_id)
        return render_template('attempt_detail.html', responses=responses)

    @app.route('/create_question', methods=['GET', 'POST'])
    @login_required
    def create_question():
        """
        Handles the GET request to render the form for creating new questions and 
        the POST request to save the newly created questions in the database. It then 
        ingests the question data into a specified location and redirects to the 
        'create_quiz' page.

        Returns:
            render_template or redirect: On a GET request, it renders the 'create_question.html' 
            template. On a POST request, it saves the created questions and answers into the database 
            and redirects to 'create_quiz' page.
        """
        if request.method == 'POST':
            # Get the submitted data
            form_data = request.form

            # Iterate through the submitted questions
            question_count = 1
            question_ids = []
            while f'question-{question_count}' in form_data:
                question_text = form_data[f'question-{question_count}']
                course = form_data[f'course-{question_count}']

                # Create a new Question object and add it to the database
                question = Question(user_id=current_user.user_id,
                                    question=question_text, course=course)
                db.session.add(question)
                db.session.flush()  # Flush the session to get the question_id

                # Iterate through the submitted answers for the current question
                answer_count = 1
                while f'answer-{question_count}-{answer_count}' in form_data:
                    answer_text = form_data[f'answer-{question_count}-{answer_count}']
                    is_correct = form_data[f'correct-answer-{question_count}'] == str(
                        answer_count)

                    # Create a new Answer object and add it to the database
                    answer = Answer(question_id=question.question_id,
                                    answer=answer_text, is_correct=is_correct)
                    db.session.add(answer)

                    answer_count += 1

                question_count += 1
                question_ids.append(question.question_id)

            db.session.commit()

            ingestor = Ingest("us-central1-gcp", "quizzes")
            ingestor.ingest_questions(question_ids)
            
            return redirect(url_for('create_quiz'))
        else:
            return render_template('create_question.html')
