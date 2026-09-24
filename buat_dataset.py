import random, pandas as pd
random.seed(42)
lok = ["gedung rektorat","gedung fakultas teknik","perpustakaan pusat","laboratorium komputer 2","ruang dosen lantai 3","gedung kuliah bersama","kantor biro akademik","asrama mahasiswa","ruang tata usaha","laboratorium jaringan"]
sis = ["SIAKAD","portal e-learning","sistem KRS online","presensi online","sistem keuangan kampus","portal penerimaan mahasiswa baru","sistem ujian daring"]
T = [
 "server {s} down total, seluruh pengguna tidak bisa mengakses sama sekali",
 "jaringan internet di {l} mati total sejak pagi, semua ruangan tidak bisa terhubung",
 "{s} error 500 saat masa pengisian berlangsung, ratusan mahasiswa gagal masuk",
 "akun admin {s} diduga diretas, ada login mencurigakan dari luar negeri",
 "ransomware menyerang komputer di {l}, file penting terenkripsi dan tidak bisa dibuka",
 "listrik UPS ruang server padam, seluruh layanan {s} berhenti mendadak",
 "data nilai di {s} hilang setelah pembaruan sistem, mohon ditangani segera",
 "{s} tidak bisa diakses saat ujian berlangsung, peserta ujian terputus massal",
 "email phishing menyebar ke seluruh dosen dan banyak yang sudah memasukkan password",
 "database {s} korup, backup terakhir belum dicoba dipulihkan, layanan lumpuh",
 "suhu ruang server naik drastis dan alarm menyala, khawatir perangkat rusak",
 "switch utama di {l} rusak sehingga seluruh lantai kehilangan koneksi jaringan",
]
S = [
 "printer di {l} tidak bisa mencetak, antrean dokumen menumpuk",
 "wifi di {l} sangat lambat, sulit membuka {s}",
 "email saya tidak bisa mengirim lampiran lebih dari satu file",
 "proyektor di {l} tidak menyala padahal ada perkuliahan siang ini",
 "saya tidak bisa login ke {s} sejak kemarin, password sudah benar",
 "koneksi VPN sering terputus saat mengakses jurnal dari rumah",
 "komputer di {l} sering restart sendiri ketika dipakai mengetik laporan",
 "aplikasi {s} lambat di akun saya, halaman lama sekali terbuka",
 "scanner di {l} tidak terdeteksi oleh komputer, dokumen perlu dipindai hari ini",
 "sound system ruang kelas di {l} berdengung dan suaranya pecah",
 "file laporan tidak bisa diunggah ke {s}, muncul pesan gagal berulang",
 "laptop inventaris kantor sering hang dan harus dinyalakan ulang berkali-kali",
]
R = [
 "mohon bantuan reset password akun {s}, saya lupa kredensialnya",
 "minta dipasangkan aplikasi pengolah data di komputer {l}",
 "bagaimana cara mengubah foto profil di {s}?",
 "permintaan penambahan mouse dan keyboard cadangan untuk {l}",
 "mohon informasi tata cara mengajukan akun email untuk dosen baru",
 "saya ingin bertanya jadwal pemeliharaan {s} bulan depan",
 "usul perubahan tampilan menu di {s} agar lebih mudah dibaca",
 "minta panduan penggunaan {s} untuk mahasiswa semester awal",
 "permohonan pemindahan colokan jaringan di {l} ke sisi jendela",
 "tanya prosedur peminjaman kabel HDMI untuk kegiatan di {l}",
 "mohon update nama pada akun {s}, ada salah ketik di nama belakang",
 "permintaan pembuatan folder bersama di penyimpanan awan untuk kelompok kerja",
]
def build(tpls, label, n):
    out=set()
    while len(out)<n:
        t=random.choice(tpls).format(l=random.choice(lok), s=random.choice(sis))
        if random.random()<0.3: t=random.choice(["mohon bantuan, ","tolong segera dicek, ","selamat siang, ","halo tim TI, "])+t
        out.add(t)
    return [(t,label) for t in out]
rows = build(T,"Tinggi",60)+build(S,"Sedang",60)+build(R,"Rendah",60)

HARD = [
 ("wifi mati di ruang saya, tidak bisa koneksi sama sekali","Sedang"),
 ("laptop saya down dan tidak bisa menyala, ada tugas yang harus dikumpulkan","Sedang"),
 ("internet tidak bisa dipakai di meja saya sejak tadi pagi","Sedang"),
 ("printer mati total tidak mau menyala sama sekali","Sedang"),
 ("akun email saya tidak bisa dibuka, takut ada yang masuk tanpa izin","Sedang"),
 ("server lab lambat sekali hari ini","Sedang"),
 ("sistem error saat saya mengisi formulir, sudah dicoba tiga kali","Sedang"),
 ("koneksi putus terus di ruang rapat, mohon dicek","Sedang"),
 ("tolong segera reset password, saya perlu masuk sistem hari ini","Rendah"),
 ("mohon dibantu install aplikasi, agak mendesak untuk rapat besok","Rendah"),
 ("tanya kenapa halaman login tampil agak berbeda dari biasanya","Rendah"),
 ("minta dicek apakah wifi di ruang saya sinyalnya bisa ditambah","Rendah"),
 ("ada beberapa mahasiswa mengeluh tidak bisa masuk sistem, mungkin masalah di akun mereka","Sedang"),
 ("website kampus agak lambat dibuka, mungkin karena banyak pengunjung","Sedang"),
 ("beberapa file di penyimpanan bersama tidak bisa dibuka lagi","Tinggi"),
 ("ada login mencurigakan di akun saya dari perangkat yang tidak dikenal","Tinggi"),
 ("sistem pembayaran uang kuliah tidak merespons untuk semua mahasiswa","Tinggi"),
 ("jaringan lantai dua putus, sekitar seratus komputer tidak bisa online","Tinggi"),
 ("aplikasi ujian tiba-tiba keluar sendiri untuk banyak peserta","Tinggi"),
 ("data mahasiswa terlihat oleh akun yang seharusnya tidak punya akses","Tinggi"),
]
rows += HARD
random.shuffle(rows)
df=pd.DataFrame(rows,columns=["deskripsi","prioritas"]); df.insert(0,"id_tiket",[f"TKT-{i+1:03d}" for i in range(len(df))])
df.to_csv("dataset_tiket_ti.csv",index=False); print(df.prioritas.value_counts()); print(df.head())
