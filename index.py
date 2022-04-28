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
from user import linkedlist,proses_nawar

def menu_admin() :
		bersihkan_console()

		print(colored("[=====================]", 'green'))
		print(colored('[+] Menu List Admin [+]', 'yellow'))
		print(colored("[=====================]", 'green'))
		print(colored('[1]', 'cyan'), 'Lihat Penawaran')
		print(colored('[2]', 'yellow'), 'Daftar Barang')
		print(colored('[3]', 'magenta'), 'Tambah Barang Lelang')
		print(colored('[4]', 'blue'), 'Ubah Barang Lelang')
		print(colored('[5]', 'red'), 'Hapus Barang Lelang ')
		print(colored('[6]', 'green'), 'Transaksi')
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
	try:
		# buat_tabel(seed=True) uncomand jika baru pertama kali Menjalankan Program ini
		bersihkan_console()
		print(colored("[======================================================]", 'green'))
		print(colored("[+]     Silahkan login jika sudah punya akun         [+]", 'yellow'))
		print(colored("[+]  Silahkan register jika anda belum memiliki akun [+]", 'yellow'))
		print(colored("[======================================================]", 'green'))

		option = input("\n(Login/Register) : ").lower()
	except KeyboardInterrupt:
		print()
		print(colored("\nSampai Nanti !",'green'))
		exit()

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
						bersihkan_console()
						lihat_penawaran()
						print(colored('[1]', 'green'), 'Proses Menawar')
						print(colored('[2]', 'red'), 'Kembali')

						menu = input('\nPilih : ')

						if menu == '1':
							proses_nawar()
						elif menu == '2':
							menu_user()

					elif menu == '4' :
						terminate = True
						return logout()

					else :
						print(colored("Masukan Menu Yang Sesuai",'red'))
						time.sleep(2)
						bersihkan_console()
		except KeyboardInterrupt:
			print()
			print(colored("\nSampai Nanti !",'green'))
			exit()
	elif option == 'register':
		register()
	else:
		print(colored('\nMasukan inputan dengan benar!', 'red'))
		time.sleep(2)
		app()
app()