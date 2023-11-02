#!/usr/bin/env python3

import argparse
import contextlib
import sys

import psycopg2

import tabletoptactics as tt

def load_objects(objecttype, table, cursor):
    cursor.execute(f'select {objecttype}, id from {table}')
    return dict(cursor.fetchall())

def load_factions(cursor):
    cursor.execute('select f.id, f.faction, g.id from factions as f join games as g on f.game_id = g.id')
    return cursor.fetchall()

def load_subfactions(cursor):
    cursor.execute('select s.id, s.subfaction, f.id, f.faction from subfactions as s join factions as f on s.faction_id = f.id')
    return cursor.fetchall()

def add_show(showdata, cursor):
    cursor.execute('insert into shows(release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id) values (%s, %s, %s, %s, %s, %s) returning id', (showdata.release_date, showdata.game_id, showdata.showtype_id, showdata.slug, showdata.youtube_slug, showdata.servoskull_id))
    return cursor.fetchall()[0][0]

def add_army(show_id, army, cursor):
    if army:
        cursor.execute('insert into armies(show_id, player_id, faction_id, subfaction_id, winner, codex_edition) values (%s, %s, %s, %s, %s, %s)', (show_id, army.player_id, army.faction_id, army.subfaction_id, army.winner, army.edition))

def add_campaign_entry(showdata, show_id, cursor):
    if showdata.campaign:
        cursor.execute('insert into narrativeshows(show_id, campaign_id, campaign_sequence) values (%s, %s, %s)', (show_id, showdata.campaign.campaign_id, showdata.campaign.sequence))

def add_league_entry(showdata, show_id, cursor):
    if showdata.league:
        cursor.execute('insert into leagueshows(show_id, league_season, episode) values (%s, %s, %s)', (show_id, showdata.league.season, showdata.league.episode))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dryrun', action='store_true', help='Print out what would be written to the database instead of doing it')
    parser.add_argument('inputdata')
    args = parser.parse_args()

    conn = psycopg2.connect('dbname=tabletoptactics')

    with open(args.inputdata) as f:
        input_data = tt.parse_input(f.read())

    with contextlib.closing(conn.cursor()) as cursor:
        games = load_objects('game', 'games', cursor)
        showtypes = load_objects('showtype', 'showtypes', cursor)
        players = load_objects('nickname', 'players', cursor)
        campaigns = load_objects('campaign', 'campaigns', cursor)
        factions = load_factions(cursor)
        subfactions = load_subfactions(cursor)

        builder = tt.ShowDataBuilder(games, showtypes, players, campaigns, factions, subfactions)

        showdata = builder.build(input_data)

        if args.dryrun:
            print(showdata)
        else:
            show_id = add_show(showdata, cursor)

            add_army(show_id, showdata.army1, cursor)
            add_army(show_id, showdata.army2, cursor)

            add_campaign_entry(showdata, show_id, cursor)
            add_league_entry(showdata, show_id, cursor)

            conn.commit()

if __name__ == '__main__':
    main()
