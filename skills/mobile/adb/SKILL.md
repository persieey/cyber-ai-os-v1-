# Skill: ADB (Android Debug Bridge)

## Setup
```bash
adb devices           # list connected devices
adb start-server
adb kill-server
```

## File Operations
```bash
adb pull /sdcard/file.txt .          # download from device
adb push local.txt /sdcard/          # upload to device
adb pull /data/data/<pkg>/databases/ . # app database (root needed)
```

## Shell
```bash
adb shell                            # interactive shell
adb shell <command>                  # one-shot
adb shell pm list packages           # installed apps
adb shell pm path <package>          # APK location
adb shell dumpsys <service>          # service info
adb shell logcat                     # live logs
adb logcat | grep -i "error\|token\|password"
```

## App Management
```bash
adb install app.apk                  # install APK
adb uninstall <package>              # uninstall
adb shell am start -n <pkg>/<activity>  # launch activity
adb shell am start -a android.intent.action.VIEW -d "url"
```

## Pentest Usage
```bash
# Extract APK
adb shell pm path com.example.app
adb pull /data/app/com.example.app-1/base.apk app.apk

# Read shared prefs (root)
adb shell cat /data/data/<pkg>/shared_prefs/*.xml

# Read SQLite DB (root)
adb shell sqlite3 /data/data/<pkg>/databases/main.db ".tables"

# Port forward (Burp proxy)
adb reverse tcp:8080 tcp:8080
```
