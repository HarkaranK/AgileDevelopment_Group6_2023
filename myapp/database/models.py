from .db import db
from datetime import datetime


class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)  # Updated ForeignKey
    question = db.Column(db.Text, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    quiz_questions = db.relationship('QuizQuestion', backref='question', lazy=True)
    answers = db.relationship('Answer', backref='question', lazy=True)


class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)  # Updated ForeignKey
    quiz_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    quiz_questions = db.relationship('QuizQuestion', backref='quiz', lazy=True)
    participants = db.relationship('QuizParticipant', backref='quiz', lazy=True)


class QuizQuestion(db.Model):
    quiz_question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)


class Answer(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)


class QuizParticipant(db.Model):
    participation_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    participant_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)  # Updated ForeignKey
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    responses = db.relationship('UserResponse', backref='participation', lazy=True)


class UserResponse(db.Model):
    response_id = db.Column(db.Integer, primary_key=True)
    participation_id = db.Column(db.Integer, db.ForeignKey('quiz_participant.participation_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.answer_id'), nullable=False)