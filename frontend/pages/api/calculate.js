export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // For MVP, return mock data
    // In production, this would call the Python backend
    
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
