## Cara menggunakan aplikasi

1. Pastikan menggunakan Python versi 3.5 dan linux
2. clone atau download repository
3. pada folder aplikasi buat virtual environtment 
```
python -m venv aplikasi 
```
4. aktivasi virtual environtment
```
aplikasi\Scripts\activate.sh
```
5. install package yang dibutuhkan aplikasi
```
pip install -r requirements.txt
```
6. pada config.py isi variable dir_aplikasi dengan absolute directory dari aplikasi. Untuk mengetahuinya pada terminal navigasi kedalam directory aplikasi lalu masukan `pwd` .
7. pada config.py isi variable dir_python dengan directory dari virtual environtment python. Untuk mengatahuinya setelah aktivasi virtual environtment pada terminal masukan `which python`.
8. pada config.py isi variable curr_username dengan username linux yang diggunakan.
9. pada config.py isi variable proxy jika menggunakan proxy jika tidak isi dengan `''`.
10. pada terminal masuk ke directory aplikasi lalu jalankan
```
FLASK_APP=app.py
```
11. jalankan aplikasi dengan
```
flask run
```
12. pada web browser masukan link localhost:5000 
