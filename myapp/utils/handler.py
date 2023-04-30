import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.docstore.document import Document
import pinecone
from myapp import create_app
from myapp.database.models import Question, Answer
from myapp.database.db import db


class Handler:
    def __init__(self, pinecone_key, pinecone_env, index_name):
        self.pinecone_key = pinecone_key
        self.pinecone_env = pinecone_env
        pinecone.init(api_key=self.pinecone_key, environment=self.pinecone_env)
        self.index_name = index_name


class Search(Handler):
    def __init__(self, pinecone_key, pinecone_env, index_name, openai_key):
        super().__init__(pinecone_key, pinecone_env, index_name)
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


class Ingest(Handler):
    def __init__(self, pinecone_key, pinecone_env, index_name, openai_key):
        super().__init__(pinecone_key, pinecone_env, index_name)
        self.openai_key = openai_key
        os.environ['OPENAI_API_KEY'] = self.openai_key
        self.embeddings = OpenAIEmbeddings()
        self.app = create_app()

    def ingest_questions(self, question_ids):
        documents = []

        with self.app.app_context():
            for question_id in question_ids:
                question = db.session.get(Question, question_id)
                answers = Answer.query.filter_by(question_id=question_id).all()

                if not question or not answers:
                    print(f"No question or answers found for question_id: {question_id}")
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

        Pinecone.from_documents(documents, self.embeddings, index_name=self.index_name)
        print(f"Successfully sent {len(documents)} questions and answers to Pinecone.")


class Index(Handler):
    def __init__(self, pinecone_key, pinecone_env, index_name):
        super().__init__(pinecone_key, pinecone_env, index_name)

    def view_stats(self):
        index = pinecone.Index(self.index_name)
        stats = index.describe_index_stats()
        return stats
