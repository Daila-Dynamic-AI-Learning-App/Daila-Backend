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
    # get the details from the form
    study_level = request.form.get('studyLevel') or None
    topic_of_interest = request.form.get('topicOfInterest') or None
    study_year = request.form.get('studyYear') or None

    if not study_level and not topic_of_interest:
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

        prompt = getPrompt(start_question)
        return jsonify({ 'prompt': prompt[0] }), 200

    if request.method == 'PUT':
        # get answer from the body
        data = request.get_json()
        answer = data.get('answer')
        end = False

        if answer is None:
            abort(400)

        prompt = getPrompt(answer)

        if prompt[1]:
            obj = {"_id": ObjectId(studyId)}
            update = {'$set': { 'assessment': prompt[0], 'updated_at': datetime.now() }}
            study = database.findUpdateOne('study', obj, update)
            end = True
        return jsonify({ 'prompt': prompt[0], 'end': end }), 200

# @daila.route('/user/studies', methods=['GET'], strict_slashes=False)
# def listUserStudy():
#     """
#         Endpoint lists all assessment taken by
#         the user
#     """
#     # get all the assessments taken by the user
#     assessments = database.findAll('study', { 'userId': g.user_id })

#     # get all the objects in cursor object
#     assess_list = []
#     for ass in assessments:
#         ass['userId'] = str(ass.get('userId'))
#         assess_list.append(ass)

#     # return list of assessment for a user
#     return jsonify(assessments=assess_list), 200
