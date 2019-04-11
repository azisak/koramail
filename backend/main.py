from flask import Flask, request, jsonify
from digital_signature import *
from ecc.curve import ECC
from ecc.point import Point
from ecc.utils import *
from ecc.koblitz import *

import sys
import os
import json
import hashlib

app = Flask(__name__)

# Reading config
with open('config.json') as config_file:
    config = json.load(config_file)
    config_file.close()

# ECC Elgamal initialization
ecc = ECC(
    config['ecc']['a'],
    config['ecc']['b'],
    config['ecc']['p'],
    config['ecc']['k'],
    config['ecc']['n']
)

# Generate base point
point_basis = ecc.create_basis_point()
print("Basis:", point_basis, "is_on_curve:", ecc.is_on_curve(point_basis))

# Generating public and private keys
generate_keys("sender", ecc, point_basis, config['ecc']['n'])

# Reading public and private keys
private_key = read_private_key("keys/sender.pri")
public_key = read_public_key("keys/sender.pub")


@app.route('/api/sign', methods=['POST'])
def sign():
    """Give signature to a message
    Returns:
      signature 
    """
    message = request.form['message']
    signature = sign_message(message, ecc, point_basis, public_key)

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
    message = request.form['message']
    signature = request.form['signature']
    err_msg = ""
    try:
        isVerified = verified(message, signature, ecc, private_key)
    except Exception as err:
        err_msg = "Error happened during verifying"
        isVerified = False

    response = {
        'verified': isVerified,
        'message': err_msg
    }
    return jsonify(response)
