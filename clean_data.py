
import pandas as pd
import datetime as dt

def add_and_adjust_cols(df):
    '''
    Taking the raw list of current players of NBA rosters from our get_data functions, 
    this function cleans column headers, puts dates of birth in datetime format, and 
    puts height and weight in a format that is easier to calculate on.  It also adds a BMI column.  
    '''
    headers = ['position', 'number', 'name', 'height', 'weight', 'dob', 'college', 'team']
    nba_df = pd.DataFrame(data=df, columns=headers)
    nba_df.dob = nba_df.dob.str.replace('–', '-')       # need to find a way around those long hyphens besides manually
    nba_df.dob = pd.to_datetime(nba_df.dob)

    nba_df['current_age'] = nba_df.dob.apply(lambda x: (dt.datetime.now() - x).days / 365.25)
    nba_df['height_in'] = nba_df['height'].apply(lambda x: x.split('(')[0])
    nba_df['height_in'] = nba_df['height'].apply(lambda x: (int(x.split(' ')[0]) * 12) + (int(x.split(' ')[2])))
    nba_df['weight_int'] = nba_df['weight'].apply(lambda x: int(x.split(' ')[0]))
    nba_df['bmi'] = (703 * nba_df.weight_int) / (nba_df.height_in**2)

    return nba_df