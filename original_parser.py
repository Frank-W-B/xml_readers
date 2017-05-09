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

def parse_xml(tree):
    ''' brief title ''' 
    brief_title = unidecode(tree.find('brief_title').text)
    
    ''' find sponsors and collaborators '''
    lead_sponsor = 'None'
    collaborator = 'None'
    sponsors = tree.find('sponsors')
    if sponsors is not None:
        lead_sponsor_tag = sponsors.find('lead_sponsor')
        if lead_sponsor_tag is not None:
            lead_sponsor = unidecode(lead_sponsor_tag.find('agency').text)
        collaborator_tag = sponsors.find('collaborator')
        if collaborator_tag is not None:
            collaborator = unidecode(collaborator_tag.find('agency').text)

    ''' find drug name in intervention '''
    drug = 'None' # default value
    intervention = tree.find('intervention')
    if intervention is not None:
        drug = unidecode(intervention.find('intervention_name').text)

    ''' finding contact information '''
    # default values
    first_name = 'None'
    last_name = 'None'
    email = 'None'
    overall_contact = tree.find('overall_contact')
    if overall_contact is not None:
        first_name_tag = overall_contact.find('first_name')
        if first_name_tag is not None:
            first_name = unidecode(overall_contact.find('first_name').text)
        last_name_tag = overall_contact.find('last_name')
        if last_name_tag is not None:
            last_name = unidecode(overall_contact.find('last_name').text)
        email_tag = overall_contact.find('email')
        if email_tag is not None:
            email = unidecode(overall_contact.find('email').text)
    row = [brief_title, lead_sponsor, collaborator, drug, first_name, last_name, email]
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
    columns = ['brief_title', 'lead_sponsor', 'collaborator', 'drug', 'first_name', 'last_name', 'email']
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

   
