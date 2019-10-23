from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode
import sys


#hostがclientからのsignatureをverifyする
# (hostはclientからアドレス,公開鍵の情報を取得)
# (アドレスを使ってブロックチェーンから公開鍵を取得&チャレンジレスポンス検証)

def verify(pub_key, signature, data):
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(b64decode(data))
    if signer.verify(digest, b64decode(signature)):
        return True
    else:
        return False

#https通信でclientから署名情報をもらって↓に投げる


import socket

# AF = IPv4 という意味
# TCP/IP の場合は、SOCK_STREAM を使う
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # IPアドレスとポートを指定
    s.bind(('127.0.0.1', 50007))
    # 1 接続
    s.listen(1)
    # connection するまで待つ
    while True:
        # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
        conn, addr = s.accept()
        with conn:
            while True:
                # データを受け取る
                data = conn.recv(1024)
                if not data:
                    break
                # print('data : {}, addr: {}'.format(data, addr))
                sig=data[0:349]
                print(sig)
               
    
                # クライアントにデータを返す(b -> byte でないといけない)
                conn.sendall(b'Received: ' + data)



# #　承認テスト（承認者が行う）
# if verify(pk, sig, message):##
#     print("承認 OK")
# else:
#     print("承認 NG")

# #　メッセージの書き換えに対するテスト
# changed_message = "hogehoge"
# if verify(pk, sig, changed_message):
#     print("書き換えテスト NG")
# else:
#     print("書き換えテスト OK") # 承認されなければOK

# # 間違った秘密鍵の署名に対するテスト
# sk2, pk2 = generate_key(passphrase = password)
# sig2 = sign(sk2, message, passphrase = password)
# if verify(pk, sig2, message):
#     print("不正署名テスト NG")
# else:
#     print("不正署名テスト OK") # 承認されなければOK