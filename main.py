#!/usr/bin/env python3
"""
LogMonitor - Real-time log monitoring and analysis tool
"""

import argparse
import sys
import os
import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from stats import LogStats


class LogFileHandler(FileSystemEventHandler):
    def __init__(self, logfile_path, verbose=False, filter_pattern=None, stats=None):
        self.logfile_path = logfile_path
        self.verbose = verbose
        self.filter_pattern = None
        self.file_position = 0
        self.stats = stats
        
        if filter_pattern:
            try:
                self.filter_pattern = re.compile(filter_pattern)
            except re.error as e:
                print(f"Error compiling regex pattern '{filter_pattern}': {e}", file=sys.stderr)
                sys.exit(1)
        
        with open(logfile_path, 'r') as f:
            f.seek(0, 2)
            self.file_position = f.tell()
    
    def on_modified(self, event):
        if event.src_path == self.logfile_path:
            self.read_new_lines()
    
    def read_new_lines(self):
        try:
            with open(self.logfile_path, 'r') as f:
                f.seek(self.file_position)
                new_lines = f.readlines()
                self.file_position = f.tell()
                
                for line in new_lines:
                    line = line.strip()
                    if line:
                        if self.filter_pattern:
                            if self.filter_pattern.search(line):
                                self.print_line(line)
                        else:
                            self.print_line(line)
        except Exception as e:
            if self.verbose:
                print(f"Error reading file: {e}", file=sys.stderr)
    
    def print_line(self, line):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        is_error = self.is_error_line(line)
        is_warning = self.is_warning_line(line)
        
        if self.stats:
            self.stats.update_line_count(is_error, is_warning)
        
        if is_error:
            print(f"\033[91m[{timestamp}] ERROR: {line}\033[0m")
        elif is_warning:
            print(f"\033[93m[{timestamp}] WARN: {line}\033[0m")
        else:
            print(f"[{timestamp}] {line}")
    
    def is_error_line(self, line):
        error_patterns = ['error', 'exception', 'failed', 'fatal', 'critical']
        return any(pattern in line.lower() for pattern in error_patterns)
    
    def is_warning_line(self, line):
        warning_patterns = ['warn', 'warning', 'deprecated']
        return any(pattern in line.lower() for pattern in warning_patterns)


def parse_args():
    parser = argparse.ArgumentParser(description='Monitor and analyze log files in real-time')
    parser.add_argument('logfile', help='Path to the log file to monitor')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-f', '--filter', help='Filter pattern (regex)')
    parser.add_argument('-s', '--stats', action='store_true', help='Enable statistics tracking')
    return parser.parse_args()


def main():
    args = parse_args()
    
    if not os.path.exists(args.logfile):
        print(f"Error: Log file '{args.logfile}' not found", file=sys.stderr)
        sys.exit(1)
    
    logfile_path = os.path.abspath(args.logfile)
    print(f"Starting LogMonitor for file: {logfile_path}")
    if args.filter:
        print(f"Filter pattern: {args.filter}")
    if args.stats:
        print("Statistics tracking enabled")
    
    stats = LogStats() if args.stats else None
    event_handler = LogFileHandler(logfile_path, args.verbose, args.filter, stats)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(logfile_path), recursive=False)
    
    observer.start()
    print("Monitoring started... (Press Ctrl+C to stop)")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")
        if stats:
            stats.print_summary()
    
    observer.join()


if __name__ == '__main__':
    main()