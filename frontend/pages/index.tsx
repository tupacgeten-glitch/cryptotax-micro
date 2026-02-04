import { useState } from 'react'
import Head from 'next/head'

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [method, setMethod] = useState<'FIFO' | 'LIFO'>('FIFO')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!file) {
      setError('Please select a CSV file')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('method', method)

      const response = await fetch('/api/calculate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Calculation failed')
      }

      const data = await response.json()
      setResult(data.data)
    } catch (err) {
      setError('Error calculating taxes. Please check your CSV format.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const downloadSample = () => {
    window.open('/api/sample', '_blank')
  }

  return (
    <>
      <Head>
        <title>CryptoTax Micro - Simple Crypto Tax Reports for $19/year</title>
        <meta name="description" content="Affordable crypto tax reporting for small traders. FIFO/LIFO calculations, Form 8949 export. Only $19/year." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        {/* Header */}
        <header className="border-b bg-white/80 backdrop-blur-sm">
          <div className="max-w-6xl mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold text-gray-900">CryptoTax <span className="text-blue-600">Micro</span></h1>
          </div>
        </header>

        {/* Hero Section */}
        <main className="max-w-4xl mx-auto px-4 py-12">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Simple Crypto Tax Reports
            </h2>
            <p className="text-xl text-gray-600 mb-2">
              For traders with &lt;500 transactions
            </p>
            <p className="text-3xl font-bold text-blue-600 mb-4">
              $19/year
            </p>
            <p className="text-gray-500">
              vs. $50-300/year for competitors
            </p>
          </div>

          {/* Calculator Card */}
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Try It Free (Beta)
            </h3>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Method Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Cost Basis Method
                </label>
                <div className="flex gap-4">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      value="FIFO"
                      checked={method === 'FIFO'}
                      onChange={(e) => setMethod('FIFO')}
                      className="mr-2"
                    />
                    <span>FIFO (First-In-First-Out)</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      value="LIFO"
                      checked={method === 'LIFO'}
                      onChange={(e) => setMethod('LIFO')}
                      className="mr-2"
                    />
                    <span>LIFO (Last-In-First-Out)</span>
                  </label>
                </div>
              </div>

              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload Transaction CSV
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-full file:border-0
                      file:text-sm file:font-semibold
                      file:bg-blue-50 file:text-blue-700
                      hover:file:bg-blue-100"
                  />
                  {file && (
                    <p className="mt-2 text-sm text-gray-600">
                      Selected: {file.name}
                    </p>
                  )}
                </div>
                <button
                  type="button"
                  onClick={downloadSample}
                  className="mt-2 text-sm text-blue-600 hover:underline"
                >
                  Download sample CSV template
                </button>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || !file}
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold
                  hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed
                  transition-colors"
              >
                {loading ? 'Calculating...' : 'Calculate Taxes (Free)'}
              </button>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}
            </form>
          </div>

          {/* Results */}
          {result && (
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                Tax Summary
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Total Transactions</p>
                  <p className="text-2xl font-bold">{result.total_transactions}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Total Sales</p>
                  <p className="text-2xl font-bold">{result.total_sales}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Method Used</p>
                  <p className="text-2xl font-bold">{result.method}</p>
                </div>
              </div>

              <div className="border-t pt-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-700 mb-1">Short-term Gain/Loss</p>
                    <p className={`text-2xl font-bold ${result.short_term_gain_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      ${result.short_term_gain_loss.toFixed(2)}
                    </p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-700 mb-1">Long-term Gain/Loss</p>
                    <p className={`text-2xl font-bold ${result.long_term_gain_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      ${result.long_term_gain_loss.toFixed(2)}
                    </p>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-lg">
                  <p className="text-lg mb-2">Total Capital Gain/Loss</p>
                  <p className="text-4xl font-bold">
                    ${result.total_gain_loss.toFixed(2)}
                  </p>
                </div>

                <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-sm text-yellow-800">
                    <strong>Beta Version:</strong> This is a free preview. To download your full PDF report and use for tax filing, upgrade for $19/year.
                  </p>
                  <button className="mt-3 bg-yellow-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-yellow-700">
                    Upgrade to Download PDF ($19)
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Features */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6">
              <div className="text-4xl mb-3">📊</div>
              <h4 className="font-bold text-lg mb-2">FIFO & LIFO</h4>
              <p className="text-gray-600 text-sm">
                Choose your preferred cost basis method
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-3">📄</div>
              <h4 className="font-bold text-lg mb-2">Form 8949</h4>
              <p className="text-gray-600 text-sm">
                IRS-ready PDF export for tax filing
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-3">💰</div>
              <h4 className="font-bold text-lg mb-2">$19/year</h4>
              <p className="text-gray-600 text-sm">
                Simple, transparent pricing
              </p>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="border-t mt-12 py-8 text-center text-gray-600 text-sm">
          <p className="mb-2">
            <strong>Disclaimer:</strong> This tool is for informational purposes only and does not constitute tax advice.
          </p>
          <p>
            CryptoTax Micro &copy; 2026 | Built as a $100 startup challenge
          </p>
        </footer>
      </div>
    </>
  )
}
