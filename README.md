# Footballers Transfers Insights

The goal of this project was to apply everything I have learned in the 2.024 cohort of the Data Engineering Zoomcamp by Data Talks Club. The project here below simulates a real scenario where C-suite directors of a football players' representative agency need information to take more informed decisions about where and when make investments in players.  

![main wallpaper](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Images/Wallpaper1.jpg)

## Problem statement
This could be understood in two leves: a business problem and a technical problem. 

### _Business problem:_
This agency desires to optimize its investments on actives (the players), so it can perform the more profitable commercial operations possible. However, under a tight budget, the agency faces the need to obtain data at no cost. In addition, some managers believe there is a relationship between the amount of rain in a day and the number of commercial transactions valued at 500.000 Euros or upper performed in the worldwide market. Hence, the decision takers require the better data available that allows them to identify if that believe is real or not.

### _Technical problem:_
According to the business problem, as a Data engineer, I'm required to identify and extract valuable data about the different players transactions at 500.000 Euros or upper, and the weather during the day when the transaction was executed, both from free sources available online. After that, it’s necessary to process and to clean raw data extracted, so a visualization tool can be made available to the decision takers at any time. All that, in a cloud solution that improve reliability, readability and safeness of the data at hand. 

## Solution proposed
The engineering solution proposed extract players transferences information in `**batches**` from transfermarket, one of the largest sport websites of the world. The extraction for each transference, valued at 500.000 Euros and upper, is made daily by using `selenium` to perform webscraping over the detailed website (https://www.transfermarkt.com/statistik/neuestetransfers), then saving a .csv file in Google Clud Storage (GCS) corresponding to each day. 

Once all the transferences for the day were collected, every seller team in that .csv file is used as input into Wikpedia API to get free information for each one of those teams returning fields such as the team name, nickname, foundation information, coach, and city, among others. Then the information returned for each team is collected into a .csv which will be saved into GCS. 

Therefore, the field `city` from the teams information saved from wikipedia for each day will then be used as input into weatherapi to get the weather data for each location reported. Thats the way I get the climate status and all the weather data of interest. Then the weather information returned for each location is collected into a .csv which will be saved into GCS.

Once all raw data is collected for players, teams and weather targets, a pipeline - one for each source - is implemented to clean the data and save it into individual tables in BigQuery (BQ). The cleaned data into BQ will be transformed using `dbt` to elaborate a final table in BQ which will be sent into `Looker` to generate a dashboard that allow the C-suite managers to take the required decisions. 

All those data operations are performed using `python` and a dockerized application image with selenium and `Mage` as orchestration tool. The required infrastructure in defined and modified using `Terraform`. 

See here below the infrastructure utilized:

![Tech Infraestructure](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Images/Infrastructura.gif)

### Technologies used: 


