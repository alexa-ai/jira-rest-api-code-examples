"""
Purpose of the script is to get the time spent on entire initiative.

Usage: python jira_script_timetracking_per_initiative.py <initiative_jira_key>
"""

import sys
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

"""
Get all epics for given initiative key. Get all stories/task for each epic and add up the original estimate and
time spent. JIRA does not provide accumulated estimate and time spent at epic level. We would need to look up
each story/task and get those data.
"""

# Validate the input
if len(sys.argv) == 1:
    print(
        'No argument is supplied. Use the format "python <program name> <initiative_jira_key>"'
    )
    quit()

initiative_jira_key = sys.argv[1]
issue = jira.issue(initiative_jira_key)
#print('Info: the given jira key is ' + str(issue.fields.issuetype))
if(str(issue.fields.issuetype) != 'Initiative'):
	print('Specified argument is not the Initiative key')
	quit()

# Get all the epics under the initiative
jql = " 'Parent Link' = " + sys.argv[1]
issues_in_initiative = jira.search_issues(jql)

# Initialize the final list and counters
final_list = []
total_initiative_original_estimate = 0
total_initiative_time_spent = 0

for epic in issues_in_initiative:

    issue = jira.issue(epic)
    issue_key = issue.key

    var_list = []
    var_list.append(issue_key)

    # Get all the issues under the epic
    jql = " 'Epic Link' = " + issue_key
    issues_in_epic = jira.search_issues(jql)

    # Initialize epic level counters
    total_epic_original_estimate = 0
    total_epic_time_spent = 0

    for story in issues_in_epic:

        issue = jira.issue(story)
        if hasattr(issue.fields, "aggregatetimeoriginalestimate"):
            if issue.fields.aggregatetimeoriginalestimate is not None:
                original_estimate = issue.fields.aggregatetimeoriginalestimate / 3600
                total_epic_original_estimate = (
                    total_epic_original_estimate + original_estimate
                )

        if hasattr(issue.fields, "aggregatetimespent"):
            if issue.fields.aggregatetimespent is not None:
                time_spent = issue.fields.aggregatetimespent / 3600
                total_epic_time_spent = total_epic_time_spent + time_spent

    var_list.append(total_epic_original_estimate)
    var_list.append(total_epic_time_spent)
    final_list.append(var_list)

    total_initiative_original_estimate = (
        total_initiative_original_estimate + total_epic_original_estimate
    )
    total_initiative_time_spent = total_initiative_time_spent + total_epic_time_spent

# Add the total
var_list = []
var_list.append("TOTAL")
var_list.append(total_initiative_original_estimate)
var_list.append(total_initiative_time_spent)
final_list.append(var_list)

# Print the data
labels = ["Epic", "Original Estimate (Hours)", "Time Spent (Hours)"]
df = pd.DataFrame.from_records(final_list, columns=labels)

print(tabulate(df, labels, tablefmt="grid"))
