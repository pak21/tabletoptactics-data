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
    return load_objects('faction', 'factions', cursor);

def load_subfactions(cursor):
    cursor.execute(f'select s.id, s.subfaction, f.id, f.faction from subfactions as s join factions as f on s.faction_id = f.id')
    return {s: (sid, f, fid) for sid, s, fid, f in cursor.fetchall()}

def get_id_from_slug(slug, lookup, objtype):
    for obj, obj_id in lookup.items():
        if tt.normalize_for_slug(obj) in slug:
            return obj_id, obj

    obj = input(f"Couldn't obtain {objtype} automatically, please input manually: ")
    return lookup[obj], obj

def get_game(slug, games):
    if 'warhammer-40k' in slug:
        return games['Warhammer 40,000'], 'Warhammer 40,000'

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

def input_army_details(n, army, cursor):
    player = input(f'Army {n} player? ') or None
    if army:
        if player is None:
            raise Exception(f'Must have a player for the {army.faction} army')
    else:
        if player is None:
            return
        faction = input(f'Army {n} faction? ')
        faction_id = get_faction(faction, cursor)
        army = tt.ArmyInfo(faction_id=faction_id, faction=faction)

    army.player_id = get_player(player, cursor)

    if army.subfaction_id is None:
        subfaction = input(f'Army {n} subfaction? ')
        army.subfaction_id = get_subfaction(subfaction, cursor) if subfaction else None

FACTION_DATES_9TH = {
    'Aeldari': datetime.date(2022, 2, 26),
    'Harlequins': datetime.date(2022, 2, 26),
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
        is_8th = release_date < FACTION_DATES_9TH[army.faction]
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
    cursor.execute('insert into armies(show_id, player_id, faction_id, subfaction_id, winner, codex_edition) values (%s, %s, %s, %s, %s, %s)', (show_id, army.player_id, army.faction_id, army.subfaction_id, winner, edition))

def main():
    conn = psycopg2.connect('dbname=tabletoptactics')

    with contextlib.closing(conn.cursor()) as cursor:
        games = load_games(cursor)
        showtypes = load_showtypes(cursor)
        factions = load_factions(cursor)
        subfactions = load_subfactions(cursor)

        raw_url = input('URL? ')
        release_date, slug = parse_url(raw_url)

        game_id, game = get_game(slug, games)
        showtype_id = get_showtype(slug, showtypes)

        army1, army2 = tt.extract_armies_from_slug(slug, factions, subfactions)

        youtube_slug = input('YouTube slug? ') or None

        input_army_details(1, army1, cursor)
        input_army_details(2, army2, cursor)
        if army2:
            winner = input('Winner? ') or None
            winner_id = get_player(winner, cursor) if winner else None
        else:
            winner_id = None

        servoskull = input('Servoskull? ')
        servoskull_id = get_player(servoskull, cursor) if servoskull else None

        show_id = add_show(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id, cursor)

        army1_is_winner = army1.player_id == winner_id if winner_id else None
        army1_edition = get_edition(army1, game, release_date)
        add_army(show_id, army1, army1_is_winner, army1_edition, cursor)
        if army2:
            army2_is_winner = army2.player_id == winner_id if winner_id else None
            army2_edition = get_edition(army2, game, release_date)
            add_army(show_id, army2, army2_is_winner, army2_edition, cursor)

        conn.commit()

if __name__ == '__main__':
    main()
