#!/usr/bin/env python3
"""
API Usage Examples for Slow Day Network Analyzer
Demonstrates how to interact with the REST API programmatically
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = 'http://127.0.0.1:5000/api'

def example_1_start_capture():
    """Example 1: Start a packet capture with filters"""
    print("\n=== Example 1: Start Capture ===")
    
    data = {
        'interface': None,
        'filter_ip': '192.168.1.1',
        'filter_port': 443,
        'packet_count': 50
    }
    
    response = requests.post(f'{BASE_URL}/start', json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def example_2_check_status():
    """Example 2: Check capture status"""
    print("\n=== Example 2: Check Status ===")
    
    response = requests.get(f'{BASE_URL}/status')
    status = response.json()
    
    print(f"Capturing: {status['is_capturing']}")
    print(f"Packets captured: {status['packet_count']}")

def example_3_get_packets():
    """Example 3: Retrieve captured packets"""
    print("\n=== Example 3: Get Packets ===")
    
    response = requests.get(f'{BASE_URL}/packets?limit=10')
    data = response.json()
    
    print(f"Total packets returned: {data['count']}")
    
    if data['packets']:
        print("\nFirst packet:")
        packet = data['packets'][0]
        print(f"  ID: {packet['id']}")
        print(f"  Time: {packet['timestamp']}")
        print(f"  {packet['src_ip']}:{packet['src_port']} -> {packet['dst_ip']}:{packet['dst_port']}")
        print(f"  Protocol: {packet['protocol']}")
        print(f"  Length: {packet['length']} bytes")

def example_4_get_statistics():
    """Example 4: Get traffic statistics"""
    print("\n=== Example 4: Get Statistics ===")
    
    response = requests.get(f'{BASE_URL}/statistics')
    stats = response.json()
    
    print(f"Total Packets: {stats['total_packets']}")
    print(f"TCP: {stats['tcp_count']}")
    print(f"UDP: {stats['udp_count']}")
    print(f"ICMP: {stats['icmp_count']}")
    print(f"Other: {stats['other_count']}")
    print(f"Total Bytes: {stats['total_bytes']}")

def example_5_stop_capture():
    """Example 5: Stop the capture"""
    print("\n=== Example 5: Stop Capture ===")
    
    response = requests.post(f'{BASE_URL}/stop')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def example_6_export_data():
    """Example 6: Export captured data"""
    print("\n=== Example 6: Export Data ===")
    
    response = requests.get(f'{BASE_URL}/export?limit=100')
    data = response.json()
    
    # Save to file
    filename = f"export_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Exported {data['packet_count']} packets to {filename}")

def example_7_clear_database():
    """Example 7: Clear all packets"""
    print("\n=== Example 7: Clear Database ===")
    
    response = requests.post(f'{BASE_URL}/clear')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def example_8_automated_capture():
    """Example 8: Automated capture workflow"""
    print("\n=== Example 8: Automated Workflow ===")
    
    # Start capture
    print("Starting capture...")
    requests.post(f'{BASE_URL}/start', json={
        'filter_port': 80,
        'packet_count': 20
    })
    
    # Monitor progress
    print("Monitoring progress...")
    for i in range(10):
        time.sleep(1)
        status = requests.get(f'{BASE_URL}/status').json()
        print(f"  Packets: {status['packet_count']}", end='\r')
        
        if not status['is_capturing']:
            break
    
    print("\n\nCapture complete!")
    
    # Get statistics
    stats = requests.get(f'{BASE_URL}/statistics').json()
    print(f"Total captured: {stats['total_packets']} packets")

def example_9_filter_analysis():
    """Example 9: Analyze specific traffic patterns"""
    print("\n=== Example 9: Traffic Analysis ===")
    
    # Get all packets
    response = requests.get(f'{BASE_URL}/packets?limit=1000')
    packets = response.json()['packets']
    
    # Analyze by protocol
    protocol_count = {}
    for packet in packets:
        proto = packet['protocol']
        protocol_count[proto] = protocol_count.get(proto, 0) + 1
    
    print("\nProtocol Distribution:")
    for proto, count in sorted(protocol_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {proto}: {count} packets")
    
    # Find most active IPs
    ip_count = {}
    for packet in packets:
        src_ip = packet['src_ip']
        ip_count[src_ip] = ip_count.get(src_ip, 0) + 1
    
    print("\nTop 5 Source IPs:")
    for ip, count in sorted(ip_count.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {ip}: {count} packets")

def main():
    """Run all examples"""
    print("Slow Day API Examples")
    print("=" * 50)
    print("\nMake sure the web server is running:")
    print("  sudo python3 web_server.py\n")
    
    try:
        # Check if server is running
        requests.get(f'{BASE_URL}/status', timeout=2)
    except requests.exceptions.RequestException:
        print("❌ Error: Web server is not running!")
        print("   Start it with: sudo python3 web_server.py")
        return
    
    print("✓ Server is running\n")
    
    # Run examples
    # Uncomment the ones you want to try
    
    # example_1_start_capture()
    # time.sleep(5)  # Wait for some packets
    # example_2_check_status()
    # example_3_get_packets()
    # example_4_get_statistics()
    # example_5_stop_capture()
    # example_6_export_data()
    # example_7_clear_database()  # Be careful with this!
    example_8_automated_capture()
    # example_9_filter_analysis()
    
    print("\n" + "=" * 50)
    print("Examples complete!")

if __name__ == '__main__':
    main()
