{{
    config(
        materialized='view'
    )
}}

with 

players_data as (

    select *,
        row_number() over(partition by tm_id, clean_data) as rn
    from {{ source("staging", "players_data_cleaned")}}
    where tm_id is not null

)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['tm_id', 'clean_data']) }} as transfer_id,
    cast(tm_id as integer) as tm_id,
    player_name,
    player_position,
    player_details,
    cast(player_age as integer) as player_age,
    player_nationality,
    team_left,
    league_left,
    country_previous,
    team_joined,
    league_joined,
    country_current,
    -- timestamps
    cast(clean_data as timestamp) as transfer_datetime,

    -- market value:
    cast(market_value_clean as integer) as market_value_clean,

from players_data
where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}
    
    limit 100 

{% endif %}