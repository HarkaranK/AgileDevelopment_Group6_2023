import os
from myapp import create_app
from myapp.database.models import Question, Answer
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.docstore.document import Document
import pinecone

PINECONE_API_KEY = "cddf4fa5-371b-4fc1-941b-c33c33980784"
PINECONE_ENV = "us-central1-gcp"
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
os.environ['OPENAI_API_KEY'] = ""
embeddings = OpenAIEmbeddings()
index_name = "quizzes"
app = create_app()


def combine_question_and_answers(question, answers):
    combined = f"{question.question}\n"
    for answer in answers:
        combined += f"- {answer.answer}\n"
    return combined


def send_openai_embeddings_to_pinecone_langchain(question_id):
    with app.app_context():
        question = Question.query.get(question_id)
        answers = Answer.query.filter_by(question_id=question_id).all()

    if not question or not answers:
        print(f"No question or answers found for question_id: {question_id}")
        return

    combined = combine_question_and_answers(question, answers)

    document = Document(
        page_content=combined,
        metadata={
            "course": question.course,
            "question_id": question_id,
        },
    )

    Pinecone.from_documents([document], embeddings, index_name=index_name)

    print(f"Successfully sent question {question_id} and answers to Pinecone using Langchain and OpenAI embeddings.")


# Replace this with the actual question_id you want to send to Pinecone
question_id_to_send = 4
send_openai_embeddings_to_pinecone_langchain(question_id_to_send)
