import org.scalatest.FunSuite

//import javax.inject._
import models.{NewTodoListItem, TodoListItem}
import models.RequestItem
import play.api.libs.json._
import play.api.mvc.{Action, AnyContent, BaseController, ControllerComponents}
//import scala.collection.mutable

class JsonSpec extends FunSuite {
  test("CubeCalculator.cube") {
    assert(27 === 27)
  }

  test("BasicJsonTest") {
    implicit val newTodoListJson = Json.format[NewTodoListItem]

    val body: String = """{"color":"red", "description": "some new item"}"""
    val jsonObject = Some(Json.parse(body))

    val newItem = jsonObject.flatMap(Json.fromJson[NewTodoListItem](_).asOpt)

    assert(newItem.get.color === "red")
  }

}
