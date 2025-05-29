package main

import (
	"context"
	"fmt"
	"log"
	"os"

	jira "github.com/andygrunwald/go-jira/v2/onpremise"
	"github.com/trivago/tgo/tcontainer"
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

	//check_ticket(client, "PPEP-8629")

	return client

}

func check_ticket(jiraClient *jira.Client, issueId string)  {
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

	log.Printf("End of SubTasks")

}


func check_issue(jiraClient *jira.Client, issueId string) (*jira.Issue) {

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


func update_issue(jiraClient *jira.Client, issue *jira.Issue) {

	ctx := context.Background()

	customerFieldsUpdate := tcontainer.NewMarshalMap()
	customerFieldsUpdate["customfield_11018"] = map[string]string{"value": "Assurance"}
	//customerFieldsUpdate["customfield_10002"] = map[string]int{"value": 1}

	issueUpdate := jira.Issue{
		Key: issue.Key,
		Fields: &jira.IssueFields{
			Assignee: &jira.User{Name: "jose.ibanez@vodafone.com"},
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

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	jc := get_jira()
	//fmt.Printf("jiraClient: %v\n", jc)

	targetIssueId := "PPEP-8629"

	issue := check_issue(jc, targetIssueId)
	update_issue(jc, issue)
	check_issue(jc, targetIssueId)


}
