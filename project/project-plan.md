# Project Plan

## Title
<!-- Give your project a short title. -->
Predicting Customer Churn for Optimized Account Management For MADE project.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. What variables most substantially contribute to customer churn in the marketing agency's client base, and how can this data be used to design effective retention strategies?
2. Can we accurately predict customer churn based on historical data?
3. What characteristics have the most influence in predicting client churn?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
The marketing agency observes significant churn in its client base and currently assigns account managers randomly. This project aims to develop a machine-learning model to predict customer churn. By analyzing historical data, we will create a classification algorithm to classify whether a customer will likely churn. This model will enable the company to assign account managers more strategically, reducing churn and enhancing client retention. The dataset, named customer_churn.csv, contains relevant fields such as customer age, total ads purchased, account manager status, years as a customer, number of websites using the service, onboard date, location, and company name.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Customer Churn Dataset
* Metadata URL: https://www.kaggle.com/datasets/hassanamin/customer-churn/data
* Data URL: https://www.kaggle.com/datasets/hassanamin/customer-churn/download?datasetVersionNumber=1
* Data Type: CSV

This dataset contains information on client age, total ad purchases, account manager status, years as a customer, onboarding date, location, and firm name.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->
This project is divided into several work packages, each of which is described as a milestone in the GitHub repository. Each work package contains at least one issue, which is organized as follows:

1. Exploration and Preprocessing of Data
• Conduct a preliminary examination of the customer churn dataset.
• Deal with missing data and outliers.
• Use categorical variables to encode.
• Divide the data into two sets: training and testing.

2. Model Creation
• Select suitable classification algorithms.
• Use the training set to train the model.
• Assess the model's performance on the testing set.

3. Model Validation Using New Data
• Load and preprocess the newly acquired customer data.
• Use the learned model to forecast churn based on new data.

4. Analysis and interpretation of results
• Examine model projections and offer insights into customer turnover factors.

5. Reporting and visualizations
• Create model results visualizations.
• Make the repository visually appealing.
• Finish the project report and documentation.

