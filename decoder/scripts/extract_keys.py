#!/usr/bin/env python3
"""
Author: Crypto Caballeros
Date: 2025

Extract cryptographic keys from the secrets file and generate a C header file, 
to be used in decoder processes.
This script is intended to be run during the Docker build process.
"""
import os
import sys
import traceback
import json
import glob
from pathlib import Path

# Comprehensive debugging output
def print_debug_info():
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    print(f"Environment variables: {dict(os.environ)}")
    print(f"Root directory contents: {os.listdir('/')}")
    
    # Search for potential secrets files in common locations
    for search_path in ['/', '/secrets', '/global.secrets', '/decoder']:
        if os.path.exists(search_path):
            print(f"Contents of {search_path}:")
            for item in os.listdir(search_path):
                full_path = os.path.join(search_path, item)
                file_type = "directory" if os.path.isdir(full_path) else "file"
                size = os.path.getsize(full_path) if os.path.isfile(full_path) else "-"
                print(f"  {item} ({file_type}, {size} bytes)")

# Function to discover potential secrets files
def find_secrets_files():
    """Search for candidate secrets files in multiple locations"""
    candidate_paths = []
    
    # Check environment variable first
    env_path = os.environ.get("SECRETS_PATH")
    if env_path and os.path.exists(env_path):
        candidate_paths.append(env_path)
        print(f"Found secrets path from environment: {env_path}")
    
    # Check common mount points
    for base_path in ['/secrets', '/global.secrets', '/']:
        if not os.path.exists(base_path):
            continue
            
        # Look for JSON files
        for json_file in glob.glob(f"{base_path}/*.json"):
            candidate_paths.append(json_file)
            
        # Look for BIN files
        for bin_file in glob.glob(f"{base_path}/*.bin"):
            candidate_paths.append(bin_file)
            
        # Look for files without extensions that might be JSON
        for file_path in os.listdir(base_path):
            full_path = os.path.join(base_path, file_path)
            if os.path.isfile(full_path) and '.' not in file_path:
                candidate_paths.append(full_path)
    
    return candidate_paths

# Function to try parsing a file as JSON
def try_parse_json(file_path):
    """Attempt to parse a file as JSON, return None if fails"""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            # Try direct JSON parsing
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Try decoding with different encodings
                for encoding in ['utf-8', 'latin-1']:
                    try:
                        return json.loads(content.decode(encoding))
                    except:
                        pass
    except Exception as e:
        print(f"Cannot parse {file_path}: {e}")
    return None

# Function to create C header file from key data
def generate_header_file(data, output_path):
    """Generate C header file containing keys from JSON data"""
    try:
        # Extract keys (adjust based on your actual key names)
        keys_to_extract = {
            "encryption_Key": "ENCRYPTION_KEY",
            "subscription_Key": "SUBSCRIPTION_KEY", 
            "MAC_Key": "MAC_KEY"
        }
        
        extracted_keys = {}
        for json_key, header_name in keys_to_extract.items():
            if json_key in data:
                # Convert from hex to bytes for representation as C array
                key_bytes = bytes.fromhex(data[json_key])
                extracted_keys[header_name] = key_bytes
        
        # Generate header file
        with open(output_path, 'w') as f:
            f.write("/**\n")
            f.write(" * @file secret_keys.h\n")
            f.write(" * @author Auto-generated from secrets\n")
            f.write(" * @brief File containing cryptographic keys\n")
            f.write(" */\n\n")
            
            # Include guards
            f.write("#ifndef __SECRET_KEYS_H\n")
            f.write("#define __SECRET_KEYS_H\n\n")
            
            # Required includes
            f.write("#include <stdint.h>\n\n")
            
            f.write("/****************************** Define Keys *******************************/\n\n")
            
            # Write each key as a byte array
            for name, key_bytes in extracted_keys.items():
                f.write(f"/**\n * {name} extracted from secrets\n */\n")
                f.write(f"static const uint8_t {name}[] = {{\n    ")
                
                # Format bytes in rows of 8 for readability
                bytes_str = []
                for i, b in enumerate(key_bytes):
                    if i > 0 and i % 8 == 0:
                        bytes_str.append("\n    ")
                    bytes_str.append(f"0x{b:02x}")
                    if i < len(key_bytes) - 1:
                        bytes_str.append(", ")
                
                f.write("".join(bytes_str))
                f.write("\n};\n\n")
            
            # Define key sizes
            f.write("/****************************** Define Key Sizes *******************************/\n\n")
            for name in extracted_keys.keys():
                f.write(f"#define {name}_SIZE (sizeof({name}))\n\n")
            
            # Add standard utility functions
            f.write("/****************************** Utility Functions *******************************/\n\n")
            
            # Add key loading functions
            for name in extracted_keys.keys():
                f.write(f"static inline void load_{name.lower()}(uint8_t *key_buffer) {{\n")
                f.write(f"    for (int i = 0; i < {name}_SIZE; i++) {{\n")
                f.write(f"        key_buffer[i] = {name}[i];\n")
                f.write("    }\n")
                f.write("}\n\n")
            
            # Add secure clear function
            f.write("static inline void secure_clear(volatile uint8_t *buffer, size_t size) {\n")
            f.write("    if (buffer == NULL || size == 0) {\n")
            f.write("        return;\n")
            f.write("    }\n\n")
            f.write("    volatile uint8_t *p;\n\n")
            f.write("    p = buffer;\n")
            f.write("    for (size_t i = 0; i < size; i++) {\n")
            f.write("        *p++ = 0xFF;\n")
            f.write("    }\n\n")
            f.write("    __asm__ volatile (\"\" : : : \"memory\");\n\n")
            f.write("    p = buffer;\n")
            f.write("    for (size_t i = 0; i < size; i++) {\n")
            f.write("        *p++ = 0x00;\n")
            f.write("    }\n\n")
            f.write("    __asm__ volatile (\"\" : : : \"memory\");\n")
            f.write("}\n\n")
            
            # Close include guard
            f.write("#endif // __SECRET_KEYS_H\n")
        
        print(f"Successfully generated header file at {output_path}")
        return True
    except Exception as e:
        print(f"Error generating header: {e}")
        traceback.print_exc()
        return False

def main():
    """Main function to extract keys and generate header"""
    print("Starting enhanced key extraction process...")
    
    # Print comprehensive debug info
    print_debug_info()
    
    # Output file path
    output_header = "/decoder/inc/secret_keys.h"
    os.makedirs(os.path.dirname(output_header), exist_ok=True)
    
    # Find candidate secrets files
    candidate_files = find_secrets_files()
    print(f"Found {len(candidate_files)} candidate files: {candidate_files}")
    
    # Try each file until we find one that works
    for file_path in candidate_files:
        print(f"Attempting to parse: {file_path}")
        data = try_parse_json(file_path)
        if data:
            print(f"Successfully parsed {file_path}")
            if generate_header_file(data, output_header):
                print("Key extraction completed successfully!")
                return 0
    
    # Handle binary files if JSON parsing failed
    # This would need customization based on your binary format
    print("JSON parsing failed, will try .bin files...")
    bin_files = [f for f in candidate_files if f.endswith('.bin')]
    if bin_files:
        print(f"Found {len(bin_files)} .bin files to try")
        # Custom handling for .bin files would go here
        # This requires knowledge of the binary format structure
    
    print("ERROR: Could not find or parse any valid secrets file")
    return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Unhandled exception: {e}")
        traceback.print_exc()
        sys.exit(1)