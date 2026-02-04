import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const csvContent = `date,type,amount,price,symbol,fee
2023-01-15,buy,1.0,20000.00,BTC,10.00
2023-03-20,buy,10.0,1800.00,ETH,5.00
2023-06-10,buy,0.5,30000.00,BTC,7.50
2023-09-15,sell,5.0,2000.00,ETH,4.00
2024-01-05,sell,1.2,45000.00,BTC,15.00`

  res.setHeader('Content-Type', 'text/csv')
  res.setHeader('Content-Disposition', 'attachment; filename="crypto_tax_sample.csv"')
  res.status(200).send(csvContent)
}
