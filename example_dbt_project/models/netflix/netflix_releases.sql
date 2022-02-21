with source as (
    select * from {{ ref("raw_netflix_releases") }}
)

select
    show_id :: text as show_id
    , type :: text as show_type
    , title :: text as title
    , director :: text as director
    , cast_list :: text as cast_list
    , trim(split_part(country :: text, ',', 1)) as primary_country
    , country = 'United States' as is_usa_release
    , date_added :: date as show_added_date
    , release_year :: numeric as release_year
    , round(release_year, -1) as release_decade
    , listed_in :: text as listed_in
    , description :: text as description
    , rating :: text as maturity_rating
    , director is not null as has_director
    , case when duration ilike '%min' then trim(duration, 'min') :: numeric end as show_duration
    , case when duration ilike '%season' then trim(duration, 'Season') :: numeric end as season_duration

from
    source