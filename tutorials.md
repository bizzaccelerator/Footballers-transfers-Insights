# Tutorial for reproducing the project

Here bellow you can find a series of steps that allows you to reproduce this project. The requirements for this project are:

- Google cloud account.
- Terraform by HashiCorp installed in your local environment.
- Internet connection.

In that sense, and knowing that we will use selenium deployed in a deployed environment, the first thing we must is 

## 1. Prepare the cloud environment fror the project

Google Cloud was selected to elaborate the project. Google Cloud Storage and BigQuery were selected as a datalake service and data warehousing, respectably. I used `Terraform` to prepare the required google environment using both [main.tf](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/infra_terraform/main.tf) and [variables.tf](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/infra_terraform/variables.tf) files. 

## 2. Creating an image of our application

To do that, we will create a docker image based on the latest image of Mage-ai - the orchestrator -, and on top of it, we install the combo google chrome + `chrome-driver` that allow us to perform webscraping tasks, and a list of python libraries indicated [here](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/requirements.txt)

Use this [Dockerfile](https://github.com/bizzaccelerator/Footballers-transfers-Insights/blob/main/Dockerfile)

## 3. Deploy the application image into cloud


