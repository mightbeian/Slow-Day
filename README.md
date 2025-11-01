# Slow Day - Network Traffic Analyzer

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

*A minimalistic network traffic analyzer for packet capture and real-time visualization*

</div>

## 🚀 Features

- **Real-time Packet Capture** - Capture network packets with customizable filters
- **Protocol Analysis** - Supports TCP, UDP, ICMP, and other protocols
- **IP & Port Filtering** - Filter traffic by specific IP addresses or ports
- **SQLite Database** - Store captured packets for later analysis
- **Web Interface** - Clean, minimalistic HTML dashboard
- **Statistics Dashboard** - Real-time statistics with protocol breakdown
- **Data Export** - Export captured data as JSON
- **Live Updates** - Auto-refreshing interface during capture

## 📋 Prerequisites

- Python 3.8 or higher
- Root/Administrator privileges (required for packet capture)
- Linux, macOS, or Windows

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mightbeian/Slow-Day.git
cd Slow-Day
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Platform-Specific Setup

**Linux:**
```bash
# Install libpcap
sudo apt-get install libpcap-dev  # Debian/Ubuntu
sudo yum install libpcap-devel     # RHEL/CentOS
```

**macOS:**
```bash
# libpcap is pre-installed on macOS
brew install libpcap  # Optional: get latest version
```

**Windows:**
- Download and install [Npcap](https://npcap.com/#download)
- Run installer with "WinPcap API-compatible Mode" enabled

## 🎮 Usage

### Command Line Interface

```bash
# Basic capture (requires sudo/admin privileges)
sudo python3 analyzer.py

# Capture on specific interface
sudo python3 analyzer.py -i eth0

# Filter by IP address
sudo python3 analyzer.py -ip 192.168.1.100

# Filter by port
sudo python3 analyzer.py -p 443

# Capture limited number of packets
sudo python3 analyzer.py -c 100

# Combine filters
sudo python3 analyzer.py -i wlan0 -ip 8.8.8.8 -p 53
```

### Web Interface

```bash
# Start the web server (requires sudo)
sudo python3 web_server.py
```

Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 🖥️ Web Interface Features

### Control Panel
- **Interface**: Specify network interface (e.g., eth0, wlan0)
- **Filter IP**: Capture packets from/to specific IP
- **Filter Port**: Capture packets on specific port
- **Packet Limit**: Set maximum packets to capture (0 = unlimited)

### Statistics Display
- Total packets captured
- Protocol breakdown (TCP, UDP, ICMP, Other)
- Total bytes transferred
- Real-time updates during capture

### Packet Table
- Live packet display with scrolling
- Color-coded protocols
- Source/Destination IPs and ports
- Timestamp and packet length
- TCP flags display

### Actions
- **START CAPTURE** - Begin packet capture
- **STOP CAPTURE** - End capture session
- **REFRESH** - Manually update display
- **CLEAR DATA** - Remove all captured packets
- **EXPORT JSON** - Download packets as JSON file

## 📊 Database Schema

### Packets Table
```sql
CREATE TABLE packets (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    src_ip TEXT,
    dst_ip TEXT,
    protocol TEXT,
    src_port INTEGER,
    dst_port INTEGER,
    length INTEGER,
    payload TEXT,
    flags TEXT
);
```

### Statistics Table
```sql
CREATE TABLE statistics (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    total_packets INTEGER,
    tcp_count INTEGER,
    udp_count INTEGER,
    icmp_count INTEGER,
    other_count INTEGER,
    total_bytes INTEGER
);
```

## 🔐 Security & Legal

### ⚠️ Important Warnings

- **Legal Use Only**: Only use this tool on networks you own or have explicit permission to monitor
- **Privacy**: Never capture traffic on public networks or without authorization
- **Root Access**: Tool requires elevated privileges for packet capture
- **Educational Purpose**: Designed for learning and authorized security research

### Best Practices

1. Always get written permission before monitoring any network
2. Follow your organization's security policies
3. Respect privacy laws and regulations (GDPR, HIPAA, etc.)
4. Secure the database file containing captured data
5. Clear sensitive data after analysis

## 🛠️ Troubleshooting

### Common Issues

**Permission Denied**
```bash
# Run with sudo/administrator privileges
sudo python3 analyzer.py
```

**No packets captured**
- Check interface name: `ip addr` (Linux) or `ifconfig` (macOS)
- Verify network activity on the interface
- Check firewall settings
- Ensure libpcap/Npcap is properly installed

**Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Web interface not loading**
- Verify Flask is running: `ps aux | grep python`
- Check port 5000 is not in use
- Try accessing via `http://localhost:5000`

## 📚 API Endpoints

### Start Capture
```http
POST /api/start
Content-Type: application/json

{
  "interface": "eth0",
  "filter_ip": "192.168.1.1",
  "filter_port": 80,
  "packet_count": 100
}
```

### Get Packets
```http
GET /api/packets?limit=100
```

### Get Statistics
```http
GET /api/statistics
```

### Export Data
```http
GET /api/export?limit=1000
```

## 🎯 Use Cases

- **Network Diagnostics** - Troubleshoot connectivity issues
- **Security Research** - Analyze traffic patterns
- **Protocol Learning** - Understand network protocols
- **Performance Analysis** - Monitor bandwidth usage
- **Education** - Learn packet analysis and network security

## 🔮 Future Enhancements

- [ ] Deep packet inspection
- [ ] Anomaly detection with ML
- [ ] Advanced filtering with regex
- [ ] Packet replay functionality
- [ ] Protocol-specific analysis
- [ ] Geolocation of IP addresses
- [ ] Integration with Wireshark
- [ ] Multi-interface capture
- [ ] Custom alert rules
- [ ] Chart visualizations

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Disclaimer

This tool is provided for educational and authorized security research purposes only. The developers assume no liability for misuse or damage caused by this program. Users are responsible for complying with all applicable laws and regulations.

## 👤 Author

**Christian Paul Cabrera**
- GitHub: [@mightbeian](https://github.com/mightbeian)
- LinkedIn: [mightbeian](https://www.linkedin.com/in/mightbeian/)

## 🙏 Acknowledgments

- Built with [Scapy](https://scapy.net/) - Powerful packet manipulation library
- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework
- Inspired by Wireshark and tcpdump

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ for the cybersecurity community

</div>