from platform import node
import time
from database import koneksi
from termcolor import colored
from helper import formatrupiah
from prettytable import PrettyTable

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