import type { NextApiRequest, NextApiResponse } from 'next'
import formidable from 'formidable'
import fs from 'fs'

export const config = {
  api: {
    bodyParser: false,
  },
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // For now, proxy to Python backend
    // In production, this would call the deployed FastAPI backend
    const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'
    
    // Forward the request to Python backend
    const formData = new FormData()
    
    // Note: In production, you'd parse the form data and forward it
    // For now, return a mock response for frontend testing
    
    res.status(200).json({
      success: true,
      data: {
        method: 'FIFO',
        total_transactions: 5,
        total_sales: 2,
        short_term_gain_loss: 1500.00,
        long_term_gain_loss: 0.00,
        total_gain_loss: 1500.00,
        realized_gains: []
      }
    })
    
  } catch (error) {
    console.error('API Error:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
}
