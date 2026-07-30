# Skill: Objection (Runtime Mobile Exploration)

## Install
```bash
pip install objection
```

## Android Usage
```bash
# Inject into running app
objection -g <package.name> explore

# Spawn app
objection -g <package.name> explore --startup-command 'android sslpinning disable'
```

## iOS Usage
```bash
# Requires Frida on jailbroken device
objection -g <BundleID> explore
```

## Common Commands (inside objection shell)

**Android**
```
android sslpinning disable          # bypass SSL pinning
android root disable                # bypass root detection
android hooking list classes        # list all classes
android hooking list class_methods <classname>
android hooking watch class_method <class> <method>
android heap search instances <class>
env                                 # app directories
```

**iOS**
```
ios sslpinning disable
ios jailbreak simulate
ios hooking list classes
ios hooking watch method '+[ClassName methodName]'
ios keychain dump                   # extract keychain items
ios pasteboard monitor
```

## File System (both platforms)
```
ls                    # list current directory
cat <file>            # read file
download <file>       # download to local
```
