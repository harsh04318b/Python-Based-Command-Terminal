import os
import shutil

def ls(args):
    path = args[0] if args else '.'
    try:
        files = os.listdir(path)
        return '\n'.join(files)
    except FileNotFoundError:
        return f"ls: cannot access '{path}': No such file or directory"

def cd(args):
    if not args:
        return "cd: missing argument"
    try:
        os.chdir(args[0])
        return ""
    except FileNotFoundError:
        return f"cd: {args[0]}: No such file or directory"
    except NotADirectoryError:
        return f"cd: {args[0]}: Not a directory"

def pwd(args):
    return os.getcwd()

def mkdir(args):
    if not args:
        return "mkdir: missing argument"
    try:
        os.mkdir(args[0])
        return ""
    except FileExistsError:
        return f"mkdir: cannot create directory '{args[0]}': File exists"

def rm(args):
    if not args:
        return "rm: missing argument"
    target = args[0]
    try:
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        return ""
    except FileNotFoundError:
        return f"rm: cannot remove '{target}': No such file or directory"

def main():
    commands = {
        "ls": ls,
        "cd": cd,
        "pwd": pwd,
        "mkdir": mkdir,
        "rm": rm
    }

    while True:
        try:
            inp = input(f"{os.getcwd()} $ ").strip()
            if not inp:
                continue
            if inp.lower() in ['exit', 'quit']:
                break

            parts = inp.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in commands:
                output = commands[cmd](args)
                if output:
                    print(output)
            else:
                print(f"{cmd}: command not found")

        except KeyboardInterrupt:
            print("\nExiting terminal.")
            break

if __name__ == "__main__":
    main()
