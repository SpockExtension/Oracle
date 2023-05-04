import ecdsa
import hashlib
from flask import Flask, jsonify

def generate_key_pair():
    """Generate an ECDSA (SECP256k1) key pair."""
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return sk.to_string().hex(), vk.to_string().hex()

def sign_message(private_key_hex, message):
    """Sign a message with an ECDSA (SECP256k1) private key."""
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    signature = sk.sign(message.encode('utf-8'))
    return signature.hex()

def validate_signature(public_key_hex, username, signature_hex):
    """Validate an ECDSA (SECP256k1) signature with a public key."""
    nonces = read_nonce()
    for i in range(len(nonces)):
        message = f"{username}:{nonces[i]}"
        signature = bytes.fromhex(signature_hex)
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1)
        try:
            vk.verify(signature, message.encode('utf-8'))
            return True
        except ecdsa.BadSignatureError:
            pass
    return False

def read_nonce():
    with open('nonce.txt', 'r') as f:
        nonce = f.read().strip().split('\n')[-1]
    return nonce


app = Flask(__name__)

@app.route('/keygen')
def keygen():
    private_key_hex, public_key_hex = generate_key_pair()
    return jsonify({'privateKey': private_key_hex, 'publicKey': public_key_hex})

@app.route('/sign/<private_key_hex>/<message>')
def sign(private_key_hex, message):
    signature_hex = sign_message(private_key_hex, message)
    return jsonify({'signature': signature_hex})

@app.route('/verify/<public_key_hex>/<username>/<signature_hex>')
def verify(public_key_hex, username, signature_hex):
    isValid = validate_signature(public_key_hex, username, signature_hex)
    return jsonify({'isValid': isValid})

if __name__ == '__main__':
    app.run(port=5555)