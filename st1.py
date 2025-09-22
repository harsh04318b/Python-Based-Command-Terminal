import os
import shutil
import streamlit as st

# --- Command functions ---
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

# --- Streamlit App ---
st.set_page_config(page_title="Streamlit Terminal", layout="wide")

st.title("💻 Streamlit Terminal Emulator")

# Store command history in session state
if "history" not in st.session_state:
    st.session_state.history = []

commands = {
    "ls": ls,
    "cd": cd,
    "pwd": pwd,
    "mkdir": mkdir,
    "rm": rm
}

# Input box for command
command = st.text_input(f"{os.getcwd()} $", key="command_input")

if command:
    parts = command.split()
    cmd = parts[0]
    args = parts[1:]

    if cmd.lower() in ["exit", "quit"]:
        st.session_state.history.append(f"{os.getcwd()} $ {command}\nExiting terminal.")
    elif cmd in commands:
        output = commands[cmd](args)
        if output:
            st.session_state.history.append(f"{os.getcwd()} $ {command}\n{output}")
        else:
            st.session_state.history.append(f"{os.getcwd()} $ {command}")
    else:
        st.session_state.history.append(f"{os.getcwd()} $ {command}\n{cmd}: command not found")

    # Clear input after running
    st.session_state.command_input = ""

# Display terminal output (history)
st.text_area("Terminal Output", "\n".join(st.session_state.history), height=400)
