#!/usr/bin/env python3
"""
Slow Day - Network Traffic Analyzer
Captures and analyzes network packets with real-time visualization
"""

import socket
import struct
import sqlite3
import json
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
import threading
import time

class NetworkAnalyzer:
    def __init__(self, db_path='traffic.db'):
        self.db_path = db_path
        self.is_capturing = False
        self.packet_count = 0
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create packets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                src_ip TEXT,
                dst_ip TEXT,
                protocol TEXT,
                src_port INTEGER,
                dst_port INTEGER,
                length INTEGER,
                payload TEXT,
                flags TEXT
            )
        ''')
        
        # Create statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                total_packets INTEGER,
                tcp_count INTEGER,
                udp_count INTEGER,
                icmp_count INTEGER,
                other_count INTEGER,
                total_bytes INTEGER
            )
        ''')
        
        # Create filters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                filter_type TEXT,
                value TEXT,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"[+] Database initialized at {self.db_path}")
    
    def packet_callback(self, packet):
        """Process captured packets"""
        try:
            if IP in packet:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                length = len(packet)
                protocol = ""
                src_port = None
                dst_port = None
                flags = ""
                payload = ""
                
                # Determine protocol
                if TCP in packet:
                    protocol = "TCP"
                    src_port = packet[TCP].sport
                    dst_port = packet[TCP].dport
                    flags = str(packet[TCP].flags)
                elif UDP in packet:
                    protocol = "UDP"
                    src_port = packet[UDP].sport
                    dst_port = packet[UDP].dport
                elif ICMP in packet:
                    protocol = "ICMP"
                else:
                    protocol = "OTHER"
                
                # Extract payload
                if Raw in packet:
                    payload = str(packet[Raw].load)[:200]  # Limit payload size
                
                # Save to database
                self.save_packet(timestamp, src_ip, dst_ip, protocol, 
                               src_port, dst_port, length, payload, flags)
                
                self.packet_count += 1
                
                # Print summary
                print(f"[{self.packet_count}] {timestamp} | {src_ip}:{src_port} -> {dst_ip}:{dst_port} | {protocol} | {length} bytes")
                
        except Exception as e:
            print(f"[!] Error processing packet: {e}")
    
    def save_packet(self, timestamp, src_ip, dst_ip, protocol, src_port, dst_port, length, payload, flags):
        """Save packet to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO packets (timestamp, src_ip, dst_ip, protocol, src_port, dst_port, length, payload, flags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, src_ip, dst_ip, protocol, src_port, dst_port, length, payload, flags))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[!] Error saving packet to database: {e}")
    
    def start_capture(self, interface=None, filter_ip=None, filter_port=None, packet_count=0):
        """Start packet capture"""
        self.is_capturing = True
        print(f"[+] Starting capture on interface: {interface or 'default'}")
        
        # Build BPF filter
        bpf_filter = ""
        if filter_ip:
            bpf_filter += f"host {filter_ip}"
        if filter_port:
            if bpf_filter:
                bpf_filter += f" and port {filter_port}"
            else:
                bpf_filter += f"port {filter_port}"
        
        try:
            sniff(iface=interface, 
                  prn=self.packet_callback, 
                  filter=bpf_filter if bpf_filter else None,
                  count=packet_count if packet_count > 0 else 0,
                  store=False)
        except KeyboardInterrupt:
            print("\n[+] Capture stopped by user")
        except Exception as e:
            print(f"[!] Error during capture: {e}")
        finally:
            self.is_capturing = False
            self.save_statistics()
    
    def save_statistics(self):
        """Save capture statistics to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get protocol counts
            cursor.execute("SELECT protocol, COUNT(*) FROM packets GROUP BY protocol")
            protocol_counts = dict(cursor.fetchall())
            
            cursor.execute("SELECT SUM(length) FROM packets")
            total_bytes = cursor.fetchone()[0] or 0
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO statistics (timestamp, total_packets, tcp_count, udp_count, icmp_count, other_count, total_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, 
                  self.packet_count,
                  protocol_counts.get('TCP', 0),
                  protocol_counts.get('UDP', 0),
                  protocol_counts.get('ICMP', 0),
                  protocol_counts.get('OTHER', 0),
                  total_bytes))
            
            conn.commit()
            conn.close()
            print(f"[+] Statistics saved: {self.packet_count} packets captured")
        except Exception as e:
            print(f"[!] Error saving statistics: {e}")
    
    def get_recent_packets(self, limit=100):
        """Retrieve recent packets from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, src_ip, dst_ip, protocol, src_port, dst_port, length, flags
            FROM packets
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        packets = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return packets
    
    def get_statistics(self):
        """Get capture statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM statistics
            ORDER BY id DESC
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'timestamp': result[1],
                'total_packets': result[2],
                'tcp_count': result[3],
                'udp_count': result[4],
                'icmp_count': result[5],
                'other_count': result[6],
                'total_bytes': result[7]
            }
        return None
    
    def clear_database(self):
        """Clear all packets from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM packets')
        cursor.execute('DELETE FROM statistics')
        
        conn.commit()
        conn.close()
        print("[+] Database cleared")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Slow Day - Network Traffic Analyzer')
    parser.add_argument('-i', '--interface', help='Network interface to capture on')
    parser.add_argument('-ip', '--filter-ip', help='Filter by IP address')
    parser.add_argument('-p', '--filter-port', type=int, help='Filter by port number')
    parser.add_argument('-c', '--count', type=int, default=0, help='Number of packets to capture (0 = unlimited)')
    parser.add_argument('-d', '--database', default='traffic.db', help='Database file path')
    
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════╗
    ║      Slow Day - Traffic Analyzer     ║
    ║        Network Packet Capture        ║
    ╚═══════════════════════════════════════╝
    """)
    
    analyzer = NetworkAnalyzer(db_path=args.database)
    
    try:
        analyzer.start_capture(
            interface=args.interface,
            filter_ip=args.filter_ip,
            filter_port=args.filter_port,
            packet_count=args.count
        )
    except KeyboardInterrupt:
        print("\n[+] Shutting down...")
    except Exception as e:
        print(f"[!] Error: {e}")