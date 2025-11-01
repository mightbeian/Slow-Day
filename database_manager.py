#!/usr/bin/env python3
"""
Database management utilities for Slow Day
Provides tools for maintaining and analyzing the packet database
"""

import sqlite3
import argparse
from datetime import datetime, timedelta
import json

class DatabaseManager:
    def __init__(self, db_path='traffic.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_statistics(self):
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total packets
        cursor.execute('SELECT COUNT(*) FROM packets')
        total_packets = cursor.fetchone()[0]
        
        # Protocol breakdown
        cursor.execute('SELECT protocol, COUNT(*) FROM packets GROUP BY protocol')
        protocols = dict(cursor.fetchall())
        
        # Top source IPs
        cursor.execute('''
            SELECT src_ip, COUNT(*) as count 
            FROM packets 
            GROUP BY src_ip 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        top_sources = cursor.fetchall()
        
        # Top destination IPs
        cursor.execute('''
            SELECT dst_ip, COUNT(*) as count 
            FROM packets 
            GROUP BY dst_ip 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        top_destinations = cursor.fetchall()
        
        # Date range
        cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM packets')
        date_range = cursor.fetchone()
        
        # Database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        db_size = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_packets': total_packets,
            'protocols': protocols,
            'top_sources': top_sources,
            'top_destinations': top_destinations,
            'date_range': date_range,
            'database_size': db_size
        }
    
    def cleanup_old_packets(self, days=7):
        """Remove packets older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('SELECT COUNT(*) FROM packets WHERE timestamp < ?', (cutoff_str,))
        count_before = cursor.fetchone()[0]
        
        cursor.execute('DELETE FROM packets WHERE timestamp < ?', (cutoff_str,))
        
        conn.commit()
        conn.close()
        
        return count_before
    
    def vacuum_database(self):
        """Optimize database by reclaiming space"""
        conn = self.get_connection()
        conn.execute('VACUUM')
        conn.close()
        print("[+] Database vacuumed successfully")
    
    def backup_database(self, backup_path):
        """Create a backup of the database"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
        print(f"[+] Database backed up to {backup_path}")
    
    def export_to_csv(self, output_file, limit=None):
        """Export packets to CSV file"""
        import csv
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM packets ORDER BY id DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow([desc[0] for desc in cursor.description])
            # Write data
            writer.writerows(cursor.fetchall())
        
        conn.close()
        print(f"[+] Exported to {output_file}")
    
    def search_packets(self, **kwargs):
        """Search packets by various criteria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        conditions = []
        params = []
        
        if 'src_ip' in kwargs:
            conditions.append('src_ip = ?')
            params.append(kwargs['src_ip'])
        
        if 'dst_ip' in kwargs:
            conditions.append('dst_ip = ?')
            params.append(kwargs['dst_ip'])
        
        if 'protocol' in kwargs:
            conditions.append('protocol = ?')
            params.append(kwargs['protocol'])
        
        if 'port' in kwargs:
            conditions.append('(src_port = ? OR dst_port = ?)')
            params.extend([kwargs['port'], kwargs['port']])
        
        query = 'SELECT * FROM packets'
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        query += ' ORDER BY id DESC LIMIT 100'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        conn.close()
        return results
    
    def print_summary(self):
        """Print a summary of the database"""
        stats = self.get_statistics()
        
        print("\n" + "="*50)
        print("         DATABASE SUMMARY")
        print("="*50)
        print(f"\nTotal Packets: {stats['total_packets']:,}")
        print(f"Database Size: {stats['database_size']:,} bytes")
        
        if stats['date_range'][0]:
            print(f"Date Range: {stats['date_range'][0]} to {stats['date_range'][1]}")
        
        print("\nProtocol Breakdown:")
        for protocol, count in stats['protocols'].items():
            print(f"  {protocol}: {count:,}")
        
        print("\nTop 5 Source IPs:")
        for ip, count in stats['top_sources'][:5]:
            print(f"  {ip}: {count:,} packets")
        
        print("\nTop 5 Destination IPs:")
        for ip, count in stats['top_destinations'][:5]:
            print(f"  {ip}: {count:,} packets")
        
        print("\n" + "="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description='Slow Day Database Manager')
    parser.add_argument('-d', '--database', default='traffic.db', help='Database file path')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--cleanup', type=int, metavar='DAYS', help='Remove packets older than DAYS')
    parser.add_argument('--vacuum', action='store_true', help='Optimize database')
    parser.add_argument('--backup', metavar='FILE', help='Backup database to FILE')
    parser.add_argument('--export-csv', metavar='FILE', help='Export to CSV file')
    parser.add_argument('--search-ip', metavar='IP', help='Search by IP address')
    parser.add_argument('--search-port', type=int, metavar='PORT', help='Search by port')
    parser.add_argument('--search-protocol', metavar='PROTO', help='Search by protocol')
    
    args = parser.parse_args()
    
    manager = DatabaseManager(args.database)
    
    if args.stats:
        manager.print_summary()
    
    if args.cleanup:
        removed = manager.cleanup_old_packets(args.cleanup)
        print(f"[+] Removed {removed} packets older than {args.cleanup} days")
    
    if args.vacuum:
        manager.vacuum_database()
    
    if args.backup:
        manager.backup_database(args.backup)
    
    if args.export_csv:
        manager.export_to_csv(args.export_csv)
    
    if args.search_ip or args.search_port or args.search_protocol:
        search_params = {}
        if args.search_ip:
            search_params['src_ip'] = args.search_ip
        if args.search_port:
            search_params['port'] = args.search_port
        if args.search_protocol:
            search_params['protocol'] = args.search_protocol
        
        results = manager.search_packets(**search_params)
        print(f"\nFound {len(results)} matching packets:")
        for row in results[:20]:  # Show first 20
            print(f"  [{row[0]}] {row[1]} | {row[2]}:{row[5]} -> {row[3]}:{row[6]} | {row[4]}")
    
    if not any([args.stats, args.cleanup, args.vacuum, args.backup, 
                args.export_csv, args.search_ip, args.search_port, args.search_protocol]):
        parser.print_help()

if __name__ == '__main__':
    main()
