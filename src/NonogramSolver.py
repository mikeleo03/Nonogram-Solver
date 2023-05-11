# Implementasi program Nonogram Solver dengan Pendekatan Heuristik
# xx. Impor modul eksternal untuk membantu pemrosesan
from itertools import combinations
import numpy as np 
import csv
import time

# 0. Deklarasi variabel global
ROWS_VALUES = []
COLS_VALUES = []
    
# 1. Melakukan pencarian semua kemungkinan penyusunan yang mungkin terhadap konfigurasi tertentu
def arrangements(n_empty, groups, ones):
    # Menampung semua nilai kemungkinan penyusunan
    res_opts = []
    
    # Menggunakan combinations untuk mencoba semua kemungkinan pengisian kotak
    for p in combinations(range(groups + n_empty), groups):
        # Membuat senarai untuk mengisi posisi yang lain dengan "-1", penanda tidak akan diisi
        selected = [-1] * (groups + n_empty)
        # Melakukan pengecekan terhadap semua kombinasi yang terbentuk
        # Mencari indeks akan diletakannya nilai "1"
        ones_idx = 0
        for val in p:
            # Meletakkan kombinasi nilai "1" dan "0"
            selected[val] = ones_idx
            ones_idx += 1
        
        # Penentuan final kombinasi nilai
        res_opt = []
        for val in selected:
            # Kalau nilainya akan diisi, dibuat sebuah senarai solusi kemungkiann pengisiannya
            # berisi nilai ones ke val ditambah "-1" di ujung untuk memastikan tidak ada yang
            # berdekatan
            if val > -1:
                res_opt.append(ones[val]+[-1])
            # Jika tidak, maka blok tersebut memang tidak bisa diisi, tambahkan dengan list "-1"
            # untuk setiap posisi yang berkoresponden
            else:
                res_opt.append([-1])
                
        # Membuat kumpulan senarai solusi menjadi sebuah senarai opsi utuh
        opts = []
        for sublist in res_opt:
            for item in sublist:
                opts.append(item)
                
        # Memangkas nilai pada indeks terakhir karena tidak diperlukan dan memasukkannya
        # dalam senarai solusi penuh
        res_opts.append(opts[:-1])
    
    # Mengembalikan nilai semua kemungkinan penyusunan
    return res_opts

# 2. Melakukan penampungan semua solusi yang mungkin dari komponen tertentu (baris atau kolom)
def create_possibilities(values, no_of_other):
    # Menampung semua nilai kemungkinan yang akan dicobakan
    possibilities = []
    
    # Untuk setiap nilai dari nonogram yang dikirimkan
    for v in values:
        # Mengambil banyaknya grup yang terbentuk
        groups = len(v)
        # Jumlahnya blok kosong (komponen - jumlah values - grup + 1)
        no_empty = no_of_other - sum(v) - groups + 1
        # Mencetak karakter "1" sebanyak isi dari val sebagai matriks, penanda akan diisi
        ones = []
        for x in v:
            ones.append([1] * x)
        # Melakukan percobaan semua kemungkinan penyusunan dengan fungsi arrangements
        res = arrangements(no_empty, groups, ones)
        # Menambahkan semua kemungkinan hasil penyusunan pada senarai solusi
        possibilities.append(res)  
    
    # Mengembalikan semua senarai solusi yang memungkinkan
    return possibilities

# 3. Memilih indeks yang belum selesai sebagai prioritas dari baris dan kolom
def select_index_not_done(rows_done, cols_done, possibilities, row_ind):
    # Mendata yang memiliki banyaknya kemungkinna dari setiap penyusunan yang masuk
    s = []
    for i in possibilities:
        s.append(len(i))
        
    # Jika yang dianalisis merupakan baris, 
    if row_ind:
        # Jika terdapat baris yang belum selesai, maka akan diproses indeks pada baris tersebut
        selected = []
        # Melakukan enumerasi terhadap semua yang ada pada s
        for i, n in enumerate(s):
            if rows_done[i] == 0:
                selected.append((i, n, row_ind))  # dicatat baris, jumlah kemungkinan, kode
        # Mengembalikan daftar indeks baris yang belum selesai
        return selected
    # Tetap jika yang dianalisi merupakan kolom, maka melakukan hal yang sama
    else:
        # Jika terdapat kolom yang belum selesai, maka akan diproses indeks pada kolom tersebut
        selected = []
        # Melakukan enumerasi terhadap semua yang ada pada s
        for i, n in enumerate(s):
            if cols_done[i] == 0:
                selected.append((i, n, row_ind)) # dicatat kolom, jumlah kemungkinan, kode
        # Mengembalikan daftar indeks kolom yang belum selesai
        return selected

# 4. Mengambil indeks pemecahan yang hanya tinggal memiliki 1 kemungkinan saja
def get_only_one_option(values):
    # Inisiasi larik
    index = []
    for n, i in enumerate(np.array(values).T):
        # Mengambil hanya yang nilai uniknya tunggal
        if len(np.unique(i)) == 1:
            index.append((n, np.unique(i)[0]))
    
    # Mengembalikan solusi tunggal yang mungkin menyelesaikan
    return index

