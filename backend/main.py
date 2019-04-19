#!/usr/bin/python3
from flask import Flask, request, jsonify, g, Response
from digital_signature import *
from encrypt_body import *
from ecc.curve import ECC
from ecc.point import Point
from ecc.utils import *
from ecc.koblitz import *

import sys
import os
import json
import hashlib
import sqlite3
import glob


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
        'error_msg': err_msg
    }
    return jsonify(response)

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    """Encrypt body message 
    Returns:
      encrypted message
    """
    message = request.form['message']
    key = request.form['key']
    encrypted = encrypt_message(message, key)

    response = {
        'encrypted': encrypted.hex()
    }

    return json.dumps(response)

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    """Get decrypted body message 
    Returns:
      decrypted message
    """
    a = request.form['message']
    message = bytes.fromhex(a)
    key = request.form['key']
    decrypted = decrypt_message(message, key)

    response = {
        'decrypted': decrypted
    }

    return json.dumps(response)

@app.route('/api/keys/<email>', methods=['GET'])
def getKeys(email):
    """Get public and private keys from username
    Returns:
      public and private key
    """
    files = glob.glob('./keys/{}.*'.format(email))
    # Generate keys if not exists
    if (len(files) == 0):
        generate_keys(email, ecc, point_basis, config['ecc']['n'])

    files = glob.glob('./keys/{}.*'.format(email))
    if (files[0].split('.')[-1] == "pub"):
        pub_path = files[0]
        pri_path = files[1]
    else:
        pub_path = files[1]
        pri_path = files[0]
    with open(pub_path,"r") as f_pub:
        pub_content = f_pub.read()
        f_pub.close()
    with open(pri_path,"r") as f_pri:
        pri_content = f_pri.read()
        f_pri.close()
    response = {
        'public_key': pub_content,
        'private_key': pri_content
    }

    return jsonify(response)



@app.route('/api/inbox/<email>',methods=['GET','POST','DELETE'])
def inbox(email):
    """# TODO: Create docstring for inbox endpoint
    """
    if request.method == 'GET':
        inboxes = query_db("SELECT * FROM  mails WHERE receiver_mail = ?",[email])
        dict_list = [dict(zip(inbox.keys(),inbox)) for inbox in inboxes]
        return jsonify(dict_list)
    elif request.method == 'POST':
        subject = request.form['subject']
        sender_mail = request.form['sender_mail']
        content = request.form['content']
        receiver_mail = email
        insert_db('INSERT INTO mails (subject,sender_mail,receiver_mail,content) VALUES (?,?,?,?)',(subject,sender_mail, receiver_mail, content))
        return Response("Successfully insert new inbox",status=200)
    elif request.method == 'DELETE':
        mail_id = request.form['mail_id']
        delete_row('DELETE FROM mails WHERE id = ?',[mail_id])
        return Response("Successfully deleted mail with id : {}".format(mail_id), 200)


@app.route('/api/sent_mail/<email>',methods=['GET','POST','DELETE'])
def sent_mail(email):
    """# TODO: Create docstring for sent_mail endpoint
    """
    if request.method == 'GET':
        inboxes = query_db("SELECT * FROM  mails WHERE sender_mail = ?",[email])
        dict_list = [dict(zip(inbox.keys(),inbox)) for inbox in inboxes]
        return jsonify(dict_list)
    elif request.method == 'POST':
        subject = request.form['subject']
        sender_mail = email
        content = request.form['content']
        receiver_mail = request.form['receiver_mail']
        insert_db('INSERT INTO mails (subject,sender_mail,receiver_mail,content) VALUES (?,?,?,?)',(subject,sender_mail, receiver_mail, content))
        return Response("Successfully insert new sent_mail",status=200)
    elif request.method == 'DELETE':
        mail_id = request.form['mail_id']
        delete_row('DELETE FROM mails WHERE id = ?',[mail_id])
        return Response("Successfully deleted mail with id : {}".format(mail_id), 200)

def insert_db(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()

def delete_row(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(config['db'])
        db.row_factory = sqlite3.Row
        g._database = db

    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
