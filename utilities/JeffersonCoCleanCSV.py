
# coding: utf-8

# In[1]:

# get_ipython().magic('load_ext autoreload')
# get_ipython().magic('autoreload 2')

import time
import datetime as dt
import logging
from csv import DictReader, DictWriter 
import re


# In[5]:

def datefix(adate):
        if adate>1:
            try:
                time.strptime(str(int(row)), "%m%d%Y")
                return adate
            except:
                logging.warning('Fixed date on line ' + line[k])
                raise
                return ''
        else:
            return ''
        
DATASHAPE = {
          'SCH': int,
          'PARID': str,
          'STS': int,
          'OWNNAM': str,
          'OWNNAM2': str,
          'OWNNAM3': str,
          'OWNICO': str,
          'DBA': str,
          'MAILSTRNBR': str,
          'MAILSTRDIR': str,
          'MAILSTRNAM': str,
          'MAILSTRTYP': str,
          'MAILSTRSFX': str,
          'MAILSTRUNT': str,
          'MAILCTYNAM': str,
          'MAILSTENAM': str,
          'MAILZIP5': str,
          'MAILZIP4': str,
          'PRPSTRNUM': str,
          'PRPSTRDIR': str,
          'PRPSTRNAM': str,
          'PRPSTRTYP': str,
          'PRPSTRSFX': str,
          'PRPSTRUNT': str,
          'PRPCTYNAM': str,
          'PRPSTENAM': str,
          'PRPZIP5': str,
          'PRPZIP4': str,
          'CMNADRNBR': int,
          'ATD': int,
          'SUBNAM': str,
          'NHDNBR': str,
          'NHDNAM': str,
          'TAXCLS': int,
          'VALACR': float,
          'VALACT': int,
          'VALACTCHG': datefix,
          'VALFLAG': str,
          'TAXCLS2': str,
          'VALACR2': float,
          'VALACT2': int,
          'VALACTCHG2': datefix,
          'VALFLAG2': str,
          'TAXCLS3': str,
          'VALACR3': float,
          'VALACT3': int,
          'VALACTCHG3': datefix,
          'VALFLAG3': str,
          'TAXCLS4': str,
          'VALACR4': float,
          'VALACT4': int,
          'VALACTCHG4': datefix,
          'VALFLAG4': str,
          'TAXCLS5': str,
          'VALACR5': float,
          'VALACT5': int,
          'VALACTCHG5': datefix,
          'VALFLAG5': str,
          'TAXCLS6': str,
          'VALACR6': float,
          'VALACT6': int,
          'VALACTCHG6': datefix,
          'VALFLAG6': str,
          'LGLRNG': int,
          'LGLTWN': int,
          'LGLSEC': int,
          'LGLQTR': str,
          'LGLSUBCD': str,
          'LGLBLK': str,
          'LGLLOT': str,
          'LGLKEY': str,
          'LGLSQFT': int,
          'LGLRCP': str,
          'LGLRNG2': int,
          'LGLTWN2': int,
          'LGLSEC2': int,
          'LGLQTR2': str,
          'LGLSUBCD2': str,
          'LGLBLK2': str,
          'LGLLOT2': str,
          'LGLKEY2': str,
          'LGLSQFT2': int,
          'LGLRCP2': str,
          'LGLRNG3': int,
          'LGLTWN3': int,
          'LGLSEC3': int,
          'LGLQTR3': str,
          'LGLSUBCD3': str,
          'LGLBLK3': str,
          'LGLLOT3': str,
          'LGLKEY3': str,
          'LGLSQFT3': int,
          'LGLRCP3': str,
          'LGLRNG4': int,
          'LGLTWN4': int,
          'LGLSEC4': int,
          'LGLQTR4': str,
          'LGLSUBCD4': str,
          'LGLBLK4': str,
          'LGLLOT4': str,
          'LGLKEY4': str,
          'LGLSQFT4': int,
          'LGLRCP4': str,
          'STTSTRC': str,
          'STTTYPUSE': str,
          'STTYRBLT': int,
          'STTGRSAREA': int,
          'STTBSTAREA': int,
          'STTBSTTYP': str,
          'STTGARTYP': str,
          'STTNBRFLR': int,
          'STTTYPCNS': str,
          'STTNBRBLDG': int,
          'STTNBRUNT': int,
          'STTSTRC2': str,
          'STTTYPUSE2': str,
          'STTYRBLT2': int,
          'STTGRSARE2': int,
          'STTBSTARE2': int,
          'STTBSTTYP2': str,
          'STTGARTYP2': str,
          'STTNBRFLR2': int,
          'STTTYPCNS2': str,
          'STTNBRBLD2': int,
          'STTNBRUNT2': int,
          'STTSTRC3': str,
          'STTTYPUSE3': str,
          'STTYRBLT3': int,
          'STTGRSARE3': int,
          'STTBSTARE3': int,
          'STTBSTTYP3': str,
          'STTGARTYP3': str,
          'STTNBRFLR3': int,
          'STTTYPCNS3': str,
          'STTNBRBLD3': int,
          'STTNBRUNT3': int,
          'STTSTRC4': str,
          'STTTYPUSE4': str,
          'STTYRBLT4': int,
          'STTGRSARE4': int,
          'STTBSTARE4': int,
          'STTBSTTYP4': str,
          'STTGARTYP4': str,
          'STTNBRFLR4': int,
          'STTTYPCNS4': str,
          'STTNBRBLD4': int,
          'STTNBRUNT4': int,
          'SLSDT': datefix,
          'SLSAMT': int,
          'SLSCD': int,
          'DEDTYP': str,
          'SLSDT2': datefix,
          'SLSAMT2': int,
          'SLSCD2': str,
          'DEDTYP2': str,
          'SLSDT3': datefix,
          'SLSAMT3': int,
          'SLSCD3': str,
          'DEDTYP3': str,
          'SLSDT4': datefix,
          'SLSAMT4': int,
          'SLSCD4': str,
          'DEDTYP4': str,
          'PRSBUSCD1': int, #datetime
          'PRSBUSCD2': int, #datetime
          'VALCOMCHG': str,
          'QUAL': str,
          'IMPARA': int,
          'LNDARA': int,
          'COMARA': int,
          'TOTACR': float,
          'CHGDT002': datefix,
          'ASMDT': datefix,
          'RELSCH': str,
          'INCYR': int,
          'EXCYR': int,
          'ANXYR': int,
          'DEMYR': int,
          'ALTATD': int, #datetime
          'USRFLDA': str,
          'USRFLDB': str,
          'USRFLDC': str,
          'USRFLDD': str,
          'ASMASDTOT': int,
          'ASMASDLND': int,
          'ASMASDIMP': int,
          'ASMASDPRS': int,
          'ASMBSETOT': int,
          'ASMBSELND': int,
          'ASMBSEIMP': int,
          'ASMBSEPRS': int,
          'TOTACTVAL': int,
          'TOTACTLNDV': int,
          'TOTACTIMPV': int,
          'PYRTOTVAL': int,
          'TOTBSELNDA': int,
          'TOTBSEIMPA': int,
          'TOTBSEA': int,
          'TTD': int,
          'PAYCD': int,
          'GENPD': float,
          'FI': str,
          'SID': int,
          'SIDDST': str,
          'SIDASM': int,
          'GENBIL': float,
          'GENBIL1': float,
          'GENBIL2': float,
          'GENBIL3': float,
          'MOREOWN': str,
          'MOREVAL': int, #datetime
          'MORELGL': str,
          'MORESTT': int, #datetime
          'MORESLS': str,
          'BPCTYCD': str
}


