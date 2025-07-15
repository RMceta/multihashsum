import hashlib
import argparse
import os
from rich.progress import Progress
from colorama import init, Fore

init()


def hash_string(x):    
    md5 = hashlib.md5(x).hexdigest()
    sha256 = hashlib.sha256(x).hexdigest()
    sha512 = hashlib.sha512(x).hexdigest()
    sha384 = hashlib.sha384(x).hexdigest()
    sha1 = hashlib.sha1(x).hexdigest()
    output(md5, sha256, sha512, sha384, sha1)      


def hash_file(path):
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    sha384 = hashlib.sha384()
    sha1 = hashlib.sha1()
    total_size = os.path.getsize(path)

    with Progress() as progress:
        task = progress.add_task("[cyan][!] Calculando hashes...", total=total_size)
        with open(path, "rb") as f:
            while chunk := f.read(8 * 1024 * 1024):  # 8 MB
                md5.update(chunk)
                sha256.update(chunk)
                sha512.update(chunk)
                sha384.update(chunk)
                sha1.update(chunk)
                progress.update(task, advance=len(chunk))

    output(
        md5.hexdigest(),
        sha256.hexdigest(),
        sha512.hexdigest(),
        sha384.hexdigest(),
        sha1.hexdigest()
    )


def output(md5, sha256, sha512, sha384, sha1):
    print(Fore.BLUE + f"\n\n[ MD5 ]", Fore.WHITE + f" [ {md5} ]",
          Fore.BLUE + f"\n\n[ SHA256 ]", Fore.WHITE + f"[ {sha256} ]",
          Fore.BLUE + f"\n\n[ SHA512 ]", Fore.WHITE + f"[ {sha512} ]",
          Fore.BLUE + f"\n\n[ SHA384 ]", Fore.WHITE + f" [ {sha384} ]",
          Fore.BLUE + f"\n\n[ SHA1 ]", Fore.WHITE + f" [ {sha1} ]\n\n")


def main():
    parser = argparse.ArgumentParser(description='Herramienta de línea de comandos para calcular hashes (MD5, SHA1, SHA256, SHA384, SHA512) de cadenas de texto o archivos. Ideal para verificar integridad')
    parser.add_argument('-s', '--string', type=str)
    parser.add_argument('-f', '--file')
    args = parser.parse_args()

    if args.string:
        string_input = args.string.encode()
        hash_string(string_input)
    elif args.file:
        hash_file(args.file)
    else:
        print(Fore.RED + "[!] usage: multihashsum -h")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Saliendo...")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {e}")
