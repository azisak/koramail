from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)


@app.route('/api/sign', methods=['POST'])
def sign():
    """Give signature to a message
    Returns:
      signature 
    """
    # TODO: implement with real signature scenario
    message = request.form['message']
    signature = hashlib.sha1(message.encode('utf-8')).hexdigest()
    response = {
        'message': message,
        'signature': signature
    }
    return jsonify(response)


@app.route('/api/verify', methods=['POST'])
def verify():
    """Verify message and it's signature 
    Returns:
      True if verified, else False
    """
    # TODO: implement with real signature scenario
    message = request.form['message']
    signature = request.form['signature']
    m_signature = hashlib.sha1(message.encode('utf-8')).hexdigest()

    isVerified = m_signature == signature
    response = {
        'verified': isVerified
    }
    return jsonify(response)
