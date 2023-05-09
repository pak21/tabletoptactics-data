#!/usr/bin/env python3

import contextlib

import psycopg2

def get_id(value, table, column, objecttype, cursor):
    cursor.execute(f'select id from {table} where {column} = %s', (value,))
    results = cursor.fetchall()
    if not results:
        raise Exception(f'{objecttype} "{value}" does not exist. Are you sure?')

    return results[0][0]

def get_game(game, cursor):
    return get_id(game, 'games', 'game', 'Game', cursor)

def get_showtype(showtype, cursor):
    return get_id(showtype, 'showtypes', 'showtype', 'Show type', cursor)

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

def add_army(show_id, army, winner, cursor):
    cursor.execute('insert into armies(show_id, player_id, faction_id, subfaction_id, winner) values (%s, %s, %s, %s, %s)', (show_id, army['player'], army['faction'], army['subfaction'], winner))

def main():
    conn = psycopg2.connect('dbname=tabletoptactics')

    with contextlib.closing(conn.cursor()) as cursor:
        release_date = input('Show release date? ')

        game = input('Game? ')
        game_id = get_game(game, cursor)

        showtype = input('Show type? ')
        showtype_id = get_showtype(showtype, cursor)

        slug = input('tabletoptactics.tv slug? ')
        youtube_slug = input('YouTube slug? ') or None

        army1 = input_army_details(1, cursor)
        army2 = input_army_details(2, cursor)
        if army2:
            winner = input('Winner? ')
            winner_id = get_player(winner, cursor)

        servoskull = input('Servoskull? ')
        servoskull_id = get_player(servoskull, cursor) if servoskull else None

        show_id = add_show(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id, cursor)

        add_army(show_id, army1, army1['player'] == winner_id, cursor)
        if army2:
            add_army(show_id, army2, army2['player'] == winner_id, cursor)

        conn.commit()

if __name__ == '__main__':
    main()
