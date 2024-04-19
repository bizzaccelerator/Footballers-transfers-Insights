# Tutorial for reproducing the project

Here bellow you can find a series of steps that allows you to reproduce this project. The requirements for this project are:

- Google cloud account.
- Terraform by HashiCorp installed in your local environment.
- Docker installed.
- Internet connection.

In that sense, and knowing that we will use selenium deployed in a deployed environment, the first thing we must is 

## 1. Prepare the cloud environment for the project

Google Cloud was selected to elaborate the project. Google Cloud Storage and BigQuery were selected as a datalake service and data warehousing, respectably. I used `Terraform` to prepare the required google environment using both [main.tf](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/infra_terraform/main.tf) and [variables.tf](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/infra_terraform/variables.tf) files. 

## 2. Creating an image of our application

To do that, we will create a docker image based on the latest image of Mage-ai - the orchestrator -, and on top of it, we install the combo google chrome + `chrome-driver` that allow us to perform webscraping tasks, and a list of python libraries indicated [here](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/requirements.txt)

Use this [Dockerfile](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Dockerfile) and run the following command:

> Docker build

## 3. Deploy the application image into cloud

Once the base image is created, it needs to be loaded into `google cloud run`. In ordeer to do that, we need to configure Docker for our GCP to push the image into Google's container registry. This might involve configuring Docker with gcloud command-line tool if not already done.

Before you can push your Docker image to Google Artifact Registry, you need to tag it with the registry's name. The command looks something like this: 

> 'docker tag mageai/mageai:latest [REGION]-docker.pkg.dev/[PROJECT-ID]/[REPOSITORY]/[IMAGE]:[TAG]'

After that, we push the Image to Google Artifact Registry. Once tagged, you can push the Docker image to Google Artifact Registry using the following command: 

> 'docker push [REGION]-docker.pkg.dev/[PROJECT-ID]/[REPOSITORY]/[IMAGE]:[TAG]'

## 4. Build the Data Pipelines

The multistep ETL process, is orchestrated using mage-ai, and is composed by 2 set of pipelines. The firstset of pipelines start with the extraction of the transfer data for each player using selenium and its export to GCS, which is called players_raw_data. [players_scraper](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/1_1_players_scraper.py) and [players_to_gcs](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/1_2_players_to_gcs.py) are the mage blocks used here. 

Once players' transferences data is at hand, then a second pipeline is used the blocks [2_1_cities_info_loader](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/2_1_cities_info_loader.py), [2_2_wiki_api_teams](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/2_2_wiki_api_teams.py), [2_3_wiki_teams_info](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/2_3_wiki_teams_info.py) and [2_4_wiki_info_exporter](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/2_4_wiki_info_exporter.py) to consult the seller team's information data in wikipedia API, then export it into GCS.

After that, city name is used to get geographic locations and its corresponding weather at the date of transference by using the following blocks: [3_1_weather_locations](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/3_1_weather_locations.py), [3_2_curated_weather_data](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/3_2_curated_weather_data.py), [3_3_weather_data](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/3_3_weather_data.py) and [3_4_weather_exporter_to_gcs](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/3_4_weather_exporter_to_gcs.py). 

The following image illustrate the relationship between blocks in raw set of pipelines above:

![Raw data pipelines](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Images/Raw%20pipelines.jpg)

Having all the raw data into a bucket in GCS, we run the second set of pipelines which will extract the information, transform it, and save it into BigQuery. [4_1_players_data_cleaned](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/4_1_players_data_cleaned.py), [4_2_players_data_transformed](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/4_2_players_data_transformed.py), and [4_3_players_cleaned_to_bq](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/4_3_players_cleaned_to_bq.py) are the blocks used to cleand and export the players data. The blocks [5_1_city_clean_loader](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/5_1_city_clean_loader.py), [5_2_city_clean_transformer](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/5_2_city_clean_transformer.py), and [5_3_city_clean_exporter](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/5_3_city_clean_exporter.py) are used to clean and export the city information. And [6_1_weather_clean_loader](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/6_1_weather_clean_loader.py), [6_2_weather_clean_transformed](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/6_2_weather_clean_transformed.py) and [6_3_weather_cleaned_transformed](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/mage_blocks/6_3_weather_cleaned_transformed.py) are the block used to extract, clean and export the weather data.

The following image illustrate the relationship between blocks in cleaned set of pipelines above:

![Cleaned data pipelines](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Images/Cleaned%20pipelines.jpg)

## 5. Transform the data 

The last operation over data is performed into BigQuery using `dbt`. The following image illustrate the transformations applied over the cleaned data in BigQuery:

![DAG in dbt](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Images/DAG_dbt.jpg)

After configuring an empty project in dbt as explaned [here](https://docs.getdbt.com/guides/bigquery), I defined 2 sources of data as indicated in the [schema.yml](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Analytics-dezoomcamp/Footballers-transferences/models/staging/schema.yml) file. 

Then, I created two views in staging area, one for [players_data_cleaned](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Analytics-dezoomcamp/Footballers-transferences/models/staging/stg_players_data_cleaned.sql) and other for [weather_data_cleaned](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Analytics-dezoomcamp/Footballers-transferences/models/staging/stg_weather_data_cleaned.sql), which were merged into an optimized table called [fact_transferences](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Analytics-dezoomcamp/Footballers-transferences/models/core/fact_transfers.sql) by partitioning it using the date of the player's transference.

