#!/usr/bin/env python3

import sys
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile

from scanner import Lexer
from parser import Parser, InputRead
from json_to_tokens import json_to_tokens, tokens_to_file

app = Flask(__name__)
CORS(app)

def serialize_tree(node):
    """Convert the tree node to a serializable dictionary"""
    if node is None:
        return None
    
    return {
        'label': node.label,
        'is_leaf': node.is_leaf,
        'children': [serialize_tree(child) for child in node.children]
    }

def parse_json_string(json_string):
    """Parse a JSON string and return the result"""
    try:
        # Convert JSON string to tokens
        tokens = json_to_tokens(json_string)
        
        # Create a temporary file with the tokens
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            for token in tokens:
                temp_file.write(token + '\n')
            temp_file_path = temp_file.name
        
        try:
            # Use the existing InputRead class to process the tokenized input
            string_reader = InputRead(None)
            input_string = string_reader.write(temp_file_path)
            
            # Create lexer and parser instances
            lexer = Lexer(input_string)
            parser = Parser(lexer)
            
            # Parse and get the tree
            tree = parser.parse()
            
            # Convert tree to serializable format
            tree_data = serialize_tree(tree)
            
            return {
                'success': True,
                'data': tree_data,
                'input_processed': input_string,
                'tokens': tokens
            }
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        error_message = str(e)
        error_type = None
        
        # Extract error type if it's a parsing error
        if "Error Type" in error_message:
            error_type = error_message.split(":")[0].strip()
        
        return {
            'success': False,
            'error': error_message,
            'error_type': error_type
        }

@app.route('/parse', methods=['POST'])
def parse_json():
    """API endpoint to parse JSON input"""
    try:
        data = request.get_json()
        
        if not data or 'json_input' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing json_input in request body'
            }), 400
        
        json_input = data['json_input']
        
        if not json_input.strip():
            return jsonify({
                'success': False,
                'error': 'Empty JSON input'
            }), 400
        
        result = parse_json_string(json_input)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)