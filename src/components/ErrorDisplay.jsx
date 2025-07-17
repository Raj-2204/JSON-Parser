
const ErrorDisplay = ({ error, errorType }) => {
  const getErrorTypeInfo = (errorType) => {
    const errorTypes = {
      'Error Type 1': {
        title: 'Invalid Decimal Numbers',
        description: 'Decimal numbers cannot start or end with a decimal point, or start with a plus sign.',
        examples: ['Invalid: .123, 123., +123.45', 'Valid: 123.45, 0.123, 123.0']
      },
      'Error Type 2': {
        title: 'Empty Key',
        description: 'Dictionary keys cannot be empty strings or whitespace only.',
        examples: ['Invalid: {"": "value"}', 'Valid: {"key": "value"}']
      },
      'Error Type 3': {
        title: 'Invalid Numbers',
        description: 'Numbers cannot have leading zeros (except for single 0).',
        examples: ['Invalid: 01234, 00123', 'Valid: 1234, 0, 123']
      },
      'Error Type 4': {
        title: 'Reserved Words as Dictionary Key',
        description: 'The reserved words "true" and "false" cannot be used as dictionary keys.',
        examples: ['Invalid: {"true": "value", "false": "value"}', 'Valid: {"isTrue": "value", "status": false}']
      },
      'Error Type 5': {
        title: 'No Duplicate Keys in Dictionary',
        description: 'Dictionary objects cannot contain duplicate keys.',
        examples: ['Invalid: {"name": "Alice", "name": "Bob"}', 'Valid: {"firstName": "Alice", "lastName": "Bob"}']
      },
      'Error Type 6': {
        title: 'Consistent Types for List Elements',
        description: 'All elements in a list must be of the same type.',
        examples: ['Invalid: [1, "string", true]', 'Valid: [1, 2, 3] or ["a", "b", "c"]']
      },
      'Error Type 7': {
        title: 'Reserved Words as Strings',
        description: 'The reserved words "true" and "false" cannot be used as string values.',
        examples: ['Invalid: "true", "false"', 'Valid: true, false (as booleans)']
      }
    };

    return errorTypes[errorType] || {
      title: 'Unknown Error',
      description: 'An unrecognized error occurred during parsing.',
      examples: []
    };
  };

  const errorInfo = errorType ? getErrorTypeInfo(errorType) : null;

  return (
    <div className="error-display-container">
      <div className="error-header">
        <h2>Parse Error</h2>
      </div>
      
      <div className="error-content">
        <div className="error-message">
          <div className="error-icon">⚠️</div>
          <div className="error-text">
            <p className="error-main">{error}</p>
          </div>
        </div>
        
        {errorInfo && (
          <div className="error-details">
            <h3>{errorInfo.title}</h3>
            <p className="error-description">{errorInfo.description}</p>
            
            {errorInfo.examples.length > 0 && (
              <div className="error-examples">
                <h4>Examples:</h4>
                <ul>
                  {errorInfo.examples.map((example, index) => (
                    <li key={index} className="example-item">
                      <code>{example}</code>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
        
        <div className="error-suggestions">
          <h4>Suggestions:</h4>
          <ul>
            <li>Check your JSON syntax for missing commas, brackets, or quotes</li>
            <li>Ensure all string values are properly quoted</li>
            <li>Verify that object keys are unique</li>
            <li>Make sure array elements are of consistent types</li>
            <li>Avoid using reserved words (true, false) as string values</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ErrorDisplay;