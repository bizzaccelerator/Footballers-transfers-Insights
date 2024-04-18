{{
    config(
        materialized='table'
    )
}}

with players_data as (
    select * from {{ ref('stg_players_data_cleaned') }}
    where team_left != 'Without ClubWithout Club'
),
weather_data as (
    select * from {{ ref('stg_weather_data_cleaned') }}
    where latitude  is not null
)
-- dataset_unioned as (
--     select tm_id, player_position, player_age, player_nationality, team_left, league_left, team_joined, league_joined, market_value_clean  from players_data
--     union all
--     select name, latitude, longitude, state, country, sky_weather, weather_description, team, operation_date from weather_data
-- )

select * 
from players_data
inner join weather_data 
on players_data.team_left = weather_data.team
where players_data.transfer_datetime = weather_data.operation_date