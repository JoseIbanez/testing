package main

import (
	"context"
	"log"
	"os"

	jira "github.com/andygrunwald/go-jira/v2/onpremise"
	"github.com/trivago/tgo/tcontainer"
)

type SimpleIssue struct {
	IssueId  string
	Assignee string
	Points   string
	Squad    string
}

func get_jira() (*jira.Client, error) {
	// Connect to Jira using environment variables for URL and API token

	jiraURL := os.Getenv("JIRA_URL")
	jiraToken := os.Getenv("JIRA_API_TOKEN")

	log.Printf("Jira URL:%s\n", jiraURL)

	// See "Using Personal Access Tokens"
	// https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html

	tp := jira.BearerAuthTransport{
		Token: jiraToken,
	}

	client, err := jira.NewClient(jiraURL, tp.Client())
	if err != nil {
		return nil, err
	}

	u, _, err := client.User.GetSelf(context.Background())
	if err != nil {
		return nil, err
	}

	log.Printf("Connected to jira, User:%v\n", u.EmailAddress)

	return client, nil

}

func get_subtask_for_ticket(jiraClient *jira.Client, issueId string) ([]string, *SimpleIssue, error) {
	// Check the status of the issue
	log.Printf("Checking issue: %s\n", issueId)
	ctx := context.Background()

	issue, response, err := jiraClient.Issue.Get(ctx, issueId, nil)
	if err != nil {
		log.Printf("Error getting issue details. Issue:%s: Err:%v, Response:%v\n", issueId, err, response)
		return nil, nil, err
	}

	currentStatus := issue.Fields.Status.Name
	log.Printf("Story:%s Description:%s (%s)\n", issue.Key, issue.Fields.Summary, currentStatus)

	customFields, _, err := jiraClient.Issue.GetCustomFields(ctx, issueId)
	if err != nil {
		log.Printf("Error getting issue CustomFields. Issue:%s Err:%s\n", issueId, err)
		return nil, nil, err
	}

	simpleIssue := SimpleIssue{
		IssueId:  issue.Key,
		Assignee: issue.Fields.Assignee.Name,
		Points:   customFields["customfield_10002"], // Assuming this is the field for story points
		Squad:    customFields["customfield_11018"], // Assuming this is the field for squad
	}

	subTaskList := issue.Fields.Subtasks
	var idList []string

	for _, subTask := range subTaskList {
		log.Printf("SubTaks:%s Description:%s\n", subTask.Key, subTask.Fields.Summary)
		idList = append(idList, subTask.Key)
	}

	log.Printf("End of SubTasks")

	return idList, &simpleIssue, nil

}

func check_issue(jiraClient *jira.Client, issueId string) *jira.Issue {

	ctx := context.Background()

	issue, _, err := jiraClient.Issue.Get(ctx, issueId, nil)
	if err != nil {
		log.Printf("Issue:%s Get error:%s\n", issueId, err)
		return nil
	}

	customFields, _, err := jiraClient.Issue.GetCustomFields(ctx, issueId)
	if err != nil {
		log.Printf("Issue:%s GetCustomFields error:%s\n", issueId, err)
		return nil
	}

	squad := customFields["customfield_11018"]
	points := customFields["customfield_10002"]

	assignee := ""
	if issue.Fields.Assignee != nil {
		assignee = issue.Fields.Assignee.Name
	}

	log.Printf("Issue:%s, Squad:%s, Assignee:%s, SP:%s, Description:%s", issue.Key, squad, assignee, points, issue.Fields.Summary)

	return issue
}

func update_issue(jiraClient *jira.Client, simpleIssue *SimpleIssue, issue *jira.Issue) {

	ctx := context.Background()

	customerFieldsUpdate := tcontainer.NewMarshalMap()
	customerFieldsUpdate["customfield_11018"] = map[string]string{"value": simpleIssue.Squad}
	//customerFieldsUpdate["customfield_10002"] = map[string]int{"value": 1}

	issueUpdate := jira.Issue{
		Key: issue.Key,
		Fields: &jira.IssueFields{
			Assignee: &jira.User{Name: simpleIssue.Assignee},
			Unknowns: customerFieldsUpdate,
		},
	}

	issueUpdated, _, err := jiraClient.Issue.Update(ctx, &issueUpdate, nil)
	if err != nil {
		log.Printf("Issue:%s, Update Error:%s\n", issue.Key, err)
		return
	}

	log.Printf("Issue:%s, Updated", issueUpdated.Key)
}

func get_args() string {
	// Get the issue ID from command line arguments
	// Usage: jira1 <issue-id>

	if len(os.Args) < 2 {
		log.Fatalf("Usage: jira1 <issue-id>")
	}

	return os.Args[1]
}

func main() {

	// Set up logging
	log.SetPrefix("main: ")
	log.SetFlags(0)

	issueId := get_args()

	jc, err := get_jira()
	if err != nil {
		log.Fatalf("Error connecting to Jira: %v", err)
	}

	idList, simpleIssue, err := get_subtask_for_ticket(jc, issueId)
	if err != nil {
		log.Fatalf("Error getting subtasks: %v", err)
	}

	for _, subTaskId := range idList {
		log.Printf("SubTask:%s\n", subTaskId)
		issue := check_issue(jc, subTaskId)
		if issue != nil {
			update_issue(jc, simpleIssue, issue)
		}
	}

}
