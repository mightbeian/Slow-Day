#!/usr/bin/env python3
"""
Configuration file for Slow Day Network Analyzer
Modify these settings to customize the behavior
"""

# Database Configuration
DATABASE_PATH = 'traffic.db'
DATABASE_TIMEOUT = 30  # seconds

# Web Server Configuration
WEB_HOST = '127.0.0.1'  # Change to '0.0.0.0' to allow external access
WEB_PORT = 5000
DEBUG_MODE = False  # Set to True for development

# Capture Settings
DEFAULT_PACKET_LIMIT = 0  # 0 = unlimited
DEFAULT_INTERFACE = None  # None = use default interface
MAX_PAYLOAD_SIZE = 200  # Maximum payload bytes to store

# API Settings
API_RATE_LIMIT = 100  # requests per minute
MAX_EXPORT_PACKETS = 10000  # Maximum packets to export at once

# Display Settings
DEFAULT_TABLE_LIMIT = 100  # Packets to display in web interface
REFRESH_INTERVAL = 2000  # milliseconds

# Security Settings
ALLOW_REMOTE_ACCESS = False  # Enable external connections
REQUIRE_AUTH = False  # Enable basic authentication (future feature)

# Logging Configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'logs/slow_day.log'
LOG_MAX_SIZE = 10485760  # 10 MB
LOG_BACKUP_COUNT = 5

# Filter Presets
FILTER_PRESETS = {
    'http': {'port': 80},
    'https': {'port': 443},
    'dns': {'port': 53},
    'ssh': {'port': 22},
    'ftp': {'port': 21},
}

# Protocol Colors (for CLI output)
PROTOCOL_COLORS = {
    'TCP': '\033[96m',   # Cyan
    'UDP': '\033[93m',   # Yellow
    'ICMP': '\033[95m',  # Magenta
    'OTHER': '\033[91m', # Red
    'RESET': '\033[0m',  # Reset
}

# Statistics Configuration
STATS_UPDATE_INTERVAL = 10  # seconds
KEEP_STATISTICS_DAYS = 30  # Days to keep historical statistics

# Advanced Capture Options
CAPTURE_BUFFER_SIZE = 65536  # bytes
CAPTURE_TIMEOUT = 1  # seconds
PROMISCUOUS_MODE = True  # Capture all packets on network segment

# Database Cleanup
AUTO_CLEANUP = False  # Automatically remove old packets
CLEANUP_DAYS = 7  # Delete packets older than X days

# Export Settings
EXPORT_FORMAT = 'json'  # json, csv, pcap (future)
EXPORT_INCLUDE_PAYLOAD = True

# UI Customization
THEME = 'matrix'  # matrix, dark, light (future themes)
SHOW_PAYLOAD = False  # Display packet payload in table

# Performance Settings
MAX_CONCURRENT_CAPTURES = 1  # Limit simultaneous captures
PACKET_QUEUE_SIZE = 1000  # Buffer for packet processing

# Alert Configuration (Future Feature)
ENABLE_ALERTS = False
ALERT_THRESHOLDS = {
    'packets_per_second': 1000,
    'suspicious_ports': [1337, 31337, 12345],
    'unusual_protocols': ['OTHER'],
}

print("[+] Configuration loaded successfully")
