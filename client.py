# import client-ram
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode
import sys
import socket

def generate_key(keysize=2048, passphrase = None):
    new_key = RSA.generate(keysize)
    public_key = new_key.publickey().exportKey()
    secret_key = new_key.exportKey(passphrase = passphrase)
    return secret_key, public_key


def sign(secret_key, data, passphrase = None):
    try:
        rsakey = RSA.importKey(secret_key, passphrase = passphrase)
    except ValueError as e:
        print(e)
        sys.exit(1)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(b64decode(data))
    # たまにbinascii.Error: Incorrect padding
    sign = signer.sign(digest)
    return b64encode(sign)



# 秘密鍵と公開鍵を作る。（パスワードはなくても良い）
password = "password"
sk, pk = generate_key(passphrase = password)

# ホストにsig/pk投げる
with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    s.setblocking(True)
    # サーバを指定
    s.connect(('127.0.0.1', 40010))

    s.send(b'\x00H')
    data = s.recv(1024) #bytes
    bdata = int.from_bytes(data, 'big') #int
    strdata=str(bdata)

    print(data)
    print(bdata)
    meesage="hoge"
    strdata += '=' * (-len(strdata) % 4)
    print(strdata)

    print("¥n")
    # print(type(meesage))
    # print(type(str(bdata)))

    # サーバにメッセージを送る
    sig = sign(sk, strdata, passphrase = password)
    s.send(sig)
    s.send(pk)
    s.close()
    
    
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    # data = s.recv(1024)
    # print(repr(data))
    
    

