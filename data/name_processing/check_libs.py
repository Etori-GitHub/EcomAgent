import sys
try:
    import requests
    print("requests is available")
except ImportError:
    print("requests is NOT available")
    
try:
    import bs4
    print("beautifulsoup4 is available")
except ImportError:
    print("beautifulsoup4 is NOT available")