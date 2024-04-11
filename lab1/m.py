from Cryptodome.Cipher import AES
import binascii

mouths = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
def enumeration_birth():
    keys = []
    year = 1900
    for y in range(1900, 2100, 1):
        for mo in mouths:
            for da in days:
                tmp = str(y) + mo + da
                byte_string = tmp.encode('ascii')
                keys.append(byte_string)
    return keys
"""
第 1 级口令： b'd3d22dce5d5b23af59e5a0afcca548dd' 答案：b'2003091200000000'
第 2 级口令： b'9f411dee72ccfde17e73e66032c0c19c' 答案：b'zhu2003041400000'
第 3 级口令： b'a884fb6414102347f1ffc1e16126fcd4'
"""
def verify_First():
    msg = b'0000000000000000'
    cip = b'd3d22dce5d5b23af59e5a0afcca548dd'
    vks = enumeration_birth()
    for k in vks:
        zero_padding = 16 - len(k)
        k += '0'.encode('ascii') * zero_padding
        aes = AES.new(k, AES.MODE_ECB)
        encrypted_text = aes.encrypt(msg)
        cipher = binascii.b2a_hex(encrypted_text)
        if cip == cipher:
            print("Passed")
            print(k)
            break
        else:
            print("Failed")


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

def add_hundred_name_front_birth():
    hundred_name_with_birth = []
    # 读取文件内容
    with open("baijia.txt", "r") as file:
        file_content = file.read()
    hundred_name = file_content.split(" ")
    vks = enumeration_birth()
    for name in hundred_name:
        for k in vks:
            tmp = name.encode('ascii') + k
            hundred_name_with_birth.append(tmp)
    return hundred_name_with_birth



def verify_Second():
    name_front_birth = add_hundred_name_front_birth()
    msg = b'0000000000000000'
    cip = b'9f411dee72ccfde17e73e66032c0c19c'
    for k in name_front_birth:
        zero_padding = 16 - len(k)
        k += '0'.encode('ascii') * zero_padding
        aes = AES.new(k, AES.MODE_ECB)
        encrypted_text = aes.encrypt(msg)
        cipher = binascii.b2a_hex(encrypted_text)
        if cip == cipher:
            print("Passed")
            print(k)
            break
        else:
            print("Failed")

def generater_nums_combination():
    name_front_birth = add_hundred_name_front_birth()
    nums_com = []
    name_nums_combination = []
    for i in range(0, 99999999, 1):
        tmpi = str(i).encode('ascii')
        tmpi = '0'.encode('ascii') * (8 - len(tmpi)) + tmpi
        nums_com.append(tmpi)
    for name in name_front_birth:
        for num in nums_com:
            tmpn = name + num
            name_nums_combination.append(tmpn)
    return name_nums_combination


def verify_Third_paralle():
    msg = b'0000000000000000'
    cip = b'a884fb6414102347f1ffc1e16126fcd4'
    vks = generater_nums_combination()
    for k in vks:
        zero_padding = 16 - len(k)
        k += '0'.encode('ascii') * zero_padding
        aes = AES.new(k, AES.MODE_ECB)
        encrypted_text = aes.encrypt(msg)
        cipher = binascii.b2a_hex(encrypted_text)
        if cip == cipher:
            print("Passed")
            print(k)
            break
        else:
            print("Failed")

def verify_Third_serial():
    msg = b'0000000000000000'
    cip = b'a884fb6414102347f1ffc1e16126fcd4'
    vks = generate_hundred_name()
    for k in vks:
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
                break
            else:
                print("Failed : " + str(tmpk))



if __name__ == "__main__":
    # verify_First()
    # verify_Second()
    verify_Third_serial()


