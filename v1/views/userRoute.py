from v1.views import daila
from flask import abort, jsonify, request, g
from engine import database
from bson import ObjectId


@daila.route('/user/studies', methods=['GET'], strict_slashes=False)
def listUserStudy():
    """
        Endpoint lists all assessment taken by
        the user
    """
    # get limit and page query paramters
    limit = request.args.get('limit') or 5
    page = request.args.get('page') or 0
    # get all the assessments taken by the user
    assessments = database.getFieldList('study', { '_id': g.user_id }, limit, page)

    # get all the objects in cursor object
    assess_list = []
    for ass in assessments:
        assess_list.append(ass)

    # return list of assessment for a user
    return jsonify(assessments=assess_list), 200
