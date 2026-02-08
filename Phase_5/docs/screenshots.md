# Screenshot Checklist for Demo

**Purpose**: Prepare screenshots as backup for hackathon demo
**Target**: 7 key moments in the demo flow

---

## Screenshot Checklist

| # | Screenshot | Purpose | When to Capture |
|---|-----------|---------|-----------------|
| 1 | `screenshots/01-login.png` | Login screen | After opening frontend URL |
| 2 | `screenshots/02-task-list.png` | Task list overview | After login, before creating tasks |
| 3 | `screenshots/03-create-form.png` | Create task form | When form is filled out, before save |
| 4 | `screenshots/04-new-task.png` | Task in list | After saving new task, showing it in list |
| 5 | `screenshots/05-consumer-logs.png` | Event processing logs | Terminal showing consumer logs with events |
| 6 | `screenshots/06-dapr-components.png` | Dapr components | Terminal showing `kubectl get components.dapr.io` |
| 7 | `screenshots/07-pod-status.png` | Pod health | Terminal showing `kubectl get pods` with 2/2 Ready |

---

## Detailed Capture Instructions

### Screenshot 1: Login Screen

**What**: Frontend login interface

**How to Capture**:
1. Open browser to frontend URL: `minikube service todo-frontend --url`
2. Wait for page to fully load
3. Take screenshot showing:
   - Application title "Todo AI Chatbot"
   - Login form (username/password fields or OpenAI button)
   - Clean background

**Expected**: Professional login screen UI

---

### Screenshot 2: Task List Overview

**What**: Main task list showing variety of tasks

**How to Capture**:
1. After logging in
2. Ensure 3-5 tasks visible with different:
   - Priorities (high=red, medium=yellow, low=green)
   - Tags (work, personal, etc.)
   - Due dates
   - Completion status
3. Take screenshot showing task cards

**Expected**: Organized task list with visual indicators

---

### Screenshot 3: Create Task Form

**What**: Task creation form with all fields

**How to Capture**:
1. Click "New Task" button
2. Fill in all fields:
   - Title: "Daily Standup"
   - Description: "Daily team sync meeting"
   - Recurrence: Select "Daily"
   - Priority: Select "High"
   - Tags: Enter "work"
   - Due Date: Select tomorrow's date
3. Take screenshot before clicking Save/Create

**Expected**: Filled form with all advanced options visible

---

### Screenshot 4: New Task in List

**What**: Task list with newly created recurring task

**How to Capture**:
1. After creating the task from Screenshot 3
2. Wait for task to appear in list
3. Ensure task shows:
   - Recurring indicator (🔄 or similar icon)
   - Priority badge (High)
   - Tag badge (work)
   - Due date
4. Take screenshot highlighting the new task

**Expected**: Task list with new task prominently displayed

---

### Screenshot 5: Consumer Logs (Event Processing)

**What**: Terminal showing event-driven architecture in action

**How to Capture**:
1. Open terminal
2. Run: `kubectl logs deployment/todo-consumers --tail=50`
3. Create a test task (or wait if one exists)
4. Look for JSON log entries showing:
   - `"event_type": "task.created"`
   - `"consumer": "recurring-task-consumer"`
   - `"action_taken": "..."`
5. Take screenshot of terminal

**Expected**: Terminal with structured JSON logs showing event processing

---

### Screenshot 6: Dapr Components

**What**: Dapr components loaded in the cluster

**How to Capture**:
1. Open terminal
2. Run: `kubectl get components.dapr.io`
3. Wait for output showing:
   - NAME: kafka-pubsub, postgresql, kubernetes-secrets
   - STATUS: Loaded
   - AGE: Some duration
4. Take screenshot

**Expected**: Table showing 3 components with Loaded status

---

### Screenshot 7: Pod Health Status

**What**: All pods running with Dapr sidecars

**How to Capture**:
1. Open terminal
2. Run: `kubectl get pods`
3. Wait for output showing:
   - All pods STATUS=Running
   - All READY=2/2 (app + Dapr sidecar)
   - No pods in CrashLoopBackOff
4. Optionally run: `kubectl get pods -o wide`
5. Take screenshot

**Expected**: Clean output showing healthy pods

---

## Capture Tools

### Windows

**Snipping Tool** (Built-in):
1. Press `Windows Key + Shift + S`
2. Select area or window
3. Saves to Pictures\Screenshots by default

**PowerShell** (Command-line):
```powershell
# Take screenshot of specific window
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$bmp = New-Object System.Drawing.Bitmap $screen.Bounds.Width, $screen.Bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen($screen.Bounds.Location.X, $screen.Bounds.Location.Y, $screen.Bounds.Width, $screen.Bounds.Height)
$bmp.Save("$HOME\screenshot.png")
$graphics.Dispose()
$bmp.Dispose()
```

### Linux/Mac (Minikube shell)

**scrot** (Command-line):
```bash
# Take screenshot of entire screen after 5 seconds
sleep 5 && scrot screenshot.png

# Take screenshot of specific window
scrot -u screenshot.png
```

---

## Screenshot Preparation Tips

1. **Clean Up Browser**
   - Hide unnecessary bookmarks bar
   - Use full-screen mode (F11) if needed
   - Clear browser cache for consistent loading

2. **Terminal Preparation**
   - Use appropriate terminal size (120x40 minimum)
   - Increase font size for readability
   - Use light background for screenshots
   - Clear screen before running commands

3. **Consistent Styling**
   - Use same terminal theme for all screenshots
   - Ensure timestamps are visible
   - Show command prompt for context

4. **Multiple Takes**
   - Take 2-3 shots of each moment
   - Choose clearest/most representative
   - Organize in numbered folders if needed

5. **File Naming**
   - Use consistent naming convention
   - Include descriptive suffixes if variations
   - Keep all screenshots in one `screenshots/` directory

---

## Post-Capture Checklist

- [ ] All 7 screenshots captured
- [ ] File names match checklist
- [ ] Screenshots are clear and readable
- [ ] No sensitive information visible
- [ ] Terminal text is legible
- [ ] Browser UI shows consistent theme
- [ ] Screenshots organized in `screenshots/` directory
- [ ] Backup screenshots ready (in case live demo fails)

---

## Using Screenshots in Demo

If live demo fails:

1. **Fall Back to Slides**
   - Present screenshots in sequential order
   - Add narrative for each screenshot
   - Explain what would happen in live demo

2. **Reference in Documentation**
   - Link to screenshots in README
   - Include in demo documentation
   - Add to presentation slides

3. **Video Recording Alternative**
   - Use screenshots to create video walkthrough
   - Add voiceover explaining each step
   - Keep under 90 seconds target

---

## Notes

- Screenshots serve as backup for live demo
- Ensure they represent the actual functionality
- Update screenshots if UI changes significantly
- Keep screenshots in version control for reference
