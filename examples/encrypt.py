import textwrap
import zymkey


def main():
    text = "Here is a text to encrypt."
    pt = bytearray(text, "ascii")
    #output = textwrap.fill(''.join('{:02x}'.format(c) for c in pt))
    output = textwrap.fill(' '.join('{:d}'.format(c) for c in pt))
    print("Before encrypting:\n" + output)

    ct = zymkey.client.lock(pt)
    #output = textwrap.fill(''.join('{:02x}'.format(c) for c in ct))
    output = textwrap.fill(' '.join('{:d}'.format(c) for c in ct))
    print("\nAfter encrypting:\n" + output)
    
    dt = zymkey.client.unlock(ct)
    retrieved_str = dt.decode("ascii")
    print("Decrypted text:" + retrieved_str)
    

if __name__ == '__main__':
    main()
