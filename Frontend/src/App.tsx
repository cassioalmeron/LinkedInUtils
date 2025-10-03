import { useState } from 'react'
import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import './App.css'
import { getComments, getContentByUrl } from './services/CommentsService'
import Footer from './components/Footer/Index'

function App() {
  const [inputText, setInputText] = useState<string>('')
  const [generatedComment, setGeneratedComment] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isSearching, setIsSearching] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const handleGenerateClick = async () => {
    const tone = (document.getElementById('tone') as HTMLSelectElement)?.value
    const observations = (document.getElementById('observations-text') as HTMLTextAreaElement)?.value

    if (!inputText.trim()) {
      toast.error('Please enter some text to generate a comment for.')
      return
    }

    setIsLoading(true)
    setError('')
    setGeneratedComment('')

    try {
      const comment = await getComments(inputText, tone, observations || '')
      setGeneratedComment(comment)
    } catch (err) {
      toast.error('Failed to generate comment.')
      setError('Failed to generate comment. Please check your API key and try again.')
      console.error('Error generating comment:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleGenerateClickByUrl = async () => {
    const url = (document.getElementById('url') as HTMLInputElement)?.value
    
    if (!url.trim()) {
      toast.error('Please enter a URL to search.')
      return
    }

    setIsSearching(true)
    setError('')
    
    try {
      const content = await getContentByUrl(url)
      setInputText(content)
    } catch (err) {
      toast.error('Failed to fetch content from URL. Please check the URL and try again.')
      console.error('Error fetching content:', err)
    } finally {
      setIsSearching(false)
    }
  }

  const handleCopyClick = async () => {
    if (!generatedComment) return
    try {
      await navigator.clipboard.writeText(generatedComment)
      toast.success('Comment copied to clipboard!')
    } catch {
      toast.error('Failed to copy to clipboard')
    }
  }

  const handleUrlKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleGenerateClickByUrl()
    }
  }

  return (
    <>
      <div style={{ maxWidth: 720, margin: '40px auto', padding: '16px 16px 100px 16px', minWidth: 1024 }}>
        <p>Generate a comment for your LinkedIn post.</p>
        
        <div style={{ marginTop: 12, display: 'flex', alignItems: 'center', gap: 12 }}>
          <label htmlFor="url" style={{ marginBottom: 0, marginRight: 12, minWidth: 64, textAlign: 'right' }}>URL</label>
          <input 
            id="url"
            type="url"
            placeholder="Enter URL here..."
            onKeyPress={handleUrlKeyPress}
            style={{ 
              flex: 1, 
              padding: 12, 
              boxSizing: 'border-box',
              backgroundColor: '#0f1115',
              border: '1px solid #2a2f3a',
              borderRadius: 8,
              color: 'white'
            }}
          />
          <button 
            disabled={isSearching}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: isSearching ? '#6c757d' : '#28a745', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px', 
              cursor: isSearching ? 'not-allowed' : 'pointer',
              whiteSpace: 'nowrap'
            }}
            onClick={handleGenerateClickByUrl}>
            {isSearching ? 'Searching...' : 'Search on LinkedIn'}
          </button>
        </div>
        <textarea
          id="input-text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your text here..."
          rows={25}
          style={{ width: '100%', boxSizing: 'border-box', padding: 12, resize: 'vertical' }}
        />
        <div style={{ marginTop: 12, display: 'flex', alignItems: 'center', gap: 12 }}>
          <label htmlFor="tone" style={{ marginBottom: 0, marginRight: 12, minWidth: 64, textAlign: 'right' }}>Ton</label>
          <select id="tone" name="tone" style={{ flex: 1, padding: 10 }}>
            <option>✅ Agreement</option>
            <option>📊 Analytical</option>
            <option>🛡️ Authoritative</option>
            <option>😊 Casual</option>
            <option>🚧 Cautious</option>
            <option>🤝 Conciliatory</option>
            <option>🧐 Critical</option>
            <option>🤔 Disagreement</option>
            <option>🤗 Empathetic</option>
            <option>🎉 Enthusiastic</option>
            <option>😊 Friendly</option>
            <option>😂 Humorous</option>
            <option>📚 Informative</option>
            <option>✨ Inspirational</option>
            <option>📖 Narrative</option>
            <option>⚖️ Neutral</option>
            <option>🌞 Optimistic</option>
            <option>🗣️ Persuasive</option>
            <option>🌧️ Pessimistic</option>
            <option>👔 Professional</option>
            <option>❓ Questioning</option>
            <option>💭 Reflective</option>
            <option>👍 Supportive</option>
            <option>🌟 Visionary</option>
          </select>
        </div>
        <textarea
          id="observations-text"
          placeholder="Observations..."
          rows={5}
          style={{ width: '100%', boxSizing: 'border-box', padding: 12, resize: 'vertical' }}
        />
        <div style={{ marginTop: 12 }}>
          <button 
            onClick={handleGenerateClick} 
            disabled={isLoading}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: isLoading ? '#ccc' : '#007bff', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px', 
              cursor: isLoading ? 'not-allowed' : 'pointer' 
            }}
          >
            {isLoading ? 'Generating...' : 'Generate Comment'}
          </button>
        </div>

        {error && (
          <div style={{ 
            marginTop: 12, 
            padding: 12, 
            backgroundColor: '#f8d7da', 
            color: '#721c24', 
            border: '1px solid #f5c6cb', 
            borderRadius: 4 
          }}>
            {error}
          </div>
        )}

        {generatedComment && (
          <div style={{ marginTop: 12, display: 'flex', gap: 12, alignItems: 'stretch' }}>
            <div style={{ flex: 1, backgroundColor: '#0f1115', border: '1px solid #2a2f3a', borderRadius: 8, padding: 12, whiteSpace: 'pre-wrap' }}>
              {generatedComment}
            </div>
            <div>
              <button
                onClick={handleCopyClick}
                aria-label="Copy to clipboard"
                title="Copy to clipboard"
                style={{ width: 48, height: 48, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}
              >
                📋
              </button>
            </div>
          </div>
        )}

        <Footer />
      </div>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </>
  )
}

export default App
