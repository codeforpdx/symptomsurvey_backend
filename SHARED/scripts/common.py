import binascii
import hashlib

def make_hash(algorithm, iterations, key_length, password = None, salt = None):
    def hash_it_out(password, salt):
        dk = hashlib.pbkdf2_hmac(
            algorithm,
            bytes(password, 'utf-8'),
            bytes(salt, 'utf-8'),
            iterations,
            dklen=int(key_length)
        )
        return binascii.hexlify(dk)
    if password is None or salt is None:
        return hash_it_out
    else:
        return hash_it_out(password, salt)
    