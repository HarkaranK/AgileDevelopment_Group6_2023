import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from myapp import create_app
from myapp.database.models import Question, Answer
from myapp.database.db import db


class Search:
    def __init__(self, pinecone_key, pinecone_env, index_name, openai_key):
        self.pinecone_key = pinecone_key
        self.pinecone_env = pinecone_env
        pinecone.init(api_key=self.pinecone_key, environment=self.pinecone_env)
        self.index_name = index_name
        self.openai_key = openai_key
        os.environ['OPENAI_API_KEY'] = self.openai_key
        self.embeddings = OpenAIEmbeddings()
        self.app = create_app()

    def get_question_ids(self, course, topic, num, score=0.8):
        cone = Pinecone.from_existing_index(self.index_name, self.embeddings) 
        docs = cone.similarity_search_with_score(topic, num, {"course": course})
        num = min(num, len(docs))
        ids = [docs[i][0].metadata["question_id"] for i in range(num) if docs[i][1] > score]
        return ids

    def get_questions_and_answers(self, question_ids):
        question_answer_list = []

        with self.app.app_context():
            for question_id in question_ids:
                question = db.session.get(Question, question_id)
                if question:
                    answers = Answer.query.filter_by(question_id=question_id).all()
                    answer_texts = [answer.answer for answer in answers]
                    question_answer_list.append({
                        "question": question.question,
                        "answers": answer_texts
                    })

        return question_answer_list
