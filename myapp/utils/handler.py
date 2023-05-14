import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.docstore.document import Document
from langchain.llms import OpenAI
import pinecone
from myapp.database.models import Question, Answer, Quiz, QuizQuestion, QuizParticipant, UserResponse
from myapp.database.db import db


class Handler:
    def __init__(self, pinecone_env, index_name):
        self.pinecone_env = pinecone_env
        pinecone.init(
            api_key=os.environ['PINECONE_API_KEY'], environment=self.pinecone_env)
        self.index_name = index_name


class Search(Handler):
    def __init__(self, pinecone_env, index_name):
        super().__init__(pinecone_env, index_name)
        self.embeddings = OpenAIEmbeddings()

    def get_question_ids(self, course, topic, num, score=0.3):
        cone = Pinecone.from_existing_index(self.index_name, self.embeddings)
        docs = cone.similarity_search_with_score(
            topic, num, {"course": course})
        print("Docs returned:", docs)
        num = min(num, len(docs))
        ids = [docs[i][0].metadata["question_id"]
               for i in range(num) if docs[i][1] > score]
        return ids


class Predict(Handler):
    def __init__(self, pinecone_env, index_name):
        from run import app
        super().__init__(pinecone_env, index_name)
        self.embeddings = OpenAIEmbeddings()
        self.app = app

    def get_message(self, participation_id):
        quiz_manager = QuizManager(self.app)
        response_data = quiz_manager.get_responses(participation_id)
        course = response_data[0]['question'].course
        text = f"i just took a quiz on {course} and below is the question, correct answer and my answer. would you please provide feedback on the quiz? please start with 'Here's some feedback on your quiz:'. describe the overall performance and then comment only on the questions with wrong answers. make your feedback concise and no more than 100 words.\n\n"
        for res in response_data:
            text += f"question: {res['question'].question}\ncorrect answer: {next(filter(lambda answer: answer.is_correct, res['answers']), None).answer}\nmy answer: {res['response'].answer}\n\n"
        # llm = OpenAI(model_name="gpt-4", temperature=0.5)
        # feedback = llm(text)
        return text

    # def get_questions_and_answers(self, question_ids):
    #     question_answer_list = []

    #     with app.app_context():
    #         for question_id in question_ids:
    #             question = db.session.get(Question, question_id)
    #             if question:
    #                 answers = Answer.query.filter_by(question_id=question_id).all()
    #                 answer_texts = [answer.answer for answer in answers]
    #                 question_answer_list.append({
    #                     "question": question.question,
    #                     "answers": answer_texts
    #                 })

    #     return question_answer_list


class QuizManager:
    def __init__(self, app):
        self.app = app

    def get_quizzes(self, user_id):
        with self.app.app_context():
            quizzes = Quiz.query.filter_by(
                user_id=user_id).order_by(Quiz.quiz_id.desc()).all()
            return quizzes

    def get_questions_answers(self, quiz_id):
        with self.app.app_context():
            quiz_questions = QuizQuestion.query.filter_by(
                quiz_id=quiz_id).all()
            questions_answers = []

            for quiz_question in quiz_questions:
                question = quiz_question.question
                answers = Answer.query.filter_by(
                    question_id=question.question_id).all()
                questions_answers.append({
                    'question': question,
                    'answers': answers
                })

            return questions_answers

    def get_participation(self, quiz_id):
        with self.app.app_context():
            participation = QuizParticipant.query.filter_by(
                quiz_id=quiz_id).all()
            return participation

    def get_responses(self, participation_id):
        with self.app.app_context():
            user_responses = UserResponse.query.filter_by(
                participation_id=participation_id).all()
            response_data = []

            for user_response in user_responses:
                question = Question.query.filter_by(
                    question_id=user_response.question_id).first()
                answers = Answer.query.filter_by(
                    question_id=question.question_id).all()
                selected_answer = Answer.query.filter_by(
                    answer_id=user_response.answer_id).first()
                response_data.append({
                    'question': question,
                    'response': selected_answer,
                    'answers': answers
                })

            return response_data


class Ingest(Handler):
    def __init__(self, pinecone_env, index_name):
        from run import app
        super().__init__(pinecone_env, index_name)
        self.embeddings = OpenAIEmbeddings()
        self.app = app

    def ingest_questions(self, question_ids):
        documents = []

        with self.app.app_context():
            for question_id in question_ids:
                question = db.session.get(Question, question_id)
                answers = Answer.query.filter_by(question_id=question_id).all()

                if not question or not answers:
                    print(
                        f"No question or answers found for question_id: {question_id}")
                    continue

                combined = f"{question.question}\n"
                for answer in answers:
                    combined += f"- {answer.answer}\n"

                document = Document(
                    page_content=combined,
                    metadata={
                        "course": question.course,
                        "question_id": question_id,
                    },
                )

                documents.append(document)
                print("Documents to be sent:", documents)

        Pinecone.from_documents(
            documents, self.embeddings, index_name=self.index_name)
        print(
            f"Successfully sent {len(documents)} questions and answers to Pinecone.")


class Index(Handler):
    def __init__(self, pinecone_env, index_name):
        super().__init__(pinecone_env, index_name)

    def view_stats(self):
        index = pinecone.Index(self.index_name)
        stats = index.describe_index_stats()
        return stats
