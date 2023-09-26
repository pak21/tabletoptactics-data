#!/usr/bin/env python3

import contextlib
import datetime

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

def get_data(prompt):
    return input(prompt + '? ')

def input_missing(objtype):
    return get_data(f"Couldn't obtain {objtype} automatically, please input manually")

def input_army_details(n, army, factions, subfactions, players):
    player = get_data(f'Army {n} player') or None
    if army:
        if player is None:
            raise Exception(f'Must have a player for the {army.faction} army')
    else:
        if player is None:
            return None
        faction = get_data(f'Army {n} faction')
        army = tt.ArmyInfo(faction_id=factions[faction], faction=faction)

    army.player_id = players[player]

    if army.subfaction_id is None:
        subfaction = get_data(f'Army {n} subfaction')
        army.subfaction_id = subfactions[subfaction][0] if subfaction else None

    return army

def add_show(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id, cursor):
    cursor.execute('insert into shows(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id) values (%s, %s, %s, %s, %s, %s) returning id', (release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id))
    return cursor.fetchall()[0][0]

def add_army(show_id, army, winner, edition, cursor):
    cursor.execute('insert into armies(show_id, player_id, faction_id, subfaction_id, winner, codex_edition) values (%s, %s, %s, %s, %s, %s)', (show_id, army.player_id, army.faction_id, army.subfaction_id, winner, edition))

def main():
    conn = psycopg2.connect('dbname=tabletoptactics')

    with contextlib.closing(conn.cursor()) as cursor:
        games = load_games(cursor)
        showtypes = load_showtypes(cursor)
        factions = load_factions(cursor)
        subfactions = load_subfactions(cursor)
        players = load_players(cursor)

        raw_url = get_data('URL')
        release_date, slug = tt.parse_url(raw_url)

        game_id, game = tt.get_game(slug, games, lambda: input_missing('game'))
        showtype_id = tt.get_showtype(slug, showtypes, lambda: input_missing('show type'))

        army1, army2 = tt.extract_armies_from_slug(slug, factions, subfactions)

        youtube_slug = get_data('YouTube slug') or None

        army1 = input_army_details(1, army1, factions, subfactions, players)
        army2 = input_army_details(2, army2, factions, subfactions, players)
        if army2:
            winner = get_data('Winner') or None
            winner_id = players[winner] if winner else None
        else:
            winner_id = None

        servoskull = get_data('Servoskull')
        servoskull_id = players[servoskull] if servoskull else None

        army1_is_winner = army1.player_id == winner_id if winner_id else None
        army1_edition = tt.get_edition(army1, game, release_date)
        if army2:
            army2_is_winner = army2.player_id == winner_id if winner_id else None
            army2_edition = tt.get_edition(army2, game, release_date)

        show_id = add_show(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id, cursor)

        add_army(show_id, army1, army1_is_winner, army1_edition, cursor)
        if army2:
            add_army(show_id, army2, army2_is_winner, army2_edition, cursor)

        conn.commit()

if __name__ == '__main__':
    main()
