"""
Core Tax Calculation Engine
Handles FIFO/LIFO inventory tracking and capital gains calculations
"""

from typing import List, Dict, Literal
from datetime import datetime
from decimal import Decimal
import pandas as pd
from dateutil import parser


class Transaction:
    """Represents a single crypto transaction"""
    
    def __init__(
        self,
        date: str,
        transaction_type: str,  # 'buy' or 'sell'
        amount: float,
        price: float,
        symbol: str,
        fee: float = 0.0
    ):
        self.date = parser.parse(date) if isinstance(date, str) else date
        self.transaction_type = transaction_type.lower()
        self.amount = Decimal(str(amount))
        self.price = Decimal(str(price))
        self.symbol = symbol.upper()
        self.fee = Decimal(str(fee))
        self.total_cost = self.amount * self.price + self.fee
        
    def __repr__(self):
        return f"Transaction({self.date.date()}, {self.transaction_type}, {self.amount} {self.symbol} @ ${self.price})"


class TaxLot:
    """Represents a tax lot for cost basis tracking (FIFO/LIFO)"""
    
    def __init__(self, transaction: Transaction):
        self.date_acquired = transaction.date
        self.amount = transaction.amount
        self.cost_basis = transaction.total_cost
        self.price_per_unit = transaction.price
        
    def __repr__(self):
        return f"TaxLot({self.date_acquired.date()}, {self.amount} units @ ${self.price_per_unit})"


