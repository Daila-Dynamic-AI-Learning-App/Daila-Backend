from v1.views import daila
from flask import abort, jsonify, request, json
from validation.userValidation import validateEmail
from auth.authorize import AUTH

@daila.route('/register', methods=['POST'], strict_slashes=False)
def registerUser():
    """
        register users
    """
    # convert to mutable dict
    obj = dict(request.form)
    if not obj:
        abort(400)
    email = obj.get('email')
    country = obj.get('country')
    password = obj.get('password')

    if country is None or password is None:
        abort(400)

    if not validateEmail(email):
        abort(400)

    try:
        AUTH.registerUser(obj)
        return jsonify({ 'message': 'success' }), 202
    except ValueError:
        # user already exists
        abort(400)

@daila.route('/login', methods=['POST'], strict_slashes=False)
def loginUser():
    """
        login users and returns a token
        unique to each user
    """
    # to be safer, load data to json
    data = request.get_json()
    print(data)
    if not data:
        abort(400)

    email = data.get('email')
    if not validateEmail(email):
        abort(400)

    try:
        token = AUTH.loginUser(data)

        return jsonify(token=token), 200
    except ValueError:
        abort(400)

@daila.route('/logout', methods=['GET'], strict_slashes=False)
def logoutUser():
    """
        logout users
    """
    # custom header holds the token
    token = request.headers.get('X-Token')
    if not token:
        abort(400)

    try:
        AUTH.signOut(token)
        return '', 204
    except ValueError:
        # unauthorized to logout
        abort(401)
