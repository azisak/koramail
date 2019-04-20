#!/usr/bin/python3
from flask import Flask, request, jsonify, g, Response
from digital_signature import *
from encrypt_body import *

import sys
import os
import json
import hashlib
import sqlite3
import glob
import ecdsa
import keccak


app = Flask(__name__)

# Reading config
with open('config.json') as config_file:
    config = json.load(config_file)
    config_file.close()


def generate_keys(key_name):
    sk = ecdsa.SigningKey.generate()
    private_key = sk.to_string().hex()
    public_key = sk.get_verifying_key().to_string().hex()
    for key_type, key in zip(["pub", "pri"], [public_key, private_key]):
        with open("./keys/{}.{}".format(key_name, key_type), "w") as f:
            f.write(key)
            f.close()


@app.route('/api/sign', methods=['POST'])
def sign():
    """Give signature to a message
    Returns:
      message, signature 
    """
    message = request.form['message']
    private_key = request.form['private_key']

    message_digest = keccak.SHA3_512(message.encode('utf-8'))

    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key))
    signature = sk.sign(message_digest).hex()

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
    public_key = request.form['public_key']
    signature = request.form['signature']

    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key))

    try:
        message_digest = keccak.SHA3_512(message.encode('utf-8'))
        isVerified = vk.verify(bytes.fromhex(signature), message_digest)
    except ecdsa.BadSignatureError:
        isVerified = False

    response = {
        'verified': isVerified,
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
        generate_keys(email)

    files = glob.glob('./keys/{}.*'.format(email))
    if (files[0].split('.')[-1] == "pub"):
        pub_path = files[0]
        pri_path = files[1]
    else:
        pub_path = files[1]
        pri_path = files[0]
    with open(pub_path, "r") as f_pub:
        pub_content = f_pub.read()
        f_pub.close()
    with open(pri_path, "r") as f_pri:
        pri_content = f_pri.read()
        f_pri.close()
    response = {
        'public_key': pub_content,
        'private_key': pri_content
    }

    return jsonify(response)


@app.route('/api/inbox/<email>', methods=['GET', 'POST', 'DELETE'])
def inbox(email):
    """# TODO: Create docstring for inbox endpoint
    """
    if request.method == 'GET':
        inboxes = query_db(
            "SELECT * FROM  mails WHERE receiver_mail = ?", [email])
        dict_list = [dict(zip(inbox.keys(), inbox)) for inbox in inboxes]
        return jsonify(dict_list)
    elif request.method == 'POST':
        subject = request.form['subject']
        sender_mail = request.form['sender_mail']
        content = request.form['content']
        receiver_mail = email
        insert_db('INSERT INTO mails (subject,sender_mail,receiver_mail,content) VALUES (?,?,?,?)',
                  (subject, sender_mail, receiver_mail, content))
        return Response("Successfully insert new inbox", status=200)
    elif request.method == 'DELETE':
        mail_id = request.form['mail_id']
        delete_row('DELETE FROM mails WHERE id = ?', [mail_id])
        return Response("Successfully deleted mail with id : {}".format(mail_id), 200)


@app.route('/api/sent_mail/<email>', methods=['GET', 'POST', 'DELETE'])
def sent_mail(email):
    """# TODO: Create docstring for sent_mail endpoint
    """
    if request.method == 'GET':
        inboxes = query_db(
            "SELECT * FROM  mails WHERE sender_mail = ?", [email])
        dict_list = [dict(zip(inbox.keys(), inbox)) for inbox in inboxes]
        return jsonify(dict_list)
    elif request.method == 'POST':
        subject = request.form['subject']
        sender_mail = email
        content = request.form['content']
        receiver_mail = request.form['receiver_mail']
        insert_db('INSERT INTO mails (subject,sender_mail,receiver_mail,content) VALUES (?,?,?,?)',
                  (subject, sender_mail, receiver_mail, content))
        return Response("Successfully insert new sent_mail", status=200)
    elif request.method == 'DELETE':
        mail_id = request.form['mail_id']
        delete_row('DELETE FROM mails WHERE id = ?', [mail_id])
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
