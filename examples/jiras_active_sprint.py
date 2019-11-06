"""
This script lists all JIRAs that are in current sprints.
"""

import pandas as pd
from tabulate import tabulate
from jira import JIRA

pd.options.display.max_columns = 10
pd.options.display.max_rows = 200
pd.options.display.max_colwidth = 100
pd.options.display.precision = 3

options = {"server": "https://your-site.atlassian.net"}
jira = JIRA(
    options, basic_auth=("<user-name>", "<api-token>")
)

# Get all the issues in the current sprints
issues_in_sprint = jira.search_issues(
    "sprint in openSprints() AND issuetype != Sub-task"
)

# Initialize the final list
final_list = []

"""
Get all jiras for the given query
Go thru each jira and grab epic name and initiative name, if available
    customfield_10004 is epic link
    customfield_10006 is epic name
    customfield_11400.data.summary is initiative name

This code will work even if there are no initiatives in your JIRA instance. 
(Initiatives are available when you enable JIRA Portfolio)
"""

for key in issues_in_sprint:
    issue = jira.issue(key)

    issue_key = issue.key
    assignee = "Unassigned"
    if issue.fields.assignee is not None:
        assignee = issue.fields.assignee.displayName
    issue_type = issue.fields.issuetype.name
    issue_summary = issue.fields.summary
    issue_status = issue.fields.status.name

    var_list = []
    var_list.append(issue_key)
    var_list.append(assignee)
    var_list.append(issue_type)
    var_list.append(issue_summary)

    if hasattr(issue.fields, "customfield_10004"):
        if issue.fields.customfield_10004 is not None:
            epic_link = issue.fields.customfield_10004
            issue = jira.issue(epic_link)
            epic_name = issue.fields.customfield_10006
            var_list.append(epic_name)
            if (hasattr(issue.fields, "customfield_11400")) and (
                issue.fields.customfield_11400 is not None
            ):
                initiative_name = issue.fields.customfield_11400.data.summary
                var_list.append(initiative_name)
            else:
                var_list.append("None")
        else:
            var_list.append("None")
            var_list.append("None")

    final_list.append(var_list)


labels = ["key", "assignee", "type", "title", "epic", "initiative"]
df = pd.DataFrame.from_records(final_list, columns=labels)
df = df.sort_values(by=["initiative"])

print(tabulate(df, labels, tablefmt="grid"))
