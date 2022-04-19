package main

import (
    "fmt"
    "log"

    "example.com/greetings"

    "golang.org/x/example/stringutil"
    "rsc.io/quote"
)

func main() {
    fmt.Println(stringutil.Reverse("Hello"))
    fmt.Println(stringutil.ToUpper("Hello"))

    // Set properties of the predefined Logger, including
    // the log entry prefix and a flag to disable printing
    // the time, source file, and line number.
    log.SetPrefix("greetings: ")
    // log.SetFlags(0)

    fmt.Println(quote.Go())

    message, err := greetings.Hello("123")


    // If an error was returned, print it to the console and
    // exit the program.
    if err != nil {
        log.Fatal(err)
    }

    // If no error was returned, print the returned message
    // to the console.
    fmt.Println(message)

    // A slice of names.
    names := []string{"Gladys", "Samantha", "Darrin"}

    // Request greeting messages for the names.
    messages, err := greetings.Hellos(names)
    if err != nil {
        log.Fatal(err)
    }
    // If no error was returned, print the returned map of
    // messages to the console.
    fmt.Println(messages)

    for k,v := range messages {
        fmt.Println(k, v)
    }
}