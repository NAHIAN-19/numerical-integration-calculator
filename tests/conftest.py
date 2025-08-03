import sys, os
# Add project root to sys.path so io_layer (and core, gui, etc.) can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))