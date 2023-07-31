from v1.views import daila
from flask import abort, jsonify, request, g
from engine import database
import keys
from bson import ObjectId
from utils.prompter import getPrompt
from datetime import datetime
from models.assessment import Assessment
from models.study import Study
from utils.prompter import getConversation, get_question_or_assessment


@daila.route('/study', methods=['POST'], strict_slashes=False)
def studyDetails():
    """
        Gets the school details of user
    """
    # get the details from the json
    data = request.get_json()

    # study_level = data.get('studyLevel')
    topic_of_interest = data.get('topicOfInterest')
    study_year = data.get('studyYear')

    if not topic_of_interest or not study_year:
        # log this error message
        abort(400)

    # link present studyguide with the user
    study_dict = {"interest": topic_of_interest,
                  "year": study_year, "assessment_id": None, "user_id": g.user_id}

    # create the study collection
    study = Study(**study_dict)

    # get the study obj after adding
    database.addOne('study', study.to_dict())
    study = database.findOne('study', {'user_id': g.user_id})
    return jsonify({'studyId': str(study.get('_id'))}), 202


@daila.route('/question/<studyId>', methods=['GET', 'PUT'], strict_slashes=False)
def getFirstQuestion(studyId):
    """
        generates prompt from the details in study
    """
    if studyId is None:
        abort(400)

    if request.method == 'GET':
        # get the user object from db
        user = database.findOne('user', {'_id': g.user_id})

        # get the study object from db
        study = database.findOne('study', {'_id': ObjectId(studyId)})

        # study_level = study.get('level')
        study_interest = study.get('interest')
        study_year = study.get('year')
        country = user.get('country')

        start_question = keys.QUERY_STRING.format(study_year, study_interest,
                                                  country, country)

        # prompt = getPrompt(start_question, True)
        # return jsonify({'prompt': prompt[0]}), 200

        # get the conversation
        convo = getConversation()

        # get the first question
        prompt = get_question_or_assessment(convo, start_question, False)
        return jsonify({'prompt': prompt[0]}), 200

    if request.method == 'PUT':
        # get answer from the body
        data = request.get_json()
        answer = data.get('answer')
        end = False

        if answer is None:
            abort(400)

        question = get_question_or_assessment(convo, answer, False)

        # if prompt[1] is true, then the assessment is complete
        if question[1]:
            obj = {"_id": ObjectId(studyId)}

            # create the assessment collection
            val_assessment = {"assessment": question[0],
                              "user_id": g.user_id}
            asssessment = Assessment(**val_assessment)

            # add the assessment to the database
            database.addOne('assessment', asssessment.toDict())

            # get the assessment object from db
            assessment = database.findOne('assessment', {'user_id': g.user_id})

            # update the study collection
            update = {
                '$set': {'assessment_id': assessment.get('_id'), 'updated_at': datetime.now()}}
            study = database.findUpdateOne('study', obj, update)
            end = True
        return jsonify({'prompt': question[0], 'end': end}), 200
