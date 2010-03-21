import base64

def encode( istring ):
    b64s = base64.urlsafe_b64encode(istring)
    b64s = b64s.replace("=","!")
    return b64s

def decode( istring ):
    istring = istring.replace("!","=")
    b64s = base64.urlsafe_b64decode(istring)
    return b64s

if __name__ == "__main__":
    encodedone = encode("some string with")
    print encodedone
    decodedone = decode(encodedone)
    print decodedone
