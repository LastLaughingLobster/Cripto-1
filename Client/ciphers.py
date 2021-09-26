def caesar(text, s):
  encryptedText = ""

  for i in range(len(text)):
    char = text[i]
    # Encrypt uppercase characters in plain text
    
    if (char.isupper()):
      encryptedText += chr((ord(char) + s-65) % 26 + 65)
    # Encrypt lowercase characters in plain text
    else:
      encryptedText += chr((ord(char) + s - 97) % 26 + 97)

  return encryptedText
