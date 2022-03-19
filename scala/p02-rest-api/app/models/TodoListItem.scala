package models

case class TodoListItem(id: Long, description: String, isItDone: Boolean)
case class NewTodoListItem(description: String, color: String)

case class RequestItem(
  id: Long,
  description: String,
  size: String,
  state: String
)
