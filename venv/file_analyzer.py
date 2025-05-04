import hashlib
import magic
import os

class FileAnalyzer:
    def __init__(self):
        self.magic = magic.Magic()

    def get_file_hash(self, filepath, algorithm='sha256', chunk_size=65536):
        """Calculate file hash with progress tracking"""
        hasher = hashlib.new(algorithm)
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"

    def get_file_type(self, filepath):
        """Get detailed file type information"""
        try:
            return self.magic.from_file(filepath)
        except:
            return "Unknown"

    def analyze_content(self, filepath):
        """Check for suspicious patterns"""
        suspicious_patterns = [
            b'powershell', b'cmd.exe', b'regsvr32',
            b'Scripting.FileSystemObject', b'WScript.Shell'
        ]
        
        try:
            with open(filepath, 'rb') as f:
                content = f.read(4096)  # First 4KB only
                return {
                    'is_suspicious': any(pattern in content for pattern in suspicious_patterns),
                    'patterns_found': [p.decode() for p in suspicious_patterns if p in content]
                }
        except:
            return {'is_suspicious': False, 'patterns_found': []}