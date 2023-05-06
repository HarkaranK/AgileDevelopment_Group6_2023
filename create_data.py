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
            'question': 'What is the purpose of the "require" function in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What is the Event Loop in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which module is used to work with file paths in Node.js?',
            'course': 'Node.js'
        },
        {
            'user_id': 'rzhuang',
            'question': 'How can you create a child process in Node.js?',
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
        ],
        [
            {'question_id': nodejs_question_ids[4], 'answer': 'To include a module', 'is_correct': True},
            {'question_id': nodejs_question_ids[4], 'answer': 'To create a new object', 'is_correct': False},
            {'question_id': nodejs_question_ids[4], 'answer': 'To define a function', 'is_correct': False},
            {'question_id': nodejs_question_ids[4], 'answer': 'To create a new variable', 'is_correct': False}
        ],
        [
            {'question_id': nodejs_question_ids[5], 'answer': 'A feature that handles multiple connections', 'is_correct': True},
            {'question_id': nodejs_question_ids[5], 'answer': 'A programming pattern', 'is_correct': False},
            {'question_id': nodejs_question_ids[5], 'answer': 'A module in Node.js', 'is_correct': False},
            {'question_id': nodejs_question_ids[5], 'answer': 'A built-in function', 'is_correct': False}
        ],
        [
            {'question_id': nodejs_question_ids[6], 'answer': 'fs', 'is_correct': False},
            {'question_id': nodejs_question_ids[6], 'answer': 'http', 'is_correct': False},
            {'question_id': nodejs_question_ids[6], 'answer': 'path', 'is_correct': True},
            {'question_id': nodejs_question_ids[6], 'answer': 'net', 'is_correct': False}
        ],
        [
            {'question_id': nodejs_question_ids[7], 'answer': 'Using the "spawn" function', 'is_correct': True},
            {'question_id': nodejs_question_ids[7], 'answer': 'Using the "fork" function', 'is_correct': True},
            {'question_id': nodejs_question_ids[7], 'answer': 'Using the "exec" function', 'is_correct': True},
            {'question_id': nodejs_question_ids[7], 'answer': 'Using the "setTimeout" function', 'is_correct': False}
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
        },
        {
            'user_id': 'rzhuang',
            'question': 'What does the term "OSI Model" stand for?',
            'course': 'Network'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which protocol is responsible for error checking and data recovery in the transport layer?',
            'course': 'Network'
        },
        {
            'user_id': 'rzhuang',
            'question': 'What is the primary purpose of the DNS?',
            'course': 'Network'
        },
        {
            'user_id': 'rzhuang',
            'question': 'Which port number does the HTTP protocol use?',
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
        ],
        [
            {'question_id': network_question_ids[4], 'answer': 'Open Systems Interconnection', 'is_correct': True},
            {'question_id': network_question_ids[4], 'answer': 'Operating System Interface', 'is_correct': False},
            {'question_id': network_question_ids[4], 'answer': 'Optimal System Integration', 'is_correct': False},
            {'question_id': network_question_ids[4], 'answer': 'Optical Signal Interface', 'is_correct': False}
        ],
        [
            {'question_id': network_question_ids[5], 'answer': 'UDP', 'is_correct': False},
            {'question_id': network_question_ids[5], 'answer': 'TCP', 'is_correct': True},
            {'question_id': network_question_ids[5], 'answer': 'IP', 'is_correct': False},
            {'question_id': network_question_ids[5], 'answer': 'ARP', 'is_correct': False}
        ],
        [
            {'question_id': network_question_ids[6], 'answer': 'Route selection', 'is_correct': False},
            {'question_id': network_question_ids[6], 'answer': 'Error checking', 'is_correct': False},
            {'question_id': network_question_ids[6], 'answer': 'Domain name resolution', 'is_correct': True},
            {'question_id': network_question_ids[6], 'answer': 'File transfer', 'is_correct': False}
        ],
        [
            {'question_id': network_question_ids[7], 'answer': '21', 'is_correct': False},
            {'question_id': network_question_ids[7], 'answer': '25', 'is_correct': False},
            {'question_id': network_question_ids[7], 'answer': '80', 'is_correct': True},
            {'question_id': network_question_ids[7], 'answer': '110', 'is_correct': False}
        ]
    ]

    for question_answers in network_answers:
        for answer_data in question_answers:
            answer = Answer(**answer_data)
            db.session.add(answer)

    db.session.commit()


    # Create example Network questions for user with user_id 'harkaran'
    biology_questions = [
        {
            'user_id': 'harkaran',
            'question': 'Chest is used for pushing while the back is used for pulling?',
            'course': 'Biology'
        },
        {
            'user_id': 'harkaran',
            'question': 'How many heads does the bicep have?',
            'course': 'Biology'
        },
        {
            'user_id': 'harkaran',
            'question': 'How many heads does the tricep have?',
            'course': 'Biology'
        },
        {
            'user_id': 'harkaran',
            'question': 'What is the upper back usually known as?',
            'course': 'Biology'
        },
        {
            'user_id': 'harkaran',
            'question': 'What is the middle back usually known as?',
            'course': 'Biology'
        },
        {
            'user_id': 'harkaran',
            'question': 'Can working out your grip increase forearm size?',
            'course': 'Biology'
        },
        {
            'user_id': 'harkaran',
            'question': 'How many muscles groups are in the legs?',
            'course': 'Biology'
        },
        {
            'user_id': 'harkaran',
            'question': 'How many different muscle groups are in the thigh?',
            'course': 'Biology'
        },
    ]

    for question_data in biology_questions:
        question = Question(**question_data)
        db.session.add(question)

    biology_questions_ids = [Question.query.filter_by(**question_data).one().question_id for question_data in biology_questions]

    biology_answers = [
        [
            {'question_id': biology_questions_ids[0], 'answer': 'True', 'is_correct': True},
            {'question_id': biology_questions_ids[0], 'answer': 'False', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[1], 'answer': '1', 'is_correct': False},
            {'question_id': biology_questions_ids[1], 'answer': '2', 'is_correct': True},
            {'question_id': biology_questions_ids[1], 'answer': '3', 'is_correct': False},
            {'question_id': biology_questions_ids[1], 'answer': '4', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[2], 'answer': '1', 'is_correct': False},
            {'question_id': biology_questions_ids[2], 'answer': '2', 'is_correct': False},
            {'question_id': biology_questions_ids[2], 'answer': '3', 'is_correct': True},
            {'question_id': biology_questions_ids[2], 'answer': '4', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[3], 'answer': 'Traps', 'is_correct': True},
            {'question_id': biology_questions_ids[3], 'answer': 'Lats', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[4], 'answer': 'Traps', 'is_correct': False},
            {'question_id': biology_questions_ids[4], 'answer': 'Lats', 'is_correct': True},
        ],
        [
            {'question_id': biology_questions_ids[5], 'answer': 'True', 'is_correct': True},
            {'question_id': biology_questions_ids[5], 'answer': 'False', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[6], 'answer': '5', 'is_correct': False},
            {'question_id': biology_questions_ids[6], 'answer': '6', 'is_correct': False},
            {'question_id': biology_questions_ids[6], 'answer': '7', 'is_correct': True},
            {'question_id': biology_questions_ids[6], 'answer': '8', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[7], 'answer': '1', 'is_correct': False},
            {'question_id': biology_questions_ids[7], 'answer': '2', 'is_correct': False},
            {'question_id': biology_questions_ids[7], 'answer': '3', 'is_correct': True},
            {'question_id': biology_questions_ids[7], 'answer': '4', 'is_correct': False},
        ],
    ]

    for question_answers in biology_answers:
        for answer_data in question_answers:
            answer = Answer(**answer_data)
            db.session.add(answer)
    
    db.session.commit()

    physics_questions = [
        {
            'user_id': 'aaronw',
            'question': "Which of the following best describes the relationship between force, mass, and acceleration according to Newton's second law?",
            'course': 'Physics'
        },
        {
            'user_id': 'aaronw',
            'question': 'What is the SI unit of measurement for work?',
            'course': 'Physics'
        },
        {
            'user_id': 'aaronw',
            'question': 'Which of the following describes the effect of increasing the distance between two electric charges?',
            'course': 'Physics'
        },
        {
            'user_id': 'aaronw',
            'question': 'Which of the following is an example of a simple machine?',
            'course': 'Physics'
        },
        {
            'user_id': 'aaronw',
            'question': 'What is the law of conservation of energy?',
            'course': 'Physics'
        },
        {
            'user_id': 'aaronw',
            'question': 'Which of the following is an example of an exothermic process?',
            'course': 'Physics'
        },
        {
            'user_id': 'aaronw',
            'question': 'How many muscles groups are in the legs?',
            'course': 'Physics'
        },
        {
            'user_id': 'aaronw',
            'question': 'Which of the following is a type of electromagnetic radiation with the longest wavelength?',
            'course': 'Physics'
        },
    ]

    for question_data in physics_questions:
        question = Question(**question_data)
        db.session.add(question)

    physics_questions_ids = [Question.query.filter_by(**question_data).one().question_id for question_data in physics_questions]

    physics_answers = [
        [
            {'question_id': biology_questions_ids[0], 'answer': 'Force is proportional to mass, and inversely proportional to acceleration', 'is_correct': False},
            {'question_id': biology_questions_ids[0], 'answer': 'Force is proportional to acceleration, and inversely proportional to mass', 'is_correct': True},
            {'question_id': biology_questions_ids[0], 'answer': 'Mass is proportional to force, and inversely proportional to acceleration', 'is_correct': False},
            {'question_id': biology_questions_ids[0], 'answer': 'Acceleration is proportional to mass, and inversely proportional to force', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[1], 'answer': 'Joule', 'is_correct': True},
            {'question_id': biology_questions_ids[1], 'answer': 'Watt', 'is_correct': False},
            {'question_id': biology_questions_ids[1], 'answer': 'Newton', 'is_correct': False},
            {'question_id': biology_questions_ids[1], 'answer': 'Meter', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[2], 'answer': 'The force between them increases', 'is_correct': False},
            {'question_id': biology_questions_ids[2], 'answer': 'The force between them decreases', 'is_correct': True},
            {'question_id': biology_questions_ids[2], 'answer': 'The force between them remains constant', 'is_correct': False},
            {'question_id': biology_questions_ids[2], 'answer': 'The force between them becomes repulsive instead of attractive', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[3], 'answer': 'A screwdriver', 'is_correct': True},
            {'question_id': biology_questions_ids[3], 'answer': 'A computer', 'is_correct': False},
            {'question_id': biology_questions_ids[3], 'answer': 'A bicycle', 'is_correct': False},
            {'question_id': biology_questions_ids[3], 'answer': 'A television', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[4], 'answer': 'Energy cannot be created or destroyed, only transformed from one form to another', 'is_correct': True},
            {'question_id': biology_questions_ids[4], 'answer': 'Energy always flows from hot to cold objects', 'is_correct': False},
            {'question_id': biology_questions_ids[4], 'answer': 'Energy is always conserved in a closed system', 'is_correct': False},
            {'question_id': biology_questions_ids[4], 'answer': 'Energy is proportional to mass and velocity', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[5], 'answer': 'Melting ice', 'is_correct': False},
            {'question_id': biology_questions_ids[5], 'answer': 'Boiling water', 'is_correct': False},
            {'question_id': biology_questions_ids[5], 'answer': 'Burning wood', 'is_correct': True},
            {'question_id': biology_questions_ids[5], 'answer': 'Rusting iron', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[6], 'answer': 'c = λf', 'is_correct': True},
            {'question_id': biology_questions_ids[6], 'answer': 'E = mc²', 'is_correct': False},
            {'question_id': biology_questions_ids[6], 'answer': 'F = ma', 'is_correct': False},
            {'question_id': biology_questions_ids[6], 'answer': 'v = d/t', 'is_correct': False},
        ],
        [
            {'question_id': biology_questions_ids[7], 'answer': 'Gamma rays', 'is_correct': False},
            {'question_id': biology_questions_ids[7], 'answer': 'X-rays', 'is_correct': False},
            {'question_id': biology_questions_ids[7], 'answer': 'Ultraviolet light', 'is_correct': False},
            {'question_id': biology_questions_ids[7], 'answer': 'Radio waves', 'is_correct': True},
        ],
    ]

    for question_answers in physics_answers:
        for answer_data in question_answers:
            answer = Answer(**answer_data)
            db.session.add(answer)
    
    db.session.commit()
    
    communication_questions = [
        {
            'user_id': 'chrisk',
            'question': 'Which following her is not used as a possessive pronoun?',
            'course': 'Communication'
        },
        {
            'user_id': 'chrisk',
            'question': 'Which of the following represents the disadvantage of working in teams?',
            'course': 'Communication'
        },
        {
            'user_id': 'chrisk',
            'question': 'Which of the following writing corresponds with the most formal?',
            'course': 'Communication'
        },
        {
            'user_id': 'chrisk',
            'question': 'Which of the following is the most improper description of avoiding an apology?',
            'course': 'Communication'
        },
        {
            'user_id': 'chrisk',
            'question': 'Which of the following can not be used as a cc?',
            'course': 'Communication'
        },
        {
            'user_id': 'chrisk',
            'question': 'Which of the following order is correct for the closing line in a letter?',
            'course': 'Communication'
        },
        {
            'user_id': 'chrisk',
            'question': 'Which of the following is not represent for a good delivery in oral presentation?',
            'course': 'Communication'
        },
        {
            'user_id': 'chrisk',
            'question': 'Which of the following is not a type of oral presentation?',
            'course': 'Communication'
        }
    ]

    for question_data in communication_questions:
        question = Question(**question_data)
        db.session.add(question)

    communication_question_ids = [Question.query.filter_by(**question_data).one().question_id for question_data in communication_questions]

    communication_answers = [
        [
            {'question_id': communication_question_ids[0], 'answer': 'Annie drove a car for improving her driving skill.', 'is_correct': False},
            {'question_id': communication_question_ids[0], 'answer': 'Anthony is the main character from her point of view.', 'is_correct': False},
            {'question_id': communication_question_ids[0], 'answer': 'I love her enough to sacrifice my life.', 'is_correct': True},
            {'question_id': communication_question_ids[0], 'answer': 'Huckley was her first love. ', 'is_correct': False}
        ],
        [
            {'question_id': communication_question_ids[1], 'answer': 'Increased Information', 'is_correct': False},
            {'question_id': communication_question_ids[1], 'answer': 'Groupthink', 'is_correct': True},
            {'question_id': communication_question_ids[1], 'answer': 'Diversity of Views', 'is_correct': False},
            {'question_id': communication_question_ids[1], 'answer': 'Support for solutions', 'is_correct': False}
        ],
        [
            {'question_id': communication_question_ids[2], 'answer': 'Texts', 'is_correct': False},
            {'question_id': communication_question_ids[2], 'answer': 'Memos', 'is_correct': False},
            {'question_id': communication_question_ids[2], 'answer': 'Letters', 'is_correct': True},
            {'question_id': communication_question_ids[2], 'answer': 'Emails', 'is_correct': False}
        ],
        [
            {'question_id': communication_question_ids[3], 'answer': 'Apologizing keeps attention on the error or problem, not a solution.', 'is_correct': False},
            {'question_id': communication_question_ids[3], 'answer': 'Apologies may seem pretentious.', 'is_correct': True},
            {'question_id': communication_question_ids[3], 'answer': 'Apologizing can be taken as a responsibility for the problem.', 'is_correct': False},
            {'question_id': communication_question_ids[3], 'answer': 'Apologies make the writing with a negative atmosphere.', 'is_correct': False}
        ],
        [
            {'question_id': communication_question_ids[4], 'answer': 'Manager of the receiver', 'is_correct': False},
            {'question_id': communication_question_ids[4], 'answer': 'CEO', 'is_correct': False},
            {'question_id': communication_question_ids[4], 'answer': 'Councillor of the company', 'is_correct': False},
            {'question_id': communication_question_ids[4], 'answer': 'Receiver', 'is_correct': True}
        ],
        [
            {'question_id': communication_question_ids[5], 'answer': 'Complimentary close, signature, sender information, copy line, enclosure line', 'is_correct': True},
            {'question_id': communication_question_ids[5], 'answer': 'Complimentary close, sender information, signature, copy line, enclosure line', 'is_correct': False},
            {'question_id': communication_question_ids[5], 'answer': 'Complimentary close, sender information, signature, enclosure line, copy line', 'is_correct': False},
            {'question_id': communication_question_ids[5], 'answer': 'Complimentary close, signature, sender information, enclosure line, copy line', 'is_correct': False}
        ],
        [
            {'question_id': communication_question_ids[6], 'answer': 'shows poise and confidence in facial expression', 'is_correct': False},
            {'question_id': communication_question_ids[6], 'answer': 'maintains a business-like tone', 'is_correct': False},
            {'question_id': communication_question_ids[6], 'answer': 'maintains eye contact, responds to audience', 'is_correct': False},
            {'question_id': communication_question_ids[6], 'answer': 'visually present main ideas and sub-points', 'is_correct': True}
        ],
        [
            {'question_id': communication_question_ids[7], 'answer': 'Impromptu presentation', 'is_correct': False},
            {'question_id': communication_question_ids[7], 'answer': 'Abstract presentation', 'is_correct': True},
            {'question_id': communication_question_ids[7], 'answer': 'Manuscript presentation', 'is_correct': False},
            {'question_id': communication_question_ids[7], 'answer': 'Memorized presentation', 'is_correct': False}
        ]
    ]

    for question_answers in communication_answers:
        for answer_data in question_answers:
            answer = Answer(**answer_data)
            db.session.add(answer)
