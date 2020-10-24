## Data-modeling with postgresql---ETL-pipeline
# Purpose of this Mini-Project :
we are going to do a little task for a company, the startup was over the past year collectiong data in order to track their user's but this data lives in format that not suitable for data scinetist/data analyst so as  data enginner i come to help, data modeling is done to empower the analytics and that means the data should be easily to 
query for analysis.
# databases design ( schema ) :
The star schema separates business process data into facts, which hold the measurable, quantitative data about a business, and dimensions which are descriptive attributes related to fact data. Examples of fact data include sales price, sale quantity, and time, distance, speed and weight measurements. Related dimension attribute examples include product models, product colors, product sizes, geographic locations, and salesperson names.
# ETL pipeline : 
i created an ETL pipeline in order to collect data from json files and them inserts that data into tables ( database )  so that it can be queried by data scientist and analyst for analysis ( see the ETL.py file ).
# files in this repo : 
-- connect.py : contains the connection scripts to the postgresql databases.
-- ETL.py : contains the logic behind inserting the whole dataset into the fact table and dimension tables.
-- sql.py : contains sql queries that creates the tables in postgresql management system and also the queries used to insert the data.
