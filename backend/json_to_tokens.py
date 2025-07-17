#!/usr/bin/env python3

import json
import re

def json_to_tokens(json_string):
    """Convert a JSON string directly to the token format expected by the parser"""
    tokens = []
    
    # Remove whitespace and prepare for tokenization
    json_string = json_string.strip()
    
    i = 0
    while i < len(json_string):
        char = json_string[i]
        
        # Skip whitespace
        if char.isspace():
            i += 1
            continue
            
        # Handle structural characters
        if char == '{':
            tokens.append('<{>')
        elif char == '}':
            tokens.append('<}>')
        elif char == '[':
            tokens.append('<[>')
        elif char == ']':
            tokens.append('<]>')
        elif char == ':':
            tokens.append('<:>')
        elif char == ',':
            tokens.append('<,>')
        
        # Handle strings
        elif char == '"':
            start = i + 1
            i += 1
            # Find the end of the string, handling escaped quotes
            while i < len(json_string) and (json_string[i] != '"' or json_string[i-1] == '\\'):
                i += 1
            if i < len(json_string):
                string_value = json_string[start:i]
                tokens.append(f'<str, {string_value}>')
            
        # Handle numbers
        elif char.isdigit() or char == '-' or char == '.':
            start = i
            # Handle negative numbers
            if char == '-':
                i += 1
            # Consume digits
            while i < len(json_string) and (json_string[i].isdigit() or json_string[i] == '.'):
                i += 1
            i -= 1  # Back up one since we'll increment at the end
            number_value = json_string[start:i+1]
            tokens.append(f'<num, {number_value}>')
            
        # Handle booleans and null
        elif char == 't' and json_string[i:i+4] == 'true':
            tokens.append('<bool, true>')
            i += 3  # Skip the rest of 'true'
        elif char == 'f' and json_string[i:i+5] == 'false':
            tokens.append('<bool, false>')
            i += 4  # Skip the rest of 'false'
        elif char == 'n' and json_string[i:i+4] == 'null':
            tokens.append('<null>')
            i += 3  # Skip the rest of 'null'
            
        i += 1
    
    # Add EOF token
    tokens.append('<EOF>')
    
    return tokens

def tokens_to_file(tokens, filename):
    """Write tokens to a file in the format expected by the parser"""
    with open(filename, 'w') as f:
        for token in tokens:
            f.write(token + '\n')

if __name__ == "__main__":
    # Test with a simple JSON
    test_json = '{"name": "Alice", "age": 30, "active": true}'
    tokens = json_to_tokens(test_json)
    print("Tokens generated:")
    for token in tokens:
        print(token)