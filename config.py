import os

dir_aplikasi = '/home/bimaadi/AplikasiStreamTwitter2'
dir_python = '/home/bimaadi/AplikasiStreamTwitter2/venv/bin/python'
curr_username = 'bimaadi'
raw_file_directory = 'file/raw'
predict_file_directory = 'file/predict'
# if not use proxy set it ''(blank)
proxy = 'http://:@proxy.informatika.lipi.go.id:3128'
# proxy = ''
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
# set twitter token
ckey = 'e6gqHXyaol257aPnp8mx1LsYM'
consumer_secret = 'JZWMIHbagKgPdbAOW7oQjfm675LIzdJnboMEzfkHqy0yXoulxr'
access_token_key = '1052375914594545664-oeKqo83e9h2uUkrQrGHehXWrObC4dl'
access_token_secret = 'wDQKAMh1B0tW9dQRNw3B2oBqr8AIJ9oMFJ8g48eeozgTZ'
