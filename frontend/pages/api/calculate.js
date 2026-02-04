import formidable from 'formidable'
import fs from 'fs'
import csv from 'csv-parser'

export const config = {
  api: {
    bodyParser: false,
  },
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // Parse the uploaded file
    const form = formidable({ multiples: false })
    
    form.parse(req, async (err, fields, files) => {
      if (err) {
        return res.status(500).json({ error: 'Error parsing file' })
      }

      const file = files.file
      const method = fields.method || 'FIFO'
      
      if (!file) {
        return res.status(400).json({ error: 'No file uploaded' })
      }

      // Read CSV file
      const transactions = []
      
      fs.createReadStream(file.filepath)
        .pipe(csv())
        .on('data', (row) => {
          transactions.push({
            date: row.date,
            type: row.type,
            amount: parseFloat(row.amount),
            price: parseFloat(row.price),
            symbol: row.symbol,
            fee: parseFloat(row.fee || 0)
          })
        })
        .on('end', async () => {
          // Call Python backend API
          try {
            const backendResponse = await fetch(`${process.env.VERCEL_URL || 'http://localhost:3000'}/api/calculate`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                method: method,
                transactions: transactions
              })
            })

            const result = await backendResponse.json()
            res.status(200).json(result)
            
          } catch (error) {
            console.error('Backend error:', error)
            res.status(500).json({ error: 'Calculation failed' })
          }
        })
        .on('error', (error) => {
          console.error('CSV parsing error:', error)
          res.status(500).json({ error: 'Error reading CSV file' })
        })
    })
    
  } catch (error) {
    console.error('API Error:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
}
