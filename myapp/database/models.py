from .db import db
from datetime import datetime


class Question(db.Model):
    """
    Question class that represents a quiz question.

    Attributes:
        question_id: An integer that represents the unique identifier of the question.
        user_id: A string that represents the unique identifier of the user who created the question.
        question: A string that contains the actual question text.
        course: A string that represents the course for which the question is relevant.
        quiz_questions: A list of QuizQuestion objects associated with the question.
        answers: A list of Answer objects associated with the question.
    """
    question_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)  # Updated ForeignKey
    question = db.Column(db.Text, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    quiz_questions = db.relationship('QuizQuestion', backref='question', lazy=True)
    answers = db.relationship('Answer', backref='question', lazy=True)


class Quiz(db.Model):
    """
    Quiz class that represents a quiz.

    Attributes:
        quiz_id: An integer that represents the unique identifier of the quiz.
        user_id: A string that represents the unique identifier of the user who created the quiz.
        quiz_name: A string that represents the name of the quiz.
        duration: An integer that represents the duration of the quiz in minutes.
        quiz_questions: A list of QuizQuestion objects associated with the quiz.
        participants: A list of QuizParticipant objects associated with the quiz.
    """
    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)  # Updated ForeignKey
    quiz_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    quiz_questions = db.relationship('QuizQuestion', backref='quiz', lazy=True)
    participants = db.relationship('QuizParticipant', backref='quiz', lazy=True)


class QuizQuestion(db.Model):
    """
    QuizQuestion class that represents the association between quizzes and questions.

    Attributes:
        quiz_question_id: An integer that represents the unique identifier of the QuizQuestion object.
        quiz_id: An integer that represents the unique identifier of the quiz.
        question_id: An integer that represents the unique identifier of the question.
    """
    quiz_question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)


class Answer(db.Model):
    """
    Answer class that represents an answer to a quiz question.

    Attributes:
        answer_id: An integer that represents the unique identifier of the answer.
        question_id: An integer that represents the unique identifier of the question to which the answer belongs.
        answer: A string that contains the actual answer text.
        is_correct: A boolean that represents whether or not the answer is correct.
    """
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)


class QuizParticipant(db.Model):
    """
    QuizParticipant class that represents a user's participation in a quiz.

    Attributes:
        participation_id: An integer that represents the unique identifier of the participation.
        quiz_id: An integer that represents the unique identifier of the quiz.
        participant_id: A string that represents the unique identifier of the user participating in the quiz.
        start_time: A datetime object that represents when the participant started the quiz.
        end_time: A datetime object that represents when the participant ended the quiz. None if the quiz is ongoing.
        responses: A list of UserResponse objects associated with the participant's responses in the quiz.
    """

    participation_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    participant_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)  # Updated ForeignKey
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    responses = db.relationship('UserResponse', backref='participation', lazy=True)


class UserResponse(db.Model):
    """
    UserResponse class that represents a user's response to a quiz question.

    Attributes:
        response_id: An integer that represents the unique identifier of the response.
        participation_id: An integer that represents the unique identifier of the participation.
        question_id: An integer that represents the unique identifier of the question.
        answer_id: An integer that represents the unique identifier of the answer chosen by the user.
    """
    response_id = db.Column(db.Integer, primary_key=True)
    participation_id = db.Column(db.Integer, db.ForeignKey('quiz_participant.participation_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.answer_id'), nullable=False)