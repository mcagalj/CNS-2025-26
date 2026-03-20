# Simplified pseudocode-style server (essential logic only)

# ===== XOR Cipher =====
def xor_cipher(key: bytes, message: bytes) -> bytes:
    keystream = key * (len(message) // len(key)) + key[:len(message) % len(key)]
    return bytes(k ^ m for k, m in zip(keystream, message))

# ===== Server Setup =====
# The KEY is derived once at startup and reused for ALL encryptions
KEY = derive_key(...)

# The challenge ciphertext contains the flag
challenge_text = f"{some_text} - {flag}"
CHALLENGE_CIPHERTEXT = xor_cipher(KEY, challenge_text.encode('ascii'))

# ===== API Endpoints =====

# POST "/" — encrypts user-supplied hex-encoded plaintext with the SAME key
# Request:  { "plaintext": "<hex-encoded plaintext>" }
# Response: { "ciphertext": "<hex-encoded ciphertext>" }
@app.post("/")
def encrypt_plaintext(plaintext):
    plaintext_bytes = bytes.fromhex(plaintext)
    ciphertext = xor_cipher(KEY, plaintext_bytes)
    return ciphertext.hex()

# GET "/challenge" — returns the encrypted challenge (contains the flag)
# Response: { "ciphertext": "<hex-encoded ciphertext>" }
@app.get("/challenge")
def get_challenge():
    return CHALLENGE_CIPHERTEXT.hex()
