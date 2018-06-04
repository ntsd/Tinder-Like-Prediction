import os
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import urllib.request
# chcp 65001

app = Flask(__name__)
app.config.from_pyfile('settings.py')

Bootstrap(app)

import tinder_api
import fb_auth_token

from Feature import Feature
f = Feature()

class profile:
    def __init__(self, name, age, images, like, features):
        self.name = name
        self.age = age
        self.images = images
        self.like = like
        self.features = features

@app.route('/login')
def login():
    username = request.args.get('facebook_email', default = app.config['FACEBOOK_EMAIL'])
    password = request.args.get('facebook_password', default = app.config['FACEBOOK_PASSWORD'])
    fb_access_token = fb_auth_token.get_fb_access_token(username, password)
    fb_user_id = fb_auth_token.get_fb_id(fb_access_token)
    tinder_api.get_auth_token(fb_access_token, fb_user_id)

@app.route('/recommend')
def recommend():
    if not tinder_api.authverif():
        login()
    recommendations = tinder_api.get_recommendations() # output json {status='', results=[profile]}
    # print(recommendations['results']) # get list of profiles
    # print(recommendations['results'][0])
    return render_template('recommend.html')

def save_profile(profile):
    filePath = os.path.join(app.config['PROFILES_FOLDER'], profile['_id'])
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    for photo in profile['photos']:
        photo_path = os.path.join(filePath, photo['fileName'])
        features_path = os.path.join(filePath, photo['id'])
        urllib.request.urlretrieve(photo['url'], photo_path)
        features = f.getFeature(photo_path)
        if features is not None:
            np.save(features_path, features)


@app.route('/<userId>/like')
def like(userId):
    tinder_api.like(userId)
    # df.to_csv('data.csv', mode='a', header=False)

@app.route('/<userId>/dislike')
def dislike(userId):
    tinder_api.dislike(userId)
    # df.to_csv('data.csv', mode='a', header=False)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)