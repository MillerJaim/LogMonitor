# LogMonitor

A real-time log file monitoring and analysis tool built in Python.

## Features

- Real-time log file monitoring using filesystem events
- Regex pattern filtering for targeted log analysis
- Color-coded output (red for errors, yellow for warnings)
- Statistics tracking with detailed reporting
- Cross-platform compatibility

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic monitoring:
```bash
python main.py /path/to/logfile.log
```

With regex filtering:
```bash
python main.py /path/to/logfile.log -f "error|warning"
```

Enable statistics tracking:
```bash
python main.py /path/to/logfile.log -s
```

Enable verbose output:
```bash
python main.py /path/to/logfile.log -v
```

## Command Line Options

- `logfile` - Path to the log file to monitor (required)
- `-f, --filter` - Regex pattern to filter log lines
- `-s, --stats` - Enable statistics tracking and summary report
- `-v, --verbose` - Enable verbose error reporting

## Output Features

### Color Coding
- **Red**: Error lines (containing: error, exception, failed, fatal, critical)
- **Yellow**: Warning lines (containing: warn, warning, deprecated)
- **White**: Normal log lines

### Statistics Report
When using `-s` flag, LogMonitor displays a summary on exit:
- Total runtime
- Lines processed
- Error and warning counts with percentages
- Average lines per minute

## Example

```bash
$ python main.py app.log -s -f "ERROR|WARN"
Starting LogMonitor for file: /home/user/app.log
Filter pattern: ERROR|WARN
Statistics tracking enabled
Monitoring started... (Press Ctrl+C to stop)
[2025-03-28 14:25:10] ERROR: Database connection failed
[2025-03-28 14:25:15] WARN: Cache miss for key user_123
^C
Monitoring stopped.

==================================================
LOG MONITORING SUMMARY
==================================================
Runtime: 0:02:30
Total lines processed: 25
Error lines: 3 (12.0%)
Warning lines: 8 (32.0%)
Average lines per minute: 10.0
==================================================
```