package main

import (
	"flag"
	"fmt"
	"math/rand"
	"net/http"
	"strings"
	"sync"
	"time"
)

var (
	url             string
	payload         string
	threads         int
	requestCounter  int
	printedMsgs     []string
	waitGroup       sync.WaitGroup
)

func printMsg(msg string) {
	if !contains(printedMsgs, msg) {
		fmt.Printf("\n%s after %d requests\n", msg, requestCounter)
		printedMsgs = append(printedMsgs, msg)
	}
}

func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}

func init() {
	rand.Seed(time.Now().UnixNano())
}

func handleStatusCodes(statusCode int) {
	requestCounter++
	fmt.Printf("\r%d requests have been sent", requestCounter)

	if statusCode == 429 {
		printMsg("You have been throttled")
	}
	if statusCode == 500 {
		printMsg("Status code 500 received")
	}
}

func sendGET() {
	defer waitGroup.Done()

	resp, err := http.Get(url)
	if err != nil {
		return
	}
	defer resp.Body.Close()

	handleStatusCodes(resp.StatusCode)
}

func sendPOST() {
	defer waitGroup.Done()

	resp, err := http.Post(url, "application/x-www-form-urlencoded", strings.NewReader(payload))
	if err != nil {
		return
	}
	defer resp.Body.Close()

	handleStatusCodes(resp.StatusCode)
}

func main() {
	flag.StringVar(&url, "g", "", "Specify GET request. Usage: -g '<url>'")
	flag.StringVar(&url, "p", "", "Specify POST request. Usage: -p '<url>'")
	flag.StringVar(&payload, "d", "", "Specify data payload for POST request")
	flag.IntVar(&threads, "t", 500, "Specify number of threads to be used")
	flag.Parse()

	if url == "" {
		flag.Usage()
		return
	}

	if flag.NFlag() == 0 {
		flag.Usage()
		return
	}

	if flag.NFlag() == 1 {
		fmt.Println("You must specify either a GET (-g) or POST (-p) request.")
		return
	}

	waitGroup.Add(threads)

	for i := 0; i < threads; i++ {
		if url != "" {
			if payload != "" {
				go sendPOST()
			} else {
				go sendGET()
			}
		}
	}
	waitGroup.Wait()
}

