{{
    config(
        materialized='view'
    )
}}

with 

weather_data as (

    select *,
        row_number() over(partition by team, date) as rn
    from {{ source('staging', 'weather_data_cleaned') }}
    where latitude != 'No data'

)

select
    name,
    -- geolocation
    cast(latitude as numeric) as latitude,
    cast(longitude as numeric) as longitude,
    state,
    country,
    -- weather information
    sky_weather,
    weather_description,
    
    team,
    cast(date as timestamp) as operation_date,

from weather_data
where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}
    
    limit 100 

{% endif %}