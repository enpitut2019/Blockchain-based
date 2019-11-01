from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode
import sys
sys.dont_write_bytecode = True
import random
import socket
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



with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    # IPアドレスとポートを指定
    s.bind(('127.0.0.1', 40010))
    # 1 接続
    s.listen(1)
 
    # connection するまで待つ
    while True:
        
        # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
        conn, addr = s.accept()
        with conn:
            while True:
                s.setblocking(True)
                data = conn.recv(1024)
                if not data:
                    break
                if(data==b'\x00H'):
                    num=random.randint(10,10000)
                    strnum=str(num)
                    rand=num.to_bytes(2, 'big')
                    print(num)
                    print(rand)
                    conn.sendall(rand)
                elif(len(data)>790):
                    print(len(data))
                    print(data)
                    sig=data[0:344]
                    pub=data[344:800]
                    #dataにpub_keyまで渡されない時がある
                    print(sig)
                    print("¥n")
                    print(pub)
                    strnum+='=' * (-len(strnum) % 4)
                    print("here")
                
                    #　承認テスト（承認者が行う）
                    # はじめに生成したrandomNumを使って正しいかチェックする
                    if verify(pub, sig, strnum):
                        print("承認 OK")
                    else:
                        print("承認 NG")
                    # クライアントにデータを返す(b -> byte でないといけない)
                    conn.sendall(b'Received: ' + data)
                else:
                    print("fail to receive pub-key")
                    continue
                  
                 
              
