# IMPORT MODULE
import mysql.connector
from termcolor import colored
from datetime import time

from helper import hash_password, bersihkan_console

# FUNGSII UNTUK KONEKSI KE DATABASE
def koneksi() :
	# sesuaikan dengan data anda
	host 		 = 'localhost'
	user 		 = 'root'
	password = ''
	database = 'pa_Lelang'

	try :
		# masukan informasi terkait database sesuai dengan punya anda
		conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
		if conn.is_connected() : return conn
			
	except Exception as error :
		bersihkan_console()

		if error : print(colored(f'Error:\n{error}.', 'red'))

		message = f"""
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bSebelum menjalankan aplikasi ini, nyalakan dulu mysql di XAMPP, lalu install {colored('mysql-connector', 'yellow')} menggunakan pip.
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b- - - - - - - - - - - - - - - -
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bpip install mysql-connector
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b- - - - - - - - - - - - - - - -

			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bBuat database dengan nama {colored(database, 'green')}."""

		print(message)

# FUNGSI UNTUK MEMBUAT TABLE
def buat_tabel(seed=False) :
	conn = koneksi()
	cursor = conn.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `user` (
			id_user int primary key auto_increment not null,
			nama varchar(100) not null,
			email varchar(100) not null,
			no_hp varchar(100) not null,
			password text not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `admin` (
			id_admin int primary key auto_increment not null,
			nama varchar(100) not null,
			email varchar(100) not null,
			no_hp varchar(100) not null,
			password text not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `barang_lelang` (
			kode_barang int primary key not null,
			nama_barang varchar(100) not null,
			harga int not null,
			status varchar(30) not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `proses_lelang` (
			id_proses int primary key auto_increment not null,
			barang_kode int(100) not null,
			user_id int,
			tawaran varchar(25) not null,
			waktu_awal time,
			waktu_akhir time,
			status varchar(30)
		);
	""")

	# QUERY UNTUK RELASI ANTAR TABLE
	cursor.execute('ALTER TABLE `proses_lelang` ADD FOREIGN KEY (`barang_kode`) REFERENCES `barang_lelang` (`kode_barang`);')
	cursor.execute('ALTER TABLE `proses_lelang` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id_user`);')

	# CEK JIKA SEED NYA ADA ATAU = TRUE MAKA LAKUKAN QUERY DI BAWAH UNTUK DUMMY DATA
	if seed :
		cursor.execute("""
			INSERT INTO user VALUES
			(null, %s, %s, %s, %s),
			(null, %s, %s, %s, %s),
			(null, %s, %s, %s, %s),
			(null, %s, %s, %s, %s);""",
			(
				'novil','novilreon@gmail.com', '081256546083', hash_password('12345'),
				'dapa','dapa_iyok@gmail.com', '083489100254', hash_password('12345'),
				'ibe','ibe_buana@gmail.com', '082155667791', hash_password('12345'),
				'user','user@gmail.com', '089432178345', hash_password('12345'),
			)
		)

		cursor.execute("""
			INSERT INTO admin VALUES
			(null, %s, %s, %s, %s),
			(null, %s, %s, %s, %s);""",
			(
				'rizky','rizky_anug@gmail.com', '085754612468', hash_password('admin'),
				'admin','admin@gmail.com', '085567281929', hash_password('admin'),
			)
		)

		cursor.execute("""
			INSERT INTO barang_lelang VALUES
			(%s, %s, %s, %s),
			(%s, %s, %s, %s),
			(%s, %s, %s, %s),
			(%s, %s, %s, %s),
			(%s, %s, %s, %s),
			(%s, %s, %s, %s),
			(%s, %s, %s, %s),
			(%s, %s, %s, %s),
			(%s, %s, %s, %s);""",
			(
				1920,'Jam Rolex','789000', 'READY',
				1921,'Jordan Shopee','435000', 'READY',
				1922,'Laptop Dell','12000000', 'READY',
				1923,'Jam Richard Mile','1000000', 'SOLD',
				1924,'Jam Titan','4000000', 'READY',
				1925,'Kaos Uniqlo','135000', 'READY',
				1926,'Kaos Ripcurl','110000', 'READY',
				1927,'Celana Gucci','93000', 'READY',
				1928,'Lamborgini','2000', 'READY',
			)
		)

		cursor.execute("""
			INSERT INTO proses_lelang VALUES
			(null, %s, %s, %s, %s, %s, %s);""",
			(
				1923,3,'1000000',time(20,00).strftime("%H:%M"),time(23,00).strftime("%H:%M"), 'PROSES',
			)
		)

		conn.commit()

	cursor.close()