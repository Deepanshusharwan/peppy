// go build -buildmode=c-shared -o app_lister.so app_lister.go
package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"encoding/json"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"unsafe"
)

type AppInfo struct {
	Name string `json:"name"`
	Exec string `json:"exec"`
	// Count int    `json:"count"`
	Icns string `json:"icns"`
}

var appDirs = []string{
	"/Applications",
	"/System/Applications",
}

// Check if app bundle is valid and launchable
func isValidApp(appPath string) bool {
	// Info.plist, is available
	infoPlistPath := filepath.Join(appPath, "Contents", "Info.plist")
	if _, err := os.Stat(infoPlistPath); os.IsNotExist(err) {
		return false
	}

	// check if MacOS directory exists
	macOSDir := filepath.Join(appPath, "Contents", "MacOS")
	if _, err := os.Stat(macOSDir); os.IsNotExist(err) {
		return false
	}

	// check if there's at least one executable file in MacOS directory
	files, err := os.ReadDir(macOSDir)
	if err != nil {
		return false
	}

	for _, file := range files {
		if !file.IsDir() {
			filePath := filepath.Join(macOSDir, file.Name())
			if info, err := os.Stat(filePath); err == nil {
				// is file +x/executable
				if info.Mode()&0111 != 0 {
					return true
				}
			}
		}
	}
	return false
}

func getAppIcon(appPath string) string {
	resourcesDir := filepath.Join(appPath, "Contents", "Resources")
	if _, err := os.Stat(resourcesDir); os.IsNotExist(err) {
		return ""
	}

	iconPatterns := []string{
		"*.icns",
		"app.icns",
		"icon.icns",
		"AppIcon.icns",
	}
	for _, pattern := range iconPatterns {
		matches, err := filepath.Glob(filepath.Join(resourcesDir, pattern))
		if err == nil && len(matches) > 0 {
			return matches[0]
		}
	}
	return ""
}

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
	var apps []AppInfo
	appMap := make(map[string]bool) // avoid duplicates

	// Get user's HOME directory for user-specific applications
	HOME, err := os.UserHomeDir()
	if err == nil {
		userAppsDir := filepath.Join(HOME, "Applications")
		if _, err := os.Stat(userAppsDir); err == nil {
			appDirs = append(appDirs, userAppsDir)
		}
	}

	// dir crawler
	for _, dir := range appDirs {
		err := filepath.WalkDir(dir, func(path string, d fs.DirEntry, err error) error {
			if err != nil {
				return nil
			}

			if d.IsDir() && strings.HasSuffix(path, ".app") {
				appName := strings.TrimSuffix(filepath.Base(path), ".app")

				//skip, if already processed
				if appMap[appName] {
					return filepath.SkipDir
				}

				// check, if app is launchable
				if !isValidApp(path) {
					return filepath.SkipDir
				}

				appMap[appName] = true
				exenPath := "open '" + path + "'"
				iconPath := getAppIcon(path)

				apps = append(apps, AppInfo{
					Name: appName,
					Exec: exenPath,
					Icns: iconPath,
				})
				return filepath.SkipDir //don't go deeper into .app bundle
			}
			return nil
		})

		if err != nil {
			fmt.Printf("Error crawling dir %s: %v\n", dir, err)
		}
	}

	jsonBytes, _ := json.Marshal(apps)
	return C.CString(string(jsonBytes))
}

//export FreeCString
func FreeCString(ptr *C.char) {
	C.free(unsafe.Pointer(ptr))
}

func main() {}
