import json
import time
from turtle import color
import pwinput
import bcrypt
import re
from termcolor import colored

from os import path, stat
from helper import bersihkan_console,hash_password
from database import koneksi

# Make a regular expression
# for validating an Email

# Define a function for
# for validating an Email

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check(email):

	if(re.fullmatch(regex, email)):
		return "Valid Email"

	else:
		return "Invalid Email"

def login() :
	try :
		bersihkan_console()

		print(colored("[=======================]", 'green'))
		print(colored("[+]      LOGIN        [+]", 'yellow'))
		print(colored("[=======================]", 'green'))


		email = input('\nEmail    : ')
		password = pwinput.pwinput(prompt='Password : ')
		
		conn = koneksi()
		cursor = conn.cursor()

		akun_users = cursor.execute('SELECT * FROM user WHERE email = %s LIMIT 1;', (email,))
		akun_users = cursor.fetchall()

		akun_admin = cursor.execute('SELECT * FROM admin WHERE email = %s LIMIT 1;', (email,))
		akun_admin = cursor.fetchall()

		cursor.close()

		print('\nLoading...')


		# cek akun_users ada
		if len(akun_users) > 0 :
			akun_users = akun_users[0]
			password_hash = akun_users[4]
			cek_password = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
			
			# cek password
			if cek_password :
				print(colored('\nSelamat Anda Berhasil Login ^^','green'))
				time.sleep(2)
				return 'user'
			
			print(colored('\nPassword salah', 'red'))
			time.sleep(2)
			login()

		#cek akun_admin ada
		elif len(akun_admin) > 0 :
			akun_admin = akun_admin[0]
			password_hash = akun_admin[4]
			cek_password = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
			
			# cek password
			if cek_password :
				print(colored('\nSelamat Anda Berhasil Login ^^','green'))
				time.sleep(2)
				return 'admin'
			
			print(colored('\nPassword salah', 'red'))
			time.sleep(2)
			login()

		else :
			return login(colored('\nAkun tidak ditemukan', 'red'))
	except KeyboardInterrupt :
		print()
		print (colored("\nTerima Kasih Telah Mencoba Aplikasi Lelang Kami ^^",'green'))
		exit()


def register() :
	try :
		bersihkan_console()
		conn = koneksi()
		cursor = conn.cursor()
		
		print(colored("[=======================]", 'green'))
		print(colored("[+]     REGISTER      [+]", 'yellow'))
		print(colored("[=======================]", 'green'))

		nama = input('\nMasukan Nama Anda       : ')
		email = input('Masukan Email Anda      : ')
		cek_email = check(email)

		if cek_email == 'Valid Email':
			email_user = cursor.execute('SELECT email FROM user WHERE email = %s LIMIT 1;', (email,))
			email_user = cursor.fetchall()

			if len(email_user) > 0 :
				print(colored('\nEmail Telah Di Pakai ^^','red'))
				time.sleep(2)
				register()
			else:
				no_hp = input('Masukan Nomor Hp Anda   : ')
				if no_hp.isnumeric():
					password = pwinput.pwinput(prompt='Masukan Password        : ')
					password = hash_password(password)
					val = (nama, email, no_hp, password)
					sql = "INSERT INTO user (id_user, nama, email, no_hp, password) VALUES (null,%s, %s, %s, %s)"
					cursor.execute(sql,val)
					conn.commit()
				else:
					print(colored('\nNOMOR HP HARUS ANGKA !','red'))
					time.sleep(2)
					register()
				

			bersihkan_console()

			print(colored("[=============================================]", 'green'))
			print(colored("[+]     SELAMAT ANDA BERHASIL REGISTER      [+]", 'yellow'))
			print(colored("[=============================================]", 'green'))
			time.sleep(3)
			cursor.close()
			return login()

		else:
			print(colored('INVALID EMAIL','red'))
			time.sleep(2)
			register()		

	except:
		print()
		print (colored("\nTerima Kasih Telah Mencoba Aplikasi Lelang Kami ^^",'green'))
		exit()

def logout() :
	print (colored("\nTerima Kasih Telah Mencoba Aplikasi Lelang Kami ^^",'green'))
	exit()
	









