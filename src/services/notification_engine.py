"""
Notification Engine
Handles sending desktop notifications using the best available library for Python.
"""

import sys
import os
from typing import Optional


class NotificationSkill:
    """Generic notification handling class for sending desktop alerts."""
    
    def __init__(self):
        """Initialize the notification skill with the best available library."""
        self.notification_lib = self._find_best_notification_library()
    
    def _find_best_notification_library(self):
        """Find and return the best available notification library."""
        # Try different notification libraries in order of preference
        libraries_to_try = [
            ('plyer', self._init_plyer),
            ('win10toast', self._init_win10toast),
            ('plyer_fork', self._init_plyer),
        ]
        
        for lib_name, init_func in libraries_to_try:
            try:
                return init_func()
            except ImportError:
                continue
        
        # If no library is available, return None
        print(f"Warning: No notification library found. Install 'plyer' or 'win10toast' for notifications.")
        return None
    
    def _init_plyer(self):
        """Initialize plyer notification library."""
        from plyer import notification
        return notification
    
    def _init_win10toast(self):
        """Initialize win10toast notification library."""
        from win10toast import ToastNotifier
        return ToastNotifier()
    
    def send_alert(self, title: str, message: str) -> bool:
        """
        Send a desktop notification with the given title and message.
        
        Args:
            title: Title of the notification
            message: Content of the notification
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not self.notification_lib:
            return False
        
        try:
            # Try to send notification using plyer
            if hasattr(self.notification_lib, 'notify'):
                # This is plyer
                self.notification_lib.notify(
                    title=title,
                    message=message,
                    timeout=5  # Notification timeout in seconds
                )
                return True
            elif hasattr(self.notification_lib, 'show_toast'):
                # This is win10toast
                self.notification_lib.show_toast(
                    title=title,
                    msg=message,
                    duration=5,  # Duration in seconds
                    threaded=True  # Run in background thread
                )
                return True
            else:
                # Unknown library type
                return False
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False