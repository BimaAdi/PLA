from config import *
import csv

def remove_predict_raw(raw, predict):
    for _ in range(len(predict)):
        raw.remove(predict[_])
    return(raw)

def check_predict(raw, predict, filename):
    data = []
    # loop setiap file raw
    for item_raw in raw:
        # check_predict
        is_predict = False
        for item_predict in predict:
            if(item_raw == item_predict):
                is_predict = True
        
        # get file name
        item_data = {}
        item_data["filename"] = item_raw[:-4]
        if(is_predict == False):
            item_data["predict_status"] = False
        else:
            item_data["predict_status"] = True
        
        # check current file
        item_data["current"] = False
        if(item_raw == filename):
            item_data["current"] = True
        data.append(item_data)
    return(data)

def get_status_data(filename, data):
    """
    Mendapatkan status dari data, apakah data sudah 
    diprediksi atau belum.
    """
    for item in data:
        if(item["filename"] == filename):
            return(item["predict_status"])

def get_data(filename, data, predict_status):
    """
    output data untuk ditampilkan 
    """
    if(predict_status == True):
        with open(predict_file_directory + "/" + filename + ".csv", mode='r') as fh:
            rd = csv.DictReader(fh, delimiter=',') 
            rd_list = []
            for row in rd:
                rd_list.append(row)
        return(rd_list)
    else:
        with open(raw_file_directory + "/" + filename + ".csv", mode='r') as fh:
            rd = csv.DictReader(fh, delimiter=',') 
            rd_list = []
            for row in rd:
                rd_list.append(row)
        return(rd_list)