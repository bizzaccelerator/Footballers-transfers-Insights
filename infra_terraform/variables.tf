locals {
  data_lake_bucket = "soccer-dataset"
}

variable "credentials" {
  description = "My Credentials"
  default     = "C://Users/jober/OneDrive/Desktop/Footballers_transfers_Insights/credentials/data-taxi-1-a1d4e91c10cd.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}

variable "project" {
  description = "Final project for the Data Engineering Zoomcamp of Data Talks Club."
  default = "data-taxi-1"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "us-central1"
  type = string
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "football_data"
}

variable "TABLE_NAME" {
  description = "BigQuery table"
  type = string
  default = "transfer_info"
}