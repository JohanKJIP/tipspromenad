from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'User'
    user_id = Column(String, primary_key=True)
    team_name = Column(Integer) 
    
    def __repr__(self):
        return "<User(id='%s', team_name='%s')>" % (
            self.user_id, self.team_name)

class Answer(Base):
    __tablename__ = 'Answer'
    user_id = Column(String, primary_key=True)
    question_id = Column(Integer) 
    answer = Column(Integer) 
    
    def __repr__(self):
        return "<Answer(id='%s', question_id='%s')>" % (
            self.user_id, self.question_id)

class Question(Base):
    __tablename__ = 'Question'
    question_id = Column(Integer, primary_key=True)
    meta = Column(String)
    media = Column(String)
    answer = Column(Integer) 
    choice1 = Column(String)
    choice2 = Column(String)
    choice3 = Column(String)
    choice4 = Column(String)
    
    def __repr__(self):
        return "<Question(id='%s', answer='%s')>" % (
            self.question_id, self.answer)