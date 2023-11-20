# Tabletop Tactics data

Metadata about the battles played on the [Tabletop Tactics](https://tabletoptactics.tv/) channel.

## What's here?

* [tabletoptactics.sql](tabletoptactics.sql): PostgreSQL dump of the data itself; see [schema.md](schema.md) for more details.
* [inserter.py](inserter.py): simple Python script to add a new show to the database.

## Data completeness

As of 2023-09-09, the data contains shows released on the channel from 2022-02-19 to 2023-09-08. Specifically, this includes:

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
 Katie Foad       | 83
 James Jordan     | 79
 Lawrence Baker   | 56
 Michael Hebditch | 46
 Joe Ponting      | 39
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
 Ed Pemberton     | Tyranids            |  2
 Ed Pemberton     | Genestealer Cults   |  2
 Fletcher Giles   | T'au Empire         | 12
 James Beaver     | Necrons             |  1
 James Hamill     | Adepta Sororitas    |  1
 James Jordan     | Space Marines       | 36
 James Otero      | Astra Militarum     |  1
 Joe Ponting      | Chaos Space Marines | 27
 Josh Hill        | Sylvaneth           |  1
 Josh Hill        | Chaos Daemons       |  1
 Josh Hill        | Slaves to Darkness  |  1
 Josh Hill        | Space Marines       |  1
 Katie Foad       | Tyranids            | 28
 Laurens          | Adepta Sororitas    |  1
 Lawrence Baker   | Space Marines       | 24
 Lennard          | Space Marines       |  1
 Linden Forster   | Aeldari             |  2
 Mark             | Genestealer Cults   |  1
 Matt Jarvis      | Aeldari             |  2
 Maxine Blythin   | Space Marines       |  1
 Michael Hebditch | Necrons             | 20
 Ridvan Martinez  | Drukhari            |  2
 Rob              | Chaos Space Marines |  1
 Sam Weeks        | Space Marines       |  2
 Steve Joll       | Space Marines       |  1
 Stig             | Adeptus Mechanicus  | 23
```

i.e. Chaos Lord Beard's most played faction is Chaos Space Marines, which he has done 27 times.

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
 Space Marines         |   53 |     33
 Orks                  |   22 |     12
 Chaos Space Marines   |   19 |     19
 Aeldari               |   18 |     14
 T'au Empire           |   17 |     15
 World Eaters          |   13 |      4
 Astra Militarum       |   13 |     18
 Necrons               |   12 |     11
 Death Guard           |   10 |      8
 Tyranids              |   10 |     20
 Soulblight Gravelords |    9 |      0
 Adeptus Custodes      |    9 |     12
 Chaos Knights         |    8 |      3
 Adepta Sororitas      |    8 |     12
 Adeptus Mechanicus    |    8 |     17
 Grey Knights          |    7 |     13
 Imperial Knights      |    6 |      6
 Leagues of Votann     |    6 |      8
 Drukhari              |    6 |     11
 Harlequins            |    5 |      0
 Seraphon              |    5 |      2
 Idoneth Deepkin       |    5 |      3
 Thousand Sons         |    5 |      8
 Genestealer Cults     |    5 |      8
 Chaos Daemons         |    5 |     12
 Maggotkin of Nurgle   |    4 |      5
 Orruk Warclans        |    3 |      4
 Stormcast Eternals    |    3 |      4
 Hedonites of Slaanesh |    3 |      5
 Slaves to Darkness    |    3 |      5
 Ossiarch Bonereapers  |    3 |      7
 Skaven                |    2 |      1
 Blades of Khorne      |    2 |      1
 Nighthaunt            |    2 |      3
 Ogor Mawtribes        |    2 |      3
 Imperium              |    1 |      0
 Fyreslayers           |    0 |      1
 Sylvaneth             |    0 |      2
```

# License

This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
