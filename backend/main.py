#!/usr/bin/python3
from flask import Flask, request, jsonify, g, Response, send_from_directory
from encrypt_body import *

import sys
import os
import json
import hashlib
import sqlite3
import glob
import ecdsa
import keccak
import os

# Reading config
with open('config.json') as config_file:
    config = json.load(config_file)
    config_file.close()

if not os.path.exists(config['flask']['upload_path']):
        os.makedirs(config['flask']['upload_path'])

static_url_path = "/"+config['flask']['upload_path']
app = Flask(__name__, static_folder=config['flask']['upload_path'], static_url_path=static_url_path)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),config['flask']['upload_path'])


def generate_keys(key_name):
    if not os.path.exists('keys'):
        os.makedirs('keys')
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

    try:
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key))

        message_digest = keccak.SHA3_512(message.encode('utf-8'))
        isVerified = vk.verify(bytes.fromhex(signature), message_digest)
    except ecdsa.BadSignatureError:
        isVerified = False
    except Exception as err:
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
    if request.method == 'GET':
        inboxes = query_db(
            "SELECT * FROM  mails WHERE receiver_mail = ?", [email])
        dict_list = [dict(zip(inbox.keys(), inbox)) for inbox in inboxes]
        for dict_item in dict_list:
            dict_item['attachment_paths'] = dict_item['attachment_paths'].split(',') if dict_item['attachment_paths'] else []
        return jsonify(dict_list)
    elif request.method == 'POST':
        subject = request.form['subject']
        sender_mail = request.form['sender_mail']
        content = request.form['content']
        receiver_mail = email
        mail_id = insert_db('INSERT INTO mails (subject,sender_mail,receiver_mail,content) VALUES (?,?,?,?)',
                  (subject, sender_mail, receiver_mail, content))
        mail_id = str(mail_id)
        if 'file' in request.files:
            attachments = request.files.getlist('file')
            attachment_folder = os.path.join(app.config['UPLOAD_FOLDER'], mail_id)
            if not os.path.exists(attachment_folder):
                os.makedirs(attachment_folder)
            saved_paths = []
            for attachment in attachments:
                attachment.save(os.path.join(attachment_folder, attachment.filename))
                saved_path = "/{}/{}/{}".format(config['flask']['upload_path'],mail_id,attachment.filename)
                saved_paths.append(saved_path)
            insert_db('UPDATE MAILS  SET attachment_paths = ? WHERE ID = ?',(",".join(saved_paths), mail_id))
        response = {
            'status': "OK"
        }
        return jsonify(response)
    elif request.method == 'DELETE':
        mail_id = request.form['mail_id']
        delete_row('DELETE FROM mails WHERE id = ?', [mail_id])
        response = {
            'status': "OK"
        }
        return jsonify(response)



@app.route('/api/sent_mail/<email>', methods=['GET', 'POST', 'DELETE'])
def sent_mail(email):
    if request.method == 'GET':
        inboxes = query_db(
            "SELECT * FROM  mails WHERE sender_mail = ?", [email])
        dict_list = [dict(zip(inbox.keys(), inbox)) for inbox in inboxes]
        for dict_item in dict_list:
            dict_item['attachment_paths'] = dict_item['attachment_paths'].split(',') if dict_item['attachment_paths'] else []
        return jsonify(dict_list)
    elif request.method == 'POST':
        subject = request.form['subject']
        sender_mail = email
        content = request.form['content']
        receiver_mail = request.form['receiver_mail']
        mail_id = insert_db('INSERT INTO mails (subject,sender_mail,receiver_mail,content) VALUES (?,?,?,?)',
                  (subject, sender_mail, receiver_mail, content))
        mail_id = str(mail_id)
        if 'file' in request.files:
            attachments = request.files.getlist('file')
            attachment_folder = os.path.join(app.config['UPLOAD_FOLDER'], mail_id)
            if not os.path.exists(attachment_folder):
                os.makedirs(attachment_folder)
            saved_paths = []
            for attachment in attachments:
                attachment.save(os.path.join(attachment_folder, attachment.filename))
                saved_path = "/{}/{}/{}".format(config['flask']['upload_path'],mail_id,attachment.filename)
                saved_paths.append(saved_path)
            insert_db('UPDATE MAILS  SET attachment_paths = ? WHERE ID = ?',(",".join(saved_paths), mail_id))
        response = {
            'status': "OK"
        }
        return jsonify(response)
    elif request.method == 'DELETE':
        mail_id = request.form['mail_id']
        delete_row('DELETE FROM mails WHERE id = ?', [mail_id])
        response = {
            'status': "OK"
        }
        return jsonify(response)


def insert_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    return cur.lastrowid


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
