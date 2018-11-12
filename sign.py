import argparse
import textwrap
import zymkey

def get_args():
    ''' Argument parser '''
    parser = argparse.ArgumentParser(description='Generate keys')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-s', '--sign', action='store_true', help='sign a message')
    mode.add_argument('-v', '--verify', action='store_true', help='verify a message')
    parser.add_argument('-m', '--message', required=True, help='message to sign or verify')
    #parser.add_argument('-k', '--key', required=True, help='key used to sign or verify')
    parser.add_argument('-S', '--signature', required=True, help='signature used to verify message')
    return parser.parse_args()

def sign_msg(msg, filename):
    sig = zymkey.client.sign(msg)
    output = textwrap.fill(''.join('{:02x}'.format(c) for c in sig))
    print(output)
    f_out = open(filename, 'w+b')
    f_out.write(sig)
    f_out.close()

def verify_msg(msg, filename):
    f_in = open(filename, 'rb')
    data = bytearray(f_in.read())
    output = textwrap.fill(''.join('{:02x}'.format(c) for c in data))
    print(output)
    f_in.close()
    res = zymkey.client.verify(msg, data)
    print(res)

def main():
    args = get_args()
    print(args.message)
    if (args.sign):
        print("Sign message")
        sign_msg(args.message, args.signature)
    elif (args.verify):
        print("Verfiy message")
        verify_msg(args.message, args.signature)


if __name__ == '__main__':
    main()
'''
msg = 'Hello, Bob. --Alice'

sig = zymkey.client.sign(msg)
output = textwrap.fill(''.join('{:02x}'.format(c) for c in sig))
print(output)
f_out = open("signature", 'w+b')
f_out.write(sig)
f_out.close()

f_in = open("signature", 'rb')
data = bytearray(f_in.read())
output = textwrap.fill(''.join('{:02x}'.format(c) for c in data))
print(output)
f_in.close()
res = zymkey.client.verify(msg, data)
print(res)


#output = textwrap.fill(''.join('{:02x}'.format(c) for c in sig))
#print(output)

#res = zymkey.client.verify(msg, sig)
#print(res)
'''
