from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from tax_calculator import TaxCalculator, Transaction
import pandas as pd
from io import StringIO

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON request
            data = json.loads(post_data.decode('utf-8'))
            method = data.get('method', 'FIFO')
            transactions = data.get('transactions', [])
            
            # Create calculator
            calc = TaxCalculator(method=method)
            
            # Process transactions
            for txn in transactions:
                transaction = Transaction(
                    date=txn['date'],
                    transaction_type=txn['type'],
                    amount=float(txn['amount']),
                    price=float(txn['price']),
                    symbol=txn['symbol'],
                    fee=float(txn.get('fee', 0))
                )
                calc.add_transaction(transaction)
            
            # Generate summary
            summary = calc.generate_summary()
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'data': summary
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                'success': False,
                'error': str(e)
            }
            
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
