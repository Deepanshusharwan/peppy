package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"bufio"
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"unsafe"
)

type AppInfo struct {
	Name    string `json:"name"`
	Path    string `json:"path"`
	Counter int    `json:"count"`
}

// NOTE: can't directly return go maps/ slices, thus use JSON

//export testjson
// func testjson() *C.char {
// 	factory := Factory{Industry: "automotive", Place: "texas"}
// 	jsonData, err := json.Marshal(factory)
// 	if err != nil {
// 		return C.CString(`{"error": "json encoding failed"}`)
// 	}
// 	return C.CString(string(jsonData))
// }

//export listApplications
func listApplications() *C.char {
	cmd := exec.Command("mdfind", "kMDItemKind == 'Application'")
	output, err := cmd.Output()

	if err != nil {
		fmt.Println("Command execution error:", err)
		return C.CString(`[]`)
	}
	// fmt.Print("applications: \n", string(output))

	var apps []AppInfo
	scanner := bufio.NewScanner(strings.NewReader(string(output)))

	for scanner.Scan() {
		appPath := scanner.Text()

		//extract app name
		sectors := strings.Split(appPath, "/")
		appName := strings.TrimSuffix(sectors[len(sectors)-1], ".app")

		apps = append(apps, AppInfo{
			Name: appName,
			Path: appPath,
		})
	}

	jsonBytes, _ := json.Marshal(apps)
	return C.CString(string(jsonBytes))
}

//export FreeCString
func FreeCString(ptr *C.char) {
	// fmt.Printf("FreeCString called on: %p\n", ptr)
	C.free(unsafe.Pointer(ptr))
}

func main() {}
