-- SQL for the examples in README.md

select fullname, count(1) as n
from shows
join players on shows.servoskull_id = players.id
group by fullname
order by n desc;

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
