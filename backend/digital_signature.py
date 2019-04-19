import hashlib
import keccak


def sign_message(message, ecc, point_basis, public_key):
    """Signing message
    Arguments:
        message {Bytes/String} -- message to be signed
    Return:
        {String} -- Signature
    """
    if (type(message) != bytes):
        message = bytes(message, "utf-8")

    signature = keccak.SHA3_512(message)
    
    if (type(signature) == bytearray):
        signature = signature.hex()

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

    m_signature = keccak.SHA3_512(message)

    if (type(m_signature) == bytearray):
        m_signature = m_signature.hex()

    signature = ecc.decrypt_message(signature, private_key)
    signature = signature.decode('utf-8')
    return signature == m_signature
