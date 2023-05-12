# Line-solving Optimation - Nonogram Solver
> Source code ini merupakan bentuk implementasi Optimasi Metode Line-solving dengan Teknik Heuristik Pencarian Pseudo-Exhaustive untuk Menyelesaikan Permainan Nonogram

## Daftar Isi
* [Abstrak](#abstrak)
* [Implementasi Program](#implementasi-program)
* [Sistematika File](#sistematika-file)
* [Cara Menjalankan Program](#cara-menjalankan-program)

## Abstrak
Permainan Nonogram adalah sebuah permainan  berbasis logika yang mengasah pikiran. Belum cukup banyak algoritma yang diusulkan untuk dapat menyelesaikan permainan ini secara komputasional. Penyelesaian sebuah nonogram dengan cara lempang menggunakan algoritma brute force memerlukan kompleksitas waktu yang sangat tinggi sehingga algoritma ini tidak efisien. Permainan ini sendiri sudah digolongkan dalam permasalahan NP-complete sehingga akan sulit untuk merumuskan sebuah algoritma yang berhasil menyelesaikan permasalahan ini dalam kompleksitas polinomial. 

Teknik Heuristik sering digunakan untuk melakukan akselerasi pencarian  solusi tanpa harus memperoleh seluruh kemungkinan secara mendalam. Pada makalah ini akan dibahas sebuah algoritma berbasis line-solving yang penulis usulkan untuk menyelesaikan permasalahan ini dalam basis kasus-per-kasus. Algoritma diimplementasikan secara rangkap sebagai gabungan dari beberapa algoritma dengan pendekatan heuristik untuk melakukan optimasi mendekati kompleksitas polinomial. Pada makalah ini juga akan dibahas mengenai ide pengembangan lebih lanjut solusi dengan menggunakan proses propagasi dan program dinamis yang jika diimplementasikan dengan baik dapat mencapai kompleksitas rata-rata mendekati polinomial.

## Implementasi Program
Program merupakan bentuk implementasi dari algoritma pencarian *psudo-exhaustive* yang diusulkan. Program yang dibangun telah berhasil dibuat untuk melaksanakan implementasi penyelesaian permainan nonogram dengan berbagai uji kasus nonogram dengan berbagai ukuran. Lebih lanjut, proses implementasi solusi dan skema pengujian telah berhasil membuktikan bahwa algoritma rangkap yang diusulkan pada proses pembangunan algoritma terbukti cukup sangkil karena meskipun berada pada kompleksitas sekitar eksponensial (polinomial derajat tinggi), tetapi memiliki ketinggian yang cukup landai.

## Sistematika File
```bash
.
├─── doc
├─── src
│   └─── NonogramSolver.py
├─── src
│   ├─── input5x5.txt
│   ├─── input10x10.txt
│   ├─── input15x15.txt
│   ├─── input20x15.txt
│   ├─── input20x25.txt
│   └─── input25x25.txt
└─── README.md
```

## Cara Menjalankan Program
1. Lakukan *clone repository* dengan command berikut
    ``` bash
    $ git clone https://github.com/mikeleo03/Nonogram-Solver.git
    ```
2. Anda dapat melakukan pemrosesan terhadap nonogram dalam berbagai jenis ukuran yang terdapat pada direktori `test`, mulai dari nonogram persegi kecil berukuran 5x5 hingga nonogram besar non-persegi berukuran 20x25. Selain itu anda juga dapat memberikan masukan nonogram anda sendiri dengan mengikuti format masukan seperti yang terdapat pada direktori yang sama (*n* baris pertama menyatakan larik elemen penyusun kolom sejumlah *n* baris, diikuti *m* baris terakhir yang menyatakan larik elemen penyusun baris sejumlah *m*).
Referensi gambar dapat Anda lihat pada folder `test`.

Penjelasan lebih jauh terkait cara kerja algoritma dapat dibaca pada tautan [makalah berikut](doc/Optimasi%20Metode%20Line-solving%20dengan%20Teknik%20Heuristik%20Pencarian%20Pseudo-Exhaustive%20untuk%20Menyelesaikan%20Permainan%20Nonogram%20-%20Michael%20Leon%20Putra%20Widhi.pdf).