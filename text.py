def string_to_ascii(s):
    ascii_vals = []
    for c in s:
        ascii_val = ord(c)
        ascii_vals.append(ascii_val)
    return ascii_vals

text = "hello"
ascii_vals = string_to_ascii(text)
print(ascii_vals) # Output: [104, 101, 108, 108, 111]

def ascii_to_string(ascii_vals):
    text = ""
    for val in ascii_vals:
        char = chr(val)
        text += char
    return text

ascii_vals = [104, 101, 108, 108, 111]
text = ascii_to_string(ascii_vals)
print(text) # Output: hello
