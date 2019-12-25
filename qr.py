import pyqrcode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Question

engine = create_engine(
    'mysql+mysqlconnector://root:korvar123@127.0.0.1:3306/pappa',
    echo=True)
Session = sessionmaker(bind=engine)
db = Session()

end_points = ['register', 'results']

host_ip = 'http://192.168.1.138:5000/'

if __name__ == "__main__":
    for ep in end_points:
        url = pyqrcode.create(host_ip + ep)
        url.svg('QR/{0}.svg'.format(ep), scale=8)

    questions = db.query(Question)
    for question in questions:
        url = pyqrcode.create(host_ip + 'question/' + str(question.question_id))
        url.svg('QR/question{0}.svg'.format(question.question_id), scale=8)
