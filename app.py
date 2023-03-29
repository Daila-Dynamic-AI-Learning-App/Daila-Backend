from flask import Flask, jsonify, request, abort, g
from flask_cors import CORS
from v1.views import daila
from auth.tokenAuth import TokenAuth
import keys

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.register_blueprint(daila)


@app.before_request
def require_token():
    """
        Authenticate user
    """
    # endpoints to check for authorization
    if request.path not in keys.EXEMPTED_LIST:
        token = request.headers.get('X-Token')
        if not token:
            abort(400)

        try:
            # get user's id and set to globals
            g.user_id  = TokenAuth.checkToken(token)
        except ValueError:
            # not authorized
            abort(401)

@app.errorhandler(400)
def badRequest(error):
    """
        handles error for status code 400
    """
    message = 'Bad Request'
    return jsonify(error=message), 400

@app.errorhandler(401)
def unauthorized(error):
    """
        handles error for status code 401
    """
    message = 'Unauthorized'
    return jsonify(error=message), 401

@app.errorhandler(403)
def forbidden(error):
    """
        handles error for status code 403
    """
    message = 'Forbidden'
    return jsonify(error=message), 403

@app.errorhandler(404)
def forbidden(error):
    """
        handles error for status code 404
    """
    message = 'Not Found'
    return jsonify(error=message), 403

if __name__ == '__main__':
    app.run('0.0.0.0', 5001)
