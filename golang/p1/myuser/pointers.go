package myuser

import (
    "log"
)

func TestPointer(comment string) (string, error) {

    var message string = "hi there"

    val := 1

    msg2,err := mod1(message,1)
    msg3,err := mod2(&message,&val)

    log.Println(msg2)
    log.Println(message,msg3,val)

    return msg3,err
}


func mod1(msg string,val int) (string, error) {

    msg = msg + "-ddd"
    val = val + 1

    log.Println(msg)


    return msg, nil

}


func mod2(msg *string, val *int) (string, error) {


    msg1 := *msg

    msg1 = msg1 + "+ddd"
    *val = *val + 1

    log.Println(msg1)

    return msg1, nil

}

