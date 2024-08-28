import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import random

# Initialize Firebase with Streamlit secrets
if not firebase_admin._apps:
    # Convert AttrDict to regular dict
    firebase_creds = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Rest of your code remains the same...

# Helper functions
def get_high_scores():
    scores_ref = db.collection('high_scores')
    scores = scores_ref.order_by('score', direction=firestore.Query.DESCENDING).limit(10).get()
    return [(score.to_dict()['name'], score.to_dict()['questions'], score.to_dict()['score']) for score in scores]

def add_high_score(name, questions, score):
    db.collection('high_scores').add({
        'name': name,
        'questions': questions,
        'score': score
    })

@st.cache_resource
def get_quiz_names():
    quizzes = db.collection('quizzes').get()
    return [quiz.id for quiz in quizzes]

@st.cache_data
def get_questions(quiz_name):
    doc = db.collection('quizzes').document(quiz_name).get()
    if doc.exists:
        return doc.to_dict()['questions']
    return []

# Main app
st.title('Spiritual Knowledge Quiz')

# Sidebar
st.sidebar.title('Quiz Game!')
user_name = st.sidebar.text_input('Your name for the leaderboard:', max_chars=50, key='user_name')

if user_name:
    # Admin functions
    if user_name == 'admin':
        with st.sidebar.expander("Admin Functions"):
            if st.button('Reset High Scores'):
                db.collection('high_scores').get()  # Delete all documents in high_scores collection
                st.success('High scores have been reset.')

    # Quiz setup
    quiz_names = get_quiz_names()
    quiz_choice = st.sidebar.selectbox('Choose a quiz:', quiz_names)

    if quiz_choice:
        st.write(f'Selected quiz: {quiz_choice}')

        # Initialize session state
        if 'questions' not in st.session_state or st.session_state.current_quiz != quiz_choice:
            st.session_state.questions = get_questions(quiz_choice)
            random.shuffle(st.session_state.questions)
            st.session_state.question_index = 0
            st.session_state.count = 0
            st.session_state.correct = 0
            st.session_state.consecutive = 0
            st.session_state.current_quiz = quiz_choice

        # Display question
        if st.session_state.questions:
            question = st.session_state.questions[st.session_state.question_index]
            st.session_state.correct_answer = question['correctAnswer']
            
            st.write(question['question'])
            
            # Display answers in a 2x2 grid
            answers = question['incorrectAnswers'] + [st.session_state.correct_answer]
            random.shuffle(answers)
            cols = st.columns(2)
            for i, answer in enumerate(answers):
                if cols[i % 2].button(answer, key=f"answer_{i}"):
                    check_answer(answer)

            # Display score
            st.write(f'Score: {st.session_state.correct} out of {st.session_state.count}')
        else:
            st.write("No questions available for this quiz.")

    # Display high scores
    st.sidebar.subheader('High Scores')
    for name, questions, score in get_high_scores():
        st.sidebar.text(f'{name}: {score}/{questions}')

else:
    st.write('Please enter your name to start the quiz.')

# Function to check answers (place this before it's called)
def check_answer(answer):
    st.session_state.count += 1
    if answer == st.session_state.correct_answer:
        st.session_state.correct += 1
        st.session_state.consecutive += 1
        st.success(f'Correct! {answer}')
        check_and_update_high_score()
    else:
        st.error(f'Incorrect. The correct answer was {st.session_state.correct_answer}')
    st.session_state.question_index = (st.session_state.question_index + 1) % len(st.session_state.questions)

# Function to check and update high score
def check_and_update_high_score():
    current_score = st.session_state.correct
    high_scores = get_high_scores()
    if not high_scores or current_score > high_scores[0][2]:
        add_high_score(st.session_state.user_name, st.session_state.count, current_score)
        st.success(f'New high score! {current_score} correct answers!')