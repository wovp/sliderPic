import threading
from Cryptodome.Cipher import AES
import binascii

from lab1.m import generate_hundred_name

msg = b'0000000000000000'
cip = b'a884fb6414102347f1ffc1e16126fcd4'
vks = generate_hundred_name()
print(len(vks))
vks2 = vks[0: 100]
vks3 = vks[100:200]
vks4 = vks[200:300]
vks5 = vks[300:400]
vks6 = vks[400:]

def verify_key(k):
    k = k.encode('ascii')
    for i in range(0, 99999999, 1):
        tmpi = str(i).encode('ascii')
        tmpi = '0'.encode('ascii') * (8 - len(tmpi)) + tmpi
        tmpk = k
        tmpk += tmpi
        zero_padding = 16 - len(tmpk)
        tmpk += '0'.encode('ascii') * zero_padding
        aes = AES.new(tmpk, AES.MODE_ECB)
        encrypted_text = aes.encrypt(msg)
        cipher = binascii.b2a_hex(encrypted_text)
        if cip == cipher:
            print("Passed")
            print(tmpk)
            with open("anssss.txt", "a") as file:  # 使用追加模式打开文件
                file.write("Passed\n")
                file.write(tmpk.decode('ascii') + "\n")  # 将密钥写入文件

            break
        else:
            if i % 100000 == 0:
                print("Failed : " + str(tmpk))


# 创建一个线程列表
threads = []

# 启动一个线程来处理每个密钥
for k in vks5:
    thread = threading.Thread(target=verify_key, args=(k,))
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()
