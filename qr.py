import pyqrcode

if __name__ == "__main__":
    url = pyqrcode.create('http://192.168.1.138:5000/question/1')
    url.svg('q1.svg', scale=8)