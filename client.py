from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode
import sys


def generate_key(keysize=2048, passphrase = None):
    new_key = RSA.generate(keysize)
    public_key = new_key.publickey().exportKey()
    secret_key = new_key.exportKey(passphrase = passphrase)
    return secret_key, public_key


# 秘密鍵と公開鍵を作る。（パスワードはなくても良い）
password = "password"
sk, pk = generate_key(passphrase = password)

#クライアント(IoT機器は,自分のアドレス,公開鍵の情報を元にsign関数を使って署名する)

def sign(secret_key, data, passphrase = None):
    try:
        rsakey = RSA.importKey(secret_key, passphrase = passphrase)
    except ValueError as e:
        print(e)
        sys.exit(1)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(b64decode(data))
    sign = signer.sign(digest)
    return b64encode(sign)


message = "hoge"

# メッセージに署名する（署名者が行う）
sig = sign(sk, message, passphrase = password)

# ホストにsig/pk投げる

print(type(sig))
print(type(pk))
import socket
a=[pk,sig]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバを指定
    s.connect(('127.0.0.1', 50007))
    # サーバにメッセージを送る    
  
    s.send(sig)
    s.send(pk)
    
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = s.recv(1024)
    
    print(repr(data))





