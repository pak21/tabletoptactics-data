#!/usr/bin/env python3

import contextlib
import datetime
import urllib.parse

import psycopg2

DEFAULT_EDITION = {
    'Age of Sigmar': 3,
    'Warhammer 40,000': 10,
}

def load_games(cursor):
    cursor.execute(f'select id, game from games')
    results = cursor.fetchall()
    return {g: gid for gid, g in results}

def load_showtypes(cursor):
    cursor.execute(f'select id, showtype from showtypes')
    results = cursor.fetchall()
    return {st: stid for stid, st in results}

def normalize_for_slug(s):
    return s.lower().replace(' ', '-').replace(',', '')

def get_id_from_slug(slug, lookup, objtype):
    for obj, obj_id in lookup.items():
        if normalize_for_slug(obj) in slug:
            return obj_id, obj

    obj = input(f"Couldn't obtain {objtype} automatically, please input manually: ")
    return lookup[obj], obj

def get_game(slug, games):
    return get_id_from_slug(slug, games, 'game')

def get_showtype(slug, showtypes):
    return get_id_from_slug(slug, showtypes, 'show type')

def get_id(value, table, column, objecttype, cursor):
    cursor.execute(f'select id from {table} where {column} = %s', (value,))
    results = cursor.fetchall()
    if not results:
        raise Exception(f'{objecttype} "{value}" does not exist. Are you sure?')

    return results[0][0]

def get_player(player, cursor):
    return get_id(player, 'players', 'nickname', 'Player', cursor)

def get_faction(faction, cursor):
    return get_id(faction, 'factions', 'faction', 'Faction', cursor)

def get_subfaction(subfaction, cursor):
    return get_id(subfaction, 'subfactions', 'subfaction', 'Subfaction', cursor)

def input_army_details(n, cursor):
    player = input(f'Army {n} player? ')
    if not player:
        return None
    player_id = get_player(player, cursor)

    faction = input(f'Army {n} faction? ')
    faction_id = get_faction(faction, cursor)

    subfaction = input(f'Army {n} subfaction? ')
    subfaction_id = get_subfaction(subfaction, cursor) if subfaction else None

    return {'player': player_id, 'faction': faction_id, 'subfaction': subfaction_id}

def add_show(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id, cursor):
    cursor.execute('insert into shows(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id) values (%s, %s, %s, %s, %s, %s) returning id', (release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id))
    return cursor.fetchall()[0][0]

def add_army(show_id, army, winner, edition, cursor):
    cursor.execute('insert into armies(show_id, player_id, faction_id, subfaction_id, winner, codex_edition) values (%s, %s, %s, %s, %s, %s)', (show_id, army['player'], army['faction'], army['subfaction'], winner, edition))

def main():
    conn = psycopg2.connect('dbname=tabletoptactics')

    with contextlib.closing(conn.cursor()) as cursor:
        games = load_games(cursor)
        showtypes = load_showtypes(cursor)

        raw_url = input('URL? ')
        url = urllib.parse.urlparse(raw_url)
        components = url.path.split('/')
        date_components = [int(c) for c in components[1:4]]
        release_date = datetime.date(*date_components)
        slug = components[4]

        game_id, game = get_game(slug, games)
        edition = DEFAULT_EDITION[game]

        showtype_id, _ = get_showtype(slug, showtypes)

        youtube_slug = input('YouTube slug? ') or None

        army1 = input_army_details(1, cursor)
        army2 = input_army_details(2, cursor)
        if army2:
            winner = input('Winner? ') or None
            winner_id = get_player(winner, cursor) if winner else None
        else:
            winner_id = None

        servoskull = input('Servoskull? ')
        servoskull_id = get_player(servoskull, cursor) if servoskull else None

        show_id = add_show(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id, cursor)

        army1_is_winner = army1['player'] == winner_id if winner_id else None
        add_army(show_id, army1, army1_is_winner, edition, cursor)
        if army2:
            army2_is_winner = army2['player'] == winner_id if winner_id else None
            add_army(show_id, army2, army2_is_winner, edition, cursor)

        conn.commit()

if __name__ == '__main__':
    main()
