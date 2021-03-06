#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import json
import logging
import time
import yaml
import os
import logging.config


class Entry:

    def __init__(self, code, id, title, cif_file_url):
        self.code = code
        self.id = id
        self.title = title
        self.cif_file_url = cif_file_url


def setup_logging(default_path='logging.yml', default_level=logging.DEBUG, env_key='LOG_CFG'):

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'r') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def make_request(url):

    logging.info('Making the request to {}'.format(url))
    request_data = requests.get(url)
    if request_data.status_code == 200:
        logging.info('GET request succesfully done')
        return request_data
    elif request_data.status_code == 404:
        logging.error('GET request could not reach the address {}'.format(url))
        request_data = None
        return request_data
    else:
        logging.error('Error reaching the address {}'.format(url))
        logging.error('Check the log file to figure out what might have gone bad')
        logging.error('The program will now exit')
        raise SystemExit('Error making the request. Check the log file to figure out what might have gone bad')


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


def save_list_codes(list_all_codes):

    list_code_file = 'data/list_SASBDB_codes.txt'
    logging.info('Saving the list of SASBDB codes in {}'.format(list_code_file))

    with open(list_code_file, 'w') as outfile:
        outfile.write('List of SASBDB codes as of {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S %z')))
        for code in list_all_codes:
            outfile.write(code + '\n')


def download_summary(code):

    base_url_summary = 'https://www.sasbdb.org/rest-api/entry/summary/' # just add the SASDE48 name
    url = base_url_summary + code + '/'

    logging.info('Downloading the summary information for {}'.format(code))
    request_data = make_request(url)
    if request_data is not None:
        with open('data/{}_summary.json'.format(code), 'w') as jsonfile:
            logging.info('Saving the summary file for {} in the data folder - {}_summary.json'.format(code, code))
            json.dump(request_data.json(), jsonfile, indent=4, ensure_ascii=False)
    else:
        logging.warning('No sumary file available for {}'.format(code))


def download_datfile(code):

    base_url_datfiles = 'https://www.sasbdb.org/media/intensities_files/' # just add the SASDE48.dat name
    url = base_url_datfiles + code + '.dat'

    logging.info('Downloading the summary information for {}'.format(code))
    request_data = make_request(url)
    if request_data is not None:
        with open('data/{}.dat'.format(code), 'w') as datfile:
            logging.info('Saving the .dat file for {} in the data folder - {}.dat'.format(code, code))
            datfile.write(request_data.text)
    else:
        logging.warning('No .dat file available for {}'.format(code))


def download_outfile(code):

    base_url_outfiles = 'https://www.sasbdb.org/media/p_of_R_files/' # just add the SASDE48 name
    url = base_url_outfiles + code + '.out'

    logging.info('Downloading the real space information for {}'.format(code))
    request_data = make_request(url)
    if request_data is not None:
        with open('data/{}.out'.format(code), 'w') as outfile:
            logging.info('Saving the real space file for {} in the data folder - {}.out'.format(code, code))
            outfile.write(request_data.text)
    else:
        logging.warning('No real space file available for {}'.format(code))


def download_ciffile(code):

    base_url_outfiles = 'https://www.sasbdb.org/media/sascif/sascif_files/' # just add the SASDE48.sascif name
    url = base_url_outfiles + code + '.sascif'

    logging.info('Downloading the SAS CIF file for {}'.format(code))
    request_data = make_request(url)
    if request_data is not None:
        request_data.encoding = 'utf-8'
        with open('data/{}.sascif'.format(code), 'w') as outfile:
            logging.info('Saving the SAS CIF file for {} in the data folder - {}.sascif'.format(code, code))
            outfile.write(request_data.text)
    else:
        logging.warning('No SAS CIF file available for {}'.format(code))


def read_jsonfile(code):

    with open('data/{}_summary.json'.format(code), 'r') as jsonfile:
        data = json.load(jsonfile)
        print(data['guinier_rg'])


def download_all_data(code):

    logging.info('Starting acquiring data for {} from the SASBDB'.format(code))
    download_summary(code)
    download_datfile(code)
    download_outfile(code)
    download_ciffile(code)
    logging.info('Done for {}'.format(code))
    logging.info('---------------------------------------')
    time.sleep(2)


def main():

    setup_logging()

    list_all_codes = get_list_all_codes()
    save_list_codes(list_all_codes)

    for code in list_all_codes:
        download_all_data(code)


if __name__ == '__main__':
    main()
