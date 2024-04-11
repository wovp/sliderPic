import threading
from Cryptodome.Cipher import AES
import binascii

def generate_hundred_name():
    hundred_name_with_birth = []
    # 读取文件内容
    with open("baijia.txt", "r") as file:
        file_content = file.read()
    hundred_name = file_content.split(" ")
    ss = set()
    for s in hundred_name:
        ss.add(s)
    res_name = []
    for s in ss:
        res_name.append(s)
    return res_name

msg = b'0000000000000000'
cip = b'a884fb6414102347f1ffc1e16126fcd4'
vks = generate_hundred_name()
print(len(vks))
vks2 = vks[0: 25]
vks3 = vks[25:50]
vks4 = vks[50:75]
vks5 = vks[75:100]
vks6 = vks[100:125]
vks7 = vks[125:150]
vks8 = vks[150:175]
vks9 = vks[175:200]
vks10 = vks[200:225]
vks11 = vks[225:250]
vks12 = vks[250:]

begins = [0, 10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000]
end = [10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000, 99999999]

def verify_key(k):
    k = k.encode('ascii')
    for i in range(1800000, 99999999, 1):
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
for k in vks12:
    thread = threading.Thread(target=verify_key, args=(k,))
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()
