import os, shlex, shutil
try:
    import psutil
except Exception:
    psutil = None

class CommandTerminal:
    def __init__(self, root=None):
        self.cwd = os.path.abspath(root or os.getcwd())

    def _abs(self, path):
        return path if os.path.isabs(path) else os.path.abspath(os.path.join(self.cwd, path))

    def execute(self, line):
        try:
            line = line.strip()
            if not line:
                return ''
            parts = shlex.split(line)
            cmd = parts[0]
            args = parts[1:]

            if cmd == "pwd":
                return self.cwd
            elif cmd == "cd":
                target = args[0] if args else os.path.expanduser("~")
                new = self._abs(target)
                if os.path.isdir(new):
                    self.cwd = new
                    return ""
                else:
                    return f"cd: no such directory: {target}"
            elif cmd == "ls":
                target = self._abs(args[0]) if args else self.cwd
                try:
                    return "\n".join(sorted(os.listdir(target)))
                except Exception as e:
                    return f"ls: {e}"
            elif cmd == "mkdir":
                if not args:
                    return "mkdir: missing operand"
                out_lines = []
                for p in args:
                    p_abs = self._abs(p)
                    try:
                        os.makedirs(p_abs, exist_ok=True)
                    except Exception as e:
                        out_lines.append(f"mkdir: {e}")
                return "\n".join(out_lines)
            elif cmd == "rm":
                if not args:
                    return "rm: missing operand"
                out_lines = []
                for p in args:
                    t = self._abs(p)
                    if os.path.isdir(t):
                        try:
                            shutil.rmtree(t)
                        except Exception as e:
                            out_lines.append(f"rm: {e}")
                    elif os.path.exists(t):
                        try:
                            os.remove(t)
                        except Exception as e:
                            out_lines.append(f"rm: {e}")
                    else:
                        out_lines.append(f"rm: cannot remove '{p}': No such file or directory")
                return "\n".join(out_lines)
            elif cmd == "touch":
                if not args:
                    return "touch: missing operand"
                out_lines = []
                for p in args:
                    try:
                        open(self._abs(p), 'a').close()
                    except Exception as e:
                        out_lines.append(f"touch: {e}")
                return "\n".join(out_lines)
            elif cmd == "cat":
                if not args:
                    return "cat: missing operand"
                parts_out = []
                for p in args:
                    try:
                        with open(self._abs(p),'r',encoding='utf-8') as f:
                            parts_out.append(f.read())
                    except Exception as e:
                        parts_out.append(f"cat: {e}")
                return "\n".join(parts_out)
            elif cmd == "mv":
                if len(args) < 2:
                    return "mv: missing operands"
                try:
                    shutil.move(self._abs(args[0]), self._abs(args[1]))
                    return ""
                except Exception as e:
                    return f"mv: {e}"
            elif cmd == "cp":
                if len(args) < 2:
                    return "cp: missing operands"
                try:
                    src = self._abs(args[0]); dst = self._abs(args[1])
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                    return ""
                except Exception as e:
                    return f"cp: {e}"
            elif cmd == "echo":
                return " ".join(args)
            elif cmd == "sys":
                if not psutil:
                    return "sys: psutil not available"
                return f"CPU: {psutil.cpu_percent(interval=0.2)}% | Mem: {psutil.virtual_memory().percent}%"
            elif cmd == "ps":
                if not psutil:
                    return "ps: psutil not available"
                rows = []
                for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
                    info = p.info
                    rows.append(f"{info['pid']}\t{info['name']}\t{info['cpu_percent']}\t{info['memory_percent']}")
                return "\n".join(rows)
            elif cmd == "help":
                return "Supported: pwd, cd, ls, mkdir, rm, touch, cat, mv, cp, echo, sys, ps, help, exit"
            elif cmd == "exit" or cmd == "quit":
                return "__EXIT__"
            else:
                return f"{cmd}: command not found"
        except Exception as e:
            return f"Error: {e}"
