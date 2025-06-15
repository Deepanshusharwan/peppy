package main

import "C"
import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"strings"
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
func listApplications() {
	cmd := exec.Command("mdfind", "kMDItemKind == 'Application'")
	output, err := cmd.Output()

	if err != nil {
		fmt.Println("Command execution error:", err)
		return
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

	file, err := os.Create("applications.json")
	if err != nil {
		fmt.Println("Failed to create file:", err)
		return
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ") // pretty print
	err = encoder.Encode(apps)
	if err != nil {
		fmt.Println("Failed to encode JSON:", err)
		return
	}
}

func main() {}
