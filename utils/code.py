from shortuuid import ShortUUID
import string

alphabet = string.ascii_uppercase
helper =  ShortUUID(alphabet=alphabet)

def code(length):
    return helper.random(length=length)

def code_6():
    return code(6)
