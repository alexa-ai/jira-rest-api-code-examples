# jira-tutorials
This repository contains code examples to get better value from JIRA

# Instructions
First step is to install Jira module from pycontribs. Download and install using "pip install jira". If you use conda, refer <a href="https://anaconda.org/conda-forge/jira">this page</a>.

You can either use your JIRA username and password OR get API token from JIRA to connect to your JIRA instance. Getting API token is preferable, because you don't want to expose your plain text password in python code. Atlassian has <a href="https://confluence.atlassian.com/cloud/api-tokens-938839638.html">instructions</a> to create API token.

Now, you have JIRA module installed and API token created. Time to test Jira instance connection using some python code! Check the code at connect.py (under examples directory) to make sure you are able to connect to JIRA. If you are not able to connect, make sure that your api token and username are valid. 

The examples given are for JIRA cloud instance. For JIRA server instance, api token is not available. So, you would need to use password or OAuth. (Please refer <a href="https://community.atlassian.com/t5/Jira-questions/API-Tokens-for-self-hosted-Jira/qaq-p/820644">this page</a>)
