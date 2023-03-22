from flask import Flask, jsonify
from flask_cors import CORS
from v1.views import daila

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.register_blueprint(daila)


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
