# Tabletop Tactics data

Metadata about the battles played on the [Tabletop Tactics](https://tabletoptactics.tv/) channel.

## What's here?

* [tabletoptactics.sql](tabletoptactics.sql): PostgreSQL dump of the data itself; see [schema.md](schema.md) for more details.
* [inserter.py](inserter.py): simple Python script to add a new show to the database.

## Data completeness

As of 2024-01-20, the data contains shows released on the channel from 2022-01-07 to 2024-01-06. Specifically, this includes:

* All battle reports _except_ the "X vs everyone" shows (e.g. [Rogal Dorn vs everyone](https://tabletoptactics.tv/2023/02/22/the-rogal-dorn-vs-everyone-warhammer-40000-battle-report/))
* All league reports
* All narrative reports
* All list analysis shows
* The 10th edition introductory "How to play" show
* The 10th edition introductory "Faction focus" shows
* How to paint shows from 10th edition onwards

It does not currently include any:

* Faction focus shows with more than one presenter
* How to paint shows before 10th edition
* State of play shows
* Backstage shows
* Podcast episodes

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
 Katie Foad       | 94
 James Jordan     | 87
 Lawrence Baker   | 59
 Michael Hebditch | 48
 Joe Ponting      | 41
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
 David Pettitt    | Space Marines       |  4
 David Ugolini    | Chaos Space Marines |  1
 Ed Pemberton     | Genestealer Cults   |  3
 Fletcher Giles   | T'au Empire         | 12
 James Beaver     | Necrons             |  1
 James Hamill     | Adepta Sororitas    |  1
 James Jordan     | Space Marines       | 41
 James Otero      | Astra Militarum     |  1
 Joe Ponting      | Chaos Space Marines | 28
 Josh Hill        | Slaves to Darkness  |  1
 Josh Hill        | Sylvaneth           |  1
 Josh Hill        | Space Marines       |  1
 Josh Hill        | Chaos Daemons       |  1
 Katie Foad       | Tyranids            | 30
 Laurens          | Adepta Sororitas    |  1
 Lawrence Baker   | Space Marines       | 25
 Lennard          | Space Marines       |  1
 Linden Forster   | Aeldari             |  2
 Mark             | Genestealer Cults   |  1
 Matt Jarvis      | Aeldari             |  2
 Maxine Blythin   | Space Marines       |  1
 Michael Hebditch | Necrons             | 21
 Ridvan Martinez  | Drukhari            |  2
 Rob              | Chaos Space Marines |  1
 Sam Weeks        | Space Marines       |  2
 Sam Weeks        | Imperial Knights    |  2
 Steve Joll       | Space Marines       |  1
 Stig             | Adeptus Mechanicus  | 23
```

i.e. Chaos Lord Beard's most played faction is Chaos Space Marines, which he has done 28 times.

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
 Space Marines         |   58 |     35
 Orks                  |   25 |     14
 Chaos Space Marines   |   19 |     20
 Aeldari               |   18 |     14
 T'au Empire           |   18 |     17
 World Eaters          |   14 |      5
 Astra Militarum       |   14 |     20
 Necrons               |   13 |     13
 Tyranids              |   12 |     20
 Death Guard           |   11 |     10
 Grey Knights          |   11 |     13
 Adeptus Custodes      |   11 |     15
 Soulblight Gravelords |    9 |      0
 Adepta Sororitas      |    9 |     12
 Chaos Knights         |    8 |      4
 Drukhari              |    8 |     12
 Adeptus Mechanicus    |    8 |     20
 Imperial Knights      |    7 |      8
 Chaos Daemons         |    7 |     13
 Leagues of Votann     |    6 |      8
 Harlequins            |    5 |      0
 Seraphon              |    5 |      2
 Idoneth Deepkin       |    5 |      3
 Thousand Sons         |    5 |      8
 Genestealer Cults     |    5 |     10
 Maggotkin of Nurgle   |    4 |      5
 Stormcast Eternals    |    3 |      4
 Orruk Warclans        |    3 |      4
 Hedonites of Slaanesh |    3 |      5
 Slaves to Darkness    |    3 |      5
 Ossiarch Bonereapers  |    3 |      7
 Skaven                |    2 |      1
 Blades of Khorne      |    2 |      1
 Nighthaunt            |    2 |      3
 Ogor Mawtribes        |    2 |      3
 Imperium              |    1 |      0
 Tomb Kings            |    1 |      0
 Fyreslayers           |    0 |      1
 The Empire of Man     |    0 |      1
 Sylvaneth             |    0 |      2
```

# License

This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
