# Tabletop Tactics data

Metadata about the battles played on the [Tabletop Tactics](https://tabletoptactics.tv/) channel.

## What's here?

* [tabletoptactics.sql](tabletoptactics.sql): PostgreSQL dump of the data itself; see [schema.md](schema.md) for more details.
* [inserter.py](inserter.py): simple Python script to add a new show to the database.

## Data completeness

As of 2023-05-15, the data contains shows released on the channel from 2022-04-12 to 2023-05-13. Specifically, this includes:

* All battle reports _except_ the "X vs everyone" shows (e.g. [Rogal Dorn vs everyone](https://tabletoptactics.tv/2023/02/22/the-rogal-dorn-vs-everyone-warhammer-40000-battle-report/)
* All league reports
* All narrative reports
* All list analysis shows

It does not currently include any:

* Faction focus shows
* How to paint shows
* State of play shows
* Backstage shows

## Fun queries

### Most common servoskull

```
select fullname, count(1) as n
from shows
join players on shows.servoskull_id = players.id
group by fullname
order by n desc;
```

```
     fullname     | n
------------------+----
 James Jordan     | 53
 Katie Foad       | 49
 Lawrence Baker   | 35
 Michael Hebditch | 29
 Joe Ponting      | 25
```

### Most played faction by player

```
select fullname, faction, n
from
(
  select fullname, faction, count(1) as n, rank() over (partition by fullname order by count(1) desc)
  from players
  join armies on players.id = armies.player_id
  join factions on armies.faction_id = factions.id
  group by fullname, faction
) as x
where rank = 1;
``` 

```
     fullname     |       faction       | n
------------------+---------------------+----
 David Methven    | Sylvaneth           |  1
 David Pettitt    | Space Marines       |  3
 David Ugolini    | Chaos Space Marines |  1
 Ed Pemberton     | Genestealer Cults   |  1
 Fletcher Giles   | T'au Empire         | 11
 James Hamill     | Adepta Sororitas    |  1
 James Jordan     | Space Marines       | 20
 James Otero      | Astra Militarum     |  1
 Joe Ponting      | Chaos Space Marines | 20
 Josh Hill        | Sylvaneth           |  1
 Katie Foad       | Tyranids            | 19
 Lawrence Baker   | Space Marines       | 15
 Mark             | Genestealer Cults   |  1
 Matt Jarvis      | Aeldari             |  2
 Maxine Blythin   | Space Marines       |  1
 Michael Hebditch | Necrons             | 13
 Ridvan Martinez  | Drukhari            |  1
 Sam Weeks        | Space Marines       |  2
 Stig             | Adeptus Mechanicus  | 15
```

i.e. Chaos Lord Beard's most played faction is Chaos Space Marines, which he has done 20 times.

### Wins and losses for each faction

```
select faction, coalesce(wins, 0) as wins, coalesce(losses, 0) as losses
from crosstab('
  select faction, winner, count(1)
  from armies
  join factions on armies.faction_id = factions.id
  where winner is not null
  group by faction, winner
  order by faction
', 'select distinct winner from armies where winner is not null')
as pivot(faction text, losses bigint, wins bigint)
order by wins desc, losses;
```

```
        faction        | wins | losses
-----------------------+------+--------
 Space Marines         |   34 |     19
 Orks                  |   16 |      9
 Chaos Space Marines   |   12 |     16
 Necrons               |    9 |      6
 T'au Empire           |    9 |      9
 Astra Militarum       |    9 |     12
 Soulblight Gravelords |    7 |      0
 World Eaters          |    7 |      2
 Leagues of Votann     |    6 |      5
 Adeptus Mechanicus    |    6 |      8
 Aeldari               |    6 |     11
 Chaos Knights         |    5 |      1
 Death Guard           |    5 |      3
 Adeptus Custodes      |    5 |      4
 Imperial Knights      |    5 |      5
 Drukhari              |    5 |      6
 Grey Knights          |    5 |      9
 Tyranids              |    5 |     14
 Idoneth Deepkin       |    4 |      2
 Seraphon              |    4 |      2
 Adepta Sororitas      |    4 |      5
 Harlequins            |    3 |      0
 Maggotkin of Nurgle   |    3 |      3
 Stormcast Eternals    |    3 |      3
 Slaves to Darkness    |    3 |      3
 Thousand Sons         |    3 |      5
 Nighthaunt            |    2 |      2
 Chaos Daemons         |    2 |      6
 Ossiarch Bonereapers  |    2 |      6
 Skaven                |    1 |      0
 Ogor Mawtribes        |    1 |      1
 Blades of Khorne      |    1 |      1
 Orruk Warclans        |    1 |      3
 Genestealer Cults     |    1 |      5
 Hedonites of Slaanesh |    1 |      5
 Sylvaneth             |    0 |      2
```

# License

This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
