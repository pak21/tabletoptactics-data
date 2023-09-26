#!/usr/bin/env python3

import contextlib
import datetime
import sys

import psycopg2

import tabletoptactics as tt

def load_objects(objecttype, table, cursor):
    cursor.execute(f'select {objecttype}, id from {table}')
    return dict(cursor.fetchall())

def load_games(cursor):
    return load_objects('game', 'games', cursor)

def load_showtypes(cursor):
    return load_objects('showtype', 'showtypes', cursor)

def load_factions(cursor):
    return load_objects('faction', 'factions', cursor)

def load_subfactions(cursor):
    cursor.execute(f'select s.id, s.subfaction, f.id, f.faction from subfactions as s join factions as f on s.faction_id = f.id')
    return {s: (sid, f, fid) for sid, s, fid, f in cursor.fetchall()}

def load_players(cursor):
    return load_objects('nickname', 'players', cursor)

def input_army_details(n, army, factions, subfactions, players, input_data):
    prefix = f'army{n}'
    player = getattr(input_data, prefix + 'player')
    if army:
        if player is None:
            raise Exception(f'Must have a player for the {army.faction} army')
    else:
        if player is None:
            return None
        faction = getattr(input_data, prefix + 'faction')
        army = tt.ArmyInfo(faction_id=factions[faction], faction=faction)

    army.player_id = players[player]

    if army.subfaction_id is None:
        subfaction = getattr(input_data, prefix + 'subfaction')
        army.subfaction_id = subfactions[subfaction][0] if subfaction else None

    return army

def add_show(showdata, cursor):
    cursor.execute('insert into shows(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id) values (%s, %s, %s, %s, %s, %s) returning id', (showdata.release_date, showdata.game_id, showdata.showtype_id, showdata.slug, showdata.youtube_slug, showdata.servoskull_id))
    return cursor.fetchall()[0][0]

def add_army(show_id, army, cursor):
    cursor.execute('insert into armies(show_id, player_id, faction_id, subfaction_id, winner, codex_edition) values (%s, %s, %s, %s, %s, %s)', (show_id, army.player_id, army.faction_id, army.subfaction_id, army.winner, army.edition))

def main():
    conn = psycopg2.connect('dbname=tabletoptactics')

    with open(sys.argv[1]) as f:
        input_data = tt.parse_input(f.read())

    with contextlib.closing(conn.cursor()) as cursor:
        games = load_games(cursor)
        showtypes = load_showtypes(cursor)
        factions = load_factions(cursor)
        subfactions = load_subfactions(cursor)
        players = load_players(cursor)

        release_date, slug = tt.parse_url(input_data.url)

        game_id, game = tt.get_game(slug, games, input_data.game)
        showtype_id = tt.get_showtype(slug, showtypes, input_data.showtype)

        army1, army2 = tt.extract_armies_from_slug(slug, factions, subfactions)

        army1 = input_army_details(1, army1, factions, subfactions, players, input_data)
        army2 = input_army_details(2, army2, factions, subfactions, players, input_data)
        if army2:
            winner = input_data.winner
            winner_id = players[winner] if winner else None
        else:
            winner_id = None

        army1.winner = army1.player_id == winner_id if winner_id else None
        army1.edition = tt.get_edition(army1, game, release_date)
        if army2:
            army2.winner = army2.player_id == winner_id if winner_id else None
            army2.edition = tt.get_edition(army2, game, release_date)

        servoskull = input_data.servoskull
        servoskull_id = players[servoskull] if servoskull else None

        showdata = tt.ShowData(release_date, slug, input_data.youtube, game_id, showtype_id, servoskull_id, army1, army2)

        if True:
            print()
            print(showdata)

            raise Exception('x')

        show_id = add_show(showdata, cursor)

        add_army(show_id, showdata.army1, cursor)
        if showdata.army2:
            add_army(show_id, showdata.army2, cursor)

        conn.commit()

if __name__ == '__main__':
    main()
