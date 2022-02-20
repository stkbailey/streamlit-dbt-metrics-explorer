{{ config(materialized="table") }}

with matches as (
    select * from {{ ref("raw_soccer_matches") }}
)

select
    date :: date as match_date
    , home_team :: text as home_team_name
    , away_team :: text as away_team_name
    , home_score :: number as home_score
    , away_score :: number as away_score
    , tournament :: text as tournament
    , city :: text as city
    , country :: text as country
    , neutral :: text as is_neutral
    , tournament ilike '%friendly%' as is_friendly
    , home_score = away_score as is_tie
    , home_score > away_score as is_home_win
from
    matches
