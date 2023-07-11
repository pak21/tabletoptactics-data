#!/usr/bin/env python3

import contextlib
import datetime
import urllib.parse

import psycopg2

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
    showtype_id, _ = get_id_from_slug(slug, showtypes, 'show type')
    return showtype_id

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

    return {'player': player_id, 'faction': faction_id, 'faction_name': faction, 'subfaction': subfaction_id}

FACTION_DATES_9TH = {
    'Tyranids': datetime.date(2022, 4, 9),
    'Chaos Knights': datetime.date(2022, 5, 7),
    'Imperial Knights': datetime.date(2022, 5, 10),
    'Chaos Space Marines': datetime.date(2022, 6, 25),
    'Chaos Daemons': datetime.date(2022, 8, 27),
    'Leagues of Votann': datetime.date(2022, 9, 17), # Included for reference, but can't be any games before this!
    'Astra Militarum': datetime.date(2022, 11, 12),
    'World Eaters': datetime.date(2023, 2, 4),
}

def get_edition_wh40k(army, release_date):
    # Last 9th Edition game on the channel was 2023-05-30
    if release_date > datetime.date(2023, 5, 30):
        return 10

    try:
        is_8th = release_date < FACTION_DATES_9TH[army['faction_name']]
    except KeyError:
        is_8th = False

    return 8 if is_8th else 9

EDITION_FUNCTIONS = {
    'Warhammer 40,000': get_edition_wh40k,
    'Age of Sigmar': lambda a, rd: 3
}

def get_edition(army, game, release_date):
    return EDITION_FUNCTIONS[game](army, release_date)

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

        showtype_id = get_showtype(slug, showtypes)

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
        army1_edition = get_edition(army1, game, release_date)
        add_army(show_id, army1, army1_is_winner, army1_edition, cursor)
        if army2:
            army2_is_winner = army2['player'] == winner_id if winner_id else None
            army2_edition = get_edition(army2, game, release_date)
            add_army(show_id, army2, army2_is_winner, army2_edition, cursor)

        conn.commit()

if __name__ == '__main__':
    main()
