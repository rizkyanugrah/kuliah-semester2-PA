from platform import node
import time
from admin import lihat_penawaran
from database import koneksi
from termcolor import colored
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


#     def fibonanci_search(self,isi, x, n):
#         fibonaci2 = 0 
#         fibonaci1 = 1 
#         fibonaci = fibonaci2 + fibonaci1 
#         while (fibonaci < n):
#             fibonaci2 = fibonaci1
#             fibonaci1 = fibonaci
#             fibonaci = fibonaci2 + fibonaci1
#         offset = -1
#         while (fibonaci > 1):
#             i = min(offset+fibonaci2, n-1)
#             if (isi[i] < x):
#                 fibonaci = fibonaci1
#                 fibonaci1 = fibonaci2
#                 fibonaci2 = fibonaci - fibonaci1
#                 offset = i
#             elif (isi[i] > x):
#                 fibonaci = fibonaci2
#                 fibonaci1 = fibonaci1 - fibonaci2
#                 fibonaci2 = fibonaci - fibonaci1
#             else:
#                 return i
#         if(fibonaci1 and isi[n-1] == x):
#             return n-1


#     def search_barang(self):
#         conn = koneksi()
#         cursor = conn.cursor()
#         asdlist =  []

#         try:
#             sql = "SELECT kode_barang, nama_barang FROM barang_lelang"
#             cursor.execute(sql)
#             tes = cursor.fetchall()
#         except:
#                 print(colored('Data Tidak Ada / Kosong!','yellow'))
#                 time.sleep(2)
#                 return

#         self.daftar_barang()
        
#         search = input('Masukan Barang Yang Ingin Di Cari : ')

#         for i in range(len(tes)):
#             for j in range(len(tes[i])):
#                 asdlist.append(tes[i][j])
#         # asdlist.sort()
#         print(asdlist)
#         input('...')
#         # result = self.fibonanci_search(asdlist,search,len(asdlist))


# l = linkedlist()
# l.search_barang()

def proses_nawar():
    queue = []

    conn = koneksi()
    cursor = conn.cursor()

    kode_barang = input("\nMasukkan kode barang yang ingin ditawar : ")

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
                queue.append("UPDATE proses_lelang SET user_id = %s, tawaran = %s WHERE barang_kode = %s")

                # ambil data berdasarkan di qeueu
                cursor.execute(queue[0],(auth.data_user[0], int(tawaran), int(kode_barang)))

                conn.commit()

                # hapus data yang ada di queue
                queue.pop(0)
                
                bersihkan_console()
                lihat_penawaran()

                print(colored("\nBerhasil melakukan penawaran!", 'green'))
                time.sleep(3)
            else:
                proses_nawar()
    else:
        print(colored('\nKode barang tidak ditemukan!', 'red'))
