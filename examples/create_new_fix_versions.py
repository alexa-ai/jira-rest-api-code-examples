'''
Purpose of this script:

JIRA does not have feature to create fix version for multiple projects at once. This is problematic,
if your team manages multiple projects and all need same fix version. Instead of manually creating
fix version for each project, you can use this script to add fix version for all projects.
'''

from jira import JIRA

# You can either use your Jira username and password OR get API token from Jira to connect to
# your Jira instance. Getting API token is preferable, because you don't want to expose your plain text
# password in python code.
# Atlassian has instructions at https://confluence.atlassian.com/cloud/api-tokens-938839638.html
# to create api token.


options = {"server": "https://your-site.atlassian.net"}
jira = JIRA(options, basic_auth=("your-user-name", "api-token"))

LIST_OF_PROJECTS = ["PLATFORM", "PAYMENTS", "ENTERPRISE", "DATA"]

# Expand this list, if you want to create multiple fix versions at once.
# Make sure fixversion and releaseDates lists have same number of values
LIST_OF_FIXVERSIONS = ["2019-12-18 US Release"]
LIST_OF_RELEASEDATES = ["2019-12-18"]

# Loop thru project list and create fix versions for each project.
# Don't worry about creating duplicate fix version, JIRA will reject duplicate requests
for i in enumerate(LIST_OF_PROJECTS):
    for j in enumerate(LIST_OF_FIXVERSIONS):
        newversion = jira.create_version(
            name=LIST_OF_FIXVERSIONS[j],
            project=LIST_OF_PROJECTS[i],
            releaseDate=LIST_OF_RELEASEDATES[j],
        )
        print(LIST_OF_FIXVERSIONS[j] + " is created for project " + LIST_OF_PROJECTS[i])