# In[7]:


now = dt.datetime.utcnow()                                                        
logging.basicConfig(filename='ATSDTA_ATSP600_clean' + str(now) + '.log', level=logging.WARNING)

pnum = re.compile(r'^P\d{3}$') 
tickmarks = re.compile(r"^`+$")

CSVFILE2013 = '../data/JeffersonCo/JeffcoData Nov 2013/ATSDTA_ATSP600.txt'
CSVFILECLEAN2013 = '../data/JeffersonCo/JeffcoData Nov 2013/CLEANED_ATSDTA_ATSP600.csv'
#CSVFILECLEAN2013 =  '/Users/vmd/GitHub/Jeffco-Properties/Data/JeffersonCo/Datasets/test1.csv'

with open(CSVFILE2013, 'r', encoding='utf-8', errors='ignore', newline='') as csvread:
    reader = DictReader(csvread)
    with open(CSVFILECLEAN2013, 'w') as csvwrite:
        writer = DictWriter(csvwrite, delimiter=',', fieldnames=reader.fieldnames)
        writer.writeheader()
        for line in reader:
            for k,i in line.items():
                line[k] = i.strip(" ")
            if tickmarks.match(line['PRPZIP4']):
                line['PRPZIP4'] = ''
                logging.debug(' Cleaned "^`+$" match from line ' + line['SCH'] + ' PRPZIP4 ' + str(line['PRPZIP4']),) 
            if pnum.match(line['TTD']):
                line['TTD'] = line['TTD'].strip('P')
                logging.debug(' Cleaned "^P\d{3}$" match from line ' + line['SCH'] + ' TTD ' + str(line['TTD']),)
            if pnum.match(line['ATD']):
                line['ATD'] = line['ATD'].strip('P')
                logging.debug(' Cleaned "^P\d{3}$" match from line ' + line['SCH'] + ' ATD ' + str(line['ATD']),)
            if line['ALTATD'] == 'N99':
                line['ALTATD'] = ''
                logging.warning(""" Cleaned line['ALTATD'] match from line """ + line['SCH'] + ' ALTATD ' + str(line['ALTATD']),)
            for k,i in line.items():
                if i != '':
                    try:
                        DATASHAPE[k](line[k])
                        if DATASHAPE[k]==datefix:
                            line[k] = datefix(i)
                    except Exception as e:
                        logging.debug(' ' + k + ' is ' + str(e))
            writer.writerow(line)

