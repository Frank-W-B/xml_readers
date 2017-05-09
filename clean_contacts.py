import pandas as pd





if __name__ == '__main__':
    filename_raw = 'raw_contacts.csv'
    filename_cleaned = 'cleaned_contacts.csv'
    df = pd.read_csv(filename_raw)
    df_contacts = df[~pd.isnull(df['contact_name'])]
    df_contacts = df_contacts[['contact_name','contact_phone','contact_phone_ext','contact_email']]
    df_contacts = df_contacts[~(pd.isnull(df_contacts['contact_phone']) & pd.isnull(df_contacts['contact_email']))]
    df_contacts.columns = ['name','phone','phone_ext','email']
    
    df_backups = df[~pd.isnull(df['backup_name'])]
    df_backups = df_backups[['backup_name','backup_phone','backup_phone_ext','backup_email']]
    df_backups = df_backups[~(pd.isnull(df_backups['backup_phone']) & pd.isnull(df_backups['backup_email']))]
    df_backups.columns = ['name','phone','phone_ext','email']

    print "Raw data read in {0}".format(filename_raw)
    print "              Rows in raw file: {0}".format(df.shape[0])
    print " Rows of contacts before merge: {0}".format(df_contacts.shape[0])
    print "  Rows of backups before merge: {0}".format(df_backups.shape[0])

    df_list = [df_contacts, df_backups]
    df_merged = pd.concat(df_list)

    print "      Rows of merged dataframe: {0}".format(df_merged.shape[0])

    df_merged.sort_values(by='name',inplace=True)
    df_merged.drop_duplicates(inplace=True)
    
    print "Rows after dropping duplicates: {0}".format(df_merged.shape[0])

    df_merged.to_csv(filename_cleaned, index = False)

    print "Clean contacts written to {0}".format(filename_cleaned)

    
