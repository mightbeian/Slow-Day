# Slow Day - Usage Guide

Comprehensive guide for using the Slow Day Network Traffic Analyzer.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Command Line Usage](#command-line-usage)
3. [Web Interface](#web-interface)
4. [Database Management](#database-management)
5. [Advanced Filtering](#advanced-filtering)
6. [Examples](#examples)

## Quick Start

### 1. Basic Capture

```bash
# Start capturing on default interface
sudo python3 analyzer.py
```

### 2. Web Interface

```bash
# Launch web dashboard
sudo python3 web_server.py

# Open browser to http://127.0.0.1:5000
```

## Command Line Usage

### Basic Options

```bash
# Show help
python3 analyzer.py --help

# Capture on specific interface
sudo python3 analyzer.py -i eth0

# Use custom database file
sudo python3 analyzer.py -d custom.db
```

### Filtering Options

#### By IP Address

```bash
# Capture traffic from/to specific IP
sudo python3 analyzer.py -ip 192.168.1.100

# Monitor traffic to Google DNS
sudo python3 analyzer.py -ip 8.8.8.8
```

#### By Port

```bash
# Capture HTTP traffic
sudo python3 analyzer.py -p 80

# Capture HTTPS traffic
sudo python3 analyzer.py -p 443

# Monitor SSH connections
sudo python3 analyzer.py -p 22
```

#### Packet Count Limit

```bash
# Capture exactly 100 packets
sudo python3 analyzer.py -c 100

# Capture 1000 packets from specific IP
sudo python3 analyzer.py -ip 10.0.0.1 -c 1000
```

### Combined Filters

```bash
# Monitor HTTPS traffic to specific IP
sudo python3 analyzer.py -ip 1.1.1.1 -p 443

# Capture DNS traffic on WiFi interface
sudo python3 analyzer.py -i wlan0 -p 53 -c 500

# Monitor specific server's traffic
sudo python3 analyzer.py -i eth0 -ip 192.168.1.50 -p 8080
```

## Web Interface

### Starting the Server

```bash
sudo python3 web_server.py
```

The server will start on `http://127.0.0.1:5000`

### Interface Features

#### Control Panel

1. **Interface Field**
   - Leave blank for default interface
   - Specify interface name (e.g., `eth0`, `wlan0`)
   - Find interface name: `ip addr` (Linux) or `ifconfig` (macOS)

2. **Filter IP**
   - Filter traffic by specific IP address
   - Captures both source and destination traffic
   - Example: `192.168.1.1` or `8.8.8.8`

3. **Filter Port**
   - Filter by port number
   - Common ports:
     - `80` - HTTP
     - `443` - HTTPS
     - `22` - SSH
     - `3389` - RDP
     - `3306` - MySQL

4. **Packet Limit**
   - `0` = Unlimited capture
   - Set specific number to stop automatically

#### Actions

- **START CAPTURE**: Begin packet capture with current settings
- **STOP CAPTURE**: End capture session (saves statistics)
- **REFRESH**: Manually update packet display
- **CLEAR DATA**: Remove all packets from database
- **EXPORT JSON**: Download captured data as JSON file

#### Statistics Display

- **Total Packets**: Overall count of captured packets
- **TCP**: TCP protocol packets (cyan color)
- **UDP**: UDP protocol packets (yellow color)
- **ICMP**: ICMP protocol packets (magenta color)
- **Other**: All other protocols (orange color)
- **Total Bytes**: Cumulative size of all packets

### Live Monitoring

- Status indicator shows capture state (green = active)
- Packet table auto-refreshes every 2 seconds during capture
- Latest packets appear at the top
- Color-coded protocols for easy identification

## Database Management

### Using db_manager.py

#### View Statistics

```bash
# Show database overview
python3 db_manager.py stats
```

Output:
```
============================================================
               DATABASE STATISTICS
============================================================

Total Packets:        1,234
Total Bytes:          567,890
Unique Source IPs:    45
Unique Dest IPs:      67

Time Range:
  Start: 2025-01-15 10:30:00.123456
  End:   2025-01-15 11:45:30.654321

Protocol Distribution:
  TCP     :  1,000 (81.04%)
  UDP     :    200 (16.21%)
  ICMP    :     30 ( 2.43%)
  OTHER   :      4 ( 0.32%)
```

#### Query by IP

```bash
# Find all packets from/to specific IP
python3 db_manager.py ip 192.168.1.100
```

#### Query by Port

```bash
# Find all packets on port 443
python3 db_manager.py port 443
```

#### Query by Protocol

```bash
# Find all TCP packets
python3 db_manager.py protocol TCP

# Find all ICMP packets
python3 db_manager.py protocol ICMP
```

#### Top Talkers

```bash
# Show top 10 most active IPs
python3 db_manager.py talkers

# Show top 20
python3 db_manager.py talkers -l 20
```

#### Top Ports

```bash
# Show most active ports
python3 db_manager.py ports

# Show top 15 ports
python3 db_manager.py ports -l 15
```

#### Conversations

```bash
# Show top IP-to-IP conversations
python3 db_manager.py conversations

# Show top 25 conversations
python3 db_manager.py conversations -l 25
```

#### Search Payload

```bash
# Search for specific text in packet payloads
python3 db_manager.py search "password"

# Search for HTTP methods
python3 db_manager.py search "GET"
```

#### Export Data

```bash
# Export all packets
python3 db_manager.py export output.json

# Export limited number
python3 db_manager.py export output.json -l 500
```

## Advanced Filtering

### Multiple Criteria

Combine multiple filters for precise capture:

```bash
# Web traffic from specific IP on WiFi
sudo python3 analyzer.py -i wlan0 -ip 192.168.1.50 -p 80

# Limited HTTPS capture
sudo python3 analyzer.py -p 443 -c 200

# DNS monitoring on specific interface
sudo python3 analyzer.py -i eth0 -p 53
```

### BPF Filters

The tool uses Berkeley Packet Filter (BPF) syntax internally. Filters are automatically combined:

- IP filter: `host 192.168.1.1`
- Port filter: `port 80`
- Combined: `host 192.168.1.1 and port 80`

## Examples

### Example 1: Monitor Web Server

```bash
# Capture HTTP and HTTPS traffic to web server
sudo python3 analyzer.py -ip 203.0.113.50

# Then query the results
python3 db_manager.py ip 203.0.113.50
```

### Example 2: Analyze DNS Queries

```bash
# Capture 1000 DNS packets
sudo python3 analyzer.py -p 53 -c 1000

# View statistics
python3 db_manager.py stats

# Export for analysis
python3 db_manager.py export dns_traffic.json
```

### Example 3: Security Monitoring

```bash
# Monitor SSH attempts
sudo python3 analyzer.py -p 22

# Check top talkers (potential brute force)
python3 db_manager.py talkers -l 20
```

### Example 4: Network Diagnostics

```bash
# Capture all traffic on interface
sudo python3 analyzer.py -i eth0 -c 500

# View protocol distribution
python3 db_manager.py stats

# Check top conversations
python3 db_manager.py conversations
```

### Example 5: Bandwidth Analysis

```bash
# Capture traffic for analysis
sudo python3 analyzer.py -i wlan0 -c 5000

# View top bandwidth consumers
python3 db_manager.py talkers -l 10

# Check most used ports
python3 db_manager.py ports -l 10
```

## Best Practices

### 1. Always Use Proper Privileges

```bash
# Use sudo for packet capture
sudo python3 analyzer.py

# Database management doesn't need sudo
python3 db_manager.py stats
```

### 2. Start with Limited Captures

```bash
# Test with small packet count first
sudo python3 analyzer.py -c 100
```

### 3. Regular Database Maintenance

```bash
# Export important data before clearing
python3 db_manager.py export backup.json

# Clear database via web interface or manually
rm traffic.db
```

### 4. Monitor Resource Usage

- Large captures can fill disk space
- Database grows with each packet
- Use packet limits for long-term captures

### 5. Security Considerations

- Only capture on authorized networks
- Protect database files (contain sensitive data)
- Clear captures after analysis
- Never share packet captures without sanitizing

## Troubleshooting

### No Packets Captured

```bash
# Check interface name
ip addr  # Linux
ifconfig  # macOS

# Verify interface is correct
sudo python3 analyzer.py -i <correct_interface>
```

### Permission Errors

```bash
# Always use sudo for capture
sudo python3 analyzer.py

# Check user groups (Linux)
sudo usermod -aG wireshark $USER
```

### Database Locked

```bash
# Stop all running instances
pkill -f analyzer.py
pkill -f web_server.py

# Then restart
```

### Web Interface Not Loading

```bash
# Check if server is running
ps aux | grep web_server.py

# Check port availability
sudo lsof -i :5000

# Try different port (modify web_server.py)
# Change: app.run(host='127.0.0.1', port=5000)
# To: app.run(host='127.0.0.1', port=8080)
```

## Tips & Tricks

### 1. Quick Statistics

```bash
# One-liner for quick stats
python3 db_manager.py stats | grep -A 5 "Protocol Distribution"
```

### 2. Find Your Interface

```bash
# Linux
ip link show

# macOS
networksetup -listallhardwareports
```

### 3. Background Capture

```bash
# Run capture in background
sudo python3 analyzer.py -c 10000 &

# Check progress
python3 db_manager.py stats
```

### 4. Automated Analysis

```bash
#!/bin/bash
# Capture and analyze script
sudo python3 analyzer.py -c 1000
python3 db_manager.py stats > report.txt
python3 db_manager.py export capture_$(date +%Y%m%d).json
```

---

For more information, visit the [GitHub repository](https://github.com/mightbeian/Slow-Day) or open an issue.