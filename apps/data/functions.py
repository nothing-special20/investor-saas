import sys
import os
import zipfile
import csv

import re
import shutil
import pandas as pd
import urllib.request as request
import pandas as pd
from contextlib import closing
from bs4 import BeautifulSoup

from sqlalchemy import create_engine

from dbfread import DBF, FieldParser, InvalidValue

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/functions_library')


HILLSBOROUGH_PROP_APP_LINK = 'https://downloads.hcpafl.org/'

BMT_DATA_FOLDER = os.getenv('BMT_DATA_FOLDER')
PARCEL_DATA_FOLDER = BMT_DATA_FOLDER + 'fl/hillsb/prop_app/'

#Paths to files downloaded from PA website
PARCEL_SALES_DOWNLOAD_FILE = PARCEL_DATA_FOLDER + 'raw/allsales.dbf'
PARCEL_GENERAL_DOWNLOAD_FILE = PARCEL_DATA_FOLDER + 'raw/parcel.dbf'

#Paths to the CSV export
PARCEL_SALES_CSV_FILE = PARCEL_DATA_FOLDER + 'proc/hillsborough_pa_allsales.txt'
PARCEL_GENERAL_CSV_FILE = PARCEL_DATA_FOLDER + 'proc/hillsborough_pa_parcel.txt'

def engine_fn():
    user = 'postgres' #os.getenv('INVESTOR_DB_USER')
    pw = 'postgres' #os.getenv('INVESTOR_DB_PW')
    host = 'localhost' #os.getenv('INVESTOR_DB_HOST')
    port = '54320' #os.getenv('INVESTOR_DB_PORT')
    db = 'investor_saas' # os.getenv('INVESTOR_DB_NAME')
    container = 'db'

    # string = "postgresql+psycopg2://" + str(user) + \
    #             ":" + str(pw) + '@' + str(host) + ":" + str(port) + "/" + str(db)

    conn_url = ''.join(['postgresql+psycopg2://', user, ':', pw, '@', host, ':', port,'/', db])

    print(conn_url)

    engine = create_engine(conn_url)

    return engine

def ftp_file_list(ftp_link, search_term):
    html_page = request.urlopen(ftp_link).read().decode('utf8')
    soup = BeautifulSoup(html_page, 'lxml')
    data_files = str(soup)
    data_files = data_files.split('\n')
    data_files = [x.split(' ') for x in data_files]
    data_files = [x[len(x)-1] for x in data_files]
    data_files = [x for x in data_files if search_term in x]
    data_files = list(set(data_files))
    data_files = [re.sub('\\?', '', x) for x in data_files]
    return data_files

FILES_TO_DOWNLOAD = ftp_file_list(HILLSBOROUGH_PROP_APP_LINK, 'allsales_')
print(FILES_TO_DOWNLOAD)

class MyFieldParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data)
        except ValueError:
            # return str(data)
            return InvalidValue(data)

if __name__ == "__main__":
    #download data
    if sys.argv[1]=='download_data':
        # parcel_sales_data = DBF('/Users/rapple2018/Downloads/allsales_09_02_2022/allsales.dbf')
        # parcel_sales_data = pd.DataFrame(iter(parcel_sales_data))
        # print(parcel_sales_data.head())
        # parcel_sales_data.to_csv('allsales.csv', sep='\t', quoting=csv.QUOTE_ALL, index=False)

        parcel_general_data = DBF('/Users/rapple2018/Downloads/parcel_09_02_2022/parcel.dbf', parserclass=MyFieldParser)
        parcel_general_data = pd.DataFrame(data=iter(parcel_general_data), dtype='str')
        parcel_general_data.to_csv('parcel_data.csv', sep='\t', quoting=csv.QUOTE_ALL, index=False)


    if sys.argv[1]=='upload_data_to_db':
        engine = engine_fn()
        parcel_sales_data = pd.read_csv('allsales.csv', sep='\t', dtype='str', nrows=10000)
        parcel_sales_data.rename(columns={
            "S_AMT": "SALE_AMOUNT",
             "S_DATE": "SALE_DATE"
             },
             inplace=True)

        parcel_sales_data['COUNTY'] = 'HILLSBOROUGH'
        parcel_sales_data = parcel_sales_data[['PIN', 'FOLIO', 'SALE_AMOUNT', 'SALE_DATE', 'GRANTOR', 'GRANTEE', 'COUNTY']]
        
        parcel_sales_data.to_sql('find_investors_sales', engine, index=False, if_exists='replace')

        parcel_general_data = pd.read_csv('parcel_data.csv', sep='\t', dtype='str', nrows=10000)
        parcel_general_data.rename(columns={
            "tBEDS": "NUMBER_OF_BEDS",  
            "tBATHS": "NUMBER_OF_BATHS",
            "tSTORIES": "NUMBER_OF_STORIES", 
            "tUNITS": "NUMBER_OF_UNITS",
             },
             inplace=True)

        

        parcel_general_data['SQUARE_FEET'] = None
        parcel_general_data['YEAR_BUILT'] = None
        parcel_general_data['COUNTY'] = 'HILLSBOROUGH'
        parcel_general_data = parcel_general_data[['PIN','FOLIO','OWNER','ADDR_1','ADDR_2','CITY','STATE','ZIP','NUMBER_OF_BEDS','NUMBER_OF_BATHS','SQUARE_FEET','YEAR_BUILT','NUMBER_OF_STORIES','NUMBER_OF_UNITS','ACREAGE','COUNTY']]

        print(parcel_general_data.head())

        parcel_general_data.to_sql('find_investors_parcelinfo', engine, index=False, if_exists='replace')
        print('wee')
        

