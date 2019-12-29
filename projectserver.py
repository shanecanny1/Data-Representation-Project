from flask import Flask

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/Movies')
def getAll():
    return"in getAll"

@app.route('/Movies/<int:id>')
def findByid(id):
    return"in find By id for id"+str(id)

if __name__=='__main__' :
    app.run(debug=True)
