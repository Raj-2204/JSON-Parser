import { useState } from 'react';
import './ParseTreeDisplay.css';

const TreeNode = ({ node, depth = 0, isLast = false, parentPrefix = '' }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  
  if (!node) return null;

  const hasChildren = node.children && node.children.length > 0;
  const isExpandable = hasChildren && !node.is_leaf;
  
  // Create the prefix for this node
  const currentPrefix = parentPrefix + (isLast ? '└── ' : '├── ');
  const childPrefix = parentPrefix + (isLast ? '    ' : '│   ');

  const getNodeTypeClass = (label) => {
    if (label.includes('STRING:')) return 'node-string';
    if (label.includes('NUMBER:')) return 'node-number';
    if (label.includes('BOOLEAN:')) return 'node-boolean';
    if (label.includes('null')) return 'node-null';
    if (label.includes('dict')) return 'node-dict';
    if (label.includes('list:')) return 'node-list';
    if (label.includes('pair:')) return 'node-pair';
    if (label.includes('value:')) return 'node-value';
    return 'node-default';
  };

  const toggleExpanded = () => {
    if (isExpandable) {
      setIsExpanded(!isExpanded);
    }
  };

  return (
    <div className="tree-node">
      <div className="node-line">
        <span className="node-prefix">{currentPrefix}</span>
        <span 
          className={`node-label ${getNodeTypeClass(node.label)} ${isExpandable ? 'expandable' : ''}`}
          onClick={toggleExpanded}
        >
          {isExpandable && (
            <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
              ▶
            </span>
          )}
          {node.label}
        </span>
      </div>
      
      {hasChildren && isExpanded && (
        <div className="node-children">
          {node.children.map((child, index) => (
            <TreeNode
              key={index}
              node={child}
              depth={depth + 1}
              isLast={index === node.children.length - 1}
              parentPrefix={childPrefix}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const ParseTreeDisplay = ({ parseResult, onExport }) => {
  const [viewMode, setViewMode] = useState('tree'); // 'tree' or 'json'

  if (!parseResult) {
    return (
      <div className="parse-tree-container">
        <div className="tree-header">
          <h2>Parse Tree</h2>
        </div>
        <div className="tree-placeholder">
          <p>Enter JSON and click "Parse JSON" to see the parse tree visualization</p>
        </div>
      </div>
    );
  }

  const exportTree = () => {
    const dataStr = JSON.stringify(parseResult.data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'parse-tree.json';
    link.click();
    
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = () => {
    const dataStr = JSON.stringify(parseResult.data, null, 2);
    navigator.clipboard.writeText(dataStr).then(() => {
      alert('Parse tree copied to clipboard!');
    });
  };

  return (
    <div className="parse-tree-container">
      <div className="tree-header">
        <h2>Parse Tree</h2>
        <div className="tree-controls">
          <div className="view-toggle">
            <button 
              className={viewMode === 'tree' ? 'active' : ''}
              onClick={() => setViewMode('tree')}
            >
              Tree View
            </button>
            <button 
              className={viewMode === 'json' ? 'active' : ''}
              onClick={() => setViewMode('json')}
            >
              JSON View
            </button>
          </div>
          <div className="export-buttons">
            <button onClick={copyToClipboard} className="copy-btn">
              Copy
            </button>
            <button onClick={exportTree} className="export-btn">
              Export
            </button>
          </div>
        </div>
      </div>
      
      <div className="tree-content">
        {viewMode === 'tree' ? (
          <div className="tree-view">
            <TreeNode node={parseResult.data} />
          </div>
        ) : (
          <div className="json-view">
            <pre>{JSON.stringify(parseResult.data, null, 2)}</pre>
          </div>
        )}
      </div>
      
      {parseResult.tokens && (
        <div className="tokens-section">
          <h3>Generated Tokens</h3>
          <div className="tokens-list">
            {parseResult.tokens.map((token, index) => (
              <span key={index} className="token">
                {token}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ParseTreeDisplay;