#!/usr/bin/env python3
"""Decode a signed .shortcut file to XML.

Usage:
    python3 decode_shortcut.py INPUT.shortcut OUTPUT.xml

The script handles:
1. Extracting the signing certificate's public key from the AEA1 auth plist
2. Decrypting the Apple Archive with aea(1)
3. Extracting the embedded bplist and converting to XML via plistlib
"""

import struct
import plistlib
import subprocess
import sys
import os
import tempfile


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} INPUT.shortcut OUTPUT.xml", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_xml = sys.argv[2]

    with open(input_file, 'rb') as f:
        data = f.read()

    if data[:4] != b'AEA1':
        print("Error: Not a valid AEA1 shortcut file", file=sys.stderr)
        sys.exit(1)

    # --- Step 1: Extract signing certificate public key ---
    plist_len = struct.unpack('<I', data[8:12])[0]
    auth_plist = plistlib.loads(data[12:12 + plist_len])
    leaf_cert = auth_plist['SigningCertificateChain'][0]

    cert_path = os.path.join(tempfile.gettempdir(), 'signing_cert.der')
    pubkey_path = os.path.join(tempfile.gettempdir(), 'signing_pub.pem')
    decoded_path = os.path.join(tempfile.gettempdir(), 'decoded.bin')

    with open(cert_path, 'wb') as f:
        f.write(leaf_cert)

    subprocess.run([
        'openssl', 'x509', '-inform', 'DER', '-in', cert_path,
        '-pubkey', '-noout', '-out', pubkey_path
    ], check=True)

    # --- Step 2: Decrypt the Apple Archive ---
    subprocess.run([
        'aea', 'decrypt', '-profile', '0', '-sign-pub', pubkey_path,
        '-i', input_file, '-o', decoded_path
    ], check=True)

    # --- Step 3: Extract bplist and convert to XML ---
    with open(decoded_path, 'rb') as f:
        decoded = f.read()

    idx = decoded.find(b'bplist')
    if idx == -1:
        print("Error: No bplist found in decoded archive", file=sys.stderr)
        sys.exit(1)

    plist = plistlib.loads(decoded[idx:])
    xml = plistlib.dumps(plist, fmt=plistlib.FMT_XML).decode('utf-8')

    with open(output_xml, 'w') as f:
        f.write(xml)

    # Clean up temp files
    for p in [cert_path, pubkey_path, decoded_path]:
        try:
            os.unlink(p)
        except OSError:
            pass

    print(f"Decoded to {output_xml} ({len(xml)} bytes)")


if __name__ == '__main__':
    main()
