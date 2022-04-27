import time
from database import koneksi
from termcolor import colored
from prettytable import PrettyTable

def lihat_penawaran():
    conn = koneksi()
    cursor = conn.cursor()

    print(colored('[+] DAFTAR PENAWARAN [+]', 'green'))
    try:
        sql = "SELECT proses_lelang.id_proses, user.nama, barang_lelang.nama_barang, proses_lelang.tawaran FROM proses_lelang INNER JOIN user ON proses_lelang.id_proses = user.id_user INNER JOIN barang_lelang on proses_lelang.barang_kode = barang_lelang.kode_barang"
        cursor.execute(sql)
    except:
            print(colored('Data Tidak Ada / Kosong!','yellow'))
            time.sleep(2)
            return


    tables = PrettyTable(["ID", "NAMA PENAWAR", "NAMA BARANG", "TAWARAN"])
    for data in cursor:
        tables.add_row(data)

    print(tables)

    return

def tambah():
    try:
        conn = koneksi()
        cursor = conn.cursor()

        try:
            code = int(input("\nMasukkan Kode : ")) 
        except ValueError:
                print(colored("KODE Harus Angka", 'red'))
                time.sleep(2)
                return

        code_item = cursor.execute('SELECT * FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (code,))
        code_item = cursor.fetchall()

        if len(code_item) > 0 :
            print(colored("\nKode Telah Di Pakai!", 'red'))
            time.sleep(2)
            return
        else:
            name_item = input("\nNama Barang : ")
            try:  
                price_item = int(input("Harga Barang : "))
            except ValueError:
                print(colored("\nMasukan Harga Dengan Benar", 'red'))
                time.sleep(2)
                return
            # status = input("Status Barang : ").upper()
            status = 'READY'


        val = (code, name_item, price_item, status)

        sql = "INSERT INTO barang_lelang (kode_barang, nama_barang, harga, status) VALUES (%s, %s, %s, %s)"

        cursor.execute(sql, val)

        conn.commit()


    except ValueError:
            print(colored("Masukan Data Dengan Sesuai", 'red'))
            time.sleep(2)
            return

def ubah():
    conn = koneksi()
    cursor = conn.cursor()

    try:
        code = int(input("\nPilih Data Dengan Kode : ")) 
    except ValueError:
        print(colored("Masukan KODE dengan benar!", 'red'))
        time.sleep(2)
        return

    code_item = cursor.execute('SELECT * FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (code,))
    code_item = cursor.fetchall()

    if len(code_item) > 0 :
        index = code_item[0]
        print(colored('Note: Ketik Enter jika data tidak ingin diubah', 'yellow'))
        try:
            new_code_item = int(input("\nMasukkan Kode : ") or index[0] )
        except ValueError:
            print(colored("Masukan Kode Yang Sesuai", 'red'))
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
    else:
        print(colored('Data Not Found!', 'red'))
        time.sleep(2)
        return 

    sql = "UPDATE barang_lelang SET kode_barang=%s, nama_barang=%s, harga=%s, status=%s WHERE kode_barang=%s"

    val = (new_code_item, new_name_item, new_price_item, new_status, code)

    cursor.execute(sql, val)

    conn.commit()


def hapus():
    conn = koneksi()
    cursor = conn.cursor()

    try:
        code = int(input("\nPilih data dengan kode : "))
    except ValueError:
        print(colored("Masukan Kode Yang Sesuai", 'red'))
        time.sleep(2)
        return

    code_item = cursor.execute('SELECT * FROM barang_lelang WHERE kode_barang = %s LIMIT 1;', (code,))
    code_item = cursor.fetchall()

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
    

# def transaksi():
#     # self.showAll()
#         try:
#             code = int(input("\nPilih data dengan kode : "))
#         except ValueError:
#             print(colored("Masukan Kode Yang Sesuai", 'red'))
#             time.sleep(2)
#             return

#         df = pandas.read_csv(self.BARANG_BRANDED, index_col=False)

#         selectedData = df.loc[df['KODE'] == code]

#         if selectedData.empty:
#             print(colored('Barang tidak ditemukan!', 'red'))
#             time.sleep(2)

#             return
#         elif selectedData.values[0][3] == 'SOLD':
#             print(colored('Mohon Maaf Barang Telah Terjual!', 'red'))
#             time.sleep(2)

#             return

#         code = selectedData.values[0][0]
#         name = selectedData.values[0][1]
#         price = selectedData.values[0][2]
#         status = selectedData.values[0][3]

#         print(f'\Barang dengan KODE {code} tersedia.\n')

#         print(tabulate({'KODE': [code],
#                         'NAMA': [name],
#                         'HARGA': [price],
#                         'STATUS': [status],
#                         }, headers='keys'))

#         coloredName = colored(name, 'cyan')
#         coloredPrice = colored(price, 'green')
        
#         print(f'\nHarga dari {coloredName} adalah {coloredPrice}.')
        
#         priceWithOutRP = self.slice(price)
        
#         summary = priceWithOutRP * 1
#         summaryRP = self.formatrupiah(summary)
#         summary = colored(summaryRP,'green')

#         print(f'\nTotal = {price} x {1} = {summary}')

#         print(f'Total pembayaran adalah : {summary}')

#         customer_name = input('\nMasukkan nama pembeli : ')
#         if customer_name.isalpha() == False:
#             print(colored("Nama Hanya Boleh HURUF!", 'red'))
#             time.sleep(2)
#             return

#         paid = input('\nApakah sudah selesai membayar (Y/N) : ').lower()

#         if paid == 'n':
#             print(colored('Pembayaran tidak dilanjutkan!', 'red'))
#             time.sleep(2)

#             return
#         elif paid == 'y':
#             # substraction the existing stock based on stock input
#             df.loc[df.KODE == code, 'STATUS'] = 'SOLD'

#             self.addToTransactionHistory(
#                 selectedData, customer_name, 1, summaryRP)

#             df.to_csv(self.BARANG_BRANDED, index=False)

#             print(colored('\nTerima kasih sudah membayar! ^^', 'green'))
#             time.sleep(2)

#             return
#         else:
#             print(colored("Konfirmasi Dengan Benar!", 'red'))
#             time.sleep(2)
#             return
 