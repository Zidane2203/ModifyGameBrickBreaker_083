# Brick Breaker (Modifikasi)

Modifikasi dari game Brick Breaker (referensi GeeksforGeeks) menggunakan Python + Pygame.

## Fitur baru
- **Power-up acak** jatuh dari brick yang hancur (peluang 25%), tangkap dengan paddle:
  - **S (cyan)** - setiap bola memecah menjadi 2 (bola baru keluar dari bola itu sendiri)
  - **P (pink)** - 2 bola baru ditembakkan dari paddle (pin player)
- **Multi-ball aman**: bola yang jatuh tidak langsung game over. Game over/hilang nyawa hanya jika **semua** bola habis.
- Sistem nyawa (3), skor, level bertingkat, brick dengan HP berbeda.
- Pantulan paddle bergantung posisi benturan.
- Kode dipisah modular: `constants.py`, `entities.py`, `powerups.py`, `main.py`.

## Cara main
```
pip install pygame
python main.py
```
Kontrol: panah kiri/kanan atau A/D, SPASI meluncurkan bola, R restart, ESC keluar.
