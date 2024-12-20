package main

import (
	"context"
	"fmt"
	"log"
	"os"

	jira "github.com/andygrunwald/go-jira/v2/onpremise"
)

func get_jira() *jira.Client {

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
		panic(err)
	}

	u, _, err := client.User.GetSelf(context.Background())
	if err != nil {
		panic(err)
	}

	log.Printf("Connected to jira, User:%v\n", u.EmailAddress)

	check_ticket(client, "PPEP-310")

	return client

}

func check_ticket(jiraClient *jira.Client, issueId string) {
	issue, _, _ := jiraClient.Issue.Get(context.Background(), issueId, nil)
	currentStatus := issue.Fields.Status.Name
	fmt.Printf("Current status: %s\n", currentStatus)

	subTaskList := issue.Fields.Subtasks
	ctx := context.Background()

	for _, subTask := range subTaskList {
		log.Printf("SubTaks:%s Description:%s\n", subTask.Key, subTask.Fields.Summary)

		customFields, _, _ := jiraClient.Issue.GetCustomFields(ctx, subTask.Key)

		log.Printf("v: %v", customFields["customfield_11018"])

	}

}

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	jc := get_jira()
	fmt.Printf("jiraClient: %v\n", jc)

}
