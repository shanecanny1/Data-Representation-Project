## Author: Shane Canny
## Title: Data Representation Project 2019
## Date: 01st Jan 2019


from flask import Flask, jsonify, request, abort, make_response
from zprojectDOA import projectDAO
## from flask_cors import CORS

app = Flask(__name__, static_url_path='',static_folder='../')
#CORS(app)


# Retrieving all items of content from the Chart List by using a GET method
## Get All Movie Listings
@app.route('/Movies')
def get_Movies():
    results=projectDAO.getAll()
    return jsonify(results)
# curl -i http://127.0.0.1:5000/Movies

# Retrieving individual items of content from the Chart List by using its position in the Chart and using a GET method

#findByChartNo
@app.route('/Movies/<int:ChartNo>', methods =['GET'])
def findByID(ChartNo):
    foundMovie = projectDAO.findByID(ChartNo)
    return jsonify(foundMovie)
#curl -i http://127.0.0.1:5000/Movies/1

# Updating the Chart List by using a POST method i.e. including a new Movie
# Create
@app.route('/Movies', methods=['POST'])
def create_Movie():
    if not request.json:
        abort(400)
    if not 'ChartNo' in request.json:
        abort(400)
    Movie={
        "ChartNo":  request.json['ChartNo'],
        "Title": request.json['Title'],
        "Director": request.json['Director'],
        "Budget":request.json['Budget'],
        "Box Office":request.json['Box Office'],
        "RunningTimeMinutes":request.json['RunningTimeMinutes']
    }
    
    values = (Movie['ChartNo'], Movie['Title'], Movie['Director'], Movie['Budget'], Movie['Box Office'], Movie['RunningTimeMinutes'])
    newID = projectDAO.create(values)
    Movie['ChartNo'] = newID
    return jsonify(Movie),201
# curl -i -H "Content-Type:application/json" -X POST -d "{\"ChartNo\":\"6\",\"Title\":\"We Win Again\",\"Director\":\"Shane Canny\",\"Budget\":\"12\",\"Box Office\":\"105\",\"RunningTimeMinutes\":3000150}" http://127.0.0.1:5000/Movies

# Updating the contents of the Chart List by using its position in the Chart using a PUT method 
#Put
@app.route('/Movies/<int:ChartNo>', methods =['PUT'])
def update_Movie(ChartNo):
    foundMovie=projectDAO.findByID(ChartNo)
    if not foundMovie:
        abort(404)
    if not request.json:
        abort(400)
    if 'ChartNo' in request.json and type(request.json['ChartNo']) is not str:
        abort(400)
    if 'Title' in request.json:
        foundMovie['Title'] = request.json['Title'] 

    if 'Director' in request.json:
        foundMovie['Director'] = request.json['Director']
    
    if 'Budget' in request.json:
        foundMovie['Budget'] = request.json['Budget']
    
    if 'BoxOffice' in request.json:
        foundMovie['BoxOffice'] = request.json['BoxOffice']
    
    if 'RunningTimeMinutes' in request.json:
        foundMovie['RunningTimeMinutes'] = request.json['RunningTimeMinutes']
   
    values = (foundMovie['ChartNo'],foundMovie['Title'], foundMovie['Director'], foundMovie['Budget'], foundMovie['BoxOffice'], foundMovie['RunningTimeMinutes'])
    
    projectDAO.update(values)
    return jsonify(foundMovie),201

#curl -i -H "Content-Type:application/json" -X PUT -d "{\"Director\":\"Niamh Canny\"}" http://127.0.0.1:5000/Movies/2

# Deleting a Movie by using its position in the Chart i.e. ChartNo
@app.route('/Movies/<int:ChartNo>', methods =['DELETE'])
def delete_Movie(ChartNo):
    projectDAO.delete(ChartNo)
    return jsonify( {'Item Deleted':True })

#curl -i -H "Content-Type:application/json" -X "DELETE" http://127.0.0.1:5000/Movies/0

@app.errorhandler(404)
def not_found404(error):
   return make_response( jsonify( {'error':'Not found' }), 404)

@app.errorhandler(400)
def not_found400(error):
   return make_response( jsonify( {'error':'Bad Request' }), 400)

# included error handling functions to aid debugging

if __name__ == '__main__' :
    app.run(debug= True)
