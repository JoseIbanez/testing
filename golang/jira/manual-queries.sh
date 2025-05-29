curl -X PUT \
  -H "Authorization: Bearer $JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value": "3"}' \
  "$JIRA_URL/rest/agile/1.0/issue/PPEP-8635"
