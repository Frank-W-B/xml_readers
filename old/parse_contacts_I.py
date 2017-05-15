from lxml import etree
import os
import csv
from unidecode import unidecode

def get_filenames(sstr):
    ''' returns a list of filenames in the current directory that contain sstr '''
    filenames = [f for f in os.listdir('.') if os.path.isfile(f) and sstr in f]
    print "Gathering filenames."
    return filenames

def check_type(text):
    ''' checks if the text is type string and will call unidecode if not '''
    if isinstance(text, str):
        return text
    else:
        return unidecode(text)

def parse_xml(tree):
    '''nct_id''' 
    nct_id = None
    id_info = tree.find('id_info')
    if id_info is not None:
        nct_id = id_info.find('nct_id')
        if nct_id is not None:
            nct_id = check_type(nct_id.text)
    
    '''location'''
    facility_name = None
    location = tree.find('location')
    if location is not None:
        facility = location.find('facility')
        if facility is not None:
            facility_name = facility.find('name')
            if facility_name is not None:
                facility_name = check_type(facility_name.text)

    '''contact'''
    contact_name = None
    contact_phone = None
    contact_ext = None
    contact_email = None
    location = tree.find('location')
    if location is not None:
        contact = location.find('contact')
        if contact is not None:
            contact_name = contact.find('last_name')
            if contact_name is not None:
                contact_name = check_type(contact_name.text)
            contact_phone = contact.find('phone')
            if contact_phone is not None:
                contact_phone = check_type(contact_phone.text) 
            contact_ext = contact.find('phone_ext')
            if contact_ext is not None:
                contact_ext = check_type(contact_ext.text)
            contact_email = contact.find('email')
            if contact_email is not None:
                contact_email = check_type(contact_email.text)
    
    '''backup contact'''
    backup_name = None
    backup_phone = None
    backup_ext = None
    backup_email = None
    location = tree.find('location')
    if location is not None:
        backup = location.find('contact_backup')
        if backup is not None:
            backup_name = backup.find('last_name')
            if backup_name is not None:
                backup_name = check_type(backup_name.text)
            backup_phone = backup.find('phone')
            if backup_phone is not None:
                backup_phone = check_type(backup_phone.text) 
            backup_ext = backup.find('phone_ext')
            if backup_ext is not None:
                backup_ext = check_type(backup_ext.text)
            backup_email = backup.find('email')
            if backup_email is not None:
                backup_email = check_type(backup_email.text)

    row = [nct_id, facility_name,
           contact_name, contact_phone, contact_ext, contact_email,
           backup_name, backup_phone, backup_ext, backup_email]
    return row


if __name__ == '__main__':
    # Inputs 
    filename_search_str = 'NCT' # uses this string to find files to parse in cwd
    outputfile = 'raw_contacts.csv' # csv where parsed results are stored
    # Calcuations
    print "\nProgram starting."
    rows = []
    fnames = get_filenames(filename_search_str)
    print "There are {0} files to parse.".format(len(fnames))
    columns = ['nct_id', 'facility',
               'contact_name', 'contact_phone', 'contact_phone_ext', 'contact_email',
               'backup_name', 'backup_phone', 'backup_phone_ext', 'backup_email']
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

   
