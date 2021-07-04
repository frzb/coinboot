package main

import (
	"./jsonrpc_sgminer"
	"log"
)

func main() {

	client, err := jsonrpc_sgminer.Dial("tcp", "127.0.0.1:4029")
	if err != nil {
		log.Fatal("dial error:", err)
	}

	var reply string

	err = client.Call("summary", "", &reply)
	if err != nil {
		log.Fatal("Call Error:", err)
	}
	log.Printf("%q", reply)
}
