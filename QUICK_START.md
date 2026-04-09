# 🚀 QUICK START GUIDE

## Installation (2 minutes)

### Step 1: Install Dependencies
```bash
python install_dependencies.py
```

### Step 2: Verify Installation
You should see:
```
✅ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!
🚀 You can now run: python3 AIlinuxV2.py
```

## Running the Tool (30 seconds)

### Launch
```bash
python AIlinuxV2.py
```

### First Time Setup

1. **Configure Settings** (left panel):
   - Max Concurrent Tools: Select **2** (recommended)
   - CPU Threshold: Keep at **70%**
   - RAM Threshold: Keep at **75%**

2. **Enter Target**:
   - Type target IP or domain (e.g., `192.168.1.1` or `example.com`)

3. **Select Tools** (optional):
   - Default selection is fine for first run
   - Or uncheck tools you don't want to run

4. **Start Scan**:
   - Click **"▶ INITIATE SCAN"**

## What You'll See

### Top Section
```
🚀 CYBERPUNK AI PENTEST AGENT 2077 🚀
SYSTEM READY • NEURAL NETWORK ONLINE • AWAITING TARGET
```

### Left Panel
- Target input field
- Control buttons (Start/Stop/Export)
- Settings sliders
- Tool selection checkboxes

### Right Panel - Top
```
🖥️ SYSTEM RESOURCES
CPU: 45.2% [▓▓▓▓▓░░░░░]
RAM: 62.8% [▓▓▓▓▓▓░░░░]
```

### Right Panel - Middle
```
📋 TOOL EXECUTION QUEUE
⚡ RUNNING:
  • nmap (45s)
  • nikto (23s)

📋 QUEUED:
  • sqlmap
  • wpscan
  ... and 3 more

✅ COMPLETED: 5
❌ FAILED: 0
```

### Right Panel - Bottom
```
📱 NEURAL CONSOLE OUTPUT
[14:23:45] 🚀 CYBERPUNK AI PENTEST AGENT INITIALIZED
[14:23:46] 🎯 TARGET ACQUIRED: example.com
[14:23:47] ⚡ LAUNCHING: nmap
[14:23:48] ⚡ LAUNCHING: nikto
[14:24:32] ✅ COMPLETED nmap
...
```

## Understanding the Interface

### Resource Meters
- **Green**: Healthy (< 80% of threshold)
- **Yellow**: Caution (80-100% of threshold)
- **Red**: At capacity (> threshold)

### Tool Status Icons
- ⏳ **PENDING**: Not yet queued
- 📋 **QUEUED**: Waiting for resources
- ⚡ **RUNNING**: Currently executing
- ✅ **COMPLETED**: Successfully finished
- ❌ **FAILED**: Execution failed

### Console Colors
- 🔵 **Cyan**: System information
- 💚 **Green**: Success messages
- 💛 **Yellow**: Running/warning
- 💗 **Pink**: Round/phase info
- ❤️ **Red**: Errors/critical findings

## Common Scenarios

### Scenario 1: Fast System, Many Tools
```
Settings:
✓ Max Concurrent: 3
✓ CPU Threshold: 80%
✓ RAM Threshold: 85%

Result: Faster scans, tools complete quickly
```

### Scenario 2: Slow System, Few Tools
```
Settings:
✓ Max Concurrent: 1
✓ CPU Threshold: 60%
✓ RAM Threshold: 65%

Result: Slower but stable, system remains responsive
```

### Scenario 3: Balanced (Recommended)
```
Settings:
✓ Max Concurrent: 2
✓ CPU Threshold: 70%
✓ RAM Threshold: 75%

Result: Good balance of speed and stability
```

## Tips for Best Results

### ✅ DO:
- Start with default settings
- Monitor resource meters
- Wait for each round to complete
- Review the console output
- Export logs when done

### ❌ DON'T:
- Set thresholds too high (>85%)
- Run 3+ tools on low-end systems
- Close terminal windows that open
- Interrupt scans unnecessarily

> **Personal note:** On my machine (8GB RAM, older i5) I found that setting
> Max Concurrent to **1** and RAM Threshold to **70%** gives the most stable
> results — the default 2 concurrent tools occasionally caused lag spikes.
