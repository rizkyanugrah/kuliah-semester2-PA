# IMPORT MODULE DAN BEBERAPA FUNGSI DARI FILE LAIN
import time
from database import koneksi
from termcolor import colored
from helper import formatrupiah,hours_minute
from prettytable import PrettyTable

# FUNGSI UNTUK MELIHAT PENAWARAN
def lihat_penawaran():
    # koneksi ke database
    conn = koneksi()
    cursor = conn.cursor()

    print(colored('[+] DAFTAR PENAWARAN [+]', 'green'))
    try:
        # query mengambil beberapa column dari table
        sql = "SELECT proses_lelang.id_proses, user.nama, barang_lelang.kode_barang, barang_lelang.nama_barang, proses_lelang.tawaran, proses_lelang.waktu_awal, proses_lelang.waktu_akhir FROM proses_lelang LEFT JOIN user ON proses_lelang.user_id = user.id_user INNER JOIN barang_lelang on proses_lelang.barang_kode = barang_lelang.kode_barang"
        cursor.execute(sql)
    except:
            print(colored('Data Tidak Ada / Kosong!','yellow'))
            time.sleep(2)
            return

    # menggunakan prettytable agar tampilan menarik
    tables = PrettyTable(["ID", "NAMA PENAWAR", "KODE BARANG","NAMA BARANG", "TAWARAN", "WAKTU AWAL", "WAKTU AKHIR"])
    # perulangan untuk memasukan semua data yang telah di query di atas ke pretytable
    for data in cursor:
        data_fix = data[0],data[1],data[2],data[3],formatrupiah(data[4]),data[5],data[6]
        tables.add_row(data_fix)

    print(tables)

