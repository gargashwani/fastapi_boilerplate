#!/usr/bin/env python3

import click
from pathlib import Path
import os
import secrets
from typing import List
import subprocess
import sys
from fastapi import Depends
from app.cli import app

if __name__ == '__main__':
    app() 