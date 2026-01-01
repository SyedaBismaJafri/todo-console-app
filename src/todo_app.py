#!/usr/bin/env python3
"""
Todo Console Application
A simple in-memory todo application with a professional UI using Rich library.
This is a legacy entry point. Use main.py for the new architecture.
"""

from manager import ApplicationManager


def main():
    """Main entry point for the application."""
    app_manager = ApplicationManager()
    app_manager.start()


if __name__ == "__main__":
    main()