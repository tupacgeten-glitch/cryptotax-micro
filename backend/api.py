"""
FastAPI Backend for CryptoTax Micro
Handles CSV uploads, tax calculations, and PDF generation
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Literal, Optional
import pandas as pd
import io
from tax_calculator import TaxCalculator, Transaction
from pdf_generator import generate_pdf_report
import os
import tempfile

app = FastAPI(
    title="CryptoTax Micro API",
    description="Simple crypto tax calculations for small traders",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalculateRequest(BaseModel):
    method: Literal['FIFO', 'LIFO'] = 'FIFO'
    transactions: list


class CalculateResponse(BaseModel):
    method: str
    total_transactions: int
    total_sales: int
    short_term_gain_loss: float
    long_term_gain_loss: float
    total_gain_loss: float
    realized_gains: list


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CryptoTax Micro API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "ok",
        "database": "not_required",
        "calculations": "ready"
    }


@app.post("/api/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    method: str = 'FIFO'
):
    """
    Upload a CSV file and get tax calculations
    
    Expected CSV format:
    date,type,amount,price,symbol,fee
    2023-01-15,buy,1.0,20000.00,BTC,10.00
    """
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV content
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate required columns
        required_cols = ['date', 'type', 'amount', 'price', 'symbol']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_cols)}"
            )
        
        # Create calculator and process transactions
        calc = TaxCalculator(method=method)
        
        for _, row in df.iterrows():
            transaction = Transaction(
                date=row['date'],
                transaction_type=row['type'],
                amount=float(row['amount']),
                price=float(row['price']),
                symbol=row['symbol'],
                fee=float(row.get('fee', 0))
            )
            calc.add_transaction(transaction)
        
        # Generate summary
        summary = calc.generate_summary()
        
        return {
            "success": True,
            "data": summary,
            "transactions_processed": len(df)
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


@app.post("/api/calculate")
async def calculate(request: CalculateRequest):
    """
    Calculate taxes from JSON transaction data
    """
    try:
        calc = TaxCalculator(method=request.method)
        
        for txn_data in request.transactions:
            transaction = Transaction(
                date=txn_data['date'],
                transaction_type=txn_data['type'],
                amount=float(txn_data['amount']),
                price=float(txn_data['price']),
                symbol=txn_data['symbol'],
                fee=float(txn_data.get('fee', 0))
            )
            calc.add_transaction(transaction)
        
        summary = calc.generate_summary()
        
        return {
            "success": True,
            "data": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.post("/api/generate-pdf")
async def generate_pdf(request: CalculateRequest):
    """
    Generate a PDF tax report
    Returns a downloadable PDF file
    """
    try:
        # Calculate taxes
        calc = TaxCalculator(method=request.method)
        
        for txn_data in request.transactions:
            transaction = Transaction(
                date=txn_data['date'],
                transaction_type=txn_data['type'],
                amount=float(txn_data['amount']),
                price=float(txn_data['price']),
                symbol=txn_data['symbol'],
                fee=float(txn_data.get('fee', 0))
            )
            calc.add_transaction(transaction)
        
        summary = calc.generate_summary()
        
        # Generate PDF in temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf_path = tmp.name
            generate_pdf_report(summary, pdf_path)
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=f'crypto_tax_report_{request.method}.pdf'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")


@app.get("/api/sample-csv")
async def get_sample_csv():
    """
    Download a sample CSV template
    """
    sample_path = "sample_transactions.csv"
    
    if not os.path.exists(sample_path):
        # Create sample CSV if it doesn't exist
        sample_data = """date,type,amount,price,symbol,fee
2023-01-15,buy,1.0,20000.00,BTC,10.00
2023-03-20,buy,10.0,1800.00,ETH,5.00
2023-06-10,buy,0.5,30000.00,BTC,7.50
2023-09-15,sell,5.0,2000.00,ETH,4.00
2024-01-05,sell,1.2,45000.00,BTC,15.00"""
        
        with open(sample_path, 'w') as f:
            f.write(sample_data)
    
    return FileResponse(
        sample_path,
        media_type='text/csv',
        filename='crypto_tax_sample.csv'
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
