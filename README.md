# bill-search
Command Line Tool for Searching Senate Resolution Bills in the 116th session that
have a summary which matches a particular regular expression for bills in a 
supplied .zip file.


# Installing Dependencies
These instructions assume that you are using Python 3 (3.7.4 to be exact).

Then, using pip, install the required libraries.

`pip install -r requirements.txt`


# bill-search Examples
For help with the tool, use the help option:

`python billsearch.py --help`

Without any options, the tool can be used like this:
```
$ python billsearch.py "technology"
Searching through Data Engineering Deliverable - BILLSTATUS-116-sres.zip

Number of bills that match: 3

SRES 103
SRES 259
SRES 331
```

You can also specify the show_text option. Matching text will be underlined (though not shown in example below).
```
$ python billsearch.py "technology" --show_text True
Searching through Data Engineering Deliverable - BILLSTATUS-116-sres.zip

Number of bills that match: 3

SRES 103
This resolution supports the designation of National Assistive Technology Awareness Day.  It also 
commends assistive technology specialists, program coordinators, organizations, and researchers for 
their assistance in helping people with disabilities to access such technology.

SRES 259
This resolution expresses the Senate's position that world leadership in the implementation of 
5G wireless technology is a national priority.

SRES 331
This resolution instructs Senate conferees on the conference committee for S. 1790 (National Defense 
Authorization Act for Fiscal Year 2020) to insist upon inclusion of the provisions of S. 2118 (Defending 
America's 5G Future Act), which relates to Huawei Technologies Co. Ltd. and technology from foreign adversaries.
```

# Testing bill-search
You can run the unit tests with the following command:

`python test_billsearch.py`
