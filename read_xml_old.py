from lxml import etree
import os
import csv
from unidecode import unidecode
import pandas as pd

def get_filenames(sstr):
    ''' returns a list of filenames in the current directory that contain sstr '''
    filenames = [f for f in os.listdir('.') if os.path.isfile(f) and sstr in f]
    print "Gathering filenames."
    return filenames

def parse_date(date_string):
    ''' parse date to month/day/year '''
    mon_day, year = date_string.split(',')
    words = mon_day.split()
    day, month, year = words[-1], words[-2].lower(), year.strip()
    months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    month_str = '0' 
    for i, mnth in enumerate(months, 1):
        if mnth in month:
            month_str = str(i)
    return month_str + '/' + day + '/' + year

def parse_xml(tree):
    ''' parse desired elements in xml file '''
    required_header = tree.find('required_header')
    download_date_raw = required_header.find('download_date').text
    download_date = parse_date(download_date_raw)
    url = unidecode(required_header.find('url').text)
       
    id_info = tree.find('id_info')
    ii_org_study_id = unidecode(id_info.find('org_study_id').text)
    ii_nct_id = unidecode(id_info.find('nct_id').text)

    brief_title = unidecode(tree.find('brief_title').text)

    brief_summary = tree.find('brief_summary')
    bs_textblock = ' '.join([word for word in (brief_summary.find('textblock').text).split()])
    bs_textblock = unidecode(bs_textblock.replace(',',''))

    start_date = unidecode(tree.find('start_date').text)

    completion_date = unidecode(tree.find('completion_date').text)

    phase = tree.find('phase').text

    primary_outcome = tree.find('primary_outcome')
    po_measure = ' '.join([word for word in (primary_outcome.find('measure').text).split()])
    po_measure = unidecode(po_measure.replace(',',''))
    # for multiple outcomes use:
    # primary_outcomes = tree.xpath("//primary_outcome") 
    
    condition = unidecode((tree.find('condition').text).replace(',',''))

    arm_group = tree.find('arm_group')
    # below is check I should use for elements that may not exist 
    if arm_group is not None: 
        ag_label = unidecode((arm_group.find('arm_group_label').text).replace(',',''))
    else:
        ag_label = ' '

    eligibility = tree.find('eligibility')
    el_crit = eligibility.find('criteria')
    el_crit_textblock_words = unidecode((el_crit.find('textblock').text).replace(',','')).split()
    el_crit_textblock = ' '.join(word for word in el_crit_textblock_words)

    row = [download_date, ii_nct_id, ii_org_study_id, url, brief_title, bs_textblock,
           start_date, completion_date, phase, po_measure, condition,
           ag_label, el_crit_textblock]
    return row


if __name__ == '__main__':
    # Inputs 
    filename_search_str = 'NCT' # uses this string to find files to parse in cwd
    outputfile = 'outfile.csv' # csv where parsed results are stored
    
    # Calcuations
    print "\nProgram starting."
    rows = []
    fnames = get_filenames(filename_search_str)
    print "There are {0} files to parse.".format(len(fnames))
    columns = ['download_date', 'nct_id', 'org_study_id', 'url', 'brief_title', 'brief_summary',
               'start_date', 'completion_date', 'phase', 'primary_outcome_measure', 'condition',
               'arm_group_label', 'eligibility']
    with open(outputfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(columns)
        for fname in fnames:
            print "Parsing {0}".format(fname)
            tree = etree.parse(fname)
            row = parse_xml(tree)
            writer.writerow(row)
    print "\nParsed data available in file: {0}".format(outputfile)
    print "Program completed.\n"
    df = pd.read_csv(outputfile)

   
