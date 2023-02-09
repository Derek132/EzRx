import pandas as pd
from datetime import datetime, timedelta

def search_type(search_string):
    if ":" in search_string:
        request_keywords = search_string.strip().split(':')
        return 'special_search_request'
    else:
        return 'default search_request'

# def recipient_search(search_string):
#
#     search_param = len(search_keys)
#
#
#     if search_param == 0:
#         print('Empty search_string! Return 0')
#         return 0
#     elif search_param ==1:
#         print('1 condition Search. search_keys: ', search_keys)
#
#         '''
#             Possibility:
#                 1. lastName or firstName.
#                     Requirement: isNumeric == False
#                     Search Method: search partial match in patientFullName
#                 2. DOB:
#                     Requirement: isNumber == True, Format = mmddyy
#                     Search Method:???
#                 3. Phone:
#                     Requirement: isNumber == True, Format = xxxx (last 4 digits)
#                     Search Method:???
#         '''
#
#         return search_keys
#     else:
#         print('Too Many Search Conditions! Return -1')
#         return -1


def recipient_search(search_input,recipient_csv_file_path):
    print('search for: ', search_input)
    headers = ['DoctorName', 'Street1', 'Phone', 'Fax', 'NPI', 'City', 'Zip', 'State', 'DEA','classification','notes']
    df = pd.read_csv(recipient_csv_file_path,
                     usecols=headers,
                     dtype={
                         'DoctorName': str,
                         'Street1':str,
                         'Phone': str,
                         'Fax':str,
                         'NPI': str,
                         'Zip': str,
                         'DEA': str,
                         'City': str,
                         'classification': str,
                         'notes': str
                     })

    result_df = pd.DataFrame()

    if search_type(search_input) == 'special_search_request':
        search_request = search_input.strip().split(':')
        special_request = search_request[0]
        search_keyword = search_request[1].strip()

        if special_request == 'add':        # Search Address
            print('Search Address: ', search_keyword)
            result_df = df[df['Street1'].str.contains(search_keyword, case=False, na=False)]

        elif special_request == 'phone':        # Search Phone
            print('Search Phone: ', search_keyword)
            result_df = df[df['Phone'].str.contains(search_keyword, case=False, na=False)]

    else:
        if "," in search_input:     # Multiple Condition Search: fullName & address
            search_keywords = search_input.strip().split(',')
            search_key_1 = search_keywords[0].strip()
            search_key_2 = search_keywords[1].strip()
            result_df = df[df['DoctorName'].str.contains(search_key_1, case=False, na=False)
                           & df['Street1'].str.contains(search_key_2, case=False, na=False)]

        else:   # Single Condition Search    # Search Recipient Full Name
            search_keyword = search_input
            result_df = df[df['DoctorName'].str.contains(search_keyword, case=False, na=False)]

    result_df = result_df.sort_values(by=['DoctorName'])

    print(result_df)
    return result_df


def auto_complete_drug_generator(dispensing_record_csv_path):
    '''
        Purpose: To Create a list of unique drug from pharmacy dispensing records (Can be use for auto complete)
        Output: A list of unique Drug (csv file)
    '''
    use_cols = ['DRUG NAME','GENERIC CODE']
    df = pd.read_csv(dispensing_record_csv_path,delimiter='|',usecols=use_cols).sort_values(by=['DRUG NAME'],ascending = True)
    df = df.drop_duplicates(subset=['GENERIC CODE']).reset_index(drop=True)
    df = df.drop(columns=['GENERIC CODE'])
    df.to_csv('auto_complete_drug_list.csv', index=False)
    print(df)


def read_quick_dial_csv(quick_dial_csv_file_path):
    headers = ['DoctorName', 'Street1', 'Phone', 'Fax', 'NPI', 'City', 'Zip', 'State', 'DEA', 'classification',	'notes']
    df = pd.read_csv(quick_dial_csv_file_path,
                     usecols=headers,
                     dtype={
                         'DoctorName': str,
                         'Street1':str,
                         'Phone': str,
                         'Fax':str,
                         'NPI': str,
                         'Zip': str,
                         'DEA': str,
                         'City': str,
                         'classification': str,
                         'notes': str
                     })

    df = df.sort_values(by=['DoctorName'])
    return df

def get_thermometer_data(thermometer_data_csv_file_path):
    headers = ['Pacific_TimeStamp', 'freezerTemp',	'fridgeTemp', 'CalibrationDueDate']
    # ,	'Battery', 'SerialNumber', 'DeviceKey', 'Model', 'Id', 'AccountId'

    df = pd.read_csv(thermometer_data_csv_file_path,
                     usecols=headers,
                     parse_dates=['Pacific_TimeStamp','CalibrationDueDate']).tail(48)

    df['Pacific_TimeStamp'] = df['Pacific_TimeStamp'].dt.tz_localize(None)

    # inplace=True is used to update the original DataFrame instead of creating a new one.
    df = df.drop_duplicates(subset=['Pacific_TimeStamp'])

    df = df.sort_values(by=['Pacific_TimeStamp'], ascending=False, inplace=False)
    last_datetime = df['Pacific_TimeStamp'].max()

    # current time
    now = datetime.now()

    # calculate time difference
    time_difference = pd.Timedelta(now - last_datetime)
    time_difference_in_seconds = time_difference.total_seconds()
    time_difference_in_minutes = round(time_difference_in_seconds / 60, 2)

    current_fridge_temp = df.loc[df['Pacific_TimeStamp'] == last_datetime, 'fridgeTemp'].values[0]
    current_freezer_temp = df.loc[df['Pacific_TimeStamp'] == last_datetime, 'freezerTemp'].values[0]

    # keep only the rows with datetime values within the last 24 hours
    df_last_24_hours = df.loc[df['Pacific_TimeStamp'] >= datetime.now() - timedelta(hours=24)]

    average_fridge_temp = round(df_last_24_hours['fridgeTemp'].mean(),2)
    average_freezer_temp = round(df_last_24_hours['freezerTemp'].mean(),2)

    thermometer_data_dict = {'df': df, 'last_datetime': last_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                             'current_fridge_temp':current_fridge_temp,
                             'current_freezer_temp':current_freezer_temp,
                             'average_fridge_temp':average_fridge_temp,
                             'average_freezer_temp':average_freezer_temp,
                             'minutes_since_last_datetime': time_difference_in_minutes}

    return thermometer_data_dict

def sig_list_filter(search_key,sig_csv_file_path):
    print('Sig Input: ', search_key)
    headers = ['sig', 'translation', 'sig_translation']
    df = pd.read_csv(sig_csv_file_path,
                     usecols=headers,
                     dtype={
                         'sig': str,
                         'translation': str,
                         'sig_translation': str,

                     })

    result_df = pd.DataFrame()
    result_df = df[df['sig'].str.contains(search_key, case=False, na=False)]
    result_df = result_df.drop(columns=['sig_translation'])
    return result_df




# auto_complete_drug_generator(dispensing_record_csv_path=r'D:\__HelloRx Pharmacy\KC Corporation\O drive\report\autofill\option1_rxlog_filled_and_hold.csv')