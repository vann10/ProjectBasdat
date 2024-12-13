CREATE DATABASE SMAN1Surakarta;

USE SMAN1SURAKARTA;

-- Tabel dataguru
CREATE TABLE dataguru (
    id_guru VARCHAR(50) PRIMARY KEY,
    nuptk INT NOT NULL UNIQUE,
    nama_guru VARCHAR(50) NOT NULL,
    jenis_kelamin VARCHAR(50) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    alamat VARCHAR(50) NOT NULL
);

-- Tabel kelas
CREATE TABLE kelas (
    id_kelas VARCHAR(50) PRIMARY KEY,
    id_guru VARCHAR(50) NOT NULL,
    kelas VARCHAR(50) NULL,
    CONSTRAINT kelas_id_guru_foreign
        FOREIGN KEY (id_guru) REFERENCES dataguru (id_guru)
);

-- Tabel datasiswa
CREATE TABLE datasiswa (
    id_siswa VARCHAR(50) PRIMARY KEY,
    nisn INT NOT NULL UNIQUE,
    nama_siswa VARCHAR(50) NOT NULL,
    jenis_kelamin VARCHAR(50) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    alamat VARCHAR(100) NOT NULL,
    id_kelas VARCHAR(50) NOT NULL,
    CONSTRAINT datasiswa_id_kelas_foreign
        FOREIGN KEY (id_kelas) REFERENCES kelas (id_kelas)
);

-- Tabel matapelajaran
CREATE TABLE matapelajaran (
    id_mapel VARCHAR(50) PRIMARY KEY,
    mata_pelajaran VARCHAR(50) NOT NULL,
    kelas INT NOT NULL,
    id_guru VARCHAR(50) NOT NULL,
    CONSTRAINT matapelajaran_id_guru_foreign
        FOREIGN KEY (id_guru) REFERENCES dataguru (id_guru),
);

-- Tabel jadwal
CREATE TABLE jadwal (
    id_jadwal VARCHAR(50) PRIMARY KEY,
    id_kelas VARCHAR(50) NOT NULL,
    id_mapel VARCHAR(50) NOT NULL,
    id_guru VARCHAR(50) NOT NULL,
    hari VARCHAR(50) NOT NULL,
    jam_mulai TIME NOT NULL,
    jam_selesai TIME NOT NULL,
    CONSTRAINT jadwal_id_guru_foreign
        FOREIGN KEY (id_guru) REFERENCES dataguru (id_guru),
    CONSTRAINT jadwal_id_kelas_foreign
        FOREIGN KEY (id_kelas) REFERENCES kelas (id_kelas),
    CONSTRAINT jadwal_id_mapel_foreign
        FOREIGN KEY (id_mapel) REFERENCES matapelajaran (id_mapel)
);

-- Tabel absensisiswa
CREATE TABLE absensisiswa (
    id_absensisiswa VARCHAR(50) PRIMARY KEY,
    id_siswa VARCHAR(50) NOT NULL,
    tanggal DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    CONSTRAINT absensi_id_siswa_foreign
        FOREIGN KEY (id_siswa) REFERENCES datasiswa (id_siswa)
);

-- Tabel absensiguru
CREATE TABLE absensiguru (
    id_absensiguru VARCHAR(50) PRIMARY KEY,
    id_guru VARCHAR(50) NOT NULL,
    tanggal DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    CONSTRAINT absensi_id_guru_foreign
        FOREIGN KEY (id_guru) REFERENCES dataguru (id_guru)
);

-- Tabel pembayaran
CREATE TABLE pembayaran (
    id_pembayaran VARCHAR(50) PRIMARY KEY,
    id_siswa VARCHAR(50) NOT NULL,
    total_tagihan INT,
    status VARCHAR(50) NOT NULL,
    tanggal_transaksi DATE,
    CONSTRAINT pembayaran_id_siswa_foreign
        FOREIGN KEY (id_siswa) REFERENCES datasiswa (id_siswa)
);


-- Tabel nilai
CREATE TABLE nilai (
    id_nilai VARCHAR(50) PRIMARY KEY,
    id_mapel VARCHAR(50) NOT NULL,
    id_siswa VARCHAR(50) NOT NULL,
    nilai INT,
    CONSTRAINT nilai_id_mapel_foreign
        FOREIGN KEY (id_mapel) REFERENCES matapelajaran (id_mapel),
    CONSTRAINT nilai_id_siswa_foreign
        FOREIGN KEY (id_siswa) REFERENCES datasiswa (id_siswa)
);


-- Tabel evaluasi
CREATE TABLE evaluasi (
    id_evaluasi VARCHAR(50) PRIMARY KEY,
    id_siswa VARCHAR(50) NOT NULL,
    status_evaluasi VARCHAR(25) NOT NULL,
    rerata_kehadiran INT,
    rerata_nilai INT,
    CONSTRAINT evaluasi_id_siswa_foreign
        FOREIGN KEY (id_siswa) REFERENCES datasiswa (id_siswa)
);

--Menampilkan semua tabel
SELECT table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE';

--Menampilkan semua tabel beserta isinya
DECLARE @tableName NVARCHAR(128)
DECLARE @sql NVARCHAR(MAX)

DECLARE table_cursor CURSOR FOR
SELECT table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'

OPEN table_cursor
FETCH NEXT FROM table_cursor INTO @tableName

WHILE @@FETCH_STATUS = 0
BEGIN
    SET @sql = 'SELECT * FROM ' + @tableName
    EXEC sp_executesql @sql
    FETCH NEXT FROM table_cursor INTO @tableName
END

CLOSE table_cursor
DEALLOCATE table_cursor
