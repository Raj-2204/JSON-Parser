import { useState } from 'react';

const JsonInput = ({ onParse, isLoading }) => {
  const [jsonInput, setJsonInput] = useState('');

  const sampleJsons = [
    {
      name: 'Valid Object',
      json: '{"name": "Alice", "age": 30, "active": true}'
    },
    {
      name: 'Valid Array',
      json: '[1, 2, 3, 4, 5]'
    },
    {
      name: 'Nested Structure',
      json: '{"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}'
    },
    {
      name: 'Invalid - Duplicate Keys',
      json: '{"name": "Alice", "name": "Bob"}'
    },
    {
      name: 'Invalid - Mixed Array Types',
      json: '[1, "string", true]'
    },
    {
      name: 'Invalid - Reserved Word as Key',
      json: '{"true": "value"}'
    },
    {
      name: 'Invalid - Invalid Number',
      json: '{"number": 01234}'
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (jsonInput.trim()) {
      onParse(jsonInput);
    }
  };

  const loadSample = (sampleJson) => {
    setJsonInput(sampleJson);
  };

  const clearInput = () => {
    setJsonInput('');
  };

  return (
    <div className="json-input-container">
      <div className="input-header">
        <h2>JSON Input</h2>
        <div className="sample-buttons">
          <select 
            onChange={(e) => e.target.value && loadSample(e.target.value)}
            value=""
            className="sample-select"
          >
            <option value="">Load Sample JSON</option>
            {sampleJsons.map((sample, index) => (
              <option key={index} value={sample.json}>
                {sample.name}
              </option>
            ))}
          </select>
          <button 
            type="button" 
            onClick={clearInput}
            className="clear-btn"
          >
            Clear
          </button>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          placeholder="Enter your JSON here..."
          className="json-textarea"
          rows="20"
          disabled={isLoading}
        />
        
        <div className="input-actions">
          <button 
            type="submit" 
            className="parse-btn"
            disabled={isLoading || !jsonInput.trim()}
          >
            {isLoading ? 'Parsing...' : 'Parse JSON'}
          </button>
        </div>
      </form>
      
      <div className="input-info">
        <p>
          Enter a JSON string to validate and visualize its parse tree. 
          The parser enforces semantic rules and will show specific error types for invalid JSON.
        </p>
      </div>
    </div>
  );
};

export default JsonInput;