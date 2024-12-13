use SMAN1SURAKARTA;

INSERT INTO jadwal (id_jadwal, id_kelas, id_mapel, id_guru, hari, jam_mulai, jam_selesai)
VALUES
('JDW0001', 'KLS0001', 'MPL0001', 'GRU0001', 'Senin', '7:30:00 AM', '9:40:00 AM'),
('JDW0002', 'KLS0001', 'MPL0002', 'GRU0002', 'Senin', '10:10:00 AM', '10:40:00 AM'),
('JDW0003', 'KLS0002', 'MPL0003', 'GRU0003', 'Senin', '7:30:00 AM', '9:40:00 AM'),
('JDW0004', 'KLS0002', 'MPL0005', 'GRU0005', 'Senin', '10:10:00 AM', '11:35:00 AM'),
('JDW0005', 'KLS0006', 'MPL0015', 'GRU0005', 'Selasa', '7:30:00 AM', '8:55:00 AM'),
('JDW0006', 'KLS0006', 'MPL0017', 'GRU0007', 'Selasa', '9:00:00 AM', '10:50:00 AM'),
('JDW0007', 'KLS0007', 'MPL0017', 'GRU0007', 'Rabu', '7:30:00 AM', '8:55:00 AM'),
('JDW0008', 'KLS0007', 'MPL0011', 'GRU0001', 'Rabu', '9:00:00 AM', '11:35:00 AM'),
('JDW0009', 'KLS0012', 'MPL0024', 'GRU0004', 'Kamis', '7:30:00 AM', '9:40:00 AM'),
('JDW0010', 'KLS0012', 'MPL0022', 'GRU0014', 'Kamis', '10:10:00 AM', '1:40:00 AM'),
('JDW0011', 'KLS0013', 'MPL0026', 'GRU0006', 'Jumat', '7:30:00 AM', '8:55:00 AM'),
('JDW0012', 'KLS0013', 'MPL0025', 'GRU0005', 'Jumat', '9:00:00 AM', '10:50:00 AM'),
('JDW0013', 'KLS0007', 'MPL0009', 'GRU0009', 'Jumat', '7:30:00 AM', '9:15:00 AM'),
('JDW0014', 'KLS0007', 'MPL0010', 'GRU0010', 'Jumat', '9:45:00 AM', '10:50:00 AM'),
('JDW0015', 'KLS0005', 'MPL0007', 'GRU0007', 'Jumat', '1:45:00 PM', '2:25:00 PM');

select * from jadwal