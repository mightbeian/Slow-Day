#!/usr/bin/env python3
"""
Web server for Slow Day Network Analyzer
Provides REST API and serves HTML interface
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from analyzer import NetworkAnalyzer
import threading
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
analyzer = NetworkAnalyzer()
capture_thread = None

@app.route('/')
def index():
    """Serve main HTML interface"""
    return send_from_directory('templates', 'index.html')

@app.route('/api/start', methods=['POST'])
def start_capture():
    """Start packet capture"""
    global capture_thread
    
    if analyzer.is_capturing:
        return jsonify({'error': 'Capture already in progress'}), 400
    
    data = request.json
    interface = data.get('interface')
    filter_ip = data.get('filter_ip')
    filter_port = data.get('filter_port')
    packet_count = data.get('packet_count', 0)
    
    # Start capture in background thread
    capture_thread = threading.Thread(
        target=analyzer.start_capture,
        args=(interface, filter_ip, filter_port, packet_count)
    )
    capture_thread.daemon = True
    capture_thread.start()
    
    return jsonify({'status': 'Capture started', 'message': 'Packet capture initiated'})

@app.route('/api/stop', methods=['POST'])
def stop_capture():
    """Stop packet capture"""
    if not analyzer.is_capturing:
        return jsonify({'error': 'No capture in progress'}), 400
    
    analyzer.is_capturing = False
    return jsonify({'status': 'Capture stopped', 'message': 'Packet capture terminated'})

@app.route('/api/packets', methods=['GET'])
def get_packets():
    """Get recent packets"""
    limit = request.args.get('limit', 100, type=int)
    packets = analyzer.get_recent_packets(limit)
    return jsonify({'packets': packets, 'count': len(packets)})

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get capture statistics"""
    stats = analyzer.get_statistics()
    
    if stats:
        return jsonify(stats)
    else:
        return jsonify({
            'total_packets': 0,
            'tcp_count': 0,
            'udp_count': 0,
            'icmp_count': 0,
            'other_count': 0,
            'total_bytes': 0
        })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current capture status"""
    return jsonify({
        'is_capturing': analyzer.is_capturing,
        'packet_count': analyzer.packet_count
    })

@app.route('/api/clear', methods=['POST'])
def clear_database():
    """Clear all packets from database"""
    if analyzer.is_capturing:
        return jsonify({'error': 'Cannot clear database while capturing'}), 400
    
    analyzer.clear_database()
    analyzer.packet_count = 0
    return jsonify({'status': 'Database cleared', 'message': 'All packets removed'})

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export packets as JSON"""
    limit = request.args.get('limit', 1000, type=int)
    packets = analyzer.get_recent_packets(limit)
    
    return jsonify({
        'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'packet_count': len(packets),
        'packets': packets
    })

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════╗
    ║      Slow Day - Web Interface        ║
    ║    Network Traffic Analyzer UI       ║
    ╚═══════════════════════════════════════╝
    
    [+] Starting web server on http://127.0.0.1:5000
    [+] Open your browser and navigate to the URL above
    """)
    
    app.run(host='127.0.0.1', port=5000, debug=False)