# 5. Menghapus kemungkinan jika baris atau kolom terakit sudah masuk dalam papan
def remove_possibilities(possibilities, i, val):
    # Inisiasi larik
    removed = []
    for p in possibilities:
        # Kalau masih memenuhi batasan, maka akan solusi akan lanjut diproses
        if p[i] == val:
            removed.append(p)
            
    # Isi dari removed adalah isi setelah dihapus
    return removed

# 6. Menampilkan isi papan ke terminal berdasarkan kondisi dan restriksi batasan
def display_board(board, rows, max_len_rows, matr_rows_out, cols, max_len_cols, matr_cols_out):
    # Mencetak bagian atas
    for p in range (max_len_cols + 1):
        # Bagian spasi di tepi kiri atas, pemisah angka baris dan kolom
        for q in range (max_len_rows + 1):
            print(" ", end = " ")
        # Mencetak bagian angka pada kolom tersebut secara bergantian
        for r in range (cols):
            # Jika berupa angka, maka cetak
            if (matr_cols_out[p][r] != 0):
                # Penaganan untuk elemen lebih dari 1 digit
                if (matr_cols_out[p][r] < 10):
                    print(matr_cols_out[p][r], end = " ")
                else:
                    print(matr_cols_out[p][r], end = "")
            # Jika tidak, maka cetak spasi
            else :
                print(" ", end = " ")
        print(" ") # pemisah antar baris kolom atas dengan penyetakan isi nonogram
    # Mencetak nonogram dan info di sebelah kirinya
    for i in range (rows) :
        # Mencetak informasi angka
        for k in range (max_len_rows + 1):
            # Jika berupa angka, maka cetak
            if (matr_rows_out[i][k] != 0):
                # Penaganan untuk elemen lebih dari 1 digit
                if (matr_rows_out[i][k] < 10):
                    print(matr_rows_out[i][k], end = " ")
                else:
                    print(matr_rows_out[i][k], end = "")
            # Jika tidak, maka cetak spasi
            else :
                print(" ", end = " ")
        # Mencetak isi nonogram yang sudah diselesaikan
        for j in range (cols):
            # Jika isi papan "-1", maka cetak petak kosong
            if (board[i][j] == -1) :
                print(" ", end = " ")
            # Jika isinya "1", maka cetak petak isi
            elif (board[i][j] == 1):
                print("█", end = "█")
            # Jika isinya "0" belum diselesaikan, isi dengan titik
            else :
                print(".", end = " ")
        # Bagian spasi bawah untuk menyelesaikan
        print(" ")
    print(" ") # spasi final jeda ke bawah

# 7. Prosedur untuk melakukan pembaharuan terhadap nilai pada rows_done dan cols_done
def update_done(board, rows_done, cols_done, row_ind, idx):
    # Mengecek baris atau kolom yang baru diubah nilainya
    if row_ind: 
        vals = board[idx]
    else: 
        vals = [row[idx] for row in board]
    # Jika sudah selesai (tidak ada lagi nilai 0), maka 
    if (0 not in vals):
        # Jika baris, perbaharui nilai rows_done
        if row_ind: 
            rows_done[idx] = 1
        # Jika kolom, perbaharui nilai cols_done
        else: 
            cols_done[idx] = 1 

# 8. Mengecek apakah baris dan kolom terkait sudah selesai, tergantung flag row_ind
def check_done(rows_done, cols_done, row_ind, idx):
    if row_ind : 
        return rows_done[idx]
    else: 
        return cols_done[idx]

# 9. Mengecek apakah nonogram sudah diselesaikan
def check_solved(rows_done, cols_done):
    if (0 not in rows_done) and (0 not in cols_done):
        return True

# 10. Melakukan pembacaan data masukan nonogram dari file
def read_file():
    global ROWS_VALUES, COLS_VALUES
    valid = False
    while (not valid):
        print("=============   PEMILIHAN FILE   =============")
        folder = input("Masukkan nama file yang akan dianalisis\n>> ")
        print("\n=============   PEMBACAAN DATA   =============")
        print("Sedang membaca data...")
        try:
            f = open(folder, "r")
        except:
            print("File tidak ditemukan!\n")
            exit()
        
        n_row = int(input("Masukkan jumlah baris : "))
        n_col = int(input("Masukkan jumlah kolom : "))
        
        data_baris = csv.reader(f)
        count = 0
        for row in data_baris:
            if (count < n_row):
                for i in range(len(row)):
                    row[i] = float(row[i])
                    if row[i] % 1.0 == 0:
                        row[i] = int(row[i])
                ROWS_VALUES.append(row)
                count += 1
            else :
                for i in range(len(row)):
                    row[i] = float(row[i])
                    if row[i] % 1.0 == 0:
                        row[i] = int(row[i])
                COLS_VALUES.append(row)
                count += 1
        
        if (count - n_col != n_row):
            print("\nMasukan file tidak tepat, ulangi!\n")
            valid = False
            ROWS_VALUES = []
            COLS_VALUES = []
        else :
            print("Proses pembacaan selesai dilakukan")
            valid = True

