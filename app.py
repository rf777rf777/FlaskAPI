from flask import Flask,jsonify,request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'ScoreRecord'
app.config['MONGO_URI'] = 'mongodb://35.194.249.50:27017/ScoreRecord'

#關掉Flask會將自動導向網址加上"/"的機制
app.url_map.strict_slashes = False

mongo = PyMongo(app)

@app.route('/score', methods=['GET'])
def get_all_Scores():
  scoreList = mongo.db.Scores
  output = []
  for score in scoreList.find():
    output.append({'playerName' : score['name'], 'score' : score['score'] , 'picture' : score['picture'] })
  return jsonify({'result' : output})

@app.route('/score/<name>', methods=['GET'])
def get_one_Scores(name):
  scoreList = mongo.db.Scores
  score = scoreList.find_one({'name' : name })
  if score:
    output = {'playerName' : score['name'], 'score' : score['score'] , 'picture' : score['picture'] }
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/score', methods=['POST'])
def add_Scores():
  scoreList = mongo.db.Scores
  playerName = request.json['playerName']
  score = request.json['score']
  picture = request.json['picture']
  score_id = scoreList.insert({'name': playerName, 'score': score , 'picture': picture })
  new_score = scoreList.find_one({'_id': score_id })
  output = {'playerName' : new_score['name'], 'score' : new_score['score'], 'picture' : new_score['picture'] }
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
