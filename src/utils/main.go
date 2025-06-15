package main

import "C"
import (
	"fmt"
	"os"
	"os/exec"
)

//export listApplications
func listApplications() {
	// open or create the output file
	file, err := os.Create("applications.txt")
	if err != nil {
		fmt.Println("Failed to create file:", err)
		return
	}
	defer file.Close()
	cmd := exec.Command("mdfind", "kMDItemKind == 'Application'")

	// Redirect command output to the file
	cmd.Stdout = file

	// Run the command
	err = cmd.Run()
	if err != nil {
		fmt.Println("Command execution error:", err)
		return
	}
}
func main() {
}
