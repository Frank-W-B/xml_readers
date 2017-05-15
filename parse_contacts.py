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

def parse_tree(tree, tags):
    text_field = " " 
    child = []
    for i, tag in enumerate(tags):
        if i == 0:
            child.append(tree.find(tag))
        else:
            child.append(child[i-1].find(tag))
        if child[i] is None:
            break
        if i == len(tags)-1:
            text_field = check_type(child[i].text)
    return text_field

def parse_subtree(element, tags):
    child = [] 
    for i, tag in enumerate(tags):
        if i == 0:
            child.append(element.find(tag))
        else:
            child.append(child[i-1].find(tag))
        if child[i] is None:
            return " "
        if i == len(tags)-1:
            return check_type(child[i].text)
    
def parse_location(tree):
    locations = tree.xpath("//location")
    facility_tags = ['facility','name']
    city_tags = ['facility', 'address', 'city']
    zip_tags = ['facility', 'address', 'zip']
    country_tags = ['facility', 'address', 'country']
    contact_tags = ['contact','last_name']
    email_tags = ['contact', 'email']

    facilities = []
    cities = []
    zips = []
    countries = []
    contacts = []
    emails = []
    row_data = []
    
    for location in locations:
        facilities.append(parse_subtree(location, facility_tags))
        cities.append(parse_subtree(location, city_tags))
        zips.append(parse_subtree(location, zip_tags)) 
        countries.append(parse_subtree(location, country_tags))
        contacts.append(parse_subtree(location, contact_tags))
        emails.append(parse_subtree(location, email_tags))
    for i in range(len(locations)):
        row_data.append([facilities[i], cities[i], zips[i], countries[i],
                        contacts[i], emails[i]])
    return row_data

if __name__ == '__main__':
    # Inputs 
    filename_search_str = 'NCT' # uses this string to find files to parse in cwd
    outputfile = 'raw_contacts.csv' # csv where parsed results are stored
    nctid_tags = ['id_info', 'nct_id']
    condition_tags = ['condition']
    columns = ['nct_id', 'condition', 'facility', 'city', 'zip', 'country', 
               'contact', 'email']
    out_interval = 5000
    
    # Calcuations
    nctids_processed = set() 
    print "\nProgram starting."
    fnames = get_filenames(filename_search_str)
    num_studies = len(fnames)
    print "There are {0} files to parse.\n".format(num_studies)
    num_processed = 0 
    with open(outputfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(columns)
        for fname in fnames:
            tree = etree.parse(fname)
            nct_id = parse_tree(tree, nctid_tags)
            condition = parse_tree(tree, condition_tags)
            location_data = parse_location(tree)
            for loc in location_data:
                # check if email address exists
                if loc[5] != ' ': 
                    facility, city, zipcode = loc[0], loc[1], loc[2]
                    country, contact, email = loc[3], loc[4], loc[5]
                    row = [nct_id, condition, facility, city, zipcode, country,
                           contact, email]
                    writer.writerow(row)
                    nctids_processed.add(nct_id)
            num_processed += 1
            if num_processed % out_interval == 0:
                print "Processed {0} files.".format(num_processed)
    print "\nParsed data available in file: {0}".format(outputfile)
    num_studies_with_data = len(nctids_processed)
    print "\nOf {0} studies, {1} are represented in the output.".format(num_studies,
                                                                       num_processed)
    print "Program completed.\n"

   
