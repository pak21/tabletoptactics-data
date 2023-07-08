# Schema

The two primary tables in the database are `shows`, which represents the individual shows, and `armies`, which represents the armies used in each show.

## 10th Edition WIP

I'm still working out how all this fits together for 10th Edition. Things may need to change!

## `shows`

Each row in this table represents one show.

```
tabletoptactics=> \d shows
                                Table "public.shows"
    Column     |  Type   | Collation | Nullable |              Default              
---------------+---------+-----------+----------+-----------------------------------
 id            | integer |           | not null | nextval('shows_id_seq'::regclass)
 release_date  | date    |           | not null | 
 game_id       | integer |           | not null | 
 showtype_id   | integer |           | not null | 
 slug          | text    |           | not null | 
 youtube_slug  | text    |           |          | 
 servoskull_id | integer |           |          | 
```

* `id`: synthetic primary key for this show.
* `release_date`: the date on which the show was released.
  * Strictly, the date equivalent to the `yyyy/mm/dd` part of the URL for the show on [tabletoptactics.tv](https://tabletoptactics.tv), e.g. `2023-04-28` for [https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/](https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/). There are a few instances on which the date when the show was actually released doesn't agree with the date in the URL.
* `game_id`: reference to `games.id` indicating the game played in this show (Warhammer 40,000, Age of Sigmar, etc).
* `showtype_id`: reference to `showtypes.id` indicating the type of show (battle report, league report, etc).
* `slug`: the "descriptive" part of the URL for the show on [tabletoptactics.tv](https://tabletoptactics.tv), e.g. `thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report` for [https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/](https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/).
  * The URL for a show can be reconstructed from this and the `release_date` field.
* `youtube_slug`: the YouTube ID for the show, e.g. `tTbrnKS7keo` for [https://tabletoptactics.tv/2023/04/19/orks-vs-astra-militarum-season-2-ep-8-warhammer-40000-league-report/](https://tabletoptactics.tv/2023/04/19/orks-vs-astra-militarum-season-2-ep-8-warhammer-40000-league-report/), which can be found at [https://www.youtube.com/watch?v=tTbrnKS7keo](https://www.youtube.com/watch?v=tTbrnKS7keo). Present only for freeview shows.
* `servoskull_id`: reference to `players.id` indicating the "servoskull" (camera operator) for the show.
  * Yes, this is typically called "endless spell" for Age of Sigmar shows. No, I don't care.

## `armies`

Each row in this table represents one army taking part in one show.

```
tabletoptactics=> \d armies
                                Table "public.armies"
    Column     |  Type   | Collation | Nullable |              Default               
---------------+---------+-----------+----------+------------------------------------
 id            | integer |           | not null | nextval('armies_id_seq'::regclass)
 show_id       | integer |           | not null | 
 player_id     | integer |           | not null | 
 faction_id    | integer |           | not null | 
 subfaction_id | integer |           |          | 
 winner        | boolean |           |          | 
 codex_edition | integer |           | not null |
```

* `id`: synthetic primary key for this army.
* `show_id`: reference to `shows.id` indicating which show this army took part in.
* `player_id`: reference to `players.id` indicating which player controlled this army.
* `faction_id`: reference to `factions.id` indicating the faction for this army (see "Factions and subfactions" below for details on the modelling).
* `subfaction_id`: reference to `subfactions.id` indicating the subfaction, if any, for this army (see "Factions and subfactions" below for details on the modelling).
* `winner`: true if this army was on the winning side of the battle, false if it was on the losing side. Null if the battle was a draw or otherwise inconclusive.
  * Generally you can expect there to be one winning army and one losing army for each non-drawn battle, but in some cases (narrative shows) there may be more than one winner or loser.
* `codex_edition`: the edition of the game the codex for this faction was released for - e.g. `8` or `9` for Warhammer 40,000 factions, or `2` or `3` for Age of Sigmar factions.
  * This gives a clue as to which subfactions are relevant for a faction - e.g. 8th Edition Harlequins use masques, while 9th Edition Harlequins use saedaths. There is currently no attempt to model this relationship though.
  * Yes, these are battletomes in Age of Sigmar. No, I don't care.

## Other tables

```
tabletoptactics=> \dt
            List of relations
 Schema |      Name      | Type  | Owner
--------+----------------+-------+--------
 public | armies         | table | philip
 public | campaigns      | table | philip
 public | factions       | table | philip
 public | games          | table | philip
 public | leagueseasons  | table | philip
 public | narrativeshows | table | philip
 public | players        | table | philip
 public | shows          | table | philip
 public | showtypes      | table | philip
 public | subfactions    | table | philip
```

### `campaigns`

Each row represents one narrative campaign.

```
tabletoptactics=> \d campaigns
                             Table "public.campaigns"
  Column  |  Type   | Collation | Nullable |                Default
----------+---------+-----------+----------+---------------------------------------
 id       | integer |           | not null | nextval('campaigns_id_seq'::regclass)
 campaign | text    |           | not null |
```

* `id`: synthetic primary key for this narrative campaign.
* `campaign`: the name of the narrative campaign, e.g. "Cinder Ark".

### `factions`

Each row represents one faction; see "Factions and subfactions" below for details on the modelling.

```
tabletoptactics=> \d factions
                             Table "public.factions"
 Column  |  Type   | Collation | Nullable |               Default
---------+---------+-----------+----------+--------------------------------------
 id      | integer |           | not null | nextval('factions_id_seq'::regclass)
 faction | text    |           | not null |
 game_id | integer |           | not null |
```

* `id`: synthetic primary key for this faction.
* `faction`: the name of this faction, e.g. "Space Marines".
* `game_id`: reference to `games.id` indicating the game this faction is part of.

### `games`

Each row represents one game.

```
tabletoptactics=> \d games
                            Table "public.games"
 Column |  Type   | Collation | Nullable |              Default
--------+---------+-----------+----------+-----------------------------------
 id     | integer |           | not null | nextval('games_id_seq'::regclass)
 game   | text    |           | not null |
```

* `id`: synthetic primary key for this game.
* `game`: the name of this game, e.g. "Warhammer 40,000".

### `leagueseasons`

Each row represents one battle in a league season.

```
tabletoptactics=> \d leagueseasons
                                Table "public.leagueseasons"
    Column     |  Type   | Collation | Nullable |                  Default
---------------+---------+-----------+----------+-------------------------------------------
 id            | integer |           | not null | nextval('leagueseasons_id_seq'::regclass)
 show_id       | integer |           | not null |
 league_season | integer |           | not null |
 episode       | integer |           | not null |
```

* `id`: synthetic primary key for this mapping.
* `show_id`: reference to `shows.id` indicating which show this mapping is for.
* `league_season`: which league season this show is part of, e.g. "2" for [https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/](https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/) as it is part of the second league season.
* `episode`: which episode of the season this show represents, e.g. "9" for [https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/](https://tabletoptactics.tv/2023/04/28/thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report/) as it is the ninth show of that season.

### `narrativeshows`

Each row represents one show in a narrative campaign.

```
tabletoptactics=> \d narrativeshows
                                  Table "public.narrativeshows"
      Column       |  Type   | Collation | Nullable |                  Default
-------------------+---------+-----------+----------+--------------------------------------------
 id                | integer |           | not null | nextval('narrativeshows_id_seq'::regclass)
 show_id           | integer |           | not null |
 campaign_id       | integer |           | not null |
 campaign_sequence | integer |           | not null |
```

* `id`: synthetic primary key for this mapping.
* `show_id`: reference to `shows.id` indicating which show this mapping is for.
* `campaign_id`: reference to `campaigns.id` indicating which narrative campaign this show is part of.
* `campaign_sequence`: where this show fits into the narrative campaign, e.g. "1" for [https://tabletoptactics.tv/2023/01/21/dark-angels-vs-black-legion-warhammer-40000-narrative-report/](https://tabletoptactics.tv/2023/01/21/dark-angels-vs-black-legion-warhammer-40000-narrative-report/) as it is the first show of the Cinder Ark narrative campaign.

### `players`

Each row represents one player.

```
tabletoptactics=> \d players
                             Table "public.players"
  Column  |  Type   | Collation | Nullable |               Default
----------+---------+-----------+----------+-------------------------------------
 id       | integer |           | not null | nextval('players_id_seq'::regclass)
 fullname | text    |           | not null |
 nickname | text    |           | not null |
```

* `id`: synthetic primary key for this player.
* `fullname`: the full name of this player, e.g. "Lawrence Baker".
  * Stig's full name is Stig. This is a fact.
* `nickname`: the nickname of this player, e.g. "Spider".
  * This can be somewhat artificial for guest challengers who may not have a well-defined nickname.

### `showtypes`

Each row represents one type of show on the channel.

```
tabletoptactics=> \d showtypes
                             Table "public.showtypes"
  Column  |  Type   | Collation | Nullable |                Default
----------+---------+-----------+----------+---------------------------------------
 id       | integer |           | not null | nextval('showtypes_id_seq'::regclass)
 showtype | text    |           | not null |
```

* `id`: synthetic primary key for this show type.
* `showtype`: brief description of the show type, e.g. "Battle report".

### `subfactions`

Each row represents one subfaction. See "Factions and subfactions" below for details on the modelling.

```
tabletoptactics=> \d subfactions
                              Table "public.subfactions"
   Column   |  Type   | Collation | Nullable |                 Default
------------+---------+-----------+----------+-----------------------------------------
 id         | integer |           | not null | nextval('subfactions_id_seq'::regclass)
 subfaction | text    |           | not null |
 faction_id | integer |           | not null |
```

* `id`: synthetic primary key for this subfaction.
* `subfaction`: the name of this subfaction, e.g. "Dark Angels".
* `faction_id`: reference to `factions.id` indicating which faction this subfaction is part of.

## Factions and subfactions

"Faction" isn't quite as tightly defined in the game as it sometimes appears - for example, a battle-forged army can choose "Imperium" as its faction and build a "soup" list from multiple Imperium codexes. 9th Edition in particular discourages this type of army building in that it means everything in the army loses its "super doctrine" (e.g. Masters of the Warp for Grey Knights) so it's pretty rare, but in theory in can happen. There was for example, one successful list which put (pre-nerf) Tzeentch Flamers into a Death Guard army, making it formally a "Chaos" army. For the purposes of this database, I've mapped "faction" to "codex" with one exception: pre-10th Edition, Harlequins are a separate faction from Aeldari proper. (Ynnari remain part of the Aeldari faction, even though they can include both Drukhari and Harlequins. This isn't perfect, but there's no perfect solution here).

Everything above applies double to "subfaction". For some factions, the subfaction makes a huge difference to the army - consider a Dark Angels army vs a Deathwatch army. For some factions, it's a important choice but not all defining - consider Thousand Sons Cult of Duplicity vs Cult of Time. For some factions, the subfaction isn't really a meaningful concept - consider 9th Edition Astra Militarum, which can now pull from all regiments. I've listed subfactions for the first two cases but haven't for the third case (primarily Astra Militarum and Chaos Daemons).

Some other factors can reduce the completeness and/or accuracy of subfaction information:

* The subfaction often isn't listed in the show title so I've had to obtain it by listening to the list breakdown. I might have got it wrong, missed it or maybe the player just didn't say it.
* Most factions allow creation of custom subfactions by selecting from a list of traits. I haven't attempted to model these and have just left the subfaction empty in these cases.
  * This also applies to things like the Drukhari Realspace Raid which allow selection from multiple subfactions.
  * One exception here is the Necron "Obsekh Dynasty" (Eternal Conquerors + Relentlessly Expansionist), mostly because that's what Chef used in his Season 1 league list.

### 10th Edition WIP

* I'm currently using the detachment (Gladius Task Force, Invasion Fleet, etc) as the subfaction in 10th Edition. Time will tell if this is useful modelling or not.
* 10th Edition Harlequins are just an Aeldari army for now; I'm assuming they'll get some more unique rules when the codex comes out.
