import os
import traceback

import config
import cv2
import pymongo
from flask import Flask, jsonify
from flask import request
from photo_processor import PhotoProcessor
from repository.statistics_repository import StatisticsRepository
from repository.user_repository import UserRepository

app = Flask("E-AT")
mongo_client = pymongo.MongoClient(
    'mongodb://%s:%s@%s:27017' % (config.database_user, config.database_password, config.database_host))
user_repository = UserRepository(mongo_client['e_at_db'])
stats_repository = StatisticsRepository(mongo_client['e_at_db'])
photo_processor = PhotoProcessor(stats_repository)


@app.route('/register', methods=['POST'])
def register_user():
    try:
        json_request = request.get_json()
        user_repository.register(json_request['username'], json_request['password'])
        return {"result": "user created"}
    except ValueError as error:
        return {"result": str(error)}, 400
    except Exception as err:
        return {"result": str(err)}, 500


@app.route('/login', methods=['POST'])
def login():
    try:
        json_request = request.get_json()
        user_repository.check_user(json_request['username'], json_request['password'])
        generated_token = user_repository.login(json_request['username'])
        return {"token": generated_token}
    except ValueError as error:
        return {"result": str(error)}, 400
    except Exception as err:
        return {"result": str(err)}, 500


@app.route('/logout', methods=['POST'])
def logout():
    try:
        token = request.headers.get('e_at_token')
        username = user_repository.check_token(token)
        user_repository.logout(username)
        return {"result": "user logged out"}
    except ValueError as error:
        return {"result": str(error)}, 400
    except Exception as err:
        return {"result": str(err)}, 500


@app.route('/statistics', methods=['GET'])
def get_statistics():
    try:
        token = request.headers.get('e_at_token')
        username = user_repository.check_token(token)
        return jsonify(stats_repository.find_for_user(username)), 200
    except ValueError as error:
        return {"result": str(error)}, 400
    except Exception as err:
        return {"result": str(err)}, 500


@app.route('/postImage', methods=['POST'])
def post_photo():
    try:
        token = request.headers.get('e_at_token')
        username = user_repository.check_token(token)
        if 'file' not in request.files:
            return {"result": "Photo expected"}, 400
        file = request.files['file']
        filepath = "image.jpg"
        file.save(filepath)
        file_img = cv2.imread(filepath)
        photo_processor.main_alg(username, file_img)
        os.remove(filepath)
        return {"result": "Success"}, 200

    except ValueError as error:
        return {"result": str(error)}, 400
    except Exception as err:
        traceback.print_tb(err)
        return {"result": str(err)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
