{{
    config(
        materialized='view'
    )
}}

with 

city_data as (

    select *,
        row_number() over(partition by team_name, city) as rn
    from {{ source('staging', 'city_data_cleaned') }}
    where team_name is not null

)

select

    {{ dbt_utils.generate_surrogate_key(['team_name', 'city']) }} as team_id,
    nombre,
    apodo,
    fundacion,
    presidente,
    entrenador,
    estadio,
    ubicacion,
    capacidad,
    city,
    team_name,
    cast(date as timestamp) as operation_date,

from city_data
where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}
    
    limit 100 

{% endif %}