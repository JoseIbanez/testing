package main

import (
	"context"
	"log"
	"os"

	jira "github.com/andygrunwald/go-jira/v2/onpremise"
)

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

func check_ticket(jiraClient *jira.Client, issueId string) {
	// Check the status of the issue
	log.Printf("Checking issue: %s\n", issueId)

	issue, response, err := jiraClient.Issue.Get(context.Background(), issueId, nil)
	if err != nil {
		log.Fatalf("Error getting issue %s: %v, Response:%v", issueId, err, response)
	}

	currentStatus := issue.Fields.Status.Name
	log.Printf("%s Description:%s (%s)\n", issue.Key, issue.Fields.Summary, currentStatus)

	subTaskList := issue.Fields.Subtasks
	ctx := context.Background()

	for _, subTask := range subTaskList {
		log.Printf("SubTaks:%s Description:%s\n", subTask.Key, subTask.Fields.Summary)

		customFields, _, _ := jiraClient.Issue.GetCustomFields(ctx, subTask.Key)

		log.Printf("v: %v", customFields["customfield_11018"])

	}

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

	check_ticket(jc, issueId)

}
