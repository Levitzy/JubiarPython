#!/usr/bin/env python3
import os,time,zlib,base64
from time import sleep
time.sleep(0.2)
from sys import stdin, stdout, stderr
from argparse import ArgumentParser
from pathlib import Path
from base64 import b64decode
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad

print("""\033[1;32;40m
╔═══╗╔═══╗╔╗──╔╗╔═══╗╔════╗╔═══╗────╔════╗╔═══╗╔═══╗╔╗───╔═══╗
║╔═╗║║╔═╗║║╚╗╔╝║║╔═╗║║╔╗╔╗║║╔═╗║────║╔╗╔╗║║╔═╗║║╔═╗║║║───║╔═╗║
║║─╚╝║╚═╝║╚╗╚╝╔╝║╚═╝║╚╝║║╚╝║║─║║────╚╝║║╚╝║║─║║║║─║║║║───║╚══╗
║║─╔╗║╔╗╔╝─╚╗╔╝─║╔══╝──║║──║║─║║──────║║──║║─║║║║─║║║║─╔╗╚══╗║
║╚═╝║║║║╚╗──║║──║║─────║║──║╚═╝║──────║║──║╚═╝║║╚═╝║║╚═╝║║╚═╝║
╚═══╝╚╝╚═╝──╚╝──╚╝─────╚╝──╚═══╝──────╚╝──╚═══╝╚═══╝╚═══╝╚═══╝

• Developers: @DvlJs - @BOOS_TOOLS - @Dylan_AR 
• How to use: python decrypt.py /sdcard/Download/file.tnl
• Join to channel: @CryptoTeamTools\n\n
""")

DEFAULT_FILE_EXTENSION = '.tmt'

PASSWORDS = {
    '.bdi': b'@technore 2022',
    '.tut': b'fubvx788b46v',
    '.tmt': b'$$$@mfube11!!_$$))012b4u',   #✓
    '.sks': b'dyv35224nossas!!',
    '.ziv': b'fubvx788b46v', 
    '.pb':  b'Cw1G6s0K8fJVKZmhSLZLw3L1R3ncNJ2e',
    '.temt': b'fubvx788B4mev',
    '.tsn': b'thirdy1996624',   #✓
    '.etun': b'dyv35224nossas!!',
    '.pxp': b'bKps&92&',
    '.ace': b'Ed',   #✓
    '.tsd': b'waiting',
    '.ost': b'gggggg',
    '.wt': b'fuMnrztkzbQ',   #✓
    '.tnl': b'A^ST^f6ASG6AS5asd',   #✓
    '.fks': b'fubvx788b46v',
    '.gv': b'Ed',
    '.act': b'fubvx788b46v',   #✓
    '.cnet': b'cnt',   #✓
    '.gibs': b'Ed',   #✓
    '.dvd': b'dyv35224nossas!!',   #✓
    '.ftp': b'Version6',   #✓ #old
    '.fthp': b'furious0982',   #✓ #new
    '.jph': b'fubvx788b46v',   #✓
    '.xsks': b'c7-YOcjyk1k',
    '.ht': b'error',
    '.ssi': b'Jicv',
    '.kt': b'kt',
    '.dvs': b'mtscrypt',
    '.fnet': b'62756C6F6B',   #✓
    '.mc': b'fubvx788b46v',   #✓
    '.hub': b'trfre699g79r',   #✓
    '.grd': b'fubvx788b46v',
    '.hta': b'Ed',   #✓
    '.eug': b'fubvx788b46v',   #✓
    '.sds': b'rdovx202b46v',
    '.htp': b'chanika acid, gimsara htpcag!!',
    '.bbb': b'xcode788b46z',
    '.ccc': b'fubgf777gf6',
    '.ddd': b'fubvx788b46vcatsn',
    '.eee': b'dyv35182!',
    '.cln': b'fubvx788b46v',   #✓
    '.cyh': b'dyv35182!',   #✓
    '.agn': b'cigfhfghdf665557',
    '.Tcv2': b'fubvx788b46v',
    '.NT': b'0x0',
    '.ai': b'Ed',
    'cks': b'2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx',
    '.sksrv': b'y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY',
    '.garuda': b'fubvx788b46v',
    '.tpp': b'Ed',
    '.sky': b'fubux788b46v',
    '.skyp': b'\u02bb\u02bd\u1d35\u02c6\u02c8\u02c6\u2071\u02cb.milQP\u05d9\u02d1\ufe73\u2071\uff9e\u02c6\u1d4e\u02bd\u02bc\u02bc\u02c8\u05d9\ufe76\uff9e\u05d9\u1d54\uff9e\u02ceswtIX',
    '.max': b'Ed',
}

