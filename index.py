import os
import sys
import bcrypt
import pwinput
import time
from termcolor import colored

from datetime import datetime
from helper import bersihkan_console, hash_password
from database import koneksi,buat_tabel
from auth import login, logout, register
from admin import lihat_penawaran,tambah,ubah,hapus
from user import linkedlist

def menu_admin() :
		bersihkan_console()

		print(colored("[=====================]", 'green'))
		print(colored('[+] Menu List Admin [+]', 'yellow'))
		print(colored("[=====================]", 'green'))
		print(colored('[1]', 'cyan'), 'Lihat Penawaran')
		print(colored('[2]', 'yellow'), 'Daftar Barang')
		print(colored('[3]', 'green'), 'Tambah Barang Lelang')
		print(colored('[4]', 'blue'), 'Ubah Barang Lelang')
		print(colored('[5]', 'red'), 'Hapus Barang Lelang ')
		print(colored('[6]', 'magenta'), 'Transaksi')
		print(colored('[7]', 'red'), 'Keluar')

		menu = input('\nPilih: ')

		return menu


def menu_user() :
		bersihkan_console()

		print(colored("[=====================]", 'green'))
		print(colored('[+]  Menu List User [+]', 'yellow'))
		print(colored("[=====================]", 'green'))
		print(colored('[1]', 'blue'), 'Tampilkan Daftar Barang')
		print(colored('[2]', 'green'), 'Searching Barang')
		print(colored('[3]', 'yellow'), 'Melakukan Penawaran')
		print(colored('[4]', 'red'), 'Keluar')

		menu = input('\nPilih: ')

		return menu


def app() :
	# buat_tabel(seed=True) uncomand jika baru pertama kali Menjalankan Program ini
	bersihkan_console()
	print(colored("[======================================================]", 'green'))
	print(colored("[+]     Silahkan login jika sudah punya akun         [+]", 'yellow'))
	print(colored("[+]  Silahkan register jika anda belum memiliki akun [+]", 'yellow'))
	print(colored("[======================================================]", 'green'))

	option = input("\n(Login/Register) : ").lower() 

	if option == 'login':

		l_user = linkedlist()
		role = login()
		bersihkan_console()
		terminate = False
		try:
			while terminate == False:
				if role == 'admin' :
					menu = menu_admin()
					if menu == '1' :
						bersihkan_console()
						lihat_penawaran()
						input(colored('Enter Untuk Kembali!', 'yellow'))

					elif menu == '2' :
						bersihkan_console()
						l_user.daftar_barang()
						input(colored('Enter Untuk Kembali!', 'yellow'))

					elif menu == '3' :
						bersihkan_console()
						l_user.daftar_barang()
						tambah()

					elif menu == '4' :
						bersihkan_console()
						l_user.daftar_barang()
						ubah()

					elif menu == '5' :
						bersihkan_console()
						l_user.daftar_barang()
						hapus()

					elif menu == '6' :
						print('transaksi')

					elif menu == '7':
						terminate = True
						return logout()

					else :
						print(colored("Masukan Menu Yang Sesuai",'red'))
						time.sleep(2)
						bersihkan_console()

				elif role == 'user' :
					menu = menu_user()
					if menu == '1' :
						bersihkan_console()
						l_user.daftar_barang()
						input(colored('Enter Untuk Kembali!', 'yellow'))

					elif menu == '2' :
						bersihkan_console()
						l_user.daftar_barang()
						l_user.search_barang()

					elif menu == '3' :
						print('Melakukan Penawaran')

					elif menu == '4' :
						terminate = True
						return logout()

					else :
						print(colored("Masukan Menu Yang Sesuai",'red'))
						time.sleep(2)
						bersihkan_console()
						
				else :
					print(colored("\nSampai Nanti !",'green'))
					time.sleep(2)
					return
		except KeyboardInterrupt:
			print(colored("\nSampai Nanti !",'green'))
	elif option == 'register':
		register()
	else:
		print(colored('\nMasukan inputan dengan benar!', 'red'))
		time.sleep(2)
		return app()

app()