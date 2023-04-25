
import hashlib

hashLength = 10
hashType = 'sha256'

def hash(row):
    stringedRow = '-'.join(map(str, row))
    encodedStr = stringedRow.encode()
    return hashlib.sha256(encodedStr).hexdigest()[:hashLength]
