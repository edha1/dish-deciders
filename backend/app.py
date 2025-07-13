from flask import Flask, request, jsonify
from recommender import * 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # this enables CORS for all domains by default, if running on public server, policy must be added for safety. 

@app.route('/recommend', methods = ['POST'])
def get_recommendations(): 
    user_input = request.json.get('userInput')

    if not user_input:
        return jsonify({'error': 'No userInput provided'}), 400

    recommendations_df = get_recommendations_json(user_input)
    
    # Convert the DataFrame to a list of dicts
    recommendations = recommendations_df.to_dict(orient='records')
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

