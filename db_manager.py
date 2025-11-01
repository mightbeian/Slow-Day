#!/usr/bin/env python3
"""
Database Manager for Slow Day Network Analyzer
Utility for querying and managing captured packet data
"""

import sqlite3
import json
from datetime import datetime
import argparse

class DatabaseManager:
    def __init__(self, db_path='traffic.db'):
        self.db_path = db_path
        
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def query_by_ip(self, ip_address):
        """Query packets by IP address (source or destination)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM packets
            WHERE src_ip = ? OR dst_ip = ?
            ORDER BY id DESC
        ''', (ip_address, ip_address))
        
        packets = cursor.fetchall()
        conn.close()
        
        return packets
    
    def query_by_port(self, port):
        """Query packets by port number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM packets
            WHERE src_port = ? OR dst_port = ?
            ORDER BY id DESC
        ''', (port, port))
        
        packets = cursor.fetchall()
        conn.close()
        
        return packets
    
    def query_by_protocol(self, protocol):
        """Query packets by protocol"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM packets
            WHERE protocol = ?
            ORDER BY id DESC
        ''', (protocol.upper(),))
        
        packets = cursor.fetchall()
        conn.close()
        
        return packets
    
    def query_by_timerange(self, start_time, end_time):
        """Query packets by time range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM packets
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY id DESC
        ''', (start_time, end_time))
        
        packets = cursor.fetchall()
        conn.close()
        
        return packets
    
    def get_top_talkers(self, limit=10):
        """Get most active IP addresses"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT src_ip, COUNT(*) as packet_count, SUM(length) as total_bytes
            FROM packets
            GROUP BY src_ip
            ORDER BY packet_count DESC
            LIMIT ?
        ''', (limit,))
        
        talkers = cursor.fetchall()
        conn.close()
        
        return talkers
    
    def get_top_ports(self, limit=10):
        """Get most active ports"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dst_port, COUNT(*) as packet_count
            FROM packets
            WHERE dst_port IS NOT NULL
            GROUP BY dst_port
            ORDER BY packet_count DESC
            LIMIT ?
        ''', (limit,))
        
        ports = cursor.fetchall()
        conn.close()
        
        return ports
    
    def get_protocol_distribution(self):
        """Get protocol distribution statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT protocol, COUNT(*) as count, SUM(length) as total_bytes
            FROM packets
            GROUP BY protocol
            ORDER BY count DESC
        ''')
        
        distribution = cursor.fetchall()
        conn.close()
        
        return distribution
    
    def get_conversation_pairs(self, limit=10):
        """Get most active source-destination pairs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT src_ip, dst_ip, COUNT(*) as packet_count, SUM(length) as total_bytes
            FROM packets
            GROUP BY src_ip, dst_ip
            ORDER BY packet_count DESC
            LIMIT ?
        ''', (limit,))
        
        pairs = cursor.fetchall()
        conn.close()
        
        return pairs
    
    def search_payload(self, search_term):
        """Search for packets containing specific payload data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM packets
            WHERE payload LIKE ?
            ORDER BY id DESC
        ''', (f'%{search_term}%',))
        
        packets = cursor.fetchall()
        conn.close()
        
        return packets
    
    def export_to_json(self, output_file, limit=None):
        """Export packets to JSON file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if limit:
            cursor.execute('SELECT * FROM packets ORDER BY id DESC LIMIT ?', (limit,))
        else:
            cursor.execute('SELECT * FROM packets ORDER BY id DESC')
        
        columns = [description[0] for description in cursor.description]
        packets = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        export_data = {
            'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'packet_count': len(packets),
            'packets': packets
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        conn.close()
        print(f"[+] Exported {len(packets)} packets to {output_file}")
    
    def get_database_stats(self):
        """Get overall database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total packets
        cursor.execute('SELECT COUNT(*) FROM packets')
        stats['total_packets'] = cursor.fetchone()[0]
        
        # Total bytes
        cursor.execute('SELECT SUM(length) FROM packets')
        stats['total_bytes'] = cursor.fetchone()[0] or 0
        
        # Protocol breakdown
        cursor.execute('SELECT protocol, COUNT(*) FROM packets GROUP BY protocol')
        stats['protocols'] = dict(cursor.fetchall())
        
        # Date range
        cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM packets')
        min_time, max_time = cursor.fetchone()
        stats['time_range'] = {'start': min_time, 'end': max_time}
        
        # Unique IPs
        cursor.execute('SELECT COUNT(DISTINCT src_ip) FROM packets')
        stats['unique_source_ips'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT dst_ip) FROM packets')
        stats['unique_dest_ips'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def print_stats(self):
        """Print formatted database statistics"""
        stats = self.get_database_stats()
        
        print("\n" + "="*60)
        print(" " * 15 + "DATABASE STATISTICS")
        print("="*60)
        print(f"\nTotal Packets:        {stats['total_packets']:,}")
        print(f"Total Bytes:          {stats['total_bytes']:,}")
        print(f"Unique Source IPs:    {stats['unique_source_ips']:,}")
        print(f"Unique Dest IPs:      {stats['unique_dest_ips']:,}")
        
        if stats['time_range']['start']:
            print(f"\nTime Range:")
            print(f"  Start: {stats['time_range']['start']}")
            print(f"  End:   {stats['time_range']['end']}")
        
        print(f"\nProtocol Distribution:")
        for protocol, count in stats['protocols'].items():
            percentage = (count / stats['total_packets']) * 100 if stats['total_packets'] > 0 else 0
            print(f"  {protocol:8s}: {count:6,} ({percentage:5.2f}%)")
        
        print("\n" + "="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description='Slow Day Database Manager')
    parser.add_argument('-d', '--database', default='traffic.db', help='Database file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Query by IP
    ip_parser = subparsers.add_parser('ip', help='Query packets by IP address')
    ip_parser.add_argument('address', help='IP address to search')
    
    # Query by port
    port_parser = subparsers.add_parser('port', help='Query packets by port')
    port_parser.add_argument('number', type=int, help='Port number to search')
    
    # Query by protocol
    proto_parser = subparsers.add_parser('protocol', help='Query packets by protocol')
    proto_parser.add_argument('name', help='Protocol name (TCP, UDP, ICMP, etc.)')
    
    # Top talkers
    talkers_parser = subparsers.add_parser('talkers', help='Show top talkers')
    talkers_parser.add_argument('-l', '--limit', type=int, default=10, help='Number of results')
    
    # Top ports
    ports_parser = subparsers.add_parser('ports', help='Show top ports')
    ports_parser.add_argument('-l', '--limit', type=int, default=10, help='Number of results')
    
    # Conversations
    conv_parser = subparsers.add_parser('conversations', help='Show top conversations')
    conv_parser.add_argument('-l', '--limit', type=int, default=10, help='Number of results')
    
    # Export
    export_parser = subparsers.add_parser('export', help='Export packets to JSON')
    export_parser.add_argument('output', help='Output file name')
    export_parser.add_argument('-l', '--limit', type=int, help='Limit number of packets')
    
    # Payload search
    search_parser = subparsers.add_parser('search', help='Search payload data')
    search_parser.add_argument('term', help='Search term')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    db = DatabaseManager(args.database)
    
    if args.command == 'stats':
        db.print_stats()
    
    elif args.command == 'ip':
        packets = db.query_by_ip(args.address)
        print(f"\n[+] Found {len(packets)} packets for IP {args.address}\n")
        for packet in packets[:20]:  # Show first 20
            print(f"  [{packet[0]}] {packet[1]} | {packet[2]} -> {packet[3]} | {packet[4]} | {packet[7]} bytes")
    
    elif args.command == 'port':
        packets = db.query_by_port(args.number)
        print(f"\n[+] Found {len(packets)} packets for port {args.number}\n")
        for packet in packets[:20]:
            print(f"  [{packet[0]}] {packet[1]} | {packet[2]}:{packet[5]} -> {packet[3]}:{packet[6]} | {packet[4]}")
    
    elif args.command == 'protocol':
        packets = db.query_by_protocol(args.name)
        print(f"\n[+] Found {len(packets)} {args.name.upper()} packets\n")
        for packet in packets[:20]:
            print(f"  [{packet[0]}] {packet[1]} | {packet[2]} -> {packet[3]} | {packet[7]} bytes")
    
    elif args.command == 'talkers':
        talkers = db.get_top_talkers(args.limit)
        print(f"\n[+] Top {args.limit} Talkers:\n")
        for i, (ip, count, bytes_total) in enumerate(talkers, 1):
            print(f"  {i:2d}. {ip:15s} | {count:6,} packets | {bytes_total:10,} bytes")
    
    elif args.command == 'ports':
        ports = db.get_top_ports(args.limit)
        print(f"\n[+] Top {args.limit} Ports:\n")
        for i, (port, count) in enumerate(ports, 1):
            print(f"  {i:2d}. Port {port:5d} | {count:6,} packets")
    
    elif args.command == 'conversations':
        pairs = db.get_conversation_pairs(args.limit)
        print(f"\n[+] Top {args.limit} Conversations:\n")
        for i, (src, dst, count, bytes_total) in enumerate(pairs, 1):
            print(f"  {i:2d}. {src:15s} -> {dst:15s} | {count:6,} packets | {bytes_total:10,} bytes")
    
    elif args.command == 'export':
        db.export_to_json(args.output, args.limit)
    
    elif args.command == 'search':
        packets = db.search_payload(args.term)
        print(f"\n[+] Found {len(packets)} packets containing '{args.term}'\n")
        for packet in packets[:10]:
            print(f"  [{packet[0]}] {packet[1]} | {packet[2]} -> {packet[3]} | {packet[4]}")
            if packet[8]:
                print(f"      Payload: {packet[8][:100]}...")

if __name__ == '__main__':
    main()