# 11. Program Utama
if __name__ == '__main__':
    # 1. Melakukan pembacaan dari file
    read_file()
    print("\nPemrosesan sedang dilakukan...")

    # 2.1. Instansiasi awal pemrosesan baris
    rows = len(ROWS_VALUES)
    rows_changed = [0] * rows
    rows_done = [0] * rows
    max_len_rows = 0
    for i in range (rows):
        if (max_len_rows < len(ROWS_VALUES[i])):
            max_len_rows = len(ROWS_VALUES[i])

    # 2.2. Inisiasi matriks baris
    matr_rows_out = [[0 for i in range (max_len_rows + 1)] for j in range (rows)]
    for i in range (rows):
        for j in range (len(ROWS_VALUES[i])):
            matr_rows_out[i][j] = ROWS_VALUES[i][j]

    # 3.1. Instansiasi awal pemrosesan kolom
    cols = len(COLS_VALUES)
    cols_changed = [0] * cols
    cols_done = [0] * cols
    max_len_cols = 0
    for i in range (cols):
        if (max_len_cols < len(COLS_VALUES[i])):
            max_len_cols = len(COLS_VALUES[i])

    # 3.2. Instansiasi matriks kolom
    matr_cols_out = [[0 for i in range (cols)] for j in range (max_len_cols + 1)]
    for i in range (cols):
        for j in range (len(COLS_VALUES[i])):
            matr_cols_out[j][i] = COLS_VALUES[i][j]
            
    # 4. Instansiasi papan pemrosesan nonogram
    solved = False 
    shape = (rows, cols)
    board = [[0 for c in range(cols)] for r in range(rows)]

    # 5. Mendefinisikan semua kemungkinan solusi menggunakan fungsi create_possibilities
    rows_possibilities = create_possibilities(ROWS_VALUES, cols)
    cols_possibilities = create_possibilities(COLS_VALUES, rows)

    # 6. Melakukan pemrosesan selama belum berakhir
    start = time.time()
    while not solved:
        # Melakukan pemrosesan terhadap indeks dari baris dan kolom yang belum selesai 
        lowest_rows = select_index_not_done(rows_done, cols_done, rows_possibilities, 1)
        lowest_cols = select_index_not_done(rows_done, cols_done, cols_possibilities, 0)
        # Pemrosesan dilakukan bagi nilai baris atau kolom yang memiliki kemungkinan paling sedikit
        lowest = sorted(lowest_rows + lowest_cols, key=lambda element: element[1])

        # Melakukan pemrosesan terhadap baris/kolom yang telah diurutkan pada langkah sebelumnya
        for ind1, _, row_ind in lowest:
            # Melakukan pengecekan apakah sudah diselesaikan atau belum
            if not check_done(rows_done, cols_done, row_ind, ind1):
                # Pemrosesan berdasarkan flag
                # Jika merupakan baris, ambil nilai baris pada indeks tersebut
                if row_ind: 
                    values = rows_possibilities[ind1]
                # Jika merupakan kolom, ambil nilai kolom pada indeks tersebut
                else: 
                    values = cols_possibilities[ind1]
                
                # mengambil semua baris/kolom yang berkoresponden
                same_ind = get_only_one_option(values)
                
                # melakukan pemetaan terhadap baris dan kolom terkait
                for ind2, val in same_ind:
                    if row_ind: 
                        ri = ind1
                        ci = ind2
                    else: 
                        ri = ind2
                        ci = ind1
                    
                    # Jika isi papan masih 0
                    if board[ri][ci] == 0:
                        # Ganti dengan nilai val
                        board[ri][ci] = val
                        # Lalu perbaharui nilai kemungkinan setelah kemungkinan dari indkes
                        # terkait diselesaikan, sehingga bisa dicabut
                        if row_ind: 
                            cols_possibilities[ci] = remove_possibilities(cols_possibilities[ci], ri, val)
                        else: 
                            rows_possibilities[ri] = remove_possibilities(rows_possibilities[ri], ci, val)
                
                # Lakukan pengecekan kembali apakah pemrosesan sudah selesai dilaksanakan pada
                # baris atau kolom terkait
                update_done(board, rows_done, cols_done, row_ind, ind1)
        
        # Melakukan pembaharuan nilai "solved" untuk eksekusi kalang while pada bagian atas
        solved = check_solved(rows_done, cols_done)
    finish = time.time()

    # Menampilakn hasil akhir dari papan setelah pemrosesan
    print("\n============   HASIL PEMROSESAN   ============\n")
    display_board(board, rows, max_len_rows, matr_rows_out, cols, max_len_cols, matr_cols_out)
    print("Execution time :", finish - start, "second(s)\n")