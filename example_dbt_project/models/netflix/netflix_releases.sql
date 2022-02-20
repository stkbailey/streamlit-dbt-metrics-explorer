{{ config(materialized="table") }}

with movies as (
    select * from {{ ref("raw_netflix_titles") }}
)

select
    show_id :: text as show_id
    , type :: text as show_type
    , title :: text as title
    , director :: text as director
    , cast_list :: text as cast_list
    , trim(split_part(country :: text, ',', 1)) as country
    , try_to_date(date_added) as show_added_date
    , release_year :: number as release_year
    , floor(release_year, -1) as release_decade
    , listed_in :: text as listed_in
    , description :: text as description
    , rating :: text as maturity_rating
    , case when duration ilike '%min' then trim(duration, 'min') :: number end as show_duration
    , case when duration ilike '%season' then trim(duration, 'Season') :: number end as season_duration

from
    movies