from sqlalchemy import create_engine, MetaData, Table
from decouple import config

import urllib

from sqlalchemy import create_engine, MetaData, Table, select, desc

def url_encode(word):
    """
        Encode the given word in URL format.
    """
    new_word = urllib.parse.quote(word.encode('utf-8'), safe='')
    return new_word

def is_prime(n, i=2):
    """
        Check if integer n is a prime number.
    """
    if n <= 2:
        return n == 2
    if n % i == 0:
        return False
    if i * i > n:
        return True
    return is_prime(n, i + 1)


def sort_players():
    """
        Connect the database using sqlalchemy and  retrieve all players data sorted by their names (in alphabetical order).
    """
    database = f"postgresql+psycopg2://{config('DB_USER')}:{url_encode(config('DB_PASSWORD'))}@{config('DB_HOST')}/{config('DB_NAME')}"

    engine = create_engine(database, pool_pre_ping=True)
    metadata = MetaData()

    players_table = Table('players', metadata, autoload_with=engine)
    teams_table = Table('teams', metadata, autoload_with=engine)

    #selected the tables join the table with the condition order by reverse alphabet order of player name and team name
    query = select(players_table, teams_table).join(teams_table, 
            players_table.c.team_id == teams_table.c.team_id).order_by(
            desc(players_table.c.name), desc(teams_table.c.name))

    with engine.connect() as connection:
        sorted_players = connection.execute(query).fetchall()

    sorted_list = [] 
    count = 0
    for player in sorted_players:
        if is_prime(player.jersey_no):
            print(player._fields)
            sorted_list.append(f"{player.name}, {player.name_1}")
            count += 1

    return sorted_list

sorted_playrs = sort_players()
print("---------Task 3 output----------")

for playr in sorted_playrs:
    print(playr)

print("---------End 3 output----------")

