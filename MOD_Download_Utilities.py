"""
Download url to doc-string or file
  download_to_file(url, fname, f_log)
  doc = download_to_doc(url, f_log)

ND-SRAF / McDonald : 201606 | Last update: 202201
https://sraf.nd.edu
"""


import datetime as dt
import io
import requests
import sys
import time
from urllib.request import urlopen


HEADER = {'Host': 'www.sec.gov', 'Connection': 'close',
         'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         }


def download_to_file(url, f_name, f_log=None, number_of_tries=5, sleep_time=5):
    # download file from 'url' and write to 'fname'
    downloader(url, type=1, f_name=f_name, f_log=f_log, number_of_tries=number_of_tries, sleep_time=sleep_time)


def download_to_doc(url, f_log=None, number_of_tries=5, sleep_time=5):
    # Download url content to string doc
    doc = downloader(url, type=2, f_log=f_log, number_of_tries=number_of_tries, sleep_time=sleep_time)
    return doc


def download_to_list(url, f_log=None, number_of_tries=5, sleep_time=5):
    # Download url content to create list of lines
    file_list = downloader(url, type=3, f_log=f_log, number_of_tries=number_of_tries, sleep_time=sleep_time)
    return file_list


def downloader(url, type=None, f_name=None, f_log=None, number_of_tries=5, sleep_time=5):
    # type = 1:to file, 2: to string, 3: to list
    for i in range(1, number_of_tries):
        try:
            response = requests.get(url, headers=HEADER)
            if response.status_code == 200:
                if type == 1:
                    with open(f_name, 'wb') as f:
                        f.write(response.content)
                    return True
                elif type == 2:
                    doc = response.content
                    return doc
                elif type == 3:
                    file_list = io.StringIO(response.content.decode(encoding="UTF-8", errors='ignore' )).readlines()
                    return file_list
            else:
                print(f'  Error in try #{i} downloader : URL = {url} | status_code = {response.status_code}')
                if i == number_of_tries + 1:
                    print(f'  Failed download: URL = {url}')
                    if f_log: f_log.write(f'  Failed download: URL = {url}\n')
                
        except Exception as exc:
            if i == 1:
                print('\n==>response error in downloader')
            print(f'  {i}.url  : {url} \n  exc:  {exc}')
            if '404' in str(exc):
                break
            print(f'     Retry in {sleep_time} seconds')
            time.sleep(sleep_time)
            sleep_time += sleep_time

    print('\n  ERROR:  Download failed for')
    print(f'          url:  {url}')
    
    if f_log:
        f_log.write('\nERROR:  Download failed=>')
        f_log.write(f'  _url: {url}')
        f_log.write(f'  |  {dt.datetime.now().strftime("%c")}')

    return False


def edgar_server_not_available(flag=False):
    # routine to run download only when EDGAR server allows bulk download.
    # see:  https://www.sec.gov/edgar/searchedgar/ftpusers.htm
    # local time is converted to EST for check

    from datetime import datetime as dt
    import pytz
    import time

    SERVER_BGN = 21  # Server opens at 9:00PM EST
    SERVER_END = 6   # Server closes at 6:00AM EST

    # Get UTC time from local and convert to EST
    utc_dt = pytz.utc.localize(dt.utcnow())
    est_timezone = pytz.timezone('US/Eastern')
    est_dt = est_timezone.normalize(utc_dt.astimezone(est_timezone))

    if est_dt.hour >= SERVER_BGN or est_dt.hour < SERVER_END:
        return False
    else:
        if flag:
            print('\rSleeping: ' + str(dt.now()), end='', flush=True)
        time.sleep(600)  # Sleep for 10 minutes
        return True


if __name__ == '__main__':
    # Test functions    
    start = dt.datetime.now()
    print(f"\n\n{start.strftime('%c')}\nPROGRAM NAME: {sys.argv[0]}\n")

    testfail_url = 'http://www.nd.edu/~mcdonald/xyz.html'  # set to throw an error
    test_url = 'http://www.sec.gov/Archives/edgar/data/1046568/0001193125-15-075170.txt'    
    fname = 'D:/Temp/DL_test.txt'
    f_log = open('D:/Temp/DL_log.txt', 'w')
    download_to_file(test_url, fname, f_log)
    doc = download_to_doc(test_url, f_log)
    f_list = download_to_list(test_url, f_log)

    print(f"\n\nRuntime: {(dt.datetime.now()-start)}")
    print(f"\nNormal termination.\n{dt.datetime.now().strftime('%c')}\n") 