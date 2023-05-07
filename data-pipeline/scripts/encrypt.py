import base64
from cryptography.fernet import Fernet
key = Fernet.generate_key()
#key = "18c1773dc57ba96eef6774e1253ae3d976f4fbdd020d23d83d19e20e390fc571c9a5affe01a34f1b6a46ede531c8831c2b8a72a034c639ecc7fa0c83b868c0e6200d9e4b30bf2a020f8e006bfa9baf5ad03acb20906a93a193038398f7173a0b2b51996079ef529efdcca105c9cfda7f06a41fbd921bae35dcdfb5cb8e03892b4370bf25ad1e6fd00ce8a7ae39fb975372d8a318ccfaad5a8ad348b1ac0408ded83e2e29d783d41e74e21a2ae32879ed127bb60510b55519b0962160556c0ee51f1907371fb6963bb85eb11669dfe1ebde6bf4d81d520effaccb76c0afd4ceeba3e21fd14b080ce05acb72e830c961bfe1a94a19e00c39a708207e75d62e1efa"


f = Fernet(key)
#key = base64.b64decode(key)
url_safe_key = base64.urlsafe_b64encode(key).decode('utf-8')

token = f.encrypt(b"my deep dark secret")
token
url_safe_token = base64.urlsafe_b64encode(token).decode('utf-8')

print(f"key length: {len(key)}")
print(f"key: {key}")
print(f"cyphertest: {token}")

f.decrypt(token)
b'my deep dark secret'