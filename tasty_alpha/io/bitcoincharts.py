import requests

def download_history(market_name):
    url = f"http://api.bitcoincharts.com/v1/csv/{market_name}.csv.gz"
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename

# import urllib2
# import StringIO
# import gzip
#
# def download_history(market_name):
#     # As long as the file is opened in binary mode, both Python 2 and Python 3
#     # can write response body to it without decoding.
#     with open(f'{market_name}.csv', 'wb') as f:
#         c = pycurl.Curl()
#         c.setopt(c.URL,
#                 "http://api.bitcoincharts.com/v1/csv/{market_name}.csv.gz")
#         c.setopt(c.WRITEDATA, f)
#         c.perform()
#         c.close()
#
#
#     baseURL = f"http://api.bitcoincharts.com/v1/csv/"
#     filename = f"{market_name}.csv.gz"
#     outFilePath = f"{market_name}.csv"
#
#     response = urllib2.urlopen(baseURL + filename)
#     compressedFile = StringIO.StringIO()
#     compressedFile.write(response.read())
#     #
#     # Set the file's current position to the beginning
#     # of the file so that gzip.GzipFile can read
#     # its contents from the top.
#     #
#     compressedFile.seek(0)
#
#     decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
#
#     with open(outFilePath, 'w') as outfile:
#         outfile.write(decompressedFile.read())
