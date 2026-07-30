# Skill: Frida (Dynamic Instrumentation)

## Install
```bash
pip install frida-tools

# Push frida-server to Android device (rooted)
adb push frida-server /data/local/tmp/
adb shell chmod +x /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &
```

## Basic Usage
```bash
frida-ps -U                          # list running processes (USB)
frida-ps -U | grep <appname>
frida -U -f <package> -l script.js   # spawn + inject
frida -U -p <pid> -l script.js       # attach to running
```

## SSL Pinning Bypass Script
```javascript
// ssl_bypass.js
Java.perform(function() {
    var TrustManager = Java.registerClass({
        name: 'com.example.TrustManager',
        implements: [Java.use('javax.net.ssl.X509TrustManager')],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });
});
// หรือใช้ universal script จาก codeshare.frida.re
```

## Useful Scripts (Codeshare)
```bash
frida -U -f <pkg> --codeshare pcipolloni/universal-android-ssl-pinning-bypass-with-frida
frida -U -f <pkg> --codeshare dzonerzy/fridantiroot
```

## Hook Method
```javascript
Java.perform(function() {
    var MainActivity = Java.use("com.example.MainActivity");
    MainActivity.checkPassword.implementation = function(pass) {
        console.log("Password attempt: " + pass);
        return true;  // bypass check
    };
});
```
