import subprocess
import os
import time
import sys
import threading
import re
import json
import requests
import shutil
from datetime import datetime
from pathlib import Path
import uuid
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from tkinter.font import Font
import tkinter.font as tkFont
from threading import Thread
import queue
import random
import psutil
from collections import deque
from enum import Enum

# ========== 1. إعداد متغيرات API ==========
# NOTE: Replace these placeholder API keys with your actual OpenRouter API keys
# Get your keys from: https://openrouter.ai/keys
API_KEYS = [
    "API_KEY_1",
    "API_KEY_2",
    "API_KEY_3"
]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek-coder"
active_key_index = 0

# ========== 2. تقسيم الأدوات ==========
RECON = [
    "nmap", "masscan", "amass", "sublist3r", "theHarvester", "whatweb", "wafw00f", "dnsenum", "dnsrecon", "fierce"
]
ENUM = [
    "enum4linux", "nbtscan", "smbclient", "crackmapexec", "smbmap", "rpcclient"
]
DIR_ENUM = [
    "dirb", "dirsearch", "ffuf", "gobuster", "wfuzz"
]
VULN = [
    "nikto", "wpscan", "joomscan", "droopescan", "sqlmap", "bbqsql", "sqlninja", "jexboss", "xsser", "arachni",
    "wapiti", "zaproxy", "skipfish", "nuclei"
]
EXPLOIT = [
    "hydra", "medusa", "patator", "ncrack", "john", "hashcat", "metasploit", "msfvenom", "routersploit", "searchsploit"
]
ALL_TOOLS = RECON + ENUM + DIR_ENUM + VULN + EXPLOIT

# Tool resource profiles (CPU%, RAM MB, estimated duration seconds)
TOOL_RESOURCES = {
    "nmap": {"cpu": 30, "ram": 100, "duration": 120, "priority": 1},
    "masscan": {"cpu": 80, "ram": 150, "duration": 300, "priority": 1},
    "amass": {"cpu": 40, "ram": 200, "duration": 180, "priority": 2},
    "sublist3r": {"cpu": 20, "ram": 80, "duration": 60, "priority": 2},
    "theHarvester": {"cpu": 15, "ram": 70, "duration": 90, "priority": 3},
    "whatweb": {"cpu": 10, "ram": 50, "duration": 30, "priority": 3},
    "wafw00f": {"cpu": 10, "ram": 40, "duration": 20, "priority": 3},
    "dnsenum": {"cpu": 15, "ram": 60, "duration": 45, "priority": 2},
    "dnsrecon": {"cpu": 20, "ram": 80, "duration": 60, "priority": 2},
    "fierce": {"cpu": 15, "ram": 60, "duration": 50, "priority": 3},
    "nikto": {"cpu": 25, "ram": 100, "duration": 180, "priority": 2},
    "wpscan": {"cpu": 20, "ram": 90, "duration": 120, "priority": 2},
    "sqlmap": {"cpu": 30, "ram": 120, "duration": 300, "priority": 1},
    "nuclei": {"cpu": 40, "ram": 150, "duration": 120, "priority": 1},
    "dirb": {"cpu": 20, "ram": 70, "duration": 180, "priority": 2},
    "dirsearch": {"cpu": 25, "ram": 80, "duration": 150, "priority": 2},
    "ffuf": {"cpu": 30, "ram": 100, "duration": 120, "priority": 2},
    "gobuster": {"cpu": 25, "ram": 90, "duration": 100, "priority": 2},
    "wfuzz": {"cpu": 25, "ram": 85, "duration": 110, "priority": 2},
    "hydra": {"cpu": 50, "ram": 120, "duration": 600, "priority": 1},
    "metasploit": {"cpu": 40, "ram": 300, "duration": 180, "priority": 1},
    # Add default for unknown tools
    "default": {"cpu": 20, "ram": 80, "duration": 60, "priority": 3}
}