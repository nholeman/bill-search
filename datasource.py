'''
This file handles the data source. Its primary function is to return an 
iterable that the main file can use to to check for matches.
'''
import re
import html
import os.path

from zipfile import ZipFile
import xml.etree.ElementTree as elementtree

DEFAULT_FILE='Data Engineering Deliverable - BILLSTATUS-116-sres.zip'


class DataSource:
    '''
    A class to the data source for the billsearch tool.

    ...

    Attributes
    ----------
    file_dir : string
        represents the location of the files that the billsearch tool
        will be searching through

    Methods
    -------
    get_file_name()
        returns the location of the file
    find_file_dir()
        returns a boolean indicating whether the file could be found
    get_iter()
        creates a generator which yields (bill_id,summary) tuples
    '''

    def __init__(self, file_dir=DEFAULT_FILE):
        '''
        Parameters
        ----------
        file_dir : str
            file location of the data source. Unless otherwise specified,
            DEFAULT_FILE is used.
        '''
        self.file_dir = file_dir
    

    def get_file_name(self):
        '''
        Returns location of the file
        '''
        return(self.file_dir)


    def find_file_dir(self):
        '''
        Returns a boolean indicating whether the file could be found
        '''
        return(os.path.exists(self.file_dir))


    def get_iter(self):
        '''
        Creates a generator which yields (bill_id,summary) tuples.
        Using the Zipfile library, this method searches through all files in
        the zipped data source. 
        Using the ElementTree library, this attempts to parse each file as
        xml. If the file can be parsed, the billNumber and billType are found,
        and all 'item's under billSummaries are found.
        If the file cannot be parsed as xml--or if there are no summaries--
        the method continues to the next file without yielding anything.
        '''
        with ZipFile(self.file_dir) as zip_dir:
            for name in zip_dir.namelist():
                bill = zip_dir.read(name)
                try:
                    root = elementtree.fromstring(bill)
                except elementtree.ParseError: 
                    continue

                billNumber = [elem.text for elem in root.iter('billNumber')][0]
                billType = [elem.text for elem in root.iter('billType')][0]
                bill_id = '{} {}'.format(billType, billNumber)

                summaries = []
                for elem in root.iter('billSummaries'):
                    for e in elem.findall("./item/text"):
                        text = clean_text(e.text)
                        summaries.append(text)
                if not summaries:
                    continue

                yield(bill_id, summaries[0])


def clean_text(text):
    '''
    This function cleans up Bill summary text, removing html tags,
    unescapes html entities, and strips leading/trailing whitespace.
    '''
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = html.unescape(text)
    text = text.strip()

    return(text)