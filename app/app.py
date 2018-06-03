from flask import Flask, render_template, request, jsonify
import os
# chcp 65001

app = Flask(__name__)
app.config.from_pyfile('settings.py')

import tinder_api
import fb_auth_token
# host = app.config['TINDER_HOST']

class profile:
    def __init__(self, name, age, images, like):
        self.name = name
        self.age = age
        self.images = images

@app.route('/login')
def login():
    fb_access_token = fb_auth_token.get_fb_access_token(app.config['FACEBOOK_EMAIL'], app.config['FACEBOOK_PASSWORD'])
    fb_user_id = fb_auth_token.get_fb_id(fb_access_token)
    tinder_api.get_auth_token(fb_access_token, fb_user_id)

@app.route('/recommend')
def recommend():
    if not tinder_api.authverif():
        login()
    recommendations = tinder_api.get_recommendations()
    # print(recommendations['results']) # get list of profiles
    # print(recommendations['results'][0])
    return render_template('recommend.html')

@app.route('/<userId>/like')
def like(userId):
    tinder_api.like(userId)
    df.to_csv('data.csv', mode='a', header=False)

@app.route('/<userId>/dislike')
def dislike(userId):
    tinder_api.dislike(userId)
    df.to_csv('data.csv', mode='a', header=False)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)