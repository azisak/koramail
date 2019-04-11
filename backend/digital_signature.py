import hashlib


def sign_message(message, ecc, point_basis, public_key):
    """Signing message
    Arguments:
        message {Bytes/String} -- message to be signed
    Return:
        {String} -- Signature
    """
    if (type(message) != bytes):
        message = bytes(message, "utf-8")

    # TODO: Using radiyya's SHA implementation to create signature
    signature = hashlib.sha1(message).hexdigest()

    signature = signature.encode('utf-8')
    signature = ecc.encrypt_message(signature, point_basis, public_key)
    return signature


def verified(message, signature, ecc, private_key):
    """Verifying message
    Arguments:
        message {Bytes/String}: message to be verified
        signature {String}: signature of signed message
    Return: 
        True - if message verified, else False
    """
    if (type(message) != bytes):
        message = bytes(message, "utf-8")

    # TODO: Using radiyya's SHA implementation to verify signature
    m_signature = hashlib.sha1(message).hexdigest()

    signature = ecc.decrypt_message(signature, private_key)
    signature = signature.decode('utf-8')
    return signature == m_signature
