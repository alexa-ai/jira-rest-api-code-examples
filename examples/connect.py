from jira import JIRA

options = {"server": "https://your-site.atlassian.net"}
jira = JIRA(options, basic_auth=("your-user-name", "api-token"))
