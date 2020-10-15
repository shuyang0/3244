import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

#read data from Match.csv, extract columns into pandas dataframe
data = pd.read_csv (r'Match.csv')
matches = pd.DataFrame(data , columns= ['id', 'league_id', 'home_team_goal','away_team_goal', 'home_player_1','home_player_2','home_player_3',\
                                        'home_player_4','home_player_5','home_player_6','home_player_7','home_player_8','home_player_9','home_player_10',\
                                        'home_player_11','away_player_1','away_player_2','away_player_3','away_player_4','away_player_5','away_player_6',\
                                        'away_player_7','away_player_8','away_player_9','away_player_10','away_player_11'])


#drop rows with missing information
matches = matches.dropna()

#convert all values to int
matches = matches.astype(int)

#take only EPL matches (league_id  == 1729)
matches = matches.loc[matches['league_id'] == 1729 ]

matches['goal_diff'] = 0
home_win = matches['home_team_goal'] > matches['away_team_goal']
away_win = matches['home_team_goal'] < matches['away_team_goal']
matches.loc[home_win, 'goal_diff'] = 1
matches.loc[away_win, 'goal_diff'] = -1

#remove columns not used in ML model
matches = matches.drop('home_team_goal', axis = 1)
matches = matches.drop('away_team_goal', axis = 1)
matches = matches.drop('id', axis = 1)
matches = matches.drop('league_id', axis = 1)


#read data from Player_Attributes.csv, extract columns into pandas dataframe
data = pd.read_csv (r'Player_Attributes.csv')   
players = pd.DataFrame(data , columns= ['player_api_id','overall_rating'])

#drop rows with missing information
players = players.dropna()

#take only the first instance of each player (because csv has different player ratings for different seaons
players = players.drop_duplicates(subset=['player_api_id'])


#replace all player id in matches with their ratings
for i in range(1,12):
    curr = 'home_player_' + str(i)
    matches[curr] = matches[curr].map(players.set_index('player_api_id')['overall_rating'])

for i in range(1,12):
    curr = 'away_player_' + str(i)
    matches[curr] = matches[curr].map(players.set_index('player_api_id')['overall_rating'])


print(matches)

X = matches.drop('goal_diff', axis = 1)
y = matches['goal_diff']

X_train, X_test, y_train,  y_test = train_test_split(X, y, test_size = 0.20)


clf = DecisionTreeClassifier(random_state=0)
#print(cross_val_score(clf, X, y, cv=10))

clf_2 = DecisionTreeClassifier()
clf_2 = clf_2.fit(X_train,y_train)



##model = SVC(C = 1.0, kernel = 'rbf')
##model.fit(X_train, y_train)
y_pred = clf_2.predict(X_test)
matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)
print(matrix)
print(report)