class TaxCalculator:
    """
    Main tax calculation engine
    Supports FIFO (First-In-First-Out) and LIFO (Last-In-First-Out) methods
    """
    
    def __init__(self, method: Literal['FIFO', 'LIFO'] = 'FIFO'):
        self.method = method
        self.transactions: List[Transaction] = []
        self.tax_lots: Dict[str, List[TaxLot]] = {}  # symbol -> list of tax lots
        self.realized_gains: List[Dict] = []
        
    def add_transaction(self, transaction: Transaction):
        """Add a transaction and update tax lots"""
        self.transactions.append(transaction)
        
        if transaction.transaction_type == 'buy':
            self._add_tax_lot(transaction)
        elif transaction.transaction_type == 'sell':
            self._process_sale(transaction)
            
    def _add_tax_lot(self, transaction: Transaction):
        """Add a new tax lot when buying crypto"""
        symbol = transaction.symbol
        if symbol not in self.tax_lots:
            self.tax_lots[symbol] = []
            
        lot = TaxLot(transaction)
        self.tax_lots[symbol].append(lot)
        
    def _process_sale(self, transaction: Transaction):
        """Process a sale and calculate realized gains/losses"""
        symbol = transaction.symbol
        
        if symbol not in self.tax_lots or not self.tax_lots[symbol]:
            # No cost basis - this shouldn't happen but handle gracefully
            print(f"Warning: No cost basis found for {symbol}")
            return
            
        amount_to_sell = transaction.amount
        proceeds = transaction.total_cost - transaction.fee  # Subtract fee from proceeds
        
        while amount_to_sell > 0 and self.tax_lots[symbol]:
            # Get lot based on method (FIFO=first, LIFO=last)
            lot_index = 0 if self.method == 'FIFO' else -1
            lot = self.tax_lots[symbol][lot_index]
            
            # Determine how much we're selling from this lot
            amount_from_lot = min(amount_to_sell, lot.amount)
            
            # Calculate cost basis for this portion
            cost_basis = (amount_from_lot / lot.amount) * lot.cost_basis
            
            # Calculate proceeds for this portion  
            proceeds_from_lot = (amount_from_lot / transaction.amount) * proceeds
            
            # Calculate gain/loss
            gain_or_loss = proceeds_from_lot - cost_basis
            
            # Determine holding period (short-term <1 year, long-term >=1 year)
            days_held = (transaction.date - lot.date_acquired).days
            term = 'long-term' if days_held >= 365 else 'short-term'
            
            # Record the realized gain/loss
            self.realized_gains.append({
                'symbol': symbol,
                'date_acquired': lot.date_acquired,
                'date_sold': transaction.date,
                'amount': float(amount_from_lot),
                'cost_basis': float(cost_basis),
                'proceeds': float(proceeds_from_lot),
                'gain_loss': float(gain_or_loss),
                'term': term,
                'days_held': days_held
            })
            
            # Update lot or remove if fully sold
            lot.amount -= amount_from_lot
            if lot.amount <= 0:
                self.tax_lots[symbol].pop(lot_index)
            else:
                lot.cost_basis -= cost_basis
                
            amount_to_sell -= amount_from_lot
            
    def load_csv(self, filepath: str, format: str = 'generic'):
        """
        Load transactions from CSV file
        Supports different exchange formats
        """
        df = pd.read_csv(filepath)
        
        # Map column names based on exchange format
        if format == 'coinbase':
            date_col = 'Timestamp'
            type_col = 'Transaction Type'
            amount_col = 'Quantity Transacted'
            price_col = 'Spot Price at Transaction'
            symbol_col = 'Asset'
            fee_col = 'Fees and/or Spread'
        else:  # generic format
            date_col = 'date'
            type_col = 'type'
            amount_col = 'amount'
            price_col = 'price'
            symbol_col = 'symbol'
            fee_col = 'fee'
            
        for _, row in df.iterrows():
            try:
                transaction = Transaction(
                    date=row[date_col],
                    transaction_type=row[type_col],
                    amount=float(row[amount_col]),
                    price=float(row[price_col]),
                    symbol=row[symbol_col],
                    fee=float(row.get(fee_col, 0))
                )
                self.add_transaction(transaction)
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
                
    def generate_summary(self) -> Dict:
        """Generate summary of tax calculations"""
        short_term_gains = sum(g['gain_loss'] for g in self.realized_gains if g['term'] == 'short-term')
        long_term_gains = sum(g['gain_loss'] for g in self.realized_gains if g['term'] == 'long-term')
        
        return {
            'method': self.method,
            'total_transactions': len(self.transactions),
            'total_sales': len(self.realized_gains),
            'short_term_gain_loss': round(short_term_gains, 2),
            'long_term_gain_loss': round(long_term_gains, 2),
            'total_gain_loss': round(short_term_gains + long_term_gains, 2),
            'realized_gains': self.realized_gains
        }
        
    def export_form_8949(self, output_path: str = 'form_8949.txt'):
        """Export data in Form 8949 format"""
        summary = self.generate_summary()
        
        with open(output_path, 'w') as f:
            f.write("FORM 8949 - Sales and Other Dispositions of Capital Assets\n")
            f.write("="*80 + "\n\n")
            f.write(f"Cost Basis Method: {self.method}\n\n")
            
            f.write("SHORT-TERM TRANSACTIONS (held 1 year or less)\n")
            f.write("-"*80 + "\n")
            
            for gain in self.realized_gains:
                if gain['term'] == 'short-term':
                    f.write(f"{gain['symbol']:8} ")
                    f.write(f"Acquired: {gain['date_acquired'].strftime('%m/%d/%Y')} ")
                    f.write(f"Sold: {gain['date_sold'].strftime('%m/%d/%Y')} ")
                    f.write(f"Proceeds: ${gain['proceeds']:>12.2f} ")
                    f.write(f"Cost: ${gain['cost_basis']:>12.2f} ")
                    f.write(f"Gain/Loss: ${gain['gain_loss']:>12.2f}\n")
                    
            f.write(f"\nShort-term Total: ${summary['short_term_gain_loss']:.2f}\n\n")
            
            f.write("LONG-TERM TRANSACTIONS (held more than 1 year)\n")
            f.write("-"*80 + "\n")
            
            for gain in self.realized_gains:
                if gain['term'] == 'long-term':
                    f.write(f"{gain['symbol']:8} ")
                    f.write(f"Acquired: {gain['date_acquired'].strftime('%m/%d/%Y')} ")
                    f.write(f"Sold: {gain['date_sold'].strftime('%m/%d/%Y')} ")
                    f.write(f"Proceeds: ${gain['proceeds']:>12.2f} ")
                    f.write(f"Cost: ${gain['cost_basis']:>12.2f} ")
                    f.write(f"Gain/Loss: ${gain['gain_loss']:>12.2f}\n")
                    
            f.write(f"\nLong-term Total: ${summary['long_term_gain_loss']:.2f}\n\n")
            f.write(f"TOTAL GAIN/LOSS: ${summary['total_gain_loss']:.2f}\n")


if __name__ == "__main__":
    # Example usage
    calc = TaxCalculator(method='FIFO')
    
    # Example transactions
    calc.add_transaction(Transaction('2023-01-15', 'buy', 1.0, 20000, 'BTC', 10))
    calc.add_transaction(Transaction('2023-06-20', 'buy', 0.5, 30000, 'BTC', 5))
    calc.add_transaction(Transaction('2024-01-10', 'sell', 1.2, 45000, 'BTC', 20))
    
    summary = calc.generate_summary()
    print(f"Total gain/loss: ${summary['total_gain_loss']}")
    print(f"Short-term: ${summary['short_term_gain_loss']}")
    print(f"Long-term: ${summary['long_term_gain_loss']}")
    
    calc.export_form_8949('test_form_8949.txt')
    print("Form 8949 exported to test_form_8949.txt")