# FUNGSI UNTUK MENAMBAH BARANG
def tambah():
    try:
        # koneksi ke database
        conn = koneksi()
        cursor = conn.cursor()

        try:
            code = int(input("\nMasukkan Kode : ")) 
        except ValueError:
                print(colored("KODE Harus Angka", 'red'))
                time.sleep(2)
                return

        # query mengambil semua data barang berdasarkan kodebarang
        code_item = cursor.execute('SELECT * FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (code,))
        code_item = cursor.fetchall()

        # jika  barangnya ada maka tampilkan kodenya telah terpakai
        if len(code_item) > 0 :
            print(colored("\nKode Telah Di Pakai!", 'red'))
            time.sleep(2)
            return
        #jika tidak ada maka bisa menambah data barang branded yang baru
        else:
            name_item = input("\nNama Barang : ")
            try:  
                price_item = int(input("Harga Barang : "))
            except ValueError:
                print(colored("\nMasukan Harga Dengan Benar", 'red'))
                time.sleep(2)
                return
            status = 'READY'

        # query menambahkan data ke database
        val = (code, name_item, price_item, status)
        sql = "INSERT INTO barang_lelang (kode_barang, nama_barang, harga, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, val)
        conn.commit()

    except ValueError:
            print(colored("Masukan Data Dengan Sesuai", 'red'))
            time.sleep(2)
            return

# FUNGSI UNTUK MENGUBAH BARANG
def ubah():
    # koneksi ke database
    conn = koneksi()
    cursor = conn.cursor()

    try:
        code = int(input("\nPilih Data Dengan Kode : ")) 
    except ValueError:
        print(colored("Masukan KODE dengan benar!", 'red'))
        time.sleep(2)
        return

    # query mengambil semua data barang berdasarkan kodebarang
    code_item = cursor.execute('SELECT * FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (code,))
    code_item = cursor.fetchall()

    # jika code_item lebih dari 0 atau yang berarti barangnya ada maka admin bisa merubah data barang
    if len(code_item) > 0 :
        index = code_item[0]
        print(colored('Note: Ketik Enter jika data tidak ingin diubah', 'yellow'))
        try:
            new_code_item = int(input("\nMasukkan Kode : ") or index[0] )
        except ValueError:
            print(colored("Masukan Kode Dengan Benar !", 'red'))
            time.sleep(2)
            return
        new_name_item = input("\nNama Barang : ") or index[1]
        try:
            new_price_item = int(input("Harga Barang : ") or index[2] )
        except ValueError:
            print(colored("Masukan Harga Dengan Angka Yang Benar", 'red'))
            time.sleep(2)
            return
        new_status = input("Status Barang : ").upper() or index[3]
    # jika salah maka tampilkan data tidak ada
    else:
        print(colored('Data Not Found!', 'red'))
        time.sleep(2)
        return 

    # query update barang 
    sql = "UPDATE barang_lelang SET kode_barang=%s, nama_barang=%s, harga=%s, status=%s WHERE kode_barang=%s"
    val = (new_code_item, new_name_item, new_price_item, new_status, code)
    cursor.execute(sql, val)
    conn.commit()

# FUNGSI UNTUK MENGHAPUS BARANG
def hapus():
    # koneksi ke database
    conn = koneksi()
    cursor = conn.cursor()

    try:
        code = int(input("\nPilih data dengan kode : "))
    except ValueError:
        print(colored("Masukan Kode Yang Sesuai", 'red'))
        time.sleep(2)
        return
    
    # query mengambil semua data barang berdasarkan kodebarang
    code_item = cursor.execute('SELECT * FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (code,))
    code_item = cursor.fetchall()

    # jika code itemnya lebih dari 0 atau yang berarti kode barangnya ada maka hapus barang
    if len(code_item) > 0 :
        sql = "DELETE FROM barang_lelang WHERE kode_barang=%s"
        val = (code,)
        cursor.execute(sql, val)
        conn.commit()

        print(colored('\nData berhasil di Hapus!', 'green'))
        time.sleep(2)
        return
    
    print(colored('Data tidak ditemukan!', 'red'))
    time.sleep(2)
    return

# FUNGSI UNTUK MELELANG BARANG
def tambah_ke_proses_lelang() :
    # koneksi ke database
    conn = koneksi()
    cursor = conn.cursor()

    try :
        kode_barang = int(input("\nMasukkan kode barang yang ingin di tambahkan ke proses lelang : "))
    except :
            print(colored('\nMASUKAN KODE BARANG DENGAN BENAR !','red'))
            time.sleep(2)
            return

    # query buat mengambil semua data barang berdasarkan kode barang
    code_item = cursor.execute('SELECT * FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (kode_barang,))
    code_item = cursor.fetchall()

    #cek apakah barangnya ada
    if len(code_item) > 0 :
        # query buat ambil semua data proses lelang berdasarkan kode  barang
        proses_lelang = cursor.execute('SELECT * FROM proses_lelang WHERE barang_kode = %s LIMIT 1;', (kode_barang,))
        proses_lelang = cursor.fetchall()

        # ceka apakah barangnya ada di proses lelang
        if len(proses_lelang) > 0 :
            print(colored("\nBARANG TELAH ADA DI PROSES LELANG !", 'red'))
            time.sleep(3)
            return
        else:
            try :
                print(colored("\nMasukan waktu start awal barang yang ingin di lelang",'yellow'))
                hour_awal     = int(input('Masukan jam Awal : '))
                minute_awal   = int(input('Masukan menit Awal : '))
                waktu_awal    = hour_awal + minute_awal

                print(colored("\nMasukan batas waktu terakhir barang yang dapat di lelang",'yellow'))
                hour_akhir     = int(input('Masukan jam Akhir : '))
                minute_akhir   = int(input('Masukan menit Akhir : '))
                waktu_akhir    = hour_akhir + minute_akhir

                # cek apakah waktu awal sama dengan waktu akhir
                if waktu_awal == waktu_akhir :
                    print(colored('\nWAKTU AWAL DAN AKHIR TIDAK BOLEH SAMA !','red'))
                    time.sleep(3)
                    return

            except :
                print(colored('\nMASUKAN WAKTU DENGAN BENAR !','red'))
                time.sleep(3)
                return

            # query buat mengambil data harga di tabel barang lelang
            tawaran = cursor.execute('SELECT harga FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (kode_barang,))
            tawaran = cursor.fetchone()
            status = 'PROSES'

            # query buat menambahkan ke database semua yang inputan tadi
            val = (kode_barang, tawaran[0], hours_minute(hour_awal,minute_awal), hours_minute(hour_akhir,minute_akhir), status)
            sql = "INSERT INTO proses_lelang (id_proses, barang_kode, user_id, tawaran, waktu_awal, waktu_akhir, status) VALUES (null, %s, null, %s, %s, %s, %s)"
            cursor.execute(sql, val)
            conn.commit()

            print(colored('\nBarang berhasil di tambahkan ke proses lelang!', 'green'))
            time.sleep(3)
            return

    else:
        print(colored("\nBARANG NOT FOUND !", 'red'))
        time.sleep(2)
        return

