#!/usr/bin/env python3

import contextlib
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
        players = load_players(cursor)
        factions = load_factions(cursor)
        subfactions = load_subfactions(cursor)

        builder = tt.ShowDataBuilder()

        showdata = builder.build(input_data, games, showtypes, players, factions, subfactions)

        show_id = add_show(showdata, cursor)

        add_army(show_id, showdata.army1, cursor)
        if showdata.army2:
            add_army(show_id, showdata.army2, cursor)

        conn.commit()

if __name__ == '__main__':
    main()
