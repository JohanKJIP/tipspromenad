from flask import Flask, escape, request, render_template, make_response, redirect, url_for
import uuid
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pappa.models import User, Question, Answer
import json

app = Flask(__name__, static_url_path='/static')
# yes that is a password :)
engine = create_engine(
    'mysql+mysqlconnector://root:korvar123@127.0.0.1:3306/pappa',
    echo=True)
Session = sessionmaker(bind=engine)
db = Session()

@app.route('/register')
def register():
    user_id = request.cookies.get('user_id')
    resp = make_response(render_template('register.html'))
    if user_id != None:
        user = db.query(User).filter_by(user_id=user_id).first()
        if user != None:
            return render_template('prompt_reregister.html', team_name=user.team_name)
        else:
            resp.set_cookie('sessionID', '', expires=0)
    return resp

@app.route('/welcome', methods = ['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        resp = make_response(render_template('welcome.html', team_name=request.form['team_name']))
        user_id = uuid.uuid4()
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=2)
        resp.set_cookie('user_id', str(user_id), expires=expire_date)

        # store user in db
        new_user = User(user_id=str(user_id), team_name=request.form['team_name'])
        db.add(new_user)
        db.commit()
        return resp
    
    if (request.method == 'GET'):
        user_id = request.cookies.get('user_id')
        if (user_id != None):
            user = db.query(User).filter_by(user_id=user_id).first() 
            return render_template('welcome.html', team_name=user.team_name)
        return 'No access (cookie goto: /register)'


@app.route('/question/<int:question_id>')
def show_question(question_id):
    question = db.query(Question).filter_by(question_id=question_id).first() 
    user_id = request.cookies.get('user_id')
    previous_answer = db.query(Answer).filter_by(question_id=question_id, user_id=user_id).first() 
    if (previous_answer == None):
        user = db.query(User).filter_by(user_id=user_id).first() 
        if (user_id != None and user != None):
            if (question != None):
                media = question.media
                media_type = media.split("/")[0].replace(" ", "")
                print(media_type)
                return render_template('question.html', user_id=user_id, team_name=user.team_name, question_id=question.question_id, 
                    meta=question.meta, media=question.media, choice1=question.choice1, choice2=question.choice2,
                    choice3=question.choice3, choice4=question.choice4, media_type=media_type)
            return 'Question not found!'
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('answered'))


@app.route('/select_answer', methods = ['POST'])
def select_answer():
    answer = Answer(user_id=request.form['user_id'], question_id=request.form['question_id'], answer=request.form['answer'])
    db.add(answer)
    db.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/answered', methods = ['GET'])
def answered():
    return render_template('answered.html')

@app.route('/results', methods = ['GET'])
def show_results():
    print('\n')
    print('------------------------------------')
    users = db.query(User).all()
    correct_answers = db.query(Question)
    
    first = None
    first_score = -1
    second = None
    second_score = -1
    third = None
    third_score = -1

    user_id = request.cookies.get('user_id')
    team_name = None
    team_score = 0

    if user_id != None:
        for user in users:
            print("HEEEEEEeeereewsssdaddsdad")
            correct = 0
            user_answers = db.query(Answer).filter_by(user_id=user.user_id).all()
            print(user_answers)
            print(user)
            for answer in user_answers:
                question_answer = correct_answers.get({'question_id': answer.question_id})
                print(question_answer)
                if (answer.answer == question_answer.answer):
                    correct += 1 
            # ugly
            if (correct >= first_score):
                third = second
                third_score = second_score
                second = first
                second_score = first_score
                first = user
                first_score = correct
            else:
                if (correct >= second_score):
                    third = second
                    third_score = second_score
                    second = user
                    second_score = correct
                else:
                    if (correct >= third_score):
                        third_score = correct
                        third = user

            if (user.user_id == user_id):
                team_name = user.team_name
                team_score = correct

    first_name = ""
    second_name = ""
    third_name = ""
    if (first != None):
        first_name = first.team_name
    if (second != None):
        second_name = second.team_name
    if (third != None):
        third_name = third.team_name

    return render_template('leaderboard.html', first_name=first_name, second_name=second_name, third_name=third_name,
        first_score=first_score, second_score=second_score, third_score=third_score, team_score=team_score, team_name=team_name)

@app.route('/test', methods = ['GET'])
def test():
    return render_template('test.html')