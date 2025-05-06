import os
import hashlib
from datetime import datetime
import magic
from PyQt5.QtCore import QObject, pyqtSignal
from database import db_manager
from config import MONITORED_EXTENSIONS, SUSPICIOUS_KEYWORDS

class FileAnalyzer(QObject):
    analysis_complete = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.current_analysis = []
        
    def analyze_usb_files(self, usb_path, usb_serial):
        """Analyze all files on a USB device"""
        self.current_analysis = []
        
        if not os.path.exists(usb_path):
            self.analysis_complete.emit([])
            return
            
        # Walk through all files on the USB
        for root, dirs, files in os.walk(usb_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, usb_path)
                
                try:
                    # Skip system files and hidden files
                    if file.startswith('.'):
                        continue
                        
                    # Get file info
                    file_size = os.path.getsize(file_path)
                    file_size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024**2 else f"{file_size / (1024**2):.2f} MB"
                    
                    # Calculate hashes
                    file_hash_md5 = self._calculate_file_hash(file_path, 'md5')
                    file_hash_sha256 = self._calculate_file_hash(file_path, 'sha256')
                    
                    # Check if file is suspicious
                    is_suspicious = self._check_file_suspicious(file_path, relative_path)
                    
                    # Add to analysis results
                    file_info = {
                        'file_path': relative_path,
                        'file_size': file_size_str,
                        'hash_md5': file_hash_md5,
                        'hash_sha256': file_hash_sha256,
                        'is_suspicious': is_suspicious,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    self.current_analysis.append(file_info)
                    
                    # Save to database
                    db_manager.insert_file_transfer_event({
                        'event_type': 'ANALYZED',
                        'file_path': relative_path,
                        'usb_serial': usb_serial,
                        'timestamp': file_info['timestamp'],
                        'file_hash_md5': file_hash_md5,
                        'file_hash_sha256': file_hash_sha256,
                        'file_size': file_size_str,
                        'is_suspicious': is_suspicious
                    })
                    
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {str(e)}")
        
        self.analysis_complete.emit(self.current_analysis)
        
    def _calculate_file_hash(self, file_path, algorithm='sha256'):
        """Calculate file hash using specified algorithm"""
        hash_func = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {str(e)}")
            return "Error"

    def _check_file_suspicious(self, file_path, relative_path):
        """Check if a file might be suspicious"""
        try:
            # Check file extension
            _, ext = os.path.splitext(file_path)
            if ext.lower() in MONITORED_EXTENSIONS:
                return True
                
            # Check filename for suspicious keywords
            filename = os.path.basename(file_path).lower()
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword in filename:
                    return True
                    
            # Check file content type
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            if 'executable' in file_type or 'dll' in file_type:
                return True
                
            return False
        except:
            return False