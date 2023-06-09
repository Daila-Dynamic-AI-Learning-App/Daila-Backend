from v1.views import daila
from flask import abort, jsonify, request, g
from engine import database
import keys
from bson import ObjectId
from utils.prompter import getPrompt
from datetime import datetime


@daila.route('/study', methods=['POST'], strict_slashes=False)
def studyDetails():
    """
        Gets the school details of user
    """
    # get the details from the json
    data = request.get_json()

    study_level = data.get('studyLevel')
    topic_of_interest = data.get('topicOfInterest')
    study_year = data.get('studyYear')

    if not study_level or not topic_of_interest or not study_year:
        # log this error message
        abort(400)

    # link present studyguide with the user
    study_dict = {
        "level": study_level,
        "interest": topic_of_interest,
        "year": study_year,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "assessment": "",
        "userId": g.user_id
    }

    # get the study obj after adding
    database.addOne('study', study_dict)
    study = database.findOne('study', study_dict)
    return jsonify({ 'studyId': str(study.get('_id')) }), 202


@daila.route('/question/<studyId>', methods=['GET', 'PUT'], strict_slashes=False)
def getFirstQuestion(studyId):
    """
        generates prompt from the details in study
    """
    if studyId is None:
        abort(400)

    if request.method == 'GET':
        # get the user object from db
        user = database.findOne('user', { '_id': ObjectId(g.user_id) })

        # get the study object from db
        study = database.findOne('study', { '_id': ObjectId(studyId) })

        study_level = study.get('level')
        study_interest = study.get('interest')
        study_year = study.get('year')
        country = user.get('country')

        start_question = keys.QUERY_STRING.format(study_year, study_level,
                                                study_interest, country)

        prompt = getPrompt(start_question, True)
        return jsonify({ 'prompt': prompt[0] }), 200

    if request.method == 'PUT':
        # get answer from the body
        data = request.get_json()
        answer = data.get('answer')
        end = False

        if answer is None:
            abort(400)

        prompt = getPrompt(answer, False)

        if prompt[1]:
            obj = {"_id": ObjectId(studyId)}
            update = {'$set': { 'assessment': prompt[0], 'updated_at': datetime.now() }}
            study = database.findUpdateOne('study', obj, update)
            end = True
        return jsonify({ 'prompt': prompt[0], 'end': end }), 200
