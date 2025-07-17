import { useState } from 'react'
import Layout from './components/Layout'
import JsonInput from './components/JsonInput'
import ParseTreeDisplay from './components/ParseTreeDisplay'
import ErrorDisplay from './components/ErrorDisplay'
import { parseJson } from './services/api'

function App() {
  const [parseResult, setParseResult] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleParse = async (jsonInput) => {
    setIsLoading(true)
    setError(null)
    setParseResult(null)

    try {
      const result = await parseJson(jsonInput)
      setParseResult(result)
    } catch (err) {
      setError({
        message: err.message,
        type: err.errorType || null
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Layout>
      <div className="app-panel">
        <JsonInput onParse={handleParse} isLoading={isLoading} />
      </div>
      <div className="app-panel">
        {error ? (
          <ErrorDisplay error={error.message} errorType={error.type} />
        ) : (
          <ParseTreeDisplay parseResult={parseResult} />
        )}
      </div>
    </Layout>
  )
}

export default App
