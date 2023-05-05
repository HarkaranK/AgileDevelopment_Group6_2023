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
        },
        {
            'user_id': 'rzhuang',
            'question': 'How can you export a module in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which function is used to create a new buffer in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which method is used to emit an event in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What is the default package manager for Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What does "global" object in Node.js represent?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which module provides cryptographic functionality in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What is the purpose of the "process" object in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which method is used to remove a directory in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which method is used to create a new directory in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which method is used to create a Readable stream in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What is the purpose of "util.promisify()" in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'How do you enable HTTP/2 in a Node.js server?',
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


    # Create example Network questions for user with user_id 'rzhuang'
    network_questions = [
        {
            'user_id': 'rzhuang',
            'question': 'Which layer of the OSI model is responsible for reliable communication?',
            'course': 'Network'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What protocol is used by the World Wide Web?',
            'course': 'Network'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What is the standard port number for HTTP?',
            'course': 'Network'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which protocol is used to send email?',
            'course': 'Network'
        }
    ]

    for question_data in network_questions:
        question = Question(**question_data)
        db.session.add(question)

    network_question_ids = [Question.query.filter_by(**question_data).one().question_id for question_data in network_questions]

    network_answers = [
        [
            {'question_id': network_question_ids[0], 'answer': 'Physical Layer', 'is_correct': False},
            {'question_id': network_question_ids[0], 'answer': 'Data Link Layer', 'is_correct': False},
            {'question_id': network_question_ids[0], 'answer': 'Transport Layer', 'is_correct': True},
            {'question_id': network_question_ids[0], 'answer': 'Application Layer', 'is_correct': False}
        ],
        [
            {'question_id': network_question_ids[1], 'answer': 'TCP', 'is_correct': False},
            {'question_id': network_question_ids[1], 'answer': 'UDP', 'is_correct': False},
            {'question_id': network_question_ids[1], 'answer': 'FTP', 'is_correct': False},
            {'question_id': network_question_ids[1], 'answer': 'HTTP', 'is_correct': True}
        ],
        [
            {'question_id': network_question_ids[2], 'answer': '25', 'is_correct': False},
            {'question_id': network_question_ids[2], 'answer': '80', 'is_correct': True},
            {'question_id': network_question_ids[2], 'answer': '110', 'is_correct': False},
            {'question_id': network_question_ids[2], 'answer': '443', 'is_correct': False}
        ],
        [
            {'question_id': network_question_ids[3], 'answer': 'SMTP', 'is_correct': True},
            {'question_id': network_question_ids[3], 'answer': 'POP3', 'is_correct': False},
            {'question_id': network_question_ids[3], 'answer': 'IMAP', 'is_correct': False},
            {'question_id': network_question_ids[3], 'answer': 'HTTP', 'is_correct': False}
        ]
    ]

    for question_answers in network_answers:
        for answer_data in question_answers:
            answer = Answer(**answer_data)
            db.session.add(answer)

    db.session.commit()