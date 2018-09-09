
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def build_episode_df():

    ''' Don't hide any rows in the output '''
    pd.set_option("display.max_rows", None)

    url = 'https://en.wikipedia.org/wiki/List_of_The_Office_(U.S._TV_series)_episodes#Episodes'
    ''' Pull the data from the Wikipedia page for 'List of The Office Episodes' '''
    html = requests.get(url).content
    ''' Pull the html into Pandas and don't include the header, so it's easier to df '''
    df_list = pd.read_html(html, skiprows=1, index_col=None)
    ''' Only care about the tables with episodes'''
    raw_episodes = df_list[1:10]

    ''' df the 0s into 1 dataframe '''
    df = pd.concat(raw_episodes)

    def two_parters():

        ''' Append the 2-part episodes to the end of the dataframe '''
        title = df.iloc[:,2]
        i = -1
        rows = []
        for x in title:
            i += 1
            row = df.iloc[i]
            if '‡' in x:
                rows.append(row)
            elif '*' in x:
                rows.append(row)
        return rows
    
    
    ''' Append the two parters to the end of the dataframe'''   
    df = pd.DataFrame.append(df, two_parters())
    
    ''' Convert air date to datetime format'''
    df[5] = pd.to_datetime(df[5])

    ''' Sort by air date '''
    df = df.sort_values(by=[5])
       
    ''' Clean-up some characters from the html'''                                        
    df[7] = df[7].str.split('[', expand=True) 
    for symbol in ['*', '‡', '†']:
        df[2] = df[2].str.split(symbol, expand=True)
   
    ''' Fix index numbers '''
    df.index = range(1,204)

    ''' Rename columns '''
    df.columns = ['Season', 'Episode', 'Title', 'Directed by', 'Written by', 
                'Original air date', 'Prod code', 'US viewers(mil)']
    df.pop('Prod code')

    ''' Set Seasons '''
    df.loc[0:7, 'Season'] = 1
    df.loc[7:29, 'Season'] = 2
    df.loc[29:54, 'Season'] = 3
    df.loc[54:73, 'Season'] = 4
    df.loc[73:101, 'Season'] = 5
    df.loc[101:127, 'Season'] = 6
    df.loc[127:153, 'Season'] = 7
    df.loc[153:177, 'Season'] = 8
    df.loc[177:203, 'Season'] = 9

    ''' Set Episodes '''
    df.loc[0:7, 'Episode'] = range(1,8)
    df.loc[7:29, 'Episode'] = range(1,24)
    df.loc[29:54, 'Episode'] = range(1,27)
    df.loc[54:73, 'Episode'] = range(1,21)
    df.loc[73:101, 'Episode'] = range(1,30)
    df.loc[101:127, 'Episode'] = range(1,28)
    df.loc[127:153, 'Episode'] = range(1,28)
    df.loc[153:177, 'Episode'] = range(1,26)
    df.loc[177:203, 'Episode'] = range(1,28)

    print(df)
    return(df)

def plot_it():

    ''' Get the stack '''
    stack = build_episode_df()
    ''' X axis '''
    episodes= []
    for x in range(1,204):
        episodes.append(x)
    ''' Y axis'''
    viewers = stack['US viewers(mil)'].astype(float)
   
    plt.margins(1)
    plt.axis([0, 204, 3, 24])
    plt.xlabel('Episode')
    plt.ylabel('US Viewers (millions)')
    plt.title('The Office (US) Ratings')
    plt.bar(episodes, viewers)

    plt.show()

plot_it()