lazy val root = (project in file(".")).
  settings(
    inThisBuild(List(
      organization := "com.example",
      scalaVersion := "2.13.3"
    )),
    name := "scalatest-example"
  )

libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.2" % Test
libraryDependencies += "com.softwaremill.sttp.client3" %% "core" % "3.1.1"
libraryDependencies += "com.softwaremill.sttp.client3" %% "akka-http-backend" % "3.1.1"
libraryDependencies += "com.softwaremill.sttp.client3" %% "json4s" % "3.1.1"
libraryDependencies += "org.json4s" %% "json4s-native" % "3.7.0-M8"