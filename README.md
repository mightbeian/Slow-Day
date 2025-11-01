# Slow Day - Network Traffic Analyzer

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg)

A minimalistic network traffic analyzer built for cybersecurity enthusiasts and penetration testers. Slow Day captures and analyzes network packets in real-time with an intuitive web interface.

## ✨ Features

- **Real-time Packet Capture** - Live monitoring of network traffic
- **Protocol Analysis** - Supports TCP, UDP, ICMP, and more
- **IP & Port Filtering** - Target specific hosts and services
- **Web Interface** - Clean, minimalistic HTML dashboard
- **SQLite Database** - Persistent storage of captured packets
- **Statistics Dashboard** - Visual breakdown of traffic patterns
- **Data Export** - Export captured data as JSON
- **Educational Tool** - Perfect for learning network security

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Root/Administrator privileges (required for packet capture)
- Linux or macOS (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mightbeian/Slow-Day.git
cd Slow-Day
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Command Line Interface

Basic packet capture:
```bash
sudo python3 analyzer.py
```

Capture with filters:
```bash
# Filter by IP address
sudo python3 analyzer.py -ip 192.168.1.1

# Filter by port
sudo python3 analyzer.py -p 80

# Specify interface
sudo python3 analyzer.py -i eth0

# Capture specific number of packets
sudo python3 analyzer.py -c 100
```

#### Web Interface

1. Start the web server:
```bash
sudo python3 web_server.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

3. Use the control panel to:
   - Configure capture settings (interface, IP filter, port filter)
   - Start/stop packet capture
   - View real-time statistics
   - Browse captured packets
   - Export data as JSON

## 📊 Features Overview

### Control Panel
- **Interface Selection** - Choose network interface (eth0, wlan0, etc.)
- **IP Filtering** - Monitor specific IP addresses
- **Port Filtering** - Focus on particular services
- **Packet Limit** - Set maximum packets to capture

### Statistics Dashboard
- Total packets captured
- Protocol breakdown (TCP, UDP, ICMP, Other)
- Total bytes transferred
- Real-time counters

### Packet Table
- Packet ID and timestamp
- Source/destination IP and ports
- Protocol identification
- Packet length
- TCP flags (when applicable)

### Database System

Slow Day uses SQLite for data persistence with three main tables:

1. **packets** - Stores captured packet details
2. **statistics** - Aggregated traffic statistics
3. **filters** - User-defined capture filters

## 🛡️ Security & Legal Notice

**⚠️ IMPORTANT**: This tool is designed for:
- Educational purposes
- Security research
- Network administration
- Authorized penetration testing

**Use this tool ONLY on:**
- Networks you own
- Networks you have explicit permission to monitor
- Lab/test environments

**Unauthorized network monitoring may be illegal in your jurisdiction.**

## 🔧 Technical Details

### Architecture

```
Slow Day/
│
├── analyzer.py          # Core packet capture engine
├── web_server.py        # Flask web server & REST API
├── templates/
│   └── index.html       # Web interface
├── traffic.db           # SQLite database (created on first run)
└── requirements.txt     # Python dependencies
```

### API Endpoints

- `POST /api/start` - Start packet capture
- `POST /api/stop` - Stop packet capture
- `GET /api/packets` - Retrieve captured packets
- `GET /api/statistics` - Get traffic statistics
- `GET /api/status` - Check capture status
- `POST /api/clear` - Clear database
- `GET /api/export` - Export data as JSON

## 🎨 Interface Preview

The web interface features:
- **Matrix-inspired theme** - Green on black terminal aesthetic
- **Minimalistic design** - Focus on functionality
- **Real-time updates** - Live packet counter and statistics
- **Responsive layout** - Works on desktop and tablet

## 📝 Example Use Cases

1. **Network Troubleshooting**
   ```bash
   sudo python3 analyzer.py -ip 192.168.1.100 -p 443
   ```
   Monitor SSL/TLS traffic to specific host

2. **Protocol Analysis**
   ```bash
   sudo python3 analyzer.py -i wlan0 -c 1000
   ```
   Capture 1000 packets on wireless interface

3. **Service Monitoring**
   ```bash
   sudo python3 analyzer.py -p 80
   ```
   Monitor HTTP traffic across all interfaces

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional protocol support
- Enhanced filtering options
- Visualization features
- Performance optimizations
- Cross-platform compatibility

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Christian Paul Cabrera**
- GitHub: [@mightbeian](https://github.com/mightbeian)
- LinkedIn: [mightbeian](https://www.linkedin.com/in/mightbeian/)

## 🙏 Acknowledgments

- Built with [Scapy](https://scapy.net/) - Powerful packet manipulation library
- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework
- Inspired by classic network analysis tools like tcpdump and Wireshark

## 📚 Learning Resources

If you're new to network analysis:
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [TCP/IP Protocol Suite](https://www.ietf.org/)
- [Wireshark User Guide](https://www.wireshark.org/docs/)

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.

⭐ If you find this project useful, please consider giving it a star!