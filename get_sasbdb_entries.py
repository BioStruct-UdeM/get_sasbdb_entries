#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import json
import logging
import time

class Entry:

    def __init__(self, code, id, title, cif_file_url):
        self.code = code
        self.id = id
        self.title = title
        self.cif_file_url = cif_file_url


def make_request(url):

    logging.info('Making the request to {}'.format(url))
    request_data = requests.get(url)
    if request_data.status_code == 200:
        logging.info('GET request succesfully done')
        return request_data
    else:
        logging.critical('Error reaching the address {}'.format(url))
        logging.critical('The program will now exit')


def get_list_all_codes():

    url_get_codes = 'https://www.sasbdb.org/rest-api/entry/codes/all/'

    logging.info('Parsing the entries for their SASBDB code')
    request_data = make_request(url_get_codes)
    downloaded_data = request_data.json()
    list_all_codes = []
    for entry in downloaded_data:
        list_all_codes.append(entry['code'])

    logging.info('{} SASBDB codes were retreived'.format(len(list_all_codes)))

    return list_all_codes


def download_summary(code):

    base_url_summary = 'https://www.sasbdb.org/rest-api/entry/summary/' # just add the SASDE48 name
    url = base_url_summary + code + '/'

    logging.info('Downloading the summary information for {}'.format(code))
    request_data = make_request(url)
    with open('data/{}_summary.json'.format(code), 'w') as jsonfile:
        logging.info('Saving the summary file for {} in the data folder - {}_summary.json'.format(code, code))
        json.dump(request_data.json(), jsonfile, indent=4, ensure_ascii=False)


def download_datfile(code):

    base_url_datfiles = 'https://www.sasbdb.org/media/intensities_files/' # just add the SASDE48.dat name
    url = base_url_datfiles + code + '.dat'

    logging.info('Downloading the summary information for {}'.format(code))
    request_data = make_request(url)
    with open('data/{}.dat'.format(code), 'w') as datfile:
        logging.info('Saving the .dat file for {} in the data folder - {}.dat'.format(code, code))
        datfile.write(request_data.text)


def download_outfile(code):

    base_url_outfiles = 'https://www.sasbdb.org/media/p_of_R_files/' # just add the SASDE48 name
    url = base_url_outfiles + code + '.out'

    logging.info('Downloading the real space information for {}'.format(code))
    request_data = make_request(url)
    with open('data/{}.out'.format(code), 'w') as outfile:
        logging.info('Saving the real space file for {} in the data folder - {}.out'.format(code, code))
        outfile.write(request_data.text)


def read_jsonfile(code):

    with open('data/{}_summary.json'.format(code), 'r') as jsonfile:
        data = json.load(jsonfile)
        print(data['guinier_rg'])


def main():

    logging.basicConfig(level=logging.INFO)

    list_all_codes = get_list_all_codes()

    for code in list_all_codes[0:1]:
        logging.info('---------------------------------------')
        logging.info('Starting acquiring data for {} from the SASBDB'.format(code))
        download_summary(code)
        download_datfile(code)
        download_outfile(code)
        logging.info('Done for {}'.format(code))
        time.sleep(5)


if __name__ == '__main__':
    main()

    base_url = 'https://www.sasbdb.org/data/' # just add the SASDE48 name
    base_url_zipfiles = 'https://www.sasbdb.org/media/zip_directories/' # just add the SASDE48.zip name
