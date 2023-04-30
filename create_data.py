from myapp.database.models import Question, Answer
from myapp.database.db import db
from myapp import create_app

app = create_app()

with app.app_context():
    # Create example Node.js questions for user with user_id 'rzhuang'
    nodejs_questions = [
        {
            'user_id': 'rzhuang',
            'question': 'What is the primary use of Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What command is used to install a package using npm?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What function is used to read a file in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'How can you create a server in Node.js?',
            'course': 'Node.js'
        }
    ]

    for question_data in nodejs_questions:
        question = Question(**question_data)
        db.session.add(question)

    nodejs_question_ids = [Question.query.filter_by(**question_data).one().question_id for question_data in nodejs_questions]

    nodejs_answers = [
        [
            {'question_id': nodejs_question_ids[0], 'answer': 'Web Development', 'is_correct': False},
            {'question_id': nodejs_question_ids[0], 'answer': 'Game Development', 'is_correct': False},
            {'question_id': nodejs_question_ids[0], 'answer': 'Backend Development', 'is_correct': True},
            {'question_id': nodejs_question_ids[0], 'answer': 'Machine Learning', 'is_correct': False}
        ],
        [
            {'question_id': nodejs_question_ids[1], 'answer': 'npm add', 'is_correct': False},
            {'question_id': nodejs_question_ids[1], 'answer': 'npm install', 'is_correct': True},
            {'question_id': nodejs_question_ids[1], 'answer': 'npm get', 'is_correct': False},
            {'question_id': nodejs_question_ids[1], 'answer': 'npm fetch', 'is_correct': False}
        ],
        [
            {'question_id': nodejs_question_ids[2], 'answer': 'fs.readFile()', 'is_correct': True},
            {'question_id': nodejs_question_ids[2], 'answer': 'fs.read()', 'is_correct': False},
            {'question_id': nodejs_question_ids[2], 'answer': 'fs.open()', 'is_correct': False},
            {'question_id': nodejs_question_ids[2], 'answer': 'fs.write()', 'is_correct': False}
        ],
        [
            {'question_id': nodejs_question_ids[3], 'answer': 'Using the net module', 'is_correct': False},
            {'question_id': nodejs_question_ids[3], 'answer': 'Using the fs module', 'is_correct': False},
            {'question_id': nodejs_question_ids[3], 'answer': 'Using the http module', 'is_correct': True},
            {'question_id': nodejs_question_ids[3], 'answer': 'Using the os module', 'is_correct': False}
        ]
    ]

    for question_answers in nodejs_answers:
        for answer_data in question_answers:
            answer = Answer(**answer_data)
            db.session.add(answer)

    db.session.commit()