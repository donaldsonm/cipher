from flask import Flask, render_template, jsonify, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/affine", methods=["GET", "POST"])
def affine():
    return render_template("affine.html")


@app.route("/affine/encrypt", methods=["POST"])
def encrypt_affine():

    # Check for errors like if fields are blank
    if not request.form.get("text"):
        return jsonify({"success": "error1"})
    if not request.form.get("a"):
        return jsonify({"success": "error2"})
    if not request.form.get("b"):
        return jsonify({"success": "error3"})
    if int(request.form.get("a")) % 2 == 0 or int(request.form.get("a")) % 13 == 0:
        return jsonify({"success": "error4"})


    plaintext = request.form.get("text")
    a = int(request.form.get("a"))
    b = int(request.form.get("b"))

    ciphertext = ""

    # Transform character and individually add it into empty string
    for i in range(len(plaintext)):

        asciichar = ord(plaintext[i])

        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                ciphertext += chr(((((asciichar - 65) * a) + b) % 26) + 65)

            else:
                ciphertext += chr(((((asciichar - 97) * a) + b) % 26) + 97)

        else:
            ciphertext += plaintext[i]

    return jsonify({"success": "success", "ciphertext": ciphertext})

@app.route("/affine/decrypt", methods=["POST"])
def decrypt_affine():

    # Check for errors like if fields are blank
    if not request.form.get("text"):
        return jsonify({"success": "error1"})
    if not request.form.get("a"):
        return jsonify({"success": "error2"})
    if not request.form.get("b"):
        return jsonify({"success": "error3"})
    if int(request.form.get("a")) % 2 == 0 or int(request.form.get("a")) % 13 == 0:
        return jsonify({"success": "error4"})


    ciphertext = request.form.get("text")
    a = int(request.form.get("a"))
    b = int(request.form.get("b"))

    plaintext = ""

    # Transform character and individually add it into empty string
    for k in range(len(ciphertext)):

        asciichar = ord(ciphertext[k])

        if ciphertext[k].isalpha():
            if ciphertext[k].isupper():
                plaintext += chr(((modinv(a, 26) * (asciichar - 65 - b)) % 26) + 65)

            else:
                plaintext += chr(((modinv(a, 26) * (asciichar - 97 - b)) % 26) + 97)


        else:
            plaintext += ciphertext[k]

    return jsonify({"success": "success", "plaintext": plaintext})


@app.route("/caesar", methods=["GET", "POST"])
def caesar():
    return render_template("caesar.html")


@app.route("/caesar/encrypt", methods=["POST"])
def encrypt_caesar():

    # Check for errors like if fields are blank
    if not request.form.get("text"):
        return jsonify({"success": "error1"})
    if not request.form.get("shift"):
        return jsonify({"success": "error2"})

    plaintext = request.form.get("text")
    shift = int(request.form.get("shift"))

    ciphertext = ""

    # Transform character and individually add it into empty string
    for i in range(len(plaintext)):

        asciichar = ord(plaintext[i])

        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                ciphertext += chr(((asciichar - 65 + shift) % 26) + 65)

            else:
                ciphertext += chr(((asciichar - 97 + shift) % 26) + 97)

        else:
            ciphertext += plaintext[i]

    return jsonify({"success": "success", "ciphertext": ciphertext})


@app.route("/caesar/decrypt", methods=["POST"])
def decrypt_caesar():

    # Check for errors like if fields are blank
    if not request.form.get("text"):
        return jsonify({"success": "error1"})
    if not request.form.get("shift"):
        return jsonify({"success": "error2"})

    ciphertext = request.form.get("text")
    shift = int(request.form.get("shift"))

    plaintext = ""

    # Transform character and individually add it into empty string
    for k in range(len(ciphertext)):

        asciichar = ord(ciphertext[k])

        if ciphertext[k].isalpha():
            if ciphertext[k].isupper():
                plaintext += chr(((asciichar - 65 - shift) % 26) + 65)
            else:
                plaintext += chr(((asciichar - 97 - shift) % 26) + 97)
        else:
            plaintext += ciphertext[k]

    return jsonify({"success": "success", "plaintext": plaintext})


@app.route("/vigenere", methods=["GET", "POST"])
def vigenere():
    return render_template("vigenere.html")

@app.route("/vigenere/encrypt", methods=["POST"])
def encrypt_vigenere():

    # Check for errors like if fields are blank
    if not request.form.get("text"):
        return jsonify({"success": "error1"})
    if not request.form.get("key"):
        return jsonify({"success": "error2"})
    if not request.form.get("key").isalpha():
        return jsonify({"success": "error3"})

    plaintext = request.form.get("text")
    key = request.form.get("key").upper()
    counter = 0

    ciphertext = ""

    # Transform character and individually add it into empty string
    for i in range(len(plaintext)):

        asciichar = ord(plaintext[i])

        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                ciphertext += chr(((asciichar - 65 + (ord(key[counter % len(key)]) - 65)) % 26) + 65)
                counter += 1

            else:
                ciphertext += chr(((asciichar - 97 + (ord(key[counter % len(key)]) - 65)) % 26) + 97)
                counter += 1
        else:
            ciphertext += plaintext[i]

    return jsonify({"success": "success", "ciphertext": ciphertext})


@app.route("/vigenere/decrypt", methods=["POST"])
def decrypt_vigenere():

    # Check for errors like if fields are blank
    if not request.form.get("text"):
        return jsonify({"success": "error1"})
    if not request.form.get("key"):
        return jsonify({"success": "error2"})
    if not request.form.get("key").isalpha():
        return jsonify({"success": "error3"})

    ciphertext = request.form.get("text")
    key = request.form.get("key").upper()
    counter = 0

    plaintext = ""

    # Transform character and individually add it into empty string
    for k in range(len(ciphertext)):

        asciichar = ord(ciphertext[k])

        if ciphertext[k].isalpha():
            if ciphertext[k].isupper():
                plaintext += chr(((asciichar - 65 - (ord(key[counter % len(key)]) - 65)) % 26) + 65)
                counter += 1

            else:
                plaintext += chr(((asciichar - 97 - (ord(key[counter % len(key)]) - 65)) % 26) + 97)
                counter += 1
        else:
            plaintext += ciphertext[k]

    return jsonify({"success": "success", "plaintext": plaintext})


# Function taken from https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
# to help with the decryption of the affine cipher
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m