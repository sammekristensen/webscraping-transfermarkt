import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
page = 'https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=2022&s_w=s&leihe=0&intern=0'
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

# Create the Lists for each attribute raw
Player = pageSoup('div', {'class': 'responsive-table'})
Age = pageSoup.find_all('td', {'class': 'zentriert alter-transfer-cell'})
Nationallity = pageSoup('td', {'class': 'zentriert nat-transfer-cell'})
Clubb = pageSoup('td', {'class': 'no-border-links verein-flagge-transfer-cell'})
Fee = pageSoup('td', {'class': 'rechts'})
Position = pageSoup('td', {'class': 'pos-transfer-cell'})

# AgeList 258 items
AgeList = re.findall(r'\d+', str(Age))
AgeList = list(map(int, AgeList))

# PlayerList 258 items
PlayerList = []
IOList = []
for IO in Player:
    inout = IO.find_all('th', {'class':'spieler-transfer-cell'})
    ans=str(inout).split('">')[1].split('</')[0]

    players = IO.find_all('span', {'class': 'hide-for-small'})
    for item in players:
        title = item.find('a').get('title')
        PlayerList.append(str(title))
        IOList.append(ans)


# NationallityList 258 items
data = str(Nationallity)
NationallityList = []
for item in data.split('</td>')[:-1]:
    title = item.split('title="')[1].split('"')[0]
    if '<br/>' in title:
        title = title.split('<br/>')[0]
    NationallityList.append(title)

# Clubblist 258 items
ClubbList = []
for clubbs in Clubb:
    title = clubbs.find_all('a')
    if len(title) == 0:
        ClubbList.append('retired')
    else:
        for team in title:
            ClubbList.append(team['title'])

# FeeList 258 items
FeeList = []
for players in Fee:
    player = players.find_all('a')
    if len(player) == 0:
        pass
    else:
        FeeList.append(str(player).split('">')[1].split('<')[0])

# Convert to float numbers (in €)
count = 0
for item in FeeList:
    if 'm' in item:
        FeeList[count] = float(item.split('€')[1].split('m')[0])*1000000
        count +=1
    elif 'k' in item:
        FeeList[count] = float(item.split('€')[1].split('k')[0])*1000
        count+=1
    else:
        count +=1

# PositionList 258 items
PositionList = []
for player in Position:
    PositionList.append(str(player).split('">')[1].split('</')[0])


print(len(ClubbList))
print(len(NationallityList))
print(len(PlayerList))
print(len(AgeList))
print(len(FeeList))
print(len(PositionList))
print(len(IOList))

final_df = pd.DataFrame({'Player': PlayerList,
                         'Age': AgeList,
                         'Position': PositionList,
                         'Nationallity': NationallityList,
                         'Clubb': ClubbList,
                         'In/Out': IOList,
                         'Fee': FeeList})


#final_df.drop_duplicates(subset=['Player'])
print(final_df)
final_df.to_csv('transfer_fee_pl_22')