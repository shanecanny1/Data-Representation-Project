## Author: Shane Canny
## Title: Data Representation Project 2019
## Date: 29th Dec 2019


from flask import Flask, jsonify, request, abort, make_response
## from flask_cors import CORS

app = Flask(__name__, static_url_path='',static_folder='../')
#CORS(app)
Movies = [
    {
        "ChartNo":1,
        "Title" : "Incredibles_2",
        "Director":"Brad Bird",
        "Budget":"$200 Million",
        "Box Office":"$1.243 Billion",
        "Running Time (Minutes)":118},
    {
        "ChartNo":2,
        "Title":"Jurassic World Fallen Kingdom",
        "Director":"J.A. Bayona",
        "Budget":"$187 Million",
        "Box Office":"$1.309 Billion",
        "Running Time (Minutes)":128
    },
    {
        "ChartNo":3,
        "Title":"Deadpool 2",
        "Director":"David Leitch",
        "Budget":"$110 Million",
        "Box Office":"$785 Million ",
        "Running Time (Minutes)":119
    },
    {
        "ChartNo":4,
        "Title":"The Grinch",
        "Director":"Scott Mosier",
        "Budget":"$75 Million",
        "Box Office":"$511.6 Million",
        "Running Time (Minutes)":86
    },
    {
        "ChartNo":5,
        "Title":"Mission Impossible Fallout",
        "Director":"Christopher McQuarrie",
        "Budget":"$178 Million",
        "Box Office":"$791.1 Million",
        "Running Time (Minutes)":147
    },
]

# Retrieving all items of content from the Chart List by using a GET method

@app.route('/Movies', methods=['GET'])
def get_Movies():
    return jsonify( {'Movies':Movies})
# curl -i http://127.0.0.1:5000/Movies

# Retrieving individual items of content from the Chart List by using its position in the Chart and using a GET method

@app.route('/Movies/<int:ChartNo>', methods =['GET'])
def get_Movie(ChartNo):
    foundMovie = list(filter(lambda t : t['ChartNo'] == ChartNo, Movies))
    if len(foundMovie) == 0:
        return jsonify( { 'Movies' : '' }),204
    return jsonify( { 'Movies' : foundMovie[0] })
#curl -i http://127.0.0.1:5000/Movies/1

# Updating the Chart List by using a POST method i.e. including a new Movie

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
        "Running Time (Minutes)":request.json['Running Time (Minutes)']
    }
    Movies.append(Movie)
    return jsonify( {'Movie':Movie }),201
# curl -i -H "Content-Type:application/json" -X POST -d "{\"ChartNo\":\"6\",\"Title\":\"We Win Again\",\"Director\":\"Shane Canny\",\"Budget\":\"12\",\"Box Office\":\"105\",\"Running Time (Minutes)\":3000150}" http://127.0.0.1:5000/Movies

# Updating the contents of the Chart List by using its position in the Chart using a PUT method 

@app.route('/Movies/<int:ChartNo>', methods =['PUT'])
def update_Movie(ChartNo):
    foundMovies=list(filter(lambda t : t['ChartNo'] ==ChartNo, Movies))
    if len(foundMovies) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Title' in request.json and type(request.json['Title']) != str:
        abort(400)
    if 'Director' in request.json and type(request.json['Director']) is not str:
        abort(400)
    if 'Budget' in request.json and type(request.json['Budget']) is not str:
        abort(400)
    if 'Box Office' in request.json and type(request.json['Box Office']) is not str:
        abort(400)
    if 'Running Time (Minutes)' in request.json and type(request.json['Running Time (Minutes)']) is not int:
        abort(400)
    foundMovies[0]['Title']  = request.json.get('Title', foundMovies[0]['Title'])
    foundMovies[0]['Director']  = request.json.get('Director', foundMovies[0]['Director'])
    foundMovies[0]['Budget']  = request.json.get('Budget', foundMovies[0]['Budget'])
    foundMovies[0]['Box Office'] =request.json.get('Box Office', foundMovies[0]['Box Office'])
    foundMovies[0]['Running Time (Minutes)'] =request.json.get('Running Time (Minutes)', foundMovies[0]['Running Time (Minutes)'])
    return jsonify( {'Movie':foundMovies[0]})

#curl -i -H "Content-Type:application/json" -X PUT -d "{\"Director\":\"Niamh Canny\"}" http://127.0.0.1:5000/Movies/2

# Deleting a Movie by using its position in the Chart i.e. ChartNo
@app.route('/Movies/<int:ChartNo>', methods =['DELETE'])
def delete_Movie(ChartNo):
    foundMovies = list(filter (lambda t : t['ChartNo'] == ChartNo, Movies))
    if len(foundMovies) == 0:
        abort(404)
    Movies.remove(foundMovies[0])
    return jsonify( {'Item Deleted':True })

#curl -i -H "Content-Type:application/json" -X "DELETE" -d http://127.0.0.1:5000/Movies/5

@app.errorhandler(404)
def not_found404(error):
   return make_response( jsonify( {'error':'Not found' }), 404)

@app.errorhandler(400)
def not_found400(error):
   return make_response( jsonify( {'error':'Bad Request' }), 400)

# included error handling functions to aid debugging

if __name__ == '__main__' :
    app.run(debug= True)
