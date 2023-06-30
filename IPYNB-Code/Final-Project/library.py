#TODO : list of modules
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
import os
import joblib

import librosa
import librosa.display
import IPython.display as ipd
from IPython.core.display import display
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt

import seaborn as sns
import streamlit as st
import base64
from threading import Thread
import time

from sklearn.preprocessing import MinMaxScaler

BASE = Path(__file__).parent.parent.parent
PATH = Path(__file__).parent
IMGDIR = PATH / 'gambar_kelompok'
DDIR = PATH / 'dataset'
TMPDIR = PATH / 'tmp'