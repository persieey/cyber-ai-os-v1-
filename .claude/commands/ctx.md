# Context Manager

Read workspace/active/session.md first.

Action: $ARGUMENTS

## If action is "show" or empty
Display the current session in a clean format.
If session is empty, say "ยังไม่มี session ที่ active อยู่"

## If action is "new [task name]"
Create a new session in workspace/active/session.md using the schema in src/context-engine/SCHEMA.md
Ask: task type? (CTF/Lab/Learning) and starting mode? (Hint/Guided/Walkthrough)
Then write the new session file.

## If action is "update [field] [value]"
Update the specified field in session.md
Valid fields: phase, mode, done (append), findings (append), pending (append), notes (append)

## If action is "clear"
Reset workspace/active/session.md to the empty template from src/context-engine/SCHEMA.md
Confirm with user before clearing.

## If action is "done"
Set phase to Done, move session.md to workspace/archive/[name]-[date].md
Then reset active session to empty.

Start response with:
**[Context Engine] [Action: <action>]**
