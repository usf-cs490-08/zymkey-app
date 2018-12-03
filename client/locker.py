import argparse
import zymkey

def get_args():
    ''' Argument parser '''
    parser = argparse.ArgumentParser(description='Locker and unlocker')
    parser.add_argument('data')

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-l', '--lock', action='store_true', help='lock data')
    mode.add_argument('-u', '--unlock', action='store_true', help='unlock data')
    
    return parser.parse_args()

def main():
    args = get_args()
    print(args.data)

    if args.lock:
        f = open(args.data, 'a+b')
        src = bytearray(f.read())
        f.close()
        f = open(args.data, 'wb')
        dst = zymkey.client.lock(src)
        print(type(dst))
        f.write(dst)
        f.close()
    elif args.unlock:
        f = open(args.data, 'rb')
        src = f.read()
        print(type(src))
        f.close()
        dst = zymkey.client.unlock(src)
        print(dst)

if __name__ == '__main__':
    main()
