from jira import ( JIRA,JIRAError )
import json
import os, sys

issue_types = [{"Bug":"bug"},{"Task":"feature request"}]
def parse_event_context():
    event = os.environ.get("EVENT_CONTEXT")
    event_json = json.loads(event)
    issue_type = ""
    issue_body = event_json["issue"]["body"]
    issue_title = event_json["issue"]["title"]
    for label in event_json["issue"]["labels"]:
        for issue_type_obj in issue_types:
            for k,v in issue_type_obj.items():
                if label["name"] ==  v:
                    issue_type = k
    if issue_type == "":
        print("Making default type as task")
        issue_type = "Task"
    return issue_body, issue_type, issue_title
    #print("Please set EVENT_CONTEXT Variable with github issue event type...")
    #sys.exit(1)
    #print("Could not continue creation of NPT JIRA ticket due to {}...".format(e))
    #sys.exit(1)

def run_create_issue(issue_body, issue_type, issue_title):
    """
    JIRA_SERVER environment variable will be feed from Github CI for creating issues
    JIRA_USER, JIRA_PWD will be kept as a secret for authentication
    """
    JIRA_SERVER = os.environ.get("JIRA_SERVER")
    JIRA_USER = os.environ.get("JIRA_USER")
    JIRA_PWD = os.environ.get("JIRA_PWD")

    options = {"server": JIRA_SERVER}
    try:
        jira = JIRA(basic_auth=(JIRA_USER, JIRA_PWD), options=options)
    except JIRAError as e:
        print("Could not connect to JIRA due to Auth Failure/server not reachable: {}".format(e))
        sys.exit(1)
    except Exception as e:
        print("Could not connect to JIRA due to : {}".format(e))
        sys.exit(1)
    Issue = {
        'project': {'key': 'NPT'},
        'summary': issue_title ,
        'description': issue_body,
        'issuetype': {'name': issue_type },
    }
    try:
        new_issue = jira.create_issue(fields=Issue)
        print("New Jinew_issue created {}".format(new_issue))
    except Exception as e:
        print("Could not create JIRA due to : {}", e)
        sys.exit(1)

if __name__ == "__main__":
    issue_body, issue_type, issue_title = parse_event_context()
    run_create_issue(issue_body, issue_type, issue_title)