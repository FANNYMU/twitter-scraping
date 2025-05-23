from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    try:
        
        df = pd.read_csv('tweets_clean.csv')
        
        tweets = df.to_dict('records')
        
        return jsonify({
            'status': 'success',
            'data': tweets,
            'total': len(tweets)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 