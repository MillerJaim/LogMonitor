"""
Statistics tracking module for LogMonitor
"""

import time
from collections import defaultdict
from datetime import datetime, timedelta


class LogStats:
    def __init__(self):
        self.start_time = time.time()
        self.total_lines = 0
        self.error_count = 0
        self.warning_count = 0
        self.lines_per_minute = []
        self.minute_counter = 0
        self.last_minute_check = time.time()
    
    def update_line_count(self, is_error=False, is_warning=False):
        self.total_lines += 1
        
        if is_error:
            self.error_count += 1
        elif is_warning:
            self.warning_count += 1
        
        current_time = time.time()
        if current_time - self.last_minute_check >= 60:
            self.lines_per_minute.append(self.minute_counter)
            self.minute_counter = 0
            self.last_minute_check = current_time
        else:
            self.minute_counter += 1
    
    def get_stats(self):
        current_time = time.time()
        runtime = current_time - self.start_time
        
        avg_lines_per_minute = 0
        if self.lines_per_minute:
            avg_lines_per_minute = sum(self.lines_per_minute) / len(self.lines_per_minute)
        
        return {
            'runtime_seconds': runtime,
            'total_lines': self.total_lines,
            'error_count': self.error_count,
            'warning_count': self.warning_count,
            'avg_lines_per_minute': avg_lines_per_minute,
            'error_rate': (self.error_count / self.total_lines * 100) if self.total_lines > 0 else 0,
            'warning_rate': (self.warning_count / self.total_lines * 100) if self.total_lines > 0 else 0
        }
    
    def print_summary(self):
        stats = self.get_stats()
        runtime_str = str(timedelta(seconds=int(stats['runtime_seconds'])))
        
        print("\n" + "="*50)
        print("LOG MONITORING SUMMARY")
        print("="*50)
        print(f"Runtime: {runtime_str}")
        print(f"Total lines processed: {stats['total_lines']}")
        print(f"Error lines: {stats['error_count']} ({stats['error_rate']:.1f}%)")
        print(f"Warning lines: {stats['warning_count']} ({stats['warning_rate']:.1f}%)")
        if stats['avg_lines_per_minute'] > 0:
            print(f"Average lines per minute: {stats['avg_lines_per_minute']:.1f}")
        print("="*50)