# def remove_predict_raw(raw, predict):
#     for _ in range(len(predict)):
#         raw.remove(predict[_])
#     return(raw)

def check_predict(raw, predict, filename):
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
        input_file = open(raw_file_directory + "/" + filename)
        rd_list = []
        for line in input_file:
            rd_list.append(line)
        return(rd_list)