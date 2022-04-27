import os
import sys
import bcrypt

def bersihkan_console() :
	os.system('clear' if sys.platform == 'linux' else 'cls')

def hash_password(password) :
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3 :
        return 'Rp ' + y     
    else :
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + '.' + p