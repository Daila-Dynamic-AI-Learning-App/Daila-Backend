from v1.views import daila
from flask import abort, jsonify, request, g
from engine import database, redis_client


@daila.route('/user/studies', methods=['GET'], strict_slashes=False)
def listUserStudy():
    """
        Endpoint lists all assessment taken by
        the user
    """
    # get limit and page query paramters
    limit = request.args.get('limit') or 5
    page = request.args.get('page') or 0

    # typecast to int if limit or page is present
    limit = int(limit)
    page = int(page)

    # get all the assessments taken by the user
    project = { '_id': 0, 'userId': 0 }
    assessments = database.getFieldList('study', { 'userId': g.user_id }, limit, page, project)

    # get all the objects in cursor object
    assess_list = []
    for ass in assessments:
        assess_list.append(ass)

    # return list of assessment for a user
    return jsonify(assessments=assess_list), 200

@daila.route('/user/me', methods=['GET', 'DELETE'], strict_slashes=False)
def getDelUsers():
    """
        Endpoint gets or delete the current user
        from the database
    """
    if request.method == 'GET':
        proj = { '_id': 0, 'hashed_password': 0 }
        user = database.getFieldList('user', { '_id': g.user_id }, 1, 0, proj)
        user_list = []
        for obj in user:
            user_list.append(obj)

        # check if user is present in db
        if not user_list:
            abort(403)
        return jsonify(user=user_list[0]), 200

    if request.method == 'DELETE':
        # first delete every relation to the user
        database.delMany('study', { 'userId': g.user_id })

        # then delete the user
        database.delMany('user', { '_id': g.user_id })
        # delete token from redis
        redis_client.delete(g.token)
        return jsonify(), 204
