def encrypt_char(c, shift1, shift2):
    if 'a' <= c <= 'z':
        if 'a' <= c <= 'm':
            shift = shift1 * shift2
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        else:
            shift = shift1 + shift2
            return chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
    elif 'A' <= c <= 'Z':
        if 'A' <= c <= 'M':
            shift = shift1
            return chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        else:
            shift = shift2 ** 2
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    else:
        return c


def decrypt_char(c, shift1, shift2, original_c):
    if 'a' <= original_c <= 'z':
        if 'a' <= original_c <= 'm':
            shift = shift1 * shift2
            return chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
        else:
            shift = shift1 + shift2
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    elif 'A' <= original_c <= 'Z':
        if 'A' <= original_c <= 'M':
            shift = shift1
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        else:
            shift = shift2 ** 2
            return chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
    else:
        return c


def encrypt_text(text, shift1, shift2):
    result = ""
    for c in text:
        result += encrypt_char(c, shift1, shift2)
    return result

def decrypt_text(encrypted_text, original_text, shift1, shift2):
    result = ""
    for i in range(len(encrypted_text)):
        c = encrypted_text[i]
        orig = original_text[i]
        result += decrypt_char(c, shift1, shift2, orig)
    return result


def check_correctness(original_text, decrypted_text):
    return original_text == decrypted_text


def main():
    shift1 = int(input("Insert a value for Shift1: "))
    shift2 = int(input("Insert a value for Shift2: "))

    with open("raw_text.txt", "r", encoding="utf-8") as file:
        raw_text = file.read()

    encrypted = encrypt_text(raw_text, shift1, shift2)
    with open("encrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(encrypted)
        print("Excrypted text: ",encrypted)
        print("\n\n<---------------------------------------------->")
        print("Encryption complete. Encrypted text saved to 'encrypted_text.txt'.")
        print("<---------------------------------------------->")

    # Use original raw_text to guide the decryption
    decrypted = decrypt_text(encrypted, raw_text, shift1, shift2)

    if check_correctness(raw_text, decrypted):
        print("\n\nDecrypted Text: ",decrypted)
        print("Decryption verified successfully!")
    else:
        print("Decryption failed. The texts do not match.")


if __name__ == "__main__":
    main()