def error(error_msg = 'Corrupted/unsupported file.'):
    stderr.write(f'\033[41m\033[30m X \033[0m {error_msg}\n')
    stderr.flush()

    exit(1)

def warn(warn_msg):
    stderr.write(f'\033[43m\033[30m ! \033[0m {warn_msg}\n')
    stderr.flush()

def ask(prompt):
    stderr.write(f'\033[104m\033[30m ? \033[0m {prompt} ')
    stderr.flush()

    return input()

def human_bool_to_bool(human_bool):
    return 'y' in human_bool

def main():
    # parse arguments
    parser = ArgumentParser()
    parser.add_argument('file', help='file to decrypt')

    output_args = parser.add_mutually_exclusive_group()
    output_args.add_argument('--output', '-o', help='file to output to')
    output_args.add_argument('--stdout', '-O', action='store_true', help='output to stdout', default=True)

    args = parser.parse_args()
    
    encrypted_contents = open(args.file, 'r').read()

    
    file_ext = Path(args.file).suffix
    
    if file_ext not in PASSWORDS:
        warn(f'Unknown file extension, defaulting to {DEFAULT_FILE_EXTENSION}')
        file_ext = DEFAULT_FILE_EXTENSION

    # split the file
    split_base64_contents = encrypted_contents.split('.')

    #if len(split_base64_contents) != 3:
        #raise ValueError('Unsupported file.')

    split_contents = list(map(b64decode, split_base64_contents))
    #split_contents= encrypted_contents.split('.')
   

    # derive the key
    decryption_key = PBKDF2(PASSWORDS[file_ext], split_contents[0], hmac_hash_module=SHA256)

    # decrypt the file
    cipher = AES.new(decryption_key, AES.MODE_GCM, nonce=split_contents[1])
    decrypted_contents = cipher.decrypt_and_verify(split_contents[2][:-16], split_contents[2][-16:])

    # decide where to write contents
    if args.output:
        output_file_path = Path(args.output)

        # check if the file exists
        if output_file_path.exists() and output_file_path.is_file():
            # check if the user agrees to overwrite it
            if not human_bool_to_bool(ask(f'A file named "{args.output}" already exists. Overwrite it? (y/n)')):
                # if user doesn't, quit
                exit(0)
        
        # write the contents to the file
        output_file = open(output_file_path, 'wb')
        output_file.write(decrypted_contents)
    elif args.stdout:
        # convert the config to UTF-8
        config = decrypted_contents.decode('utf-8','ignore')
        #print(config)
        print("[!] Tools by @DvlJs - @BOOS_TOOLS [!]\n\n")
        sshadd ='';port ='';user='';passw=''
        configdict ={}
        for line in config.split('\n'):
        	if line.startswith('<entry'):
        		line = line.replace('<entry key="','')
        		line = line.replace('</entry','')
        		line = line.split('">')
        		if len(line) >1:
        			configdict[line[0]] = line[1].strip(">")
        			
        		else:
        			configdict[line[0].strip('"/>')]= " ***"
        			
        for k,v in configdict.items():
        	if k in ["sshServer","sshPass","sshUser","sshPort"]:
        		continue
        	else:
        		print("[</>] " +k+" ==> " +v)
        print("[</>] sshAddress ==> "+ configdict["sshServer"]+":"+configdict["sshPort"]+"@"+configdict["sshUser"]+":"+configdict["sshPass"])     	
        print("\n[</>] @CryptoTeamTools [</>]")
        
if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        error(err)
