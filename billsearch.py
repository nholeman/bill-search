import os
import re

import click

from datasource import DataSource 


@click.command()
@click.option('--file_dir', default=None, help='Specify if desired file is not default.')
@click.option('--show_text/--no_text', default=False, \
              help='If --show_text, print text with matching section highlighted. ' \
                    'Default is --no_text')
@click.argument('search_expr')
def bill_search(search_expr, file_dir, show_text):
    '''
    This tool will search through a collection of Senate Resolution Bills.

    SEARCH_EXPR is the regular expression that will be used to find matching bills.
    
    \b
    Examples: 
        python billsearch.py "American \w+ Bureau"
        python billsearch.py --show_text True "American \w+ Bureau"
    '''

    ds = DataSource() if file_dir is None else DataSource(file_dir)
    
    if ds.find_file_dir():
        click.echo('Searching through {}\n'.format(ds.get_file_name()))
    else:
        click.echo('File not found. Please specify a valid path to the data source.\n')
        exit(1)

    matches = matches_with_substrings(ds, search_expr) if show_text else \
              simple_matches(ds, search_expr)

    click.echo('Number of bills that match: {}\n'.format(len(matches)))

    for bill_id,text_info in sorted(matches.items(), key = lambda x: int(x[0].split()[1])):
        click.echo(bill_id)
        if show_text:
            click.echo(display_matching_substring(text_info))



def simple_matches(ds, expr):
    '''
    This function uses the data source iterator and the search expression 
    to find bills that match. A dictionary of bill_id: text is returned.
    '''
    matches = {bill_id: text for bill_id,text in ds.get_iter() if re.search(expr,text)}
    return(matches)


def matches_with_substrings(ds, expr):
    '''
    This function uses the data source iterator and the search expression 
    to find bills that match *and* pinpoints the locations of all matches.
    A dictionary is returned where the key is bill_id and the value is a
    (text, matching_substrings) tuple.
    '''
    matches = {}
    for bill_id,text in ds.get_iter():
        matching_substrings = [(m.start(),m.end()) for m in re.finditer(expr, text)]
        if matching_substrings:
            matches[bill_id] = (text, matching_substrings)
    return(matches)


def display_matching_substring(text_and_matches):
    '''
    This function prints the bill summary text with the matching
    substring(s) underlined.
    '''
    text = text_and_matches[0]
    matches = text_and_matches[1]

    underline = '\033[4m'
    end_underline = '\033[0m'

    string = ''
    placeholder = 0
    for start,end in matches:
        string += text[placeholder:start]
        string += '{}{}{}'.format(underline,text[start:end],end_underline)
        placeholder=end
    string += '{}\n'.format(text[placeholder:])

    return(string)


if __name__ == '__main__':
    bill_search()