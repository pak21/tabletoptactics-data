# Tabletop Tactics data

Metadata about the battles played on the [Tabletop Tactics](https://tabletoptactics.tv/) channel.

## What's here?

* [tabletoptactics.sql](tabletoptactics.sql): PostgreSQL dump of the data itself; see [schema.md](schema.md) for more details.
* [inserter.py](inserter.py): simple Python script to add a new show to the database.

## Data completeness

As of 2023-08-08, the data contains shows released on the channel from 2022-03-19 to 2023-08-05. Specifically, this includes:

* All battle reports _except_ the "X vs everyone" shows (e.g. [Rogal Dorn vs everyone](https://tabletoptactics.tv/2023/02/22/the-rogal-dorn-vs-everyone-warhammer-40000-battle-report/))
* All league reports
* All narrative reports
* All list analysis shows
* The 10th edition introductory "How to play" show
* The 10th edition "Faction focus" shows

It does not currently include any:

* Faction focus shows before 10th edition
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
 Katie Foad       | 69
 James Jordan     | 65
 Lawrence Baker   | 43
 Michael Hebditch | 37
 Joe Ponting      | 31
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
 Fletcher Giles   | T'au Empire         | 12
 James Beaver     | Necrons             |  1
 James Hamill     | Adepta Sororitas    |  1
 James Jordan     | Space Marines       | 25
 James Otero      | Astra Militarum     |  1
 Joe Ponting      | Chaos Space Marines | 25
 Josh Hill        | Space Marines       |  1
 Josh Hill        | Slaves to Darkness  |  1
 Josh Hill        | Sylvaneth           |  1
 Katie Foad       | Tyranids            | 22
 Lawrence Baker   | Space Marines       | 19
 Lennard          | Space Marines       |  1
 Mark             | Genestealer Cults   |  1
 Matt Jarvis      | Aeldari             |  2
 Maxine Blythin   | Space Marines       |  1
 Michael Hebditch | Necrons             | 17
 Ridvan Martinez  | Drukhari            |  1
 Sam Weeks        | Space Marines       |  2
 Steve Joll       | Space Marines       |  1
 Stig             | Adeptus Mechanicus  | 21
```

i.e. Chaos Lord Beard's most played faction is Chaos Space Marines, which he has done 25 times.

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
 Space Marines         |   37 |     27
 Orks                  |   21 |     10
 Chaos Space Marines   |   16 |     17
 T'au Empire           |   14 |     12
 Astra Militarum       |   12 |     15
 Necrons               |   11 |      8
 Aeldari               |   11 |     13
 World Eaters          |    9 |      3
 Soulblight Gravelords |    8 |      0
 Adeptus Mechanicus    |    8 |     13
 Tyranids              |    7 |     15
 Chaos Knights         |    6 |      2
 Death Guard           |    6 |      5
 Leagues of Votann     |    6 |      7
 Drukhari              |    6 |      7
 Adeptus Custodes      |    6 |     10
 Grey Knights          |    6 |     10
 Harlequins            |    5 |      0
 Seraphon              |    5 |      2
 Imperial Knights      |    5 |      5
 Adepta Sororitas      |    5 |      9
 Idoneth Deepkin       |    4 |      3
 Thousand Sons         |    4 |      6
 Genestealer Cults     |    4 |      6
 Chaos Daemons         |    4 |      7
 Stormcast Eternals    |    3 |      3
 Slaves to Darkness    |    3 |      5
 Hedonites of Slaanesh |    3 |      5
 Maggotkin of Nurgle   |    3 |      5
 Ossiarch Bonereapers  |    3 |      6
 Skaven                |    2 |      0
 Blades of Khorne      |    2 |      1
 Nighthaunt            |    2 |      2
 Ogor Mawtribes        |    2 |      3
 Orruk Warclans        |    2 |      4
 Fyreslayers           |    0 |      1
 Sylvaneth             |    0 |      2
```

# License

This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
