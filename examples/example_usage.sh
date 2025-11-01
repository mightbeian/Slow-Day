#!/bin/bash
# Example usage scenarios for Slow Day Network Analyzer

echo "Slow Day - Example Usage Scenarios"
echo "==================================\n"

# Example 1: Basic capture
echo "Example 1: Basic Packet Capture"
echo "Command: sudo python3 analyzer.py -c 10"
echo "Description: Capture 10 packets from default interface\n"

# Example 2: HTTP traffic monitoring
echo "Example 2: Monitor HTTP Traffic"
echo "Command: sudo python3 analyzer.py -p 80 -c 50"
echo "Description: Capture 50 HTTP packets (port 80)\n"

# Example 3: HTTPS traffic monitoring
echo "Example 3: Monitor HTTPS Traffic"
echo "Command: sudo python3 analyzer.py -p 443 -c 50"
echo "Description: Capture 50 HTTPS packets (port 443)\n"

# Example 4: Monitor specific host
echo "Example 4: Monitor Specific Host"
echo "Command: sudo python3 analyzer.py -ip 8.8.8.8"
echo "Description: Capture all traffic to/from Google DNS\n"

# Example 5: DNS monitoring
echo "Example 5: Monitor DNS Queries"
echo "Command: sudo python3 analyzer.py -p 53 -c 20"
echo "Description: Capture 20 DNS packets\n"

# Example 6: SSH monitoring
echo "Example 6: Monitor SSH Connections"
echo "Command: sudo python3 analyzer.py -p 22"
echo "Description: Monitor SSH traffic (port 22)\n"

# Example 7: Specific interface
echo "Example 7: Capture on Specific Interface"
echo "Command: sudo python3 analyzer.py -i wlan0 -c 30"
echo "Description: Capture 30 packets on wireless interface\n"

# Example 8: Web server mode
echo "Example 8: Start Web Interface"
echo "Command: sudo python3 web_server.py"
echo "Description: Start web-based interface on port 5000\n"

# Example 9: Database statistics
echo "Example 9: View Database Statistics"
echo "Command: python3 database_manager.py --stats"
echo "Description: Show captured packet statistics\n"

# Example 10: Export data
echo "Example 10: Export to CSV"
echo "Command: python3 database_manager.py --export-csv packets.csv"
echo "Description: Export all packets to CSV file\n"

echo "\nFor more examples, see the documentation!"
