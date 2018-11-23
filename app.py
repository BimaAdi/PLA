import os
import csv
from flask import Flask, request, render_template, redirect, url_for, send_file
from crontab import CronTab
from model.sentiment import *
from stream import *
from autoStream import *
from config import *

# set Flask
app = Flask(__name__)

# set CNN model
global graph
graph = tf.get_default_graph()
vocab, tokenizer, max_length, model = load_variabels()

# Set crontab
cron = CronTab(user=curr_username)
cron.remove_all()
cron.write()

def check_predict(raw, predict):
    check = []
    for i in range(len(raw)):
        for j in range(len(predict)):
            if (raw[i] == predict[j][:-4]):
                check.append(raw[i])
            
    return(check)
def remove_predict_raw(raw, predict):
    for _ in range(len(predict)):
        raw.remove(predict[_])
    return(raw)

def check_p(raw, predict, filename):
    data = []
    for item_raw in raw:
        is_predict = False
        for item_predict in predict:
            if(item_raw == item_predict[:-4]):
                is_predict = True
        
        item_data = {}
        item_data["filename"] = item_raw
        if(is_predict == False):
            item_data["predict_status"] = False
        else:
            item_data["predict_status"] = True
            
        item_data["current"] = False
        if(item_raw == filename):
            item_data["current"] = True
        data.append(item_data)
    return(data)
def get_status_data(filename, data):
    for item in data:
        if(item["filename"] == filename):
            return(item["predict_status"])

def get_data(filename, data, predict_status):
    if(predict_status == True):
        with open(predict_file_directory + "/" + filename + ".csv", mode='r') as fh:
            rd = csv.DictReader(fh, delimiter=',') 
            rd_list = []
            for row in rd:
                rd_list.append(row)
        return(rd_list)
    else:
        input_file = open(raw_file_directory + "/" + filename)
        rd_list = []
        for line in input_file:
            rd_list.append(line)
        return(rd_list)
#-------------------- ROUTE View ---------------------------------------------------
"""
Route View berhubungan dengan untuk menampilkan templates
"""
# index route
"""
@app.route("/")
def index():
    raw_file = os.listdir(raw_file_directory)
    predict_file = os.listdir(predict_file_directory)
    sudah_di_prediksi = check_predict(raw_file, predict_file)
    raw_file = remove_predict_raw(raw_file, sudah_di_prediksi)
    # print(sudah_di_prediksi)
    # hari = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    raw_file.sort()
    # print(raw_file)
    if(len(cron) > 0):
        is_stream_run = True
    else:
        is_stream_run = False
    return render_template('index.html', raw_file=raw_file, sudah_di_prediksi=sudah_di_prediksi,is_stream_run=is_stream_run)
"""
""" ------------------------Start Experiment-------------------------"""
"""
index untuk view yang baru
- menampilkan current_file
- status current_file apakah sudah diprediksi atau belum
- tombol prediksi
- tombol download
"""
global current_file
current_file = "Tidak ada data yang dipilih"
@app.route("/")
def index():
    # check stream sedang berjalan atau tidak
    global current_file
    if(len(cron) > 0):
        is_stream_run = True
    else:
        is_stream_run = False
    # set list data dan check apakah sudah di prediksi
    raw_file = os.listdir(raw_file_directory)
    predict_file = os.listdir(predict_file_directory)
    data = check_p(raw_file, predict_file, current_file)
    # set data yang ditampilkan
    showData = {}
    showData["filename"] = current_file
    if(current_file != "Tidak ada data yang dipilih"):
        showData["predict_status"] = get_status_data(current_file, data)
        showData["data"] = get_data(current_file, data, showData["predict_status"])
        showData["display"] = True
    else:
        showData["display"] = False

    return render_template('index.html', is_stream_run=is_stream_run, data=data, showData=showData)

# lihat hasil prediksi
@app.route("/hasil_prediksi/<filename>")
def hasil_prediksi(filename):
    print(filename)
    global current_file
    current_file = str(filename)
    print(current_file)
    return redirect(url_for('index'))

""" ------------------------End Experiment--------------------------"""
# predict route
@app.route("/predict")
def predict():
    predict_file = os.listdir(predict_file_directory)
    # hari = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    predict_file.sort()
    return render_template('predict.html', predict_file=predict_file)

# lihat hasil prediksi
# @app.route("/hasil_prediksi/<filename>")
# def hasil_prediksi(filename):
#     with open(predict_file_directory + "/" + filename + ".csv", mode='r') as fh:
#         rd = csv.DictReader(fh, delimiter=',') 
#         rd_list = []
#         for row in rd:
#             rd_list.append(row)
#     return render_template('hasil.html', data=rd_list, filename=filename)

#-------------------ROUTE Fungsi-----------------------------------------
"""
Route fungsi berhubungan dengan funsionalitas seperti:
- Menjalankan dan mematikan stream twitter
- prediksi data hasil stream twitter
- Download file
"""
# twitter start stream route
@app.route("/start_stream", methods=["GET", "POST"])
def start_stream():
    """
    Route untuk menjalankan stream twitter
    pertama-tama check apakah input menit stream sudah benar
    (tidak kosong)
    """
    params = request.form
    if(params == None):
        params = flask.request.args
    if(params != None):
        if(params.get("menit") != ""):
            print(params.get("mode"))
            """
            check apakah mode stream Manual atau Automatic
            """
            if(str(params.get("mode")) == "Manual"):
                """
                Mode Stream = Manual
                Kumpulkan stream lalu simpan dalam bentuk .txt
                pertama jalankan secara manual, berikutnya menggunakan
                crontab dengan mengedit file cronjobs menggunakan package
                python-crontab
                """
                # activate stream 
                duration = int(params.get("menit"))
                saveDirectory = dir_aplikasi + "/" +raw_file_directory
                begin_stream_manual(duration, saveDirectory)

                # activate crontab 
                cron.remove_all()
                cron.write()
                duration = str(duration)
                job = cron.new(command= dir_python + ' ' + dir_aplikasi + '/streamArg.py ' + duration + ' ' + dir_aplikasi + "/" +raw_file_directory)
                duration = int(duration)
                job.minute.every(duration)
                cron.write()
            else:
                """
                Mode Stream = Automatic
                Kumpulkan stream lalu simpan dalam bentuk .txt
                lalu predict menggunakan model
                pertama jalankan secara manual, berikutnya menggunakan
                crontab (crontab untuk stream automatic belum bisa berjalan)
                dengan mengedit file cronjobs menggunakan package
                python-crontab
                """
                 # activate stream 
                duration = int(params.get("menit"))
                saveDirectory = dir_aplikasi + "/" +raw_file_directory
                begin_stream_automatic(duration, saveDirectory)

                # activate crontab 
                cron.remove_all()
                cron.write()
                duration = str(duration)
                job = cron.new(command= dir_python + ' ' + dir_aplikasi + '/autoStreamArg.py ' + duration + ' ' + dir_aplikasi + "/" +raw_file_directory)
                duration = int(duration)
                job.minute.every(duration)
                cron.write()
    
    return redirect(url_for('index'))

# twitter stop stream route
@app.route("/stop_stream")
def stop_stream():
    """
    Route untuk mematikan stream 
    mematikan stream dengan cara menghapus
    cronjobs menggunakan package python-crontab
    """
    cron.remove_all()
    cron.write()
    return redirect(url_for('index'))

# Download file route
@app.route("/download/<directory>/<filename>")
def download(directory, filename):
    """
    Route untuk mendownload file
    pertama cek dulu apakah file yang ingin didownload 'raw' (belum diprediksi)
    atau 'predict' (sudah diprediksi). hal ini dilakukan karena folder penyimpanan data
    yang belum diprediksi dan sudah diprediksi berbeda. 
    """
    if(directory == "raw"):
        return(send_file(dir_aplikasi + "/" + raw_file_directory + "/" +filename))
    else:
        return(send_file(dir_aplikasi + "/" + predict_file_directory + "/" +filename))

# Predict route using CNN Model
@app.route("/predict_txt/<filename>")
def predict_txt(filename):
    """
    Melakukan prediksi data stream twitter (<filename>) menggunakan model
    lalu data hasil prediksi di simpan dalam bentuk csv
    """
    input_file = open(raw_file_directory + "/" + filename)
    csv_head = ['text', 'conclusi', 'percent'] #csv head
    csv_body = []
    for line in input_file:
        with graph.as_default():
            percent, conclusion = predict_sentiment(line, vocab, tokenizer, max_length, model)
        csv_line = {}
        csv_line["text"] = line
        csv_line["conclusi"] = conclusion
        csv_line["percent"] = str(percent * 100)
        csv_body.append(csv_line)
    
    input_file.close()
    # os.remove(raw_file_directory + "/" + filename)

    csv_name = filename + ".csv"
    try:
        with open(predict_file_directory + "/" + csv_name, 'w') as csv_name:
            writer = csv.DictWriter(csv_name, fieldnames=csv_head)
            writer.writeheader()
            for data in csv_body:
                writer.writerow(data)
    except IOError:
            print("I/O error")
    return redirect(url_for('index'))
