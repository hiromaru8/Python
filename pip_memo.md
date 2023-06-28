#pipのメモ
py -m pip list
Package      Version
------------ -------
cffi         1.15.1
cryptography 41.0.1
numpy        1.25.0
pip          23.1.2
pycparser    2.21
setuptools   65.5.0

#py -m pip install cryptography
Collecting cryptography
  Downloading cryptography-41.0.1-cp37-abi3-win_amd64.whl (2.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.6/2.6 MB 13.0 MB/s eta 0:00:00
Collecting cffi>=1.12 (from cryptography)
  Downloading cffi-1.15.1-cp311-cp311-win_amd64.whl (179 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 179.0/179.0 kB 11.3 MB/s eta 0:00:00
Collecting pycparser (from cffi>=1.12->cryptography)
  Downloading pycparser-2.21-py2.py3-none-any.whl (118 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 118.7/118.7 kB 6.8 MB/s eta 0:00:00
Installing collected packages: pycparser, cffi, cryptography
Successfully installed cffi-1.15.1 cryptography-41.0.1 pycparser-2.21
