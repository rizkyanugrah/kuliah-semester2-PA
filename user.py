from platform import node
import time
from admin import lihat_penawaran
from database import koneksi
from termcolor import colored
from datetime import datetime
from helper import bersihkan_console, formatrupiah
from prettytable import PrettyTable
import auth
class Node:
    def __init__(self,data):
        self.data = data
        self.next = None


class linkedlist:
    def __init__(self) :
        self.head = None

    def daftar_barang(self):
        conn = koneksi()
        cursor = conn.cursor()

        try:
            sql = "SELECT * FROM  barang_lelang ORDER BY kode_barang DESC"
            cursor.execute(sql)
        except:
                print(colored('Data Tidak Ada / Kosong!','red'))
                time.sleep(2)
                return
        
        for data in cursor:
            node = Node(data)
            if self.head == None:
                self.head = node
            else:
                node.next = self.head
                self.head = node
    
        print(colored('[+] DAFTAR BARANG BRANDED [+]', 'green'))
        tables = PrettyTable(["KODE", "NAMA BARANG", "HARGA", "STATUS"])
        tables.align = "l"

        node = self.head
        while node != None:
            data_to_row = node.data[0],node.data[1],formatrupiah(node.data[2]),node.data[3]
            tables.add_row(data_to_row)
            node = node.next

        print(tables)        
        self.head = None


    def fibonanci_search(self,isi, x, n):
        fibonaci2 = 0 
        fibonaci1 = 1 
        fibonaci = fibonaci2 + fibonaci1 
        while (fibonaci < n):
            fibonaci2 = fibonaci1
            fibonaci1 = fibonaci
            fibonaci = fibonaci2 + fibonaci1
        offset = -1
        while (fibonaci > 1):
            i = min(offset+fibonaci2, n-1)
            if (isi[i] < x):
                fibonaci = fibonaci1
                fibonaci1 = fibonaci2
                fibonaci2 = fibonaci - fibonaci1
                offset = i
            elif (isi[i] > x):
                fibonaci = fibonaci2
                fibonaci1 = fibonaci1 - fibonaci2
                fibonaci2 = fibonaci - fibonaci1
            else:
                return i
        if(fibonaci1 and isi[n-1] == x):
            return n-1

    def search_barang(self):
        bersihkan_console()
        conn = koneksi()
        cursor = conn.cursor()

        try:
            # cursor.execute("SELECT nama_barang FROM barang_lelang ORDER BY barang_lelang.kode_barang ASC")
            cursor.execute("SELECT kode_barang FROM barang_lelang")
            records = cursor.fetchall()
        except:
                print(colored('Data Tidak Ada / Kosong!','yellow'))
                time.sleep(2)
                return

        self.daftar_barang()
        
        search = int(input('Masukan Barang Yang Ingin Di Cari : '))

        data_list =  []
        for i in range(len(records)):
            for j in range(len(records[i])):
                data_list.append(records[i][j])

        data_list.sort()
        print(data_list)
        result = self.fibonanci_search(data_list,search,len(data_list))
        print(result)
        input('...')


# l = linkedlist()
# l.search_barang()

queue = []
index = -1
def tambah_ke_queue(data):
    global queue
    global index

    index =+ 1
    queue += [data]
    
def hapus_queue():
    global queue
    global index

    del(queue[0])
    index =- 1

def proses_nawar():
    conn = koneksi()
    cursor = conn.cursor()
    try:
        kode_barang = input("\nMasukkan kode barang yang ingin ditawar : ")
    except :
            print(colored('BARANG NOT FOUND !','red'))
            time.sleep(2)
            return

    waktu_awal = cursor.execute("SELECT waktu_awal FROM proses_lelang WHERE barang_kode = %s ", (kode_barang,))
    waktu_awal = cursor.fetchone()

    waktu_awal = waktu_awal[0]
    now = datetime.now()

    current_time = now.strftime("%H:%M")
    # current_time = current_time.split(':')

    # waktu_awal_timedelta = now.strptime(str(waktu_awal), "%H:%M:%S")
    # jam = waktu_awal_timedelta.strptime(str(waktu_awal), "%H:%M:%S").strftime('%H')
    # menit = waktu_awal_timedelta.strptime(str(waktu_awal), "%H:%M:%S").strftime('%M')
    
    print(current_time)
    input('')

    cursor.execute("SELECT proses_lelang.id_proses, user.nama, proses_lelang.barang_kode, barang_lelang.nama_barang, proses_lelang.tawaran FROM proses_lelang INNER JOIN user ON proses_lelang.user_id = user.id_user INNER JOIN barang_lelang on proses_lelang.barang_kode = barang_lelang.kode_barang WHERE proses_lelang.barang_kode = %s", (kode_barang,))

    data = cursor.fetchone()
    if data:
        tawaran = input("Masukkan nominal penawaran : ")

        if int(tawaran) <= int(data[4]):
            print(colored('\nNominal tawaran harus lebih dari tawaran sebelumnya!', 'red'))
            time.sleep(3)
        else:
            is_sure = input(colored('\nApakah anda yakin? (y/n) : ', 'yellow'))

            if is_sure == 'y':
                # membuat queue
                tambah_ke_queue("UPDATE proses_lelang SET user_id = %s, tawaran = %s WHERE barang_kode = %s")

                # ambil data berdasarkan di qeueu
                cursor.execute(queue[0],(auth.data_user[0], int(tawaran), int(kode_barang)))

                conn.commit()

                # hapus data yang ada di queue
                hapus_queue()

                bersihkan_console()
                lihat_penawaran()

                print(colored("\nBerhasil melakukan penawaran!", 'green'))
                time.sleep(3)
            else:
                proses_nawar()
    else:
        print(colored('\nKode barang tidak ditemukan!', 'red'))

