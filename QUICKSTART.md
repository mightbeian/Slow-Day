# Quick Start Guide - Slow Day Network Analyzer

## Installation (5 minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/mightbeian/Slow-Day.git
cd Slow-Day
```

### Step 2: Run Setup Script
```bash
chmod +x setup.sh
sudo ./setup.sh
```

The script will automatically:
- Check Python version
- Install dependencies
- Set up project structure
- Test database initialization

## Usage

### Option 1: Web Interface (Recommended)

1. **Start the web server:**
   ```bash
   sudo python3 web_server.py
   ```

2. **Open your browser:**
   ```
   http://127.0.0.1:5000
   ```

3. **Use the interface:**
   - Enter filter options (IP, port, interface)
   - Click "START CAPTURE"
   - Watch packets appear in real-time
   - Click "STOP CAPTURE" when done
   - Export data as JSON if needed

### Option 2: Command Line Interface

**Basic capture (all traffic):**
```bash
sudo python3 analyzer.py
```

**Capture HTTP traffic:**
```bash
sudo python3 analyzer.py -p 80
```

**Capture specific IP:**
```bash
sudo python3 analyzer.py -ip 192.168.1.1
```

**Capture on specific interface:**
```bash
sudo python3 analyzer.py -i eth0
```

**Capture limited packets:**
```bash
sudo python3 analyzer.py -c 100
```

**Combine filters:**
```bash
sudo python3 analyzer.py -ip 192.168.1.100 -p 443 -c 50
```

## Common Use Cases

### 1. Monitor Web Traffic
```bash
# HTTP
sudo python3 analyzer.py -p 80

# HTTPS
sudo python3 analyzer.py -p 443
```

### 2. Analyze Specific Host
```bash
sudo python3 analyzer.py -ip 8.8.8.8
```

### 3. Debug Network Issues
```bash
# Capture everything for 5 minutes, then analyze
sudo python3 analyzer.py -c 5000
```

### 4. Monitor DNS Queries
```bash
sudo python3 analyzer.py -p 53
```

## Database Management

### View Statistics
```bash
python3 database_manager.py --stats
```

### Clean Old Data
```bash
python3 database_manager.py --cleanup 7  # Remove packets older than 7 days
```

### Export to CSV
```bash
python3 database_manager.py --export-csv output.csv
```

### Backup Database
```bash
python3 database_manager.py --backup traffic_backup.db
```

### Search Packets
```bash
# By IP
python3 database_manager.py --search-ip 192.168.1.1

# By Port
python3 database_manager.py --search-port 443

# By Protocol
python3 database_manager.py --search-protocol TCP
```

## Troubleshooting

### "Permission denied" error
**Solution:** Run with sudo
```bash
sudo python3 analyzer.py
```

### "No module named 'scapy'" error
**Solution:** Install dependencies
```bash
pip3 install -r requirements.txt
```

### "Could not find interface" error
**Solution:** List available interfaces
```bash
# Linux
ip link show

# macOS
ifconfig

# Then specify the interface
sudo python3 analyzer.py -i eth0
```

### Web server not accessible
**Solution:** Check if running and firewall settings
```bash
# Make sure it's running
sudo python3 web_server.py

# Check if port 5000 is open
netstat -an | grep 5000
```

### Database locked error
**Solution:** Only one capture session at a time
```bash
# Stop any running captures first
pkill -f analyzer.py
```

## Tips & Tricks

### 1. Run in Background
```bash
# Start web server in background
nohup sudo python3 web_server.py > server.log 2>&1 &

# View the log
tail -f server.log
```

### 2. Auto-start on Boot (Linux)
```bash
# Create systemd service
sudo nano /etc/systemd/system/slowday.service

# Add:
[Unit]
Description=Slow Day Network Analyzer
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/Slow-Day
ExecStart=/usr/bin/python3 /path/to/Slow-Day/web_server.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable slowday
sudo systemctl start slowday
```

### 3. Filter Multiple IPs
```bash
# Capture traffic between two hosts
sudo python3 analyzer.py -ip "192.168.1.1 or 192.168.1.2"
```

### 4. Schedule Regular Captures
```bash
# Add to crontab
crontab -e

# Capture every hour for 10 minutes
0 * * * * sudo /usr/bin/python3 /path/to/Slow-Day/analyzer.py -c 1000
```

## Security Reminders

⚠️ **IMPORTANT:**
- Only use on networks you own or have permission to monitor
- Packet capture may be illegal on unauthorized networks
- Some data may contain sensitive information
- Always follow your organization's security policies
- Use responsibly for educational and authorized testing only

## Next Steps

1. **Explore the web interface** - Most user-friendly option
2. **Check database statistics** - See what you've captured
3. **Export data** - Analyze in other tools
4. **Read the full README** - Learn advanced features
5. **Customize config.py** - Adjust settings to your needs

## Need Help?

- **Documentation:** [README.md](README.md)
- **Issues:** [GitHub Issues](https://github.com/mightbeian/Slow-Day/issues)
- **License:** [MIT License](LICENSE)

---

Happy packet hunting! 🎯
