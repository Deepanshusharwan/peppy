package main

import "C"
import (
	"encoding/json"
	"fmt"
	"os/exec"
)

type Factory struct {
	Industry string `json:"industry"`
	Place    string `json:"place"`
}

// NOTE: can't directly return go maps/ slices, thus use JSON

//export testjson
func testjson() *C.char {
	factory := Factory{Industry: "automotive", Place: "texas"}
	jsonData, err := json.Marshal(factory)
	if err != nil {
		return C.CString(`{"error": "json encoding failed"}`)
	}
	return C.CString(string(jsonData))
}

//export listApplications
func listApplications() {
	cmd := exec.Command("mdfind", "kMDItemKind == 'Application'")
	output, err := cmd.Output()

	if err != nil {
		fmt.Println("Command execution error:", err)
		return
	}
	fmt.Print("applications: \n", string(output))
}
func main() {
}
