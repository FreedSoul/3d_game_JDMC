import sys
import os

# Add project root to path (one level up from src)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main import main

if __name__ == "__main__":
    main()
