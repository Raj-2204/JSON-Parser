# JSON Parser Frontend

A React-based frontend for the JSON parser with semantic validation and parse tree visualization.

## Features

- **Interactive JSON Input**: Large textarea with sample JSON examples
- **Parse Tree Visualization**: Hierarchical tree display with collapsible nodes
- **Error Display**: Detailed error messages with explanations and examples
- **Export Functionality**: Save parse trees as JSON files
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Parsing**: Instant feedback with loading states

## Project Structure

```
json-parser-frontend/
├── src/
│   ├── components/           # React components
│   │   ├── JsonInput.jsx     # Input component with samples
│   │   ├── ParseTreeDisplay.jsx # Tree visualization
│   │   ├── ErrorDisplay.jsx  # Error handling
│   │   └── Layout.jsx        # Main layout wrapper
│   ├── services/
│   │   └── api.js           # Backend API calls
│   └── styles/              # Component styles
├── backend/
│   ├── app.py              # Flask API server
│   ├── json_to_tokens.py   # JSON tokenizer
│   └── requirements.txt    # Python dependencies
└── package.json
```

## Setup Instructions

### 1. Frontend Setup

```bash
cd json-parser-frontend
npm install
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```
The Flask server will start on `http://localhost:5001`

**Terminal 2 - Frontend:**
```bash
cd json-parser-frontend
npm run dev
```
The React app will start on `http://localhost:5173`

## Usage

1. **Enter JSON**: Type or paste JSON in the input textarea
2. **Use Samples**: Select from predefined valid/invalid JSON examples
3. **Parse**: Click "Parse JSON" to validate and generate parse tree
4. **View Results**: 
   - Valid JSON shows parse tree visualization
   - Invalid JSON shows detailed error messages
5. **Export**: Save parse trees or copy to clipboard

## Error Types

The parser detects 7 semantic error types:

1. **Invalid Decimal Numbers**: Numbers with improper decimal formatting
2. **Empty Keys**: Dictionary keys that are empty or whitespace
3. **Invalid Numbers**: Numbers with leading zeros
4. **Reserved Words as Keys**: Using 'true'/'false' as dictionary keys
5. **Duplicate Keys**: Same key appearing twice in a dictionary
6. **Inconsistent Array Types**: Mixed data types in arrays
7. **Reserved Words as Strings**: Using 'true'/'false' as string values

## API Endpoints

- `POST /parse` - Parse JSON input
- `GET /health` - Health check

## Technology Stack

- **Frontend**: React 18, Vite, CSS Modules
- **Backend**: Flask, Flask-CORS
- **Parser**: Custom lexer/parser from existing Python implementation