import ast
import base64
import importlib
import io
import random
import shutil
import socketserver
import struct
import re
import tarfile
import tempfile
import time
from collections import namedtuple, defaultdict
from copy import deepcopy
from functools import partial, wraps

import nclib
import requests
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from indent2dict import indent2dict
from lxml import etree
from parifinder import parse_pairs
from touchtouch import touch

from .keyevents import key_events
from fabisschomagut import to_rgb_hex, to_rgb_tuple
from normaltext import lookup
from typing import Literal
from punktdict import PunktDict as PunktDict_
from punktdict import dictconfig
import ctypes
import itertools
import os
import platform
import signal
import sys
import subprocess
import threading
from collections import deque
from time import sleep as sleep_
from math import floor
from functools import cache

numberreg = re.compile(r"\[([^,]+),([^,]+)\]\[([^,]+),([^,]+)\]", flags=re.I)

CREATE_NEW_PROCESS_GROUP = 0x00000200
DETACHED_PROCESS = 0x00000008

dictconfig.allow_nested_attribute_creation = False
dictconfig.allow_nested_key_creation = False
dictconfig.convert_all_dicts_recursively = True
from .parsekeyevents import get_event_labels

screenres_reg_cur = re.compile(rb"\bcur=(\d+)x(\d+)\b")
screenres_reg = re.compile(rb"\bcur=(\d+)x(\d+)\b")
from flatten_everything import flatten_everything
from argskwargsmodifierclass import change_args_kwargs

from . import c

clsrgb = namedtuple("XYRGB", ["x", "y", "r", "g", "b"])
refi = re.compile(r"([^,]+),([^,]+)-([^,]+),([^,]+)")


def _parsexmluiauto(tree):
    ellis = {}
    ellis_children = defaultdict(set)
    ellis_parents = defaultdict(set)

    ellis_children_hierachy = defaultdict(set)

    hierachyset = set()
    uniquecounter = 0
    hashcodesonly = {}

    def rec2(t, number):
        nonlocal uniquecounter
        if not hasattr(t, "getchildren"):
            method = t.iter
        else:
            method = t.getchildren
        hierachyset.add(tuple(number))
        hashcode2 = hash(t)
        if hashcode2 not in ellis:
            uniquecounter += 1
            ellis[hashcode2] = {"element": t, "uniquehash": uniquecounter}
            hashcodesonly[hashcode2] = uniquecounter

        for x in method():
            hashcode = hash(x)
            ellis_children[hashcode2].add(hashcode)
            ellis_parents[hashcode].add(hashcode2)
            ellis_children_hierachy[hashcode2].add(tuple([hashcode]))

            if hashcode not in ellis:
                uniquecounter += 1
                ellis[hashcode] = {"element": x, "uniquehash": uniquecounter}
                hashcodesonly[hashcode] = uniquecounter
            if hashcode not in number:
                rec2(x, number + [hashcode])

            else:
                rec2(x, number)

    hashroot = hash(tree)
    hashcodesonly[hashroot] = uniquecounter
    ellis[hashroot] = {"element": tree, "uniquehash": uniquecounter}
    rec2(tree, [hashroot])
    return (
        ellis_children_hierachy,
        hashroot,
        hashcodesonly,
        ellis,
        ellis_parents,
        ellis_children,
    )


def replace_rn_n(text):
    if isinstance(text, bytes):
        return text.replace(b"\r\n", b"\n")
    return [x.replace(b"\r\n", b"\n") for x in text]


re_split_quotes = re.compile(r"(['\"])")
valid_input_devices = Literal[
    "dpad",
    "keyboard",
    "mouse",
    "touchpad",
    "gamepad",
    "touchnavigation",
    "joystick",
    "touchscreen",
    "stylus",
    "trackball",
    "",
]


compiledregex = re.compile(r"^[A-Z]:\\", flags=re.I)

iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    user32 = windll.user32
    kernel32 = windll.kernel32
    GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
    CloseHandle = windll.kernel32.CloseHandle
    GetExitCodeProcess.argtypes = [
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_ulong),
    ]
    CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
    GetExitCodeProcess.restype = ctypes.c_int
    CloseHandle.restype = ctypes.c_int

    GetWindowRect = user32.GetWindowRect
    GetClientRect = user32.GetClientRect
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
else:
    invisibledict = {}


def is_process_alive(pid):
    if re.search(
        b"ProcessId=" + str(pid).encode() + rb"\s*$",
        subprocess.run(
            "wmic process list FULL", capture_output=True, **invisibledict
        ).stdout,
        flags=re.MULTILINE,
    ):
        return True
    return False


def index_all(s, n):
    indototal = 0
    allindex = []

    while True:
        try:
            indno = s[indototal:].index(n)
            indototal += indno + 1
            allindex.append(indototal - 1)
        except ValueError:
            break
    return allindex


@cache
def convert_path_to_short(string):
    if not iswindows:
        return string

    l2 = [q - 1 for q in index_all(s=string, n=":\\")]
    addtostring = []
    try:
        result1 = list_split(l=string, indices_or_sections=l2)
    except Exception:
        return string
    try:
        for string in result1:
            if not compiledregex.search(string):
                addtostring.append(string)
                continue
            activepath = ""
            lastfoundpath = ""
            lastfoundpath_end = 0
            for ini, letter in enumerate(string):
                activepath += letter
                if ini < 3:
                    continue
                if letter.isspace():
                    continue
                if os.path.exists(activepath):
                    lastfoundpath = activepath
                    lastfoundpath_end = ini
            if lastfoundpath:
                addtostring.append(get_short_path_name(lastfoundpath))
                addtostring.append(string[lastfoundpath_end + 1 :])
            else:
                addtostring.append(string)

        return "".join(addtostring)
    except Exception:
        return string


def list_split(l, indices_or_sections):
    Ntotal = len(l)
    try:
        Nsections = len(indices_or_sections) + 1
        div_points = [0] + list(indices_or_sections) + [Ntotal]
    except TypeError:
        Nsections = int(indices_or_sections)
        if Nsections <= 0:
            raise ValueError("number sections must be larger than 0.") from None
        Neach_section, extras = divmod(Ntotal, Nsections)
        section_sizes = (
            [0] + extras * [Neach_section + 1] + (Nsections - extras) * [Neach_section]
        )
        div_points = []
        new_sum = 0
        for i in section_sizes:
            new_sum += i
            div_points.append(new_sum)

    sub_arys = []
    lenar = len(l)
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[i + 1]
        if st >= lenar:
            break
        sub_arys.append((l[st:end]))

    return sub_arys


@cache
def get_short_path_name(long_name):
    try:
        if not iswindows:
            return long_name
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        return long_name


def sleep(secs):
    try:
        if secs == 0:
            return
        maxrange = 50 * secs
        if isinstance(maxrange, float):
            sleeplittle = floor(maxrange)
            sleep_((maxrange - sleeplittle) / 50)
            maxrange = int(sleeplittle)
        if maxrange > 0:
            for _ in range(maxrange):
                sleep_(0.016)

    except KeyboardInterrupt:
        return


def killthread(threadobject):
    # based on https://pypi.org/project/kthread/
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


def index_all(s, n):
    indototal = 0
    allindex = []

    while True:
        try:
            indno = s[indototal:].index(n)
            indototal += indno + 1
            allindex.append(indototal - 1)
        except ValueError:
            break
    return allindex


def send_ctrl_commands(pid, command=0):
    # CTRL_C_EVENT = 0
    # CTRL_BREAK_EVENT = 1
    # CTRL_CLOSE_EVENT = 2
    # CTRL_LOGOFF_EVENT = 3
    # CTRL_SHUTDOWN_EVENT = 4
    if iswindows:
        commandstring = r"""import ctypes, sys; CTRL_C_EVENT, CTRL_BREAK_EVENT, CTRL_CLOSE_EVENT, CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT = 0, 1, 2, 3, 4; kernel32 = ctypes.WinDLL("kernel32", use_last_error=True); (lambda pid, cmdtosend=CTRL_C_EVENT: [kernel32.FreeConsole(), kernel32.AttachConsole(pid), kernel32.SetConsoleCtrlHandler(None, 1), kernel32.GenerateConsoleCtrlEvent(cmdtosend, 0), sys.exit(0) if isinstance(pid, int) else None])(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else None) if __name__ == '__main__' else None"""
        subprocess.Popen(
            [sys.executable, "-c", commandstring, str(pid), str(command)],
            **invisibledict,
        )  # Send Ctrl-C
    else:
        os.kill(pid, signal.SIGINT)


class dequeslice(deque):
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__class__(
                itertools.islice(self, index.start, index.stop, index.step)
            )
        return deque.__getitem__(self, index)


class SubProcInputOutput:
    def __init__(
        self,
        cmd,
        invisible=False,
        print_stdout=True,
        print_stderr=True,
        limit_stdout=None,
        limit_stderr=None,
        limit_stdin=None,
        convert_to_83=True,
        separate_stdout_stderr_with_list=True,
        **kwargs,
    ):
        if convert_to_83 and iswindows:
            newcommand = []
            if isinstance(cmd, (list, tuple)):
                for element in cmd:
                    if os.path.exists(element):
                        newcommand.append(get_short_path_name(element))
                    else:
                        newcommand.append(element)
            elif isinstance(cmd, str):
                convert_path_to_short(cmd)
            cmd = newcommand

        self.cmd = cmd
        self.separate_stdout_with_list = separate_stdout_stderr_with_list
        self.separate_stderr_with_list = separate_stdout_stderr_with_list
        self.lockobject = threading.Lock()
        if self.separate_stdout_with_list:
            self.stdout = dequeslice([[]], maxlen=limit_stdout)
        else:
            self.stdout = dequeslice([], maxlen=limit_stdout)
        if self.separate_stderr_with_list:
            self.stderr = dequeslice([[]], maxlen=limit_stderr)
        else:
            self.stderr = dequeslice([], maxlen=limit_stderr)

        self.stdin = dequeslice([cmd], maxlen=limit_stdin)
        self.print_stdout = print_stdout
        self.print_stderr = print_stderr
        kwargs.update(
            {
                "stdout": subprocess.PIPE,
                "stdin": subprocess.PIPE,
                "stderr": subprocess.PIPE,
            }
        )
        if invisible:
            kwargs.update(invisibledict)
        kwargs.update({"bufsize": 0})
        self.p = subprocess.Popen(cmd, **kwargs)
        self._t_stdout = threading.Thread(target=self._read_stdout)
        self._t_stderr = threading.Thread(target=self._read_stderr)
        self._t_stdout.start()
        self._t_stderr.start()

    def _close_pipes(self, pipe):
        try:
            getattr(self.p, pipe).close()
        except Exception as e:
            sys.stderr.write(f"{e}\n")

    def _close_proc(self):
        try:
            self.p.terminate()
        except Exception as e:
            sys.stderr.write(f"{e}\n")

    def tkill(self):
        if iswindows:
            invi = invisibledict.copy()
            invi.update(
                {
                    "creationflags": DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                }
            )
            _ = subprocess.Popen(f"taskkill /F /PID {self.p.pid} /T", **invi)

    def kill_proc(
        self, press_ctrl_c=True, sleep_after_pipes=1, sleep_after_proc=1, shellkill=True
    ):
        if press_ctrl_c:
            try:
                send_ctrl_commands(self.p.pid, 0)
            except KeyboardInterrupt:
                pass
        self.tkill()
        killthread(self._t_stdout)
        killthread(self._t_stderr)
        close_stdoutpipe = threading.Thread(target=lambda: self._close_pipes("stdout"))
        close_stderrpipe = threading.Thread(target=lambda: self._close_pipes("stdin"))
        close_stdinpipe = threading.Thread(target=lambda: self._close_pipes("stderr"))
        close_stdoutpipe.start()
        close_stderrpipe.start()
        close_stdinpipe.start()
        sleep(sleep_after_pipes)
        close_proc = threading.Thread(target=self._close_proc)
        close_proc.start()
        sleep(sleep_after_proc)
        if iswindows:
            if shellkill and self.isalive():
                _ = subprocess.Popen(
                    f"taskkill /F /PID {self.p.pid} /T", **invisibledict
                )
        for thr in [close_stdoutpipe, close_stderrpipe, close_stdinpipe, close_proc]:
            try:
                killthread(thr)
            except Exception as e:
                sys.stderr.write(f"{e}\n")
                sys.stderr.flush()

    def _read_stdout(self):
        for l in iter(self.p.stdout.readline, b""):
            try:
                if self.separate_stdout_with_list:
                    self.stdout[-1].append(l)
                else:
                    self.stdout.append(l)
                if self.print_stdout:
                    sys.stdout.write(f'{l.decode("utf-8", "backslashreplace")}')
                    sys.stdout.flush()

            except Exception:
                break

    def _read_stderr(self):
        for l in iter(self.p.stderr.readline, b""):
            try:
                if self.separate_stderr_with_list:
                    self.stderr[-1].append(l)
                else:
                    self.stderr.append(l)
                if self.print_stderr:
                    sys.stderr.write(f'{l.decode("utf-8", "backslashreplace")}')
                    sys.stderr.flush()
            except Exception:
                break

    def disable_stderr_print(self):
        self.print_stderr = False
        return self

    def disable_stdout_print(self):
        self.print_stdout = False
        return self

    def enable_stderr_print(self):
        self.print_stderr = True
        return self

    def enable_stdout_print(self):
        self.print_stdout = True
        return self

    def write(
        self,
        cmd,
        wait_to_complete=0.1,
        convert_to_83=False,
        exitcommand="",
        commandtimeout=0,
    ):
        if convert_to_83:
            cmd = convert_path_to_short(cmd)

        exitcommandbytes = exitcommand.encode()

        if wait_to_complete:
            if iswindows:
                finalcommand = exitcommandbytes + b"\r\n"
            else:
                finalcommand = exitcommandbytes + b"\n"
        if isinstance(cmd, str):
            cmd = cmd.encode()
        if not cmd.endswith(b"\n"):
            cmd = cmd + b"\n"
        if cmd.startswith(b'b"') or cmd.startswith(b"b'"):
            cmd = cmd[2:-1]
        try:
            self.lockobject.acquire()
            stderrlist = []
            stdoutlist = []
            self.stdout.append(stdoutlist)
            self.stderr.append(stderrlist)

            try:
                self.p.stdin.write(cmd)
                self.p.stdin.flush()
            except OSError as e:
                sys.stderr.write(f"Connection broken {e}")
                # self._reconnect_device()
                raise e
            self.stdin.append(cmd)
        finally:
            try:
                self.lockobject.release()
            except Exception:
                pass

        if wait_to_complete:
            while True:
                if finalcommand not in b"".join(stdoutlist):
                    sleep(wait_to_complete)
                else:
                    break
            stdoutl = []
            stderrl = []
            if stdoutlist:
                stdoutl = (
                    b"".join(stdoutlist)
                    .split(finalcommand)[0]
                    .splitlines(keepends=True)
                )
            if stderrlist:
                stderrl = (
                    b"".join(stderrlist)
                    .split(finalcommand)[0]
                    .splitlines(keepends=True)
                )
            return stdoutl, stderrl
        return [stdoutlist, stderrlist]

    def get_lock(self):
        self.lockobject.acquire()
        return self

    def release_lock(self):
        self.lockobject.release()
        return self

    def flush_stdout(self):
        try:
            self.get_lock()
            self.stdout.clear()
        finally:
            try:
                self.release_lock()
            except Exception:
                pass
        return self

    def flush_stderr(self):
        try:
            self.get_lock()
            self.stderr.clear()
        finally:
            try:
                self.release_lock()
            except Exception:
                pass
        return self

    def flush_stdin(self):
        try:
            self.get_lock()
            self.stdin.clear()
        finally:
            try:
                self.release_lock()
            except Exception:
                pass
        return self

    def flush_all_pipes(self):
        self.stdin.clear()
        self.stdout.clear()
        self.stderr.clear()

    def send_ctrl_c(self):
        send_ctrl_commands(self.p.pid, command=0)
        return self

    def send_ctrl_break(self):
        send_ctrl_commands(self.p.pid, command=1)
        return self

    def send_ctrl_close(self):
        send_ctrl_commands(self.p.pid, command=2)
        return self

    def send_ctrl_logoff(self):
        send_ctrl_commands(self.p.pid, command=3)
        return self

    def send_ctrl_shutdown(self):
        send_ctrl_commands(self.p.pid, command=4)
        return self

    def isalive(self):
        if iswindows:
            return is_process_alive(self.p.pid)
        else:
            raise NotImplementedError


class PunktDict(PunktDict_):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def regex_file_search(self, expr, **kwargs):
        if isinstance(expr, str):
            expr = re.compile(expr, **kwargs)
        for key, item in self.items():
            if expr.search(item["path"]):
                yield item


def _escape_filepath(arg, argdict, instance):
    if "escape_filepath" in argdict:
        escape_filepath = argdict["escape_filepath"]
        if escape_filepath:
            return strip_quotes_and_escape(arg)
        else:
            return arg
    if hasattr(instance, "escape_filepath"):
        if instance.escape_filepath:
            return strip_quotes_and_escape(arg)
        else:
            return arg
    return arg


def add_to_kwargs(f_py=None, v=None):
    assert callable(f_py) or f_py is None

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if v:
                for kk, vv in v:
                    kwargs.update({kk: vv})
            return func(*args, **kwargs)

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator


def get_free_port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        port = s.server_address[1]
    return port


@cache
def convertcolor2rgb(x):
    return to_rgb_tuple(x.decode("utf-8"))


def sleep_random_time(sleep_after_letter):
    if sum(sleep_after_letter) > 0:
        sleep(random.uniform(*sleep_after_letter))


def format_input_command(input_device, action, command):
    if input_device:
        cmd2send = f"input {input_device} {action} {command}"
    else:
        cmd2send = f"input {action} {command}"
    return cmd2send


def remove_accents_from_text(text):
    textlist = []
    for t in text.splitlines():
        t = t.replace("ß", "ss").replace("ẞ", "SS")
        t = "".join(
            [
                lookup(k, case_sens=True, replace="", add_to_printable="")["suggested"]
                for k in t
            ]
        )
        textlist.append(t)
    text = "\n".join(textlist)
    return text


def split_text_at_quotes(text):
    return [
        f"'{x}'" if x not in '''\'""''' else repr(x)
        for x in re_split_quotes.split(text)
    ]


def split_text_in_letters(text):
    return [f"'{x}'" if x not in '''\'""''' else repr(x) for x in text]


def split_text_in_chars_or_parts(text, sleep_after_letter):
    if sum(sleep_after_letter) == 0:
        return split_text_at_quotes(text)
    else:
        return split_text_in_letters(text)


def get_tmpfile(suffix=".txt"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    purefile = filename.split(os.sep)[-1]
    return purefile, filename, partial(os.remove, tfp.name)


def strip_quotes_and_escape(s):
    if isinstance(s, bytes):
        return s
    s = s.strip("'\"")
    s = s.replace("\\", "\\\\")
    s = s.replace("%", "\\%")
    s = s.replace(" ", "\\ ")
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")
    s = s.replace("(", "\\(")
    s = s.replace(")", "\\)")
    s = s.replace("&", "\\&")
    s = s.replace("<", "\\<")
    s = s.replace(">", "\\>")
    s = s.replace(";", "\\;")
    s = s.replace("*", "\\*")
    s = s.replace("|", "\\|")
    s = s.replace("~", "\\~")
    s = s.replace("¬", "\\¬")
    s = s.replace("`", "\\`")
    s = s.replace("¦", "\\¦")
    return s


def format_url(url):
    if not url.lower().startswith("http://") and not url.lower().startswith("https://"):
        if not "://" in url:
            url = "http://" + url
    return url


class AdbControlBase(SubProcInputOutput):
    def __init__(
        self,
        adb_path,
        device_serial,
        use_busybox=False,
        connect_to_device=True,
        invisible=True,
        print_stdout=True,
        print_stderr=True,
        limit_stdout=None,
        limit_stderr=None,
        limit_stdin=None,
        convert_to_83=True,
        wait_to_complete=0.1,
        flush_stdout_before=True,
        flush_stdin_before=True,
        flush_stderr_before=True,
        su=False,
        exitcommand="xxxCOMMANDxxxDONExxx",
        commandtimeout=0,
        escape_filepath=True,
        capture_stdout_stderr_first=True,
        global_cmd=True,
        global_cmd_timeout=15,
        use_eval=False,
        eval_timeout=30,
    ):
        self.su = su
        self.use_busybox = use_busybox
        self.adbpath = adb_path
        self.device_serial = device_serial
        if convert_to_83:
            self.adb_path = get_short_path_name(adb_path)
        else:
            self.adb_path = adb_path
        self.wait_to_complete = wait_to_complete
        self.flush_stdout_before = flush_stdout_before
        self.flush_stdin_before = flush_stdin_before
        self.flush_stderr_before = flush_stderr_before
        self.invisible = invisible
        self.print_stdout = print_stdout
        self.print_stderr = print_stderr
        self.limit_stdout = limit_stdout
        self.limit_stderr = limit_stderr
        self.limit_stdin = limit_stdin
        self.convert_to_83 = convert_to_83
        self.exitcommand = exitcommand
        self.commandtimeout = commandtimeout
        self.escape_filepath = escape_filepath
        self.capture_stdout_stderr_first = capture_stdout_stderr_first
        self.tmpfolder_global = os.environ.get("TEMP", None)
        if not self.tmpfolder_global:
            self.tmpfolder_global = os.environ.get("TMP", None)
        if not self.tmpfolder_global:
            self.tmpfolder_global = os.getcwd()
        self.tmpfolder_global = os.path.normpath(self.tmpfolder_global)
        self.tstamp = str(time.time()).replace(".", "")

        self.tmpfile_global_err = f"errortmp{self.tstamp}.txt"
        self.tmpfile_global_out = f"outputtmp{self.tstamp}.txt"
        self.tmpfile_global_err_sdcard = f"/sdcard/errortmp{self.tstamp}.txt"
        self.tmpfile_global_out_sdcard = f"/sdcard/outputtmp{self.tstamp}.txt"
        self.tmpfile_global_err_sdcardbin = self.tmpfile_global_err_sdcard.encode()
        self.tmpfile_global_out_sdcardbin = self.tmpfile_global_out_sdcard.encode()
        self.tmpfile_global_err_full = os.path.join(
            self.tmpfolder_global, self.tmpfile_global_err
        )
        self.tmpfile_global_out_full = os.path.join(
            self.tmpfolder_global, self.tmpfile_global_out
        )
        self.global_cmd = global_cmd
        self.global_cmd_timeout = global_cmd_timeout
        self.use_eval = use_eval
        self.eval_timeout = eval_timeout
        self.communication_port = None
        if connect_to_device:
            subprocess.run([self.adb_path, "connect", device_serial], **invisibledict)
        super().__init__(
            [self.adb_path, "-s", self.device_serial, "shell"],
            invisible=invisible,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            limit_stdout=limit_stdout,
            limit_stderr=limit_stderr,
            limit_stdin=limit_stdin,
            convert_to_83=convert_to_83,
            separate_stdout_stderr_with_list=True,
        )
        self._correct_newlines = False

    def execute_sh_command_global(self, cmd, **kwargs):
        try:
            return self._execute_sh_command_global(cmd, **kwargs)
        except KeyboardInterrupt:
            try:
                while True:
                    sleep(1)
                    break
            except:
                pass
            try:
                self.p.stdin.flush()
                self.p.stdout.flush()
                self.p.stderr.flush()
            except Exception as fe:
                sys.stderr.write(f"{fe}\n")
                sys.stderr.flush()

    def _execute_sh_command_global(self, cmd, **kwargs):
        def delfi():
            try:
                os.remove(self.tmpfile_global_err_full)
            except Exception:
                pass
            try:
                os.remove(self.tmpfile_global_out_full)
            except Exception:
                pass

        def read_tmp_file(fi, timeout=10):
            timeoutfinal = time.time() + timeout
            while timeoutfinal > time.time():
                try:
                    with open(fi, mode="rb") as f:
                        data = f.read()
                    return data
                except Exception:
                    sleep(0.05)
            return b""

        def pullfi(fi):
            while True:
                try:
                    subprocess.run(
                        [
                            self.adbpath,
                            "-s",
                            self.device_serial,
                            "pull",
                            fi,
                            self.tmpfolder_global,
                        ],
                        capture_output=True,
                        **invisibledict,
                    )
                    return
                except Exception as e:
                    sys.stderr.write(f"{e}\n")
                    sleep(0.05)

        excom = self.exitcommand.encode()
        if isinstance(cmd, str):
            cmd = cmd.encode()
        checksize = c.ADB_SHELL_CHECK_FILESIZE.encode()
        cmd = (
            checksize
            + b"""\nexec 2>"""
            + self.tmpfile_global_err_sdcardbin
            + b"""\nexec 1>"""
            + self.tmpfile_global_out_sdcardbin
            + b"\n"
            + cmd
            + b"""\n"""
            + b"""check_if_finished_writing """
            + self.tmpfile_global_out_sdcardbin
            + b" 0.03"
            + b"""\nexec 1>&-\n"""
            + b"""exec 2>&-\n"""
            + b"""\necho -e -n """
            + excom
            + b""" >> """
            + self.tmpfile_global_out_sdcardbin
            + b"""\necho -e -n """
            + excom
            + b""" >> """
            + self.tmpfile_global_err_sdcardbin
            + b"""\n"""
            # + b"""echo\n"""
            # + b"""echo\n"""
            # + b"""echo\n"""
            # + b"""echo\n"""
        )
        su = kwargs.get("su", False)

        if su:
            cmd = b"#!/bin/bash\nsu\n" + cmd
        else:
            cmd = b"#!/bin/bash\n" + cmd
        # print(cmd)
        self.p.stdin.write(cmd)
        self.p.stdin.flush()
        tout = kwargs.get("global_cmd_timeout", self.global_cmd_timeout)
        # sleep(.05)

        # delfi()
        # sleep(.05)

        while True:
            delfi()
            sleep(0.01)
            pullfi(self.tmpfile_global_err_sdcard)
            so1 = read_tmp_file(self.tmpfile_global_err_full, tout)
            if excom in so1:
                break
            if so1:
                pullfi(self.tmpfile_global_out_sdcard)
                if os.path.exists(self.tmpfile_global_out_full):
                    with open(self.tmpfile_global_out_full, mode="rb") as bax:
                        da1 = bax.read()
                    if not da1:
                        break
                else:
                    break

        delfi()

        pullfi(self.tmpfile_global_err_sdcard)
        dataerr = (
            read_tmp_file(self.tmpfile_global_err_full, tout)
            .split(excom)[0]
            .splitlines(keepends=True)
        )
        pullfi(self.tmpfile_global_out_sdcard)
        if not os.path.exists(self.tmpfile_global_out_full):
            dataout = [b""]
        else:
            dataout = (
                read_tmp_file(self.tmpfile_global_out_full, tout)
                .split(excom)[0]
                .splitlines(keepends=True)
            )
        return [dataout, dataerr]

    def execute_sh_command_eval(self, command, timeout=10, **kwargs):
        if not isinstance(command, bytes):
            command = command.encode()
        eni = base64.standard_b64encode(command).decode("utf-8", "strict")
        path = "/sdcard/XXXXtmpcmd.txt"
        enicmd = f"base64 -d <<< $(echo -n {eni}) > {path}\n".encode()
        self.p.stdin.write(enicmd)
        self.p.stdin.flush()
        stdout = "/sdcard/outputfilexxxstdout.txt"
        stderr = "/sdcard/outputfilexxxstderr.txt"
        if not self.communication_port:
            self.communication_port = get_free_port()
            p1 = subprocess.run(
                f"{self.adbpath} -s {self.device_serial} forward tcp:{self.communication_port} tcp:{self.communication_port}",
                capture_output=True,
                **invisibledict,
            )
        su = kwargs.get("su", self.su)
        if su:
            linetoadd = f'''eval "cat {path} | su -c 'sh 2> {stderr} 1> {stdout}'"'''
        else:
            linetoadd = f'''eval "cat {path} | sh 2> {stderr} 1> {stdout}"'''

        enicmd2 = f"""
startpro(){{
{linetoadd}
echo -e -n "XXXXENDSTDOUTXXXX" >> {stdout}
echo -e -n "XXXXENDSTDERRXXXX" >> {stderr}
cat  {stdout} {stderr} | busybox nc -w {timeout} -l -p {self.communication_port}
rm -f {stderr}
rm -f {stdout}
rm -f {path}
}}
startpro 2> /dev/null
\n""".encode()
        self.p.stdin.write(enicmd2)
        self.p.stdin.flush()

        # print(p1.stdout)
        # print(p1.stderr)

        r = b""
        timeoutfinal = time.time() + timeout

        while time.time() < timeoutfinal:
            try:
                nc = nclib.Netcat(connect=("localhost", self.communication_port))

                r = nc.read_all(timeout=timeout)
                if r:
                    break
            except Exception as fe:
                print(fe)
                # continue
                try:
                    nc.close()
                except Exception as fa:
                    print(fa)
        # p2 = subprocess.run(
        #     f"{self.adbpath} -s {self.device_serial} forward --remove tcp:{freeport}",
        #     capture_output=True,
        #     **invisibledict,
        # )
        # print(p2.stdout)
        # print(p2.stderr)
        stdout, stderr = b"", b""
        try:
            stdout, stderr = r.split(b"XXXXENDSTDOUTXXXX")
            stderr = stderr.split(b"XXXXENDSTDERRXXXX")[0]
        except Exception:
            pass
        return [stdout.splitlines(keepends=True), stderr.splitlines(keepends=True)]

    def execute_sh_command(self, cmd, **kwargs):
        self._correct_newlines = True
        if isinstance(cmd, str):
            try:
                stackframe = sys._getframe(1)
                for key, item in stackframe.f_locals.items():
                    if isinstance(item, bytes):
                        asstr = str(item)
                        if asstr in cmd:
                            cmd = cmd.replace(asstr, asstr[2:-1])
            except Exception as fe:
                sys.stderr.write(f"{fe}\n")
                sys.stderr.flush()

        evalcmd = kwargs.get("use_eval", self.use_eval)

        if evalcmd:
            tout = kwargs.get("eval_timeout", kwargs.get("timeout", self.eval_timeout))
            return self.execute_sh_command_eval(cmd, timeout=tout, **kwargs)

        global_cmd = kwargs.get("global_cmd", self.global_cmd)
        if global_cmd:
            self._correct_newlines = False
            return self.execute_sh_command_global(cmd, **kwargs)

        oldvaluestdout = self.print_stdout
        oldvaluestderr = self.print_stderr

        disable_print_stdout = kwargs.get("disable_print_stdout", self.print_stdout)
        disable_print_stderr = kwargs.get("disable_print_stderr", self.print_stderr)
        wait_to_complete = kwargs.get("wait_to_complete", self.wait_to_complete)
        flush_stdout_before = kwargs.get(
            "flush_stdout_before", self.flush_stdout_before
        )
        flush_stdin_before = kwargs.get("flush_stdin_before", self.flush_stdin_before)
        flush_stderr_before = kwargs.get(
            "flush_stderr_before", self.flush_stderr_before
        )
        exitcommand = kwargs.get("exitcommand", self.exitcommand)
        su = kwargs.get("su", self.su)
        commandtimeout = kwargs.get("commandtimeout", self.commandtimeout)
        if "escape_filepath" in kwargs:
            del kwargs["escape_filepath"]
        capture_stdout_stderr_first = kwargs.get(
            "capture_stdout_stderr_first", self.capture_stdout_stderr_first
        )
        if disable_print_stdout:
            self.disable_stdout_print()
        if disable_print_stderr:
            self.disable_stderr_print()

        if flush_stdin_before:
            self.flush_stderr()
        if flush_stderr_before:
            self.flush_stderr()
        if flush_stdout_before:
            self.flush_stdout()
        if not wait_to_complete:
            exitcommand = ""
        try:
            if (cmd.startswith('b"') and cmd.endswith('"')) or (
                cmd.startswith("b'") and cmd.endswith("'")
            ):
                cmd = ast.literal_eval(str(cmd.encode("utf-8")))
        except Exception:
            pass
        if capture_stdout_stderr_first:
            bytescommand = self.format_adb_command(cmd, exitcommand=exitcommand, su=su)
        else:
            bytescommand = self.format_adb_command_screen_capture(
                cmd, exitcommand=exitcommand, su=su
            )

        stdout, stderr = self.write(
            bytescommand,
            wait_to_complete=wait_to_complete,
            convert_to_83=False,
            exitcommand=exitcommand,
            commandtimeout=commandtimeout,
        )
        self.print_stdout = oldvaluestdout
        self.print_stderr = oldvaluestderr
        return [stdout, stderr]

    def start_logcat(self, print_stdout=False, print_stderr=False):
        newinstance = self.__class__(
            adb_path=self.adbpath,
            device_serial=self.device_serial,
            use_busybox=self.use_busybox,
            connect_to_device=False,
            invisible=self.invisible,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            limit_stdout=self.limit_stdout,
            limit_stderr=self.limit_stderr,
            limit_stdin=self.limit_stdin,
            convert_to_83=False,
            wait_to_complete=0.0,
            flush_stdout_before=False,
            flush_stdin_before=False,
            flush_stderr_before=False,
            exitcommand=self.exitcommand,
            capture_stdout_stderr_first=False,
        )

        stdout, stderr = newinstance.execute_sh_command(
            "logcat",
            wait_to_complete=0,
            disable_print_stdout=True,
            disable_print_stderr=True,
        )
        return newinstance, stdout, stderr

    @staticmethod
    def connect_to_all_tcp_devices_windows(adb_path, convert_to_83=True):
        allprocs = []
        if convert_to_83:
            adb_path = get_short_path_name(adb_path)
        netstatexe = shutil.which("netstat.exe")
        p = subprocess.run(
            [netstatexe, "-a", "-b", "-n", "-o", "-p", "TCP"],
            capture_output=True,
            **invisibledict,
        )

        for ip, port in re.findall(
            rb"^\s*TCP\s*((?:127.0.0.1)|(?:0.0.0.0)):(\d+).*LISTENING",
            p.stdout,
            flags=re.M,
        ):
            allprocs.append(
                subprocess.Popen(
                    [adb_path, "connect", ip.decode() + ":" + port.decode()]
                )
            )
            sleep(0.1)
        pde = subprocess.run([adb_path, "devices", "-l"], capture_output=True)
        for pr in allprocs:
            try:
                pr.kill()
            except Exception:
                pass
        ou = [
            y
            for y in [
                q.split(maxsplit=2) for q in pde.stdout.decode("utf-8").splitlines()
            ]
            if len(y) == 3 and "devices attached" not in y
        ]
        return ou

    def format_adb_command(
        self,
        cmd,
        su=False,
        exitcommand="DONE",
        errors="strict",
    ):
        if isinstance(cmd, bytes):
            return self.format_adb_command_binary(
                cmd=cmd,
                su=su,
                exitcommand=exitcommand,
                errors=errors,
            )
        tmpfile1 = f"/sdcard/xxxxstdout{time.time()}.txt"
        tmpfile2 = f"/sdcard/xxxstderr{time.time()}.txt"

        shcommand = "sh"
        if su:
            shcommand = "su -c " + shcommand
        cmd = (
            f"""exec 3>&1 4>&2 1>{tmpfile1} 2>{tmpfile2}\n"""
            + cmd
            + f"""\nexec 1>&3 2>&4\ncat {tmpfile1}\ncat {tmpfile2} >&2\n"""
        )

        cmd = cmd + f"rm -f {tmpfile1} > /dev/null 2>&1\n"
        cmd = cmd + f"rm -f {tmpfile2} > /dev/null 2>&1\n"
        if exitcommand:
            cmd = cmd.rstrip() + f"\necho {exitcommand}\n"
        nolimitcommand = []
        base64_command = base64.standard_b64encode(cmd.encode("utf-8", errors)).decode(
            "utf-8", errors
        )
        nolimitcommand.extend(["echo", base64_command, "|"])
        if self.use_busybox:
            nolimitcommand.extend(["busybox"])
        nolimitcommand.extend(["base64", "-d", "|", shcommand])
        nolimitcommand_bytes = " ".join(nolimitcommand).encode("utf-8", errors) + b"\n"
        return nolimitcommand_bytes

    def format_adb_command_binary(
        self,
        cmd,
        su=False,
        exitcommand="DONE",
        errors="strict",
    ):
        if isinstance(exitcommand, str):
            exitcommand = exitcommand.encode()

        tmpfile1 = b"/sdcard/xxxxstdout" + str(time.time()).encode() + b".txt"
        tmpfile2 = b"/sdcard/xxxstderr" + str(time.time()).encode() + b".txt"

        shcommand = "sh"
        if su:
            shcommand = "su -c " + shcommand
        cmd = (
            b"exec 3>&1 4>&2 1>"
            + tmpfile1
            + b"  2>"
            + tmpfile2
            + b" \n"
            + cmd
            + b"\nexec 1>&3 2>&4\ncat "
            + tmpfile1
            + b" \ncat "
            + tmpfile2
            + b" >&2\n"
        )

        cmd = cmd + b"rm -f " + tmpfile1 + b" > /dev/null 2>&1\n"
        cmd = cmd + b"rm -f " + tmpfile2 + b" > /dev/null 2>&1\n"
        if exitcommand:
            cmd = cmd.rstrip() + b"\necho " + exitcommand + b"\n"
        nolimitcommand = []
        base64_command = base64.standard_b64encode(cmd).decode("utf-8", errors)
        nolimitcommand.extend(["echo", base64_command, "|"])
        if self.use_busybox:
            nolimitcommand.extend(["busybox"])
        nolimitcommand.extend(["base64", "-d", "|", shcommand])
        nolimitcommand_bytes = " ".join(nolimitcommand).encode("utf-8", errors) + b"\n"
        return nolimitcommand_bytes

    def format_adb_command_screen_capture_bytes(
        self,
        cmd,
        su=False,
        exitcommand="DONE",
        errors="strict",
    ):
        shcommand = "sh"
        if su:
            shcommand = "su -c " + shcommand
        if exitcommand:
            if isinstance(exitcommand, str):
                exitcommand = exitcommand.encode()
            cmd = cmd.rstrip() + b"\necho " + exitcommand + b"\n"
        nolimitcommand = []
        base64_command = base64.standard_b64encode(cmd).decode("utf-8", errors)

        nolimitcommand.extend(["echo", base64_command, "|"])
        if self.use_busybox:
            nolimitcommand.extend(["busybox"])
        nolimitcommand.extend(["base64", "-d", "|", shcommand])
        nolimitcommand_bytes = " ".join(nolimitcommand).encode("utf-8", errors) + b"\n"
        return nolimitcommand_bytes

    def format_adb_command_screen_capture(
        self,
        cmd,
        su=False,
        exitcommand="DONE",
        errors="strict",
    ):
        if isinstance(cmd, bytes):
            return self.format_adb_command_screen_capture_bytes(
                cmd=cmd,
                su=su,
                exitcommand=exitcommand,
                errors=errors,
            )
        shcommand = "sh"
        if su:
            shcommand = "su -c " + shcommand
        if exitcommand:
            cmd = cmd.rstrip() + f"\necho {exitcommand}\n"
        nolimitcommand = []
        base64_command = base64.standard_b64encode(cmd.encode("utf-8", errors)).decode(
            "utf-8", errors
        )
        nolimitcommand.extend(["echo", base64_command, "|"])
        if self.use_busybox:
            nolimitcommand.extend(["busybox"])
        nolimitcommand.extend(["base64", "-d", "|", shcommand])
        nolimitcommand_bytes = " ".join(nolimitcommand).encode("utf-8", errors) + b"\n"
        return nolimitcommand_bytes

    def write(
        self,
        cmd,
        wait_to_complete=0.1,
        convert_to_83=False,
        exitcommand="",
        commandtimeout=0,
    ):
        exitcommandbytes = exitcommand.encode()

        if wait_to_complete:
            if iswindows:
                finalcommand = exitcommandbytes + b"\r\n"
            else:
                finalcommand = exitcommandbytes + b"\n"
        if isinstance(cmd, str):
            cmd = cmd.encode()
        if not cmd.endswith(b"\n"):
            cmd = cmd + b"\n"

        try:
            self.lockobject.acquire()
            stderrlist = []
            stdoutlist = []
            self.stdout.append(stdoutlist)
            self.stderr.append(stderrlist)
            self.p.stdin.write(cmd)
            try:
                self.p.stdin.flush()
            except OSError as e:
                sys.stderr.write("Connection broken")
                raise e
            self.stdin.append(cmd)
        finally:
            try:
                self.lockobject.release()
            except Exception:
                pass

        if wait_to_complete:
            while True:
                if finalcommand not in b"".join(stdoutlist):
                    sleep(wait_to_complete)
                else:
                    break
            stdoutl = []
            stderrl = []
            if stdoutlist:
                stdoutl = (
                    b"".join(stdoutlist)
                    .split(finalcommand)[0]
                    .splitlines(keepends=True)
                )
            if stderrlist:
                stderrl = (
                    b"".join(stderrlist)
                    .split(finalcommand)[0]
                    .splitlines(keepends=True)
                )
            return stdoutl, stderrl
        return [stdoutlist, stderrlist]


class PressKey:
    def __init__(self, fu, event, description, longpress=False):
        self.fu = fu
        self.event = event
        self.description = description
        self.longpress = " --longpress" if longpress else ""

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

    def __call__(self, *args, **kwargs):
        return self.fu(
            f"input keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def dpad(self, *args, **kwargs):
        return self.fu(
            f"input dpad keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def keyboard(self, *args, **kwargs):
        return self.fu(
            f"input keyboard keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def mouse(self, *args, **kwargs):
        return self.fu(
            f"input mouse keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def touchpad(self, *args, **kwargs):
        return self.fu(
            f"input touchpad keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def gamepad(self, *args, **kwargs):
        return self.fu(
            f"input gamepad keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def touchnavigation(self, *args, **kwargs):
        return self.fu(
            f"input touchnavigation keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def joystick(self, *args, **kwargs):
        return self.fu(
            f"input joystick keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def touchscreen(self, *args, **kwargs):
        return self.fu(
            f"input touchscreen keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def stylus(self, *args, **kwargs):
        return self.fu(
            f"input stylus keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )

    def trackball(self, *args, **kwargs):
        return self.fu(
            f"input trackball keyevent {self.event}{self.longpress}",
            *args,
            **kwargs,
        )


class AdbControl(AdbControlBase):
    def __init__(
        self,
        adb_path,
        device_serial,
        use_busybox=False,
        connect_to_device=True,
        invisible=True,
        print_stdout=True,
        print_stderr=True,
        limit_stdout=None,
        limit_stderr=None,
        limit_stdin=None,
        convert_to_83=True,
        wait_to_complete=0.1,
        flush_stdout_before=True,
        flush_stdin_before=True,
        flush_stderr_before=True,
        exitcommand="xxxCOMMANDxxxDONExxx",
        capture_stdout_stderr_first=True,
        global_cmd=False,
        global_cmd_timeout=5,
        use_eval=False,
        eval_timeout=30,
    ):
        super().__init__(
            adb_path,
            device_serial,
            use_busybox=use_busybox,
            connect_to_device=connect_to_device,
            invisible=invisible,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            limit_stdout=limit_stdout,
            limit_stderr=limit_stderr,
            limit_stdin=limit_stdin,
            convert_to_83=convert_to_83,
            wait_to_complete=wait_to_complete,
            flush_stdout_before=flush_stdout_before,
            flush_stdin_before=flush_stdin_before,
            flush_stderr_before=flush_stderr_before,
            exitcommand=exitcommand,
            capture_stdout_stderr_first=capture_stdout_stderr_first,
            global_cmd=global_cmd,
            global_cmd_timeout=global_cmd_timeout,
            use_eval=use_eval,
            eval_timeout=eval_timeout,
        )
        self.keyevents = PunktDict(key_events)

        for key, item in key_events.items():
            self.keyevents[key]["press"] = PressKey(
                self.execute_sh_command,
                item["as_int"],
                item["description"],
                False,
            )
            self.keyevents[key]["longpress"] = PressKey(
                self.execute_sh_command,
                item["as_int"],
                item["description"],
                True,
            )
        self.keyevents_sendevent = PunktDict_({})

    def sh_input_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TAP % (int(x), int(y)), **kwargs
        )

    def sh_get_android_version(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GET_ANDROID_VERSION, **kwargs)
        if so:
            return so[0].strip().decode()

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_copy_dir_recursive(self, src, dst, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_COPY_DIR_RECURSIVE % (src, dst), **kwargs
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_paste(self, file, delimiter=" ", **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_PASTE_DS % (delimiter, file), **kwargs
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_tail_bytes(self, n, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_TAIL_BYTES % (int(n), file), **kwargs
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_tail_lines(self, n, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_TAIL_LINES % (int(n), file), **kwargs
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_head_bytes(self, n, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_HEAD_BYTES % (int(n), file), **kwargs
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_head_lines(self, n, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_HEAD_LINES % (int(n), file), **kwargs
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_remove_folder(self, folder, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_FOLDER % (folder,), **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_number_of_lines_words_chars_in_file(self, file, **kwargs):
        try:
            return list(
                map(
                    int,
                    self.execute_sh_command(
                        c.ADB_SHELL_COUNT_LINES_WORDS_CHARS % file, **kwargs
                    )[0][0]
                    .strip()
                    .split(maxsplit=3)[:3],
                )
            )
        except Exception as e:
            sys.stderr.write(f"{e}")
            sys.stderr.flush()
        return []

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_create_bak_of_file(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_CRATE_BACKUP % file, **kwargs)

    def sh_change_to_dir(self, path, **kwargs):
        if isinstance(path, str):
            path = strip_quotes_and_escape(path).encode()
        self.p.stdin.write(b"cd " + path + b"\n")
        self.p.stdin.flush()

    def sh_change_to_prev_working_dir(self, **kwargs):
        self.p.stdin.write(c.ADB_SHELL_CHANGE_TO_PREV_WORKING_DICT.encode() + b"\n")
        self.p.stdin.flush()

    def sh_ls(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_LS, **kwargs)
        if not so and se:
            kwargs.update(su=True)
            so, se = self.execute_sh_command(c.ADB_SHELL_LS, **kwargs)
        return so, se

    def sh_empty_file(self, path, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_EMPTY_FILE % path, **kwargs)

    def format_output(self, stdout):
        if iswindows and self._correct_newlines:
            p = b"".join([x.replace(b"\r\n", b"\n") for x in stdout])
            try:
                return p.split(self.exitcommand.encode())[0]
            except Exception as e:
                return p

        else:
            return b"".join(stdout).split(self.exitcommand.encode())[0]

    def sh_cat_file(self, path, **kwargs):
        path2 = strip_quotes_and_escape(path)
        da = self.execute_sh_command(c.ADB_SHELL_CAT_FILE % path2, **kwargs)[0]
        if not da:
            da = self.execute_sh_command(c.ADB_SHELL_CAT_FILE % f'"{path}"', **kwargs)[
                0
            ]

        return self.format_output(da)

    def sh_cat_file_without_newlines(self, path, **kwargs):
        path2 = strip_quotes_and_escape(path)
        da = self.execute_sh_command(
            c.ADB_SHELL_REMOVE_NEWLINES_FROM_FILE_AND_CAT % path2, **kwargs
        )[0]
        if not da:
            da = self.execute_sh_command(
                c.ADB_SHELL_REMOVE_NEWLINES_FROM_FILE_AND_CAT % f'"{path}"', **kwargs
            )[0]
        return self.format_output(da)

    def sh_ping_one_time(self, url, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ONE_TIME_PING % url, **kwargs)

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_cat_file_without_leading_whitespaces(self, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CAT_FILE_WITHOUT_LEADING_WHITESPACES % path, **kwargs
        )

    def sh_variable_exists(self, variable, **kwargs):
        so, se = self.execute_sh_command(
            c.ADB_SHELL_VARIABLE_EXISTS % variable, **kwargs
        )
        if so:
            return bool(int(so[0].strip().decode()))
        return False

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_create_file_with_content(self, filedata, path, append=False, **kwargs):
        if not isinstance(filedata, bytes):
            filedata = filedata.encode()
        eni = base64.standard_b64encode(filedata).decode("utf-8", "strict")
        if not append:
            enicmd = f"base64 -d <<< $(echo -n {eni}) > {path}".encode()
        else:
            enicmd = f"base64 -d <<< $(echo -n {eni}) >> {path}".encode()

        return self.execute_sh_command(enicmd, **kwargs)

    def sh_append_to_file(self, filedata, path, **kwargs):
        return self.sh_create_file_with_content(filedata, path, append=True, **kwargs)

    def sh_echo_rev(self, string, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ECHO_BACKWARDS % string, **kwargs)

    def sh_netstat_ip_group(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_NETSTAT_IP_GROUP, **kwargs)

    def sh_process_tree(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PSTREE, **kwargs)

    def sh_list_hdds(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_HDS, **kwargs)

    def sh_list_hdds_real(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_HDDS_REAL, **kwargs)

    def sh_lsof_filehandles(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LSOF_FILEHANDLES, **kwargs)

    def sh_list_exe_in_path(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_ALL_EXE_IN_PATH, **kwargs)

    def sh_free_memory(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_FREE_MEMORY, **kwargs)
        if so:
            return int(so[0].strip().decode())

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_cat_file_without_leading_whitespaces(self, path, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SORT_AND_UNIQUE % path, **kwargs)

    def push(self, file, folder, **kwargs):
        kwargscopy = kwargs.copy()
        kwargs.update({"wait_to_complete": 0})

        dire = strip_quotes_and_escape("/" + folder.strip("/") + "/")
        filename = strip_quotes_and_escape(file.split(os.sep)[-1])
        stdout1, stderr1 = self.execute_sh_command(
            c.ADB_SHELL_CREATE_NESTED_FOLDER % dire, **kwargs
        )
        stdout2, stderr2 = self.execute_sh_command(
            c.ADB_SHELL_TOUCH % f"{dire}{filename}", **kwargs
        )
        with open(file, mode="rb") as f:
            cmd = f.read()
        eni = base64.standard_b64encode(cmd).decode("utf-8", "strict")
        stdout3, stderr3 = self.execute_sh_command(
            f"base64 -d <<< $(echo -n {eni}) > {dire}{filename}", **kwargscopy
        )
        allout = self._all_outputlist_to_one(stdout1, stdout2, stdout3)
        allerrs = self._all_outputlist_to_one(stderr1, stderr2, stderr3)

        return [allout, allerrs]

    def _all_outputlist_to_one(self, *args):
        allout = []
        for arg in args:
            allout.extend(arg)
        return allout

    def list_all_listening_ports_and_pid(self, **kwargs):
        return [
            g
            for x in self.execute_sh_command(
                c.ADB_SHELL_LIST_ALL_LISTENING_PORT_AND_PIDS, **kwargs
            )[0]
            if len(g := (x.strip().split(maxsplit=6))) == 7
            and re.search(rb"^\d+", g[1])
        ]

    def sh_screencap(self, correct_newlines=True, **kwargs):
        if "wait_to_complete" not in kwargs:
            kwargs.update({"wait_to_complete": 0.01})

        stdout, stderr = self.execute_sh_command(c.ADB_SHELL_SCREENCAPRAW, **kwargs)
        if not correct_newlines:
            return b"".join(stdout)
        # else:
        return self.format_output(stdout)

    def sh_screencap_png(self, correct_newlines=True, **kwargs):
        if "wait_to_complete" not in kwargs:
            kwargs.update({"wait_to_complete": 0.01})

        stdout, stderr = self.execute_sh_command(c.ADB_SHELL_SCREENCAP, **kwargs)
        if not correct_newlines:
            return b"".join(stdout)
        return self.format_output(stdout)

    def open_adb_shell(self):
        if iswindows:
            cmdcom = get_comspec()
            subprocess.run(
                f'start {cmdcom} /k "{self.adbpath}" -s {self.device_serial} shell',
                shell=True,
                **invisibledict,
            )
        else:
            raise NotImplementedError

    def pull(self, path):
        stdout, stderr = self.execute_sh_command(f'cat "{path}"')
        if stderr:
            stdout, stderr = self.execute_sh_command(
                f"cat {strip_quotes_and_escape(path)}"
            )
        return self.format_output(stdout)

    def push_folder(self, folder, dstfolder):
        olddir = os.getcwd()
        os.chdir(folder)
        purefile, filename, deletefu = get_tmpfile(suffix=".tar")
        try:
            tar = tarfile.open(filename, "w")
            tar.add(".", recursive=True)
        finally:
            tar.close()
            os.chdir(olddir)
        stdout1, stderr1 = self.push(filename, dstfolder)
        stdout2, stderr2 = self.execute_sh_command(
            f"cd {dstfolder};" + c.ADB_SHELL_UNPACK_TAR % purefile
        )
        stdout3, stderr3 = self.execute_sh_command(c.ADB_SHELL_REMOVE_FILE % purefile)
        deletefu()
        allout = self._all_outputlist_to_one(stdout1, stdout2, stdout3)
        allerrs = self._all_outputlist_to_one(stderr1, stderr2, stderr3)

        return allout, allerrs

    @add_to_kwargs(v=(("su", True), ("disable_print_stdout", True)))
    def get_memdump_from_process(self, pid, **kwargs):
        memdumpfunction = c.ADB_SHELL_MEMDUMP + str(pid)
        return self.execute_sh_command(memdumpfunction, **kwargs)

    def get_imei_imsi_sim(self):
        def get_codes(v):
            return re.sub(
                r"\W+",
                "",
                "".join(
                    list(
                        flatten_everything(
                            [
                                re.findall(r"'[^']+'", x.decode("utf-8", "ignore"))
                                for x in v.splitlines()
                            ]
                        )
                    )
                ),
            )

        imsi = b"".join(self.execute_sh_command(c.ADB_GET_imsi, su=True)[0])
        imei = b"".join(self.execute_sh_command(c.ADB_GET_imei, su=True)[0])
        sims = b"".join(self.execute_sh_command(c.ADB_GET_sims, su=True)[0])
        imsi = get_codes(v=imsi)
        imei = get_codes(v=imei)
        sims = get_codes(v=sims)
        return imei, imsi, sims

    @add_to_kwargs(v=(("su", True),))
    def sh_pkill(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PKILL % package, **kwargs)

    def sh_am_kill(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_AM_KILL % package, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_killall9(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_KILLALL_9 % package, **kwargs)

    def get_imeis_multidevices(self):
        a = (
            b"".join(self.execute_sh_command(c.ADB_IMEI_MULTI1)[0])
            .strip()
            .decode("utf-8")
        )
        b = (
            b"".join(self.execute_sh_command(c.ADB_IMEI_MULTI2)[0])
            .strip()
            .decode("utf-8")
        )
        return a, b

    @add_to_kwargs(v=(("su", True),))
    def sh_kill(self, package, **kwargs):
        return self.execute_sh_command(f"kill {self.sh_get_pid_of(package)}", **kwargs)

    def sh_force_stop(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_AM_FORCE_STOP % package, **kwargs)

    def sh_get_pid_of(self, package, **kwargs):
        stdout, stderr = self.execute_sh_command(
            c.ADB_SHELL_GET_PIDOF % package, **kwargs
        )
        try:
            if stdout:
                return int(stdout[0].strip())
        except Exception:
            sys.stderr.write(f"{package} not found\n")
            return -1

    def kill_package(self, package, **kwargs):
        stdoutlist = []
        stderrlist = []
        stdout, stderr = self.sh_force_stop(package, **kwargs)
        stdoutlist.extend(stdout)
        stderrlist.extend(stderr)
        stdout, stderr = self.sh_kill(package, **kwargs)
        stdoutlist.extend(stdout)
        stderrlist.extend(stderr)
        stdout, stderr = self.sh_killall9(package, **kwargs)
        stdoutlist.extend(stdout)
        stderrlist.extend(stderr)
        stdout, stderr = self.sh_am_kill(package, **kwargs)
        stdoutlist.extend(stdout)
        stderrlist.extend(stderr)
        stdout, stderr = self.sh_pkill(package, **kwargs)
        stdoutlist.extend(stdout)
        stderrlist.extend(stderr)
        return [stdoutlist, stderrlist]

    def sh_grep(
        self,
        reg,
        path,
        escape=True,
        quote=False,
        extended_regexp=True,
        ignore_case=True,
        recursively=False,
        line_number=True,
        invert_match=False,
        files_with_matches=False,
        count=False,
        **kwargs,
    ):
        if isinstance(path, str):
            path = [path]
        if escape:
            path = [strip_quotes_and_escape(p) for p in path]
        allpath = []
        if quote:
            for p in path:
                if '"' in p:
                    p = f"'{p}'"
                else:
                    p = f'"{p}"'
            allpath.append(p)
        else:
            allpath.extend(path)
        whole_command = ["grep", f'"{reg}"', "--text"]
        if extended_regexp:
            whole_command.append("--extended-regexp")
        if ignore_case:
            whole_command.append("--ignore-case")
        if recursively:
            whole_command.append("-R")
        if line_number:
            whole_command.append("--line-number")
        if invert_match:
            whole_command.append("--invert-match")
        if files_with_matches:
            whole_command.append("--files-with-matches")
        if count:
            whole_command.append("--count")

        wholecommandstr = " ".join(whole_command) + " " + " ".join(allpath)
        return self.execute_sh_command(
            wholecommandstr,
            **kwargs,
        )

    def sh_input_dpad_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_dpad_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_keyboard_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_keyboard_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_mouse_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_mouse_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_touchpad_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_touchpad_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_gamepad_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_gamepad_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_touchnavigation_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_touchnavigation_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_joystick_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_joystick_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_touchscreen_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_touchscreen_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_stylus_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_stylus_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_trackball_longtap(self, x, y, t=1.0, **kwargs):
        return self.sh_input_trackball_drag_and_drop(x, y, x, y, t, **kwargs)

    def sh_input_dpad_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_DPAD_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_dpad_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_DPAD_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_dpad_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_DPAD_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_keyboard_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_KEYBOARD_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_keyboard_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_KEYBOARD_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_keyboard_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_KEYBOARD_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_mouse_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_MOUSE_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_mouse_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_MOUSE_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_mouse_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_MOUSE_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_touchpad_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHPAD_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_touchpad_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHPAD_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_touchpad_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_TOUCHPAD_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_gamepad_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_GAMEPAD_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_gamepad_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_GAMEPAD_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_gamepad_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_GAMEPAD_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_touchnavigation_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHNAVIGATION_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_touchnavigation_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHNAVIGATION_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_touchnavigation_roll(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHNAVIGATION_ROLL % (int(x), int(y)), **kwargs
        )

    def sh_input_joystick_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_JOYSTICK_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_joystick_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_JOYSTICK_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_joystick_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_JOYSTICK_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_touchscreen_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHSCREEN_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_touchscreen_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHSCREEN_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_touchscreen_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_TOUCHSCREEN_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_stylus_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_STYLUS_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_stylus_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_STYLUS_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_stylus_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_STYLUS_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_input_trackball_swipe(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TRACKBALL_SWIPE
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_trackball_drag_and_drop(self, x0, y0, x1, y1, t=1.0, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TRACKBALL_DRAGANDDROP
            % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_input_trackball_roll(self, x, y, **kwargs):
        return (
            self.execute_sh_command(
                c.ADB_SHELL_INPUT_TRACKBALL_ROLL % (int(x), int(y)), **kwargs
            ),
        )

    def sh_dumpsys_window(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_WINDOW, **kwargs)

    def sh_input_dpad_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_DPAD_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_keyboard_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_KEYBOARD_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_mouse_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_MOUSE_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_touchpad_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHPAD_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_gamepad_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_GAMEPAD_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_touchnavigation_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHNAVIGATION_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_joystick_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_JOYSTICK_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_touchscreen_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TOUCHSCREEN_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_stylus_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_STYLUS_TAP % (int(x), int(y)), **kwargs
        )

    def sh_input_trackball_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TRACKBALL_TAP % (int(x), int(y)), **kwargs
        )

    def sh_is_screen_locked(self, **kwargs):
        stdo, stde = self.sh_dumpsys_window(**kwargs)
        return b"mDreamingLockscreen=true" in b"".join(stdo)

    def sh_list_permission_groups(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_PERMISSION_GROUPS, **kwargs)

    def sh_resolve_activity(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_RESOLVE_ACTIVITY % package, **kwargs)

    def sh_resolve_activity_brief(self, package, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_RESOLVE_ACTIVITY_BRIEF % package, **kwargs
        )

    def sh_expand_notifications(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_EXPAND_NOTIFICATIONS, **kwargs)

    def sh_expand_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_EXPAND_SETTINGS, **kwargs)

    def sh_start_package(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_START_PACKAGE % package, **kwargs)

    def sh_get_resolution(self, **kwargs):
        try:
            width, height = [
                [int(g[0][0]), int(g[0][1])]
                for x in self.execute_sh_command(c.ADB_SHELL_DUMPSYS_WINDOW, **kwargs)[
                    0
                ]
                if (g := screenres_reg_cur.findall(x))
            ][0]
        except Exception:
            width, height = [
                [int(g[0][0]), int(g[0][1])]
                for x in self.sh_get_wm_size(**kwargs)[0]
                if (g := screenres_reg.findall(x))
            ][0]
        return width, height

    def sh_change_display_orientation(self, new_orientation=1, timeout=5, **kwargs):
        orientierung = self.sh_get_display_orientation(**kwargs)

        if new_orientation == "horizontal_upside_down" or new_orientation == 2:
            format_einfuegen = 2

        elif new_orientation == "vertical" or new_orientation == 1:
            format_einfuegen = 1

        elif new_orientation == "horizontal" or new_orientation == 0:
            format_einfuegen = 0

        elif new_orientation == "vertical_upside_down" or new_orientation == 3:
            format_einfuegen = 3
        else:
            format_einfuegen = 0
        timeoutfinal = timeout + time.time()
        while orientierung != format_einfuegen:
            if time.time() > timeoutfinal:
                break
            cmds = f"""content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0 && settings put system accelerometer_rotation 0 && content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:{format_einfuegen}"""
            stdo, stde = self.execute_sh_command(cmds, **kwargs)
            orientierung = self.sh_get_display_orientation(**kwargs)
        return orientierung

    def sh_do_random_actions(
        self,
        p=(),
        c=(),
        v=10,
        ignore_crashes=False,
        ignore_timeouts=False,
        ignore_security_exceptions=False,
        monitor_native_crashes=False,
        ignore_native_crashes=False,
        kill_process_after_error=False,
        hprof=False,
        match_description="",
        pct_touch=-1,
        pct_motion=-1,
        pct_trackball=-1,
        pct_syskeys=-1,
        pct_nav=-1,
        pct_majornav=-1,
        pct_appswitch=-1,
        pct_flip=-1,
        pct_anyevent=-1,
        pct_pinchzoom=-1,
        pct_permission=-1,
        pkg_blacklist_file="",
        pkg_whitelist_file="",
        wait_dbg=False,
        dbg_no_events=False,
        setup="",
        port=-1,
        s=-1,
        throttle_start=-1,
        throttle_end=-1,
        randomize_throttle=False,
        profile_wait=-1,
        device_sleep_time=-1,
        randomize_script=False,
        script_log=False,
        bugreport=False,
        periodic_bugreport=False,
        permission_target_system=False,
        **kwargs,
    ):
        command = ["monkey"]
        if p:
            if isinstance(p, str):
                p = [p]
            for pp in p:
                command.append(f"-p {pp}")
        if c:
            if isinstance(c, str):
                c = [c]
            for cc in c:
                command.append(f"-c {cc}")

        if ignore_crashes:
            command.append("--ignore-crashes")
        if ignore_timeouts:
            command.append("--ignore-timeouts")
        if ignore_security_exceptions:
            command.append("--ignore-security-exceptions")
        if monitor_native_crashes:
            command.append("--monitor-native-crashes")
        if ignore_native_crashes:
            command.append("--ignore-native-crashes")
        if kill_process_after_error:
            command.append("--kill-process-after-error")
        if hprof:
            command.append("--hprof")
        if match_description:
            command.append(f"--match-description {match_description}")
        if pct_touch > -1:
            command.append(f"--pct-touch {pct_touch}")
        if pct_motion > -1:
            command.append(f"--pct-motion {pct_motion}")
        if pct_trackball > -1:
            command.append(f"--pct-trackball {pct_trackball}")
        if pct_syskeys > -1:
            command.append(f"--pct-syskeys {pct_syskeys}")
        if pct_nav > -1:
            command.append(f"--pct-nav {pct_nav}")
        if pct_majornav > -1:
            command.append(f"--pct-majornav {pct_majornav}")
        if pct_appswitch > -1:
            command.append(f"--pct-appswitch {pct_appswitch}")
        if pct_flip > -1:
            command.append(f"--pct-flip {pct_flip}")
        if pct_anyevent > -1:
            command.append(f"--pct-anyevent {pct_anyevent}")
        if pct_pinchzoom > -1:
            command.append(f"--pct-pinchzoom {pct_pinchzoom}")
        if pct_permission > -1:
            command.append(f"--pct-permission {pct_permission}")

        if pkg_blacklist_file:
            command.append(f"--pkg-blacklist-file {pkg_blacklist_file}")
        if pkg_whitelist_file:
            command.append(f"--pkg-whitelist-file {pkg_whitelist_file}")
        if wait_dbg:
            command.append("--wait-dbg")
        if dbg_no_events:
            command.append("--dbg-no-events")
        if setup:
            command.append(f"--setup {setup}")
        if port > -1:
            command.append(f"--port {port}")
        if s > -1:
            command.append(f"-s {s}")
        command.append(f"-v {v}")
        if throttle_start > -1 or throttle_end > -1:
            command.append("--throttle")
            if throttle_start > -1:
                command.append(f"{throttle_start}")
            if throttle_end > -1:
                command.append(f"{throttle_end}")
        if randomize_throttle:
            command.append("--randomize-throttle")
        if profile_wait > -1:
            command.append(f"--profile-wait {profile_wait}")
        if device_sleep_time > -1:
            command.append(f"--device-sleep-time {device_sleep_time}")
        if randomize_script:
            command.append("--randomize-script")
        if script_log:
            command.append("--script-log")
        if bugreport:
            command.append("--bugreport")
        if periodic_bugreport:
            command.append("--periodic-bugreport")
        if permission_target_system:
            command.append("--permission-target-system")
        wholecommand = " ".join(command).strip()
        return self.execute_sh_command(wholecommand, **kwargs)

    def sh_netstat(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_NETSTAT, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_remove_user_cache(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_USER_CACHE, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_remove_dalvik_cache(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_DALVIK_CACHE, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_remove_data_cache(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_DATA_CACHE, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def get_imei_android_14(self, **kwargs):
        r = self.execute_sh_command(c.ADB_IMEI_ANDROID14, **kwargs)[0]
        if r:
            return r[0]

    @add_to_kwargs(v=(("su", True),))
    def sh_remount_all_rw(self, **kwargs):
        self.execute_sh_command(c.ADB_SHELL_REMOUNT_ALL_RW, **kwargs)
        cmd2 = c.ADB_SHELL_REMOUNT_ALL_RW.rstrip(" /")
        return [
            self.execute_sh_command(f"{cmd2} {y[0]} {y[2]}", **kwargs)
            for y in [
                x.decode("utf-8").split(maxsplit=3)
                for x in self.execute_sh_command(c.ADB_SHELL_MOUNT, **kwargs)[0]
            ]
        ]

    @add_to_kwargs(v=(("su", True),))
    def sh_remount_all_ro(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REMOUNT_ALL_RO, **kwargs)

    def sh_pm_dump(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PM_DUMP % package, **kwargs)

    def sh_get_wm_size(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GET_WM_SIZE, **kwargs)

        return [int(y) for y in so[0].strip().split()[-1].decode("utf-8").split("x")]

    def sh_change_wm_size(self, width, height, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CHANGE_WM_SIZE % (width, height), **kwargs
        )

    def sh_wm_reset_size(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WM_RESET_SIZE, **kwargs)

    def sh_get_wm_density(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GET_WM_DENSITY, **kwargs)

        return int(so[0].strip().split()[-1].decode("utf-8"))

    def sh_change_wm_density(self, density, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CHANGE_WM_DENSITY % density, **kwargs
        )

    def sh_wm_reset_density(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WM_RESET_DENSITY, **kwargs)

    def sh_list_features(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_FEATURES, **kwargs)

    def sh_pwd(self, **kwargs):
        return (
            self.execute_sh_command(c.ADB_SHELL_PWD, **kwargs)[0][0]
            .strip()
            .decode("utf-8")
        )

    def sh_list_services(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_SERVICES, **kwargs)

    def sh_ps_a_t_l_z(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PS_A_T_L_Z, **kwargs)

    def sh_open_url(self, url, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_OPEN_URL % format_url(url), **kwargs)

    def sh_get_ntp_server(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_NTP_SERVER, **kwargs)

    def sh_set_ntp_server(self, server, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SET_NTP_SERVER % server, **kwargs)

    def sh_pm_list_packages_f_i_u(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PM_LIST_PACKAGES_F_I_U, **kwargs)

    def sh_pm_list_packages_3(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PM_LIST_PACKAGES_3, **kwargs)

    def sh_pm_list_packages_s(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PM_LIST_PACKAGES_S, **kwargs)

    def sh_mount(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_MOUNT, **kwargs)

    def sh_dumpsys_activity_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_SETTINGS, **kwargs)

    def sh_dumpsys_activity_allowed_associations(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_DUMPSYS_ACTIVITY_ALLOWED_ASSOCIATIONS, **kwargs
        )

    def sh_dumpsys_activity_intents(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_INTENTS, **kwargs)

    def sh_dumpsys_activity_broadcasts(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_DUMPSYS_ACTIVITY_BROADCASTS, **kwargs
        )

    def sh_dumpsys_activity_broadcast_stats(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_DUMPSYS_ACTIVITY_BROADCAST_STATS, **kwargs
        )

    def sh_dumpsys_activity_providers(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_PROVIDERS, **kwargs)

    def sh_dumpsys_activity_permissions(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_DUMPSYS_ACTIVITY_PERMISSIONS, **kwargs
        )

    def sh_dumpsys_activity_services(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_SERVICES, **kwargs)

    def sh_dumpsys_activity_recents(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_RECENTS, **kwargs)

    def sh_dumpsys_activity_lastanr(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_LASTANR, **kwargs)

    def sh_dumpsys_activity_starter(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_STARTER, **kwargs)

    def sh_dumpsys_activity_activities(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_DUMPSYS_ACTIVITY_ACTIVITIES, **kwargs
        )

    def sh_dumpsys_activity_exit_info(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_EXIT_INFO, **kwargs)

    def sh_dumpsys_activity_processes(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_PROCESSES, **kwargs)

    def sh_dumpsys_activity_lru(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_ACTIVITY_LRU, **kwargs)

    def sh_make_call(self, number, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_MAKE_CALL % number, **kwargs)

    def sh_still_image_camera(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_STILL_IMAGE_CAMERA, **kwargs)

    def sh_clear_package(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_CLEAR_PACKAGE % package, **kwargs)

    @change_args_kwargs(
        args_and_function=(
            ("folder", _escape_filepath),
            ("outputfile", _escape_filepath),
        )
    )
    def sh_create_date_sorted_filelist(
        self, folder, outputfile, filefilter="*", **kwargs
    ):
        return self.execute_sh_command(
            c.ADB_SHELL_CREATE_DATE_SORTED_FILE_LIST
            % (folder, filefilter, outputfile, outputfile),
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_remove_file(self, path, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_FILE % path, **kwargs)

    def sh_disable_heads_up_notifications(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DISABLE_NOTIFICATIONS, **kwargs)

    def sh_enable_heads_up_notifications(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ENABLE_NOTIFICATIONS, **kwargs)

    def sh_screen_compat_on(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SCREEN_COMPAT_ON % package, **kwargs)

    def sh_screen_compat_off(self, package, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_SCREEN_COMPAT_OFF % package, **kwargs
        )

    def sh_list_users(self, **kwargs):
        return [
            x.decode("utf-8", "ignore").strip()
            for x in self.execute_sh_command(c.ADB_SHELL_LIST_USERS, **kwargs)[0]
            if b"{" in x
        ]

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_rescan_one_media(self, path, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_RESCAN_ONE_MEDIA % path, **kwargs)

    def _press_keyevent(self, k, **kwargs):
        longpress = kwargs.get("longpress", False)

        if "longpress" in kwargs:
            del kwargs["longpress"]
        if longpress:
            self.execute_sh_command(f"input keyevent {k} --longpress", **kwargs)
        else:
            self.execute_sh_command(f"input keyevent {k}", **kwargs)

    def k_hide_keyboard(self, **kwargs):
        return self._press_keyevent("4", **kwargs)

    def k_app_switch(self, **kwargs):
        return self._press_keyevent("KEYCODE_APP_SWITCH", **kwargs)

    def k_brightness_down(self, **kwargs):
        return self._press_keyevent("KEYCODE_BRIGHTNESS_DOWN", **kwargs)

    def k_brightness_up(self, **kwargs):
        return self._press_keyevent("KEYCODE_BRIGHTNESS_UP", **kwargs)

    def k_contacts(self, **kwargs):
        return self._press_keyevent("KEYCODE_CONTACTS", **kwargs)

    def k_copy(self, **kwargs):
        return self._press_keyevent("KEYCODE_COPY", **kwargs)

    def k_cut(self, **kwargs):
        return self._press_keyevent("KEYCODE_CUT", **kwargs)

    def k_home(self, **kwargs):
        return self._press_keyevent("KEYCODE_HOME", **kwargs)

    def k_page_down(self, **kwargs):
        return self._press_keyevent("KEYCODE_PAGE_DOWN", **kwargs)

    def k_page_up(self, **kwargs):
        return self._press_keyevent("KEYCODE_PAGE_UP", **kwargs)

    def k_paste(self, **kwargs):
        return self._press_keyevent("KEYCODE_PASTE", **kwargs)

    def k_power(self, **kwargs):
        return self._press_keyevent("KEYCODE_POWER", **kwargs)

    def k_search(self, **kwargs):
        return self._press_keyevent("KEYCODE_SEARCH", **kwargs)

    def k_sleep(self, **kwargs):
        return self._press_keyevent("KEYCODE_SLEEP", **kwargs)

    def k_tab(self, **kwargs):
        return self._press_keyevent("KEYCODE_TAB", **kwargs)

    def k_volume_down(self, **kwargs):
        return self._press_keyevent("KEYCODE_VOLUME_DOWN", **kwargs)

    def k_volume_up(self, **kwargs):
        return self._press_keyevent("KEYCODE_VOLUME_UP", **kwargs)

    def k_volume_mute(self, **kwargs):
        return self._press_keyevent("KEYCODE_VOLUME_MUTE", **kwargs)

    def k_wakeup(self, **kwargs):
        return self._press_keyevent("KEYCODE_WAKEUP", **kwargs)

    # @add_to_kwargs(v=(("wait_to_complete", 0),))
    def sh_get_display_orientation(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_USER_ROTATION, **kwargs)[0][
            0
        ].strip()

    def sh_open_date_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DATE_SETTINGS, **kwargs)

    def sh_open_application_development_settings(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_APPLICATION_DEVELOPMENT_SETTINGS, **kwargs
        )

    def sh_open_location_source_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LOCATION_SOURCE_SETTINGS, **kwargs)

    def sh_open_memory_card_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_MEMORY_CARD_SETTINGS, **kwargs)

    def sh_open_locale_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LOCALE_SETTINGS, **kwargs)

    def sh_open_search_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SEARCH_SETTINGS, **kwargs)

    def sh_open_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SETTINGS, **kwargs)

    def sh_open_account_sync_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ACCOUNT_SYNC_SETTINGS, **kwargs)

    def sh_open_display_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DISPLAY_SETTINGS, **kwargs)

    def sh_open_input_method_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_INPUT_METHOD_SETTINGS, **kwargs)

    def sh_open_sound_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SOUND_SETTINGS, **kwargs)

    def sh_open_wifi_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WIFI_SETTINGS, **kwargs)

    def sh_open_application_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_APPLICATION_SETTINGS, **kwargs)

    def sh_open_account_sync_settings_add_account(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_ACCOUNT_SYNC_SETTINGS_ADD_ACCOUNT, **kwargs
        )

    def sh_open_manage_applications_settings(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_MANAGE_APPLICATIONS_SETTINGS, **kwargs
        )

    def sh_open_sync_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SYNC_SETTINGS, **kwargs)

    def sh_open_dock_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DOCK_SETTINGS, **kwargs)

    def sh_open_add_account_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ADD_ACCOUNT_SETTINGS, **kwargs)

    def sh_open_security_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SECURITY_SETTINGS, **kwargs)

    def sh_open_device_info_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DEVICE_INFO_SETTINGS, **kwargs)

    def sh_open_wireless_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WIRELESS_SETTINGS, **kwargs)

    def sh_open_system_update_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SYSTEM_UPDATE_SETTINGS, **kwargs)

    def sh_open_manage_all_applications_settings(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_MANAGE_ALL_APPLICATIONS_SETTINGS, **kwargs
        )

    def sh_open_data_roaming_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DATA_ROAMING_SETTINGS, **kwargs)

    def sh_open_apn_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_APN_SETTINGS, **kwargs)

    def sh_open_user_dictionary_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_USER_DICTIONARY_SETTINGS, **kwargs)

    def sh_open_voice_input_output_settings(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_VOICE_INPUT_OUTPUT_SETTINGS, **kwargs
        )

    def sh_open_tts_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_TTS_SETTINGS, **kwargs)

    def sh_open_wifi_ip_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WIFI_IP_SETTINGS, **kwargs)

    def sh_open_web_search_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WEB_SEARCH_SETTINGS, **kwargs)

    def sh_open_bluetooth_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_BLUETOOTH_SETTINGS, **kwargs)

    def sh_open_airplane_mode_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_AIRPLANE_MODE_SETTINGS, **kwargs)

    def sh_open_internal_storage_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_INTERNAL_STORAGE_SETTINGS, **kwargs)

    def sh_open_accessibility_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ACCESSIBILITY_SETTINGS, **kwargs)

    def sh_open_quick_launch_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_QUICK_LAUNCH_SETTINGS, **kwargs)

    def sh_open_privacy_settings(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PRIVACY_SETTINGS, **kwargs)

    def sh_touch(self, path, **kwargs):
        folderpath = "/".join(path.split("/")[:-1])
        self.sh_mkdir(folderpath, **kwargs)
        return self.execute_sh_command(
            c.ADB_SHELL_TOUCH % strip_quotes_and_escape(path), **kwargs
        )

    @change_args_kwargs(
        args_and_function=(("src", _escape_filepath), ("dst", _escape_filepath))
    )
    def sh_rename(self, src, dst, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_RENAME_FILE % (src, dst), **kwargs)

    def sh_mkdir(self, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_MKDIR % strip_quotes_and_escape(path), **kwargs
        )

    def sh_is_folder(self, path, **kwargs):
        result, stde = self.execute_sh_command(c.ADB_SHELL_IS_FOLDER % path, **kwargs)
        isfolder = False
        try:
            if re.findall(rb"^\d+\s+\d+\s+d", result[0])[0]:
                isfolder = True
        except Exception:
            pass
        return isfolder

    def sh_is_file(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(c.ADB_SHELL_IS_FILE % path, **kwargs)[0][
                    0
                ].strip()
            )
        )

    def sh_swipe(self, x0, y0, x1, y1, t, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_SWIPE % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_sort_file_reverse(self, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_SORT_FILE_REVERSE % (file,), **kwargs
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_sort_file(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SORT_FILE % (file,), **kwargs)

    def sh_file_exists(self, path, **kwargs):
        stdout, stderr = self.execute_sh_command(
            c.ADB_SHELL_PATH_EXISTS % path, **kwargs
        )
        return bool(int(stdout[0].strip().decode("utf-8")))

    def copy_folder_to_other_location(self, src, dst):
        src = "/" + src.strip("/") + "/"
        dst = "/" + dst.strip("/") + "/"
        stdout1, stderr1 = self.execute_sh_command(f"mkdir -p {dst}")
        stdout2, stderr2 = self.execute_sh_command(
            f"(cd {src}; tar cf - .) | (cd {dst}; tar xvf -)"
        )
        stdoutall = self._all_outputlist_to_one(stdout1, stdout2)
        stderrall = self._all_outputlist_to_one(stderr1, stderr2)
        return [stdoutall, stderrall]

    def sh_get_rgb_value_at(self, x, y, width=None, height=None, **kwargs):
        if not width or not height:
            width, height = self.sh_get_resolution()

        stdout, stderr = self.execute_sh_command(
            c.ADB_SCRIPT_GET_RGB_VALUE_AT_COORD % (width, height, x, y), **kwargs
        )
        if stdout:
            stdout = stdout[0].strip().split(rb",")
            return int(stdout[2]), int(stdout[3]), int(stdout[4])

    @add_to_kwargs(
        v=(
            ("capture_stdout_stderr_first", True),
            ("wait_to_complete", 0.1),
        )
    )
    def get_all_activity_elements(self, as_pandas=False, **kwargs):
        @cache
        def findchi(ff):
            try:
                r0 = parse_pairs(string=ff, s1="{", s2="}", str_regex=False)
                datadict = {}
                maininfos = list(
                    {
                        k: v
                        for k, v in sorted(
                            r0.items(), key=lambda q: len(q[0]), reverse=True
                        )
                    }.items()
                )[0]
                otherdata = ff.split(maininfos[-1]["text"])
                t = maininfos[-1]["text"][1:-1] + " ÇÇÇÇÇÇ ÇÇÇÇÇÇ"
                infosplit = t.split(maxsplit=5)
                firstimesearch = infosplit[1]
                secondtimesearch = infosplit[2]
                datadict["START_X"] = -1
                datadict["START_Y"] = -1
                datadict["CENTER_X"] = -1
                datadict["CENTER_Y"] = -1
                datadict["AREA"] = -1
                datadict["END_X"] = -1
                datadict["END_Y"] = -1
                datadict["WIDTH"] = -1
                datadict["HEIGHT"] = -1
                datadict["START_X_RELATIVE"] = -1
                datadict["START_Y_RELATIVE"] = -1
                datadict["END_X_RELATIVE"] = -1
                datadict["END_Y_RELATIVE"] = -1

                try:
                    datadict["COORDS"] = infosplit[-3].rstrip("Ç ")
                except Exception:
                    datadict["COORDS"] = None
                try:
                    datadict["INT_COORDS"] = tuple(
                        map(int, (refi.findall(datadict["COORDS"])[0]))
                    )  # tuple(map(int, re.split(r'\W+', datadict['COORDS'])))
                except Exception:
                    datadict["INT_COORDS"] = ()
                try:
                    datadict["CLASSNAME"] = otherdata[0]
                except Exception:
                    datadict["CLASSNAME"] = None

                try:
                    datadict["HASHCODE"] = infosplit[-2].rstrip("Ç ")
                except Exception:
                    datadict["HASHCODE"] = None
                try:
                    datadict["ELEMENT_ID"] = infosplit[-1].rstrip("Ç ")
                except Exception:
                    datadict["ELEMENT_ID"] = None
                try:
                    datadict["MID"] = infosplit[0]
                except Exception:
                    datadict["MID"] = None
                try:
                    datadict["VISIBILITY"] = firstimesearch[0]
                except Exception:
                    datadict["VISIBILITY"] = None

                try:
                    datadict["FOCUSABLE"] = firstimesearch[1]
                except Exception:
                    datadict["FOCUSABLE"] = None

                try:
                    datadict["ENABLED"] = firstimesearch[2]
                except Exception:
                    datadict["ENABLED"] = None

                try:
                    datadict["DRAWN"] = firstimesearch[3]
                except Exception:
                    datadict["DRAWN"] = None

                try:
                    datadict["SCROLLBARS_HORIZONTAL"] = firstimesearch[4]
                except Exception:
                    datadict["SCROLLBARS_HORIZONTAL"] = None

                try:
                    datadict["SCROLLBARS_VERTICAL"] = firstimesearch[5]
                except Exception:
                    datadict["SCROLLBARS_VERTICAL"] = None

                try:
                    datadict["CLICKABLE"] = firstimesearch[6]
                except Exception:
                    datadict["CLICKABLE"] = None

                try:
                    datadict["LONG_CLICKABLE"] = firstimesearch[7]
                except Exception:
                    datadict["LONG_CLICKABLE"] = None

                try:
                    datadict["CONTEXT_CLICKABLE"] = firstimesearch[8]
                except Exception:
                    datadict["CONTEXT_CLICKABLE"] = None

                try:
                    datadict["PFLAG_IS_ROOT_NAMESPACE"] = secondtimesearch[0]
                except Exception:
                    datadict["PFLAG_IS_ROOT_NAMESPACE"] = None

                try:
                    datadict["PFLAG_FOCUSED"] = secondtimesearch[1]
                except Exception:
                    datadict["PFLAG_FOCUSED"] = None

                try:
                    datadict["PFLAG_SELECTED"] = secondtimesearch[2]
                except Exception:
                    datadict["PFLAG_SELECTED"] = None

                try:
                    datadict["PFLAG_PREPRESSED"] = secondtimesearch[3]
                except Exception:
                    datadict["PFLAG_PREPRESSED"] = None

                try:
                    datadict["PFLAG_HOVERED"] = secondtimesearch[4]
                except Exception:
                    datadict["PFLAG_HOVERED"] = None

                try:
                    datadict["PFLAG_ACTIVATED"] = secondtimesearch[5]
                except Exception:
                    datadict["PFLAG_ACTIVATED"] = None

                try:
                    datadict["PFLAG_INVALIDATED"] = secondtimesearch[6]
                except Exception:
                    datadict["PFLAG_INVALIDATED"] = None

                try:
                    datadict["PFLAG_DIRTY_MASK"] = secondtimesearch[7]
                except Exception:
                    datadict["PFLAG_DIRTY_MASK"] = None
                return maininfos, otherdata, datadict
            except Exception as fe:
                # sys.stderr.write(f'{fe}')
                return None

        allda = self.execute_sh_command(
            c.ADB_SHELL_GET_ALL_ACTIVITY_ELEMENTS, **kwargs
        )[0]

        allsi = list_split(
            allda,
            [
                i
                for i, x in enumerate(allda)
                if re.search(rb"^\s*(?:(?:View Hierarchy:)|(?:Looper))", x)
            ],
        )
        allsplits = [x for x in allsi if b"View Hierarchy:" in x[0]]
        allconvdata = []

        for elemtindex, a in enumerate(allsplits):
            di = indent2dict(
                b"".join(a[:]).decode("utf-8", "backslashreplace"), removespaces=True
            )
            allchildrendata = []
            hierachcounter = 0
            for f in fla_tu(di):
                allchildrendata.append([])

                hierachcounter += 1
                hierachcounter2 = 0
                for ff in f[1]:
                    try:
                        try:
                            maininfos2, otherdata2, datadict2 = findchi(ff)
                            datadict = deepcopy(datadict2)
                        except Exception:
                            continue
                        allchildrendata[-1].append(datadict)
                        allchildrendata[-1][-1]["START_X"] = sum(
                            [x["INT_COORDS"][0] for x in allchildrendata[-1]]
                        )
                        allchildrendata[-1][-1]["START_Y"] = sum(
                            [x["INT_COORDS"][1] for x in allchildrendata[-1]]
                        )
                        allchildrendata[-1][-1]["WIDTH"] = (
                            allchildrendata[-1][-1]["INT_COORDS"][2]
                            - allchildrendata[-1][-1]["INT_COORDS"][0]
                        )
                        allchildrendata[-1][-1]["HEIGHT"] = (
                            allchildrendata[-1][-1]["INT_COORDS"][3]
                            - allchildrendata[-1][-1]["INT_COORDS"][1]
                        )

                        allchildrendata[-1][-1]["END_X"] = (
                            allchildrendata[-1][-1]["START_X"]
                            + allchildrendata[-1][-1]["WIDTH"]
                        )
                        allchildrendata[-1][-1]["END_Y"] = (
                            allchildrendata[-1][-1]["START_Y"]
                            + allchildrendata[-1][-1]["HEIGHT"]
                        )
                        allchildrendata[-1][-1]["CENTER_X"] = allchildrendata[-1][-1][
                            "START_X"
                        ] + (allchildrendata[-1][-1]["WIDTH"] // 2)
                        allchildrendata[-1][-1]["CENTER_Y"] = allchildrendata[-1][-1][
                            "START_Y"
                        ] + (allchildrendata[-1][-1]["HEIGHT"] // 2)

                        allchildrendata[-1][-1]["AREA"] = (
                            allchildrendata[-1][-1]["HEIGHT"]
                            * allchildrendata[-1][-1]["WIDTH"]
                        )

                        allchildrendata[-1][-1]["START_X_RELATIVE"] = allchildrendata[
                            -1
                        ][-1]["INT_COORDS"][0]
                        allchildrendata[-1][-1]["START_Y_RELATIVE"] = allchildrendata[
                            -1
                        ][-1]["INT_COORDS"][1]
                        allchildrendata[-1][-1]["END_X_RELATIVE"] = allchildrendata[-1][
                            -1
                        ]["INT_COORDS"][2]
                        allchildrendata[-1][-1]["END_Y_RELATIVE"] = allchildrendata[-1][
                            -1
                        ]["INT_COORDS"][3]
                        allchildrendata[-1][-1]["IS_PARENT"] = True
                        allchildrendata[-1][-1]["VIEW_INDEX"] = elemtindex
                        allchildrendata[-1][-1]["HIERACHY_CLUSTER"] = hierachcounter
                        allchildrendata[-1][-1]["HIERACHY_SINGLE"] = hierachcounter2
                        hierachcounter2 = hierachcounter2 + 1

                    except Exception as e:
                        continue

            try:
                allchildrendata[-1][-1]["IS_PARENT"] = False
                allconvdata.append(deepcopy(allchildrendata))

            except Exception:
                pass
        if as_pandas:
            try:
                pd = importlib.import_module("pandas")
                alldfs = []
                for allchildrendataxx in allconvdata:
                    df = pd.concat(
                        [pd.DataFrame(x) for x in allchildrendataxx], ignore_index=True
                    )
                    alldfs.append(df)
                return pd.concat(alldfs, ignore_index=True)
            except Exception as e:
                sys.stderr.write(f"{e}\n")
                sys.stderr.flush()

        return allconvdata

    def get_activity_element_dump(
        self,
        defaultvalue="null",
        stripline=1,
        with_class=1,
        with_mid=1,
        with_hashcode=1,
        with_elementid=1,
        with_visibility=1,
        with_focusable=1,
        with_enabled=1,
        with_drawn=1,
        with_scrollbars_horizontal=1,
        with_scrollbars_vertical=1,
        with_clickable=1,
        with_long_clickable=1,
        with_context_clickable=1,
        with_pflag_is_root_namespace=1,
        with_pflag_focused=1,
        with_pflag_selected=1,
        with_pflag_prepressed=1,
        with_pflag_hovered=1,
        with_pflag_activated=1,
        with_pflag_invalidated=1,
        with_pflag_dirty_mask=1,
        **kwargs,
    ):
        scripttoexecute = (
            c.activityelements.replace(
                "ADD_TO_SCRIPT_REPLACE", str(c.activityelementsbasic)
            )
            .replace("WITH_CLASS_REPLACE", str(with_class))
            .replace("WITH_MID_REPLACE", str(with_mid))
            .replace("WITH_HASHCODE_REPLACE", str(with_hashcode))
            .replace("WITH_ELEMENTID_REPLACE", str(with_elementid))
            .replace("WITH_VISIBILITY_REPLACE", str(with_visibility))
            .replace("WITH_FOCUSABLE_REPLACE", str(with_focusable))
            .replace("WITH_ENABLED_REPLACE", str(with_enabled))
            .replace("WITH_DRAWN_REPLACE", str(with_drawn))
            .replace(
                "WITH_SCROLLBARS_HORIZONTAL_REPLACE", str(with_scrollbars_horizontal)
            )
            .replace("WITH_SCROLLBARS_VERTICAL_REPLACE", str(with_scrollbars_vertical))
            .replace("WITH_CLICKABLE_REPLACE", str(with_clickable))
            .replace("WITH_LONG_CLICKABLE_REPLACE", str(with_long_clickable))
            .replace("WITH_CONTEXT_CLICKABLE_REPLACE", str(with_context_clickable))
            .replace(
                "WITH_PFLAG_IS_ROOT_NAMESPACE_REPLACE",
                str(with_pflag_is_root_namespace),
            )
            .replace("WITH_PFLAG_FOCUSED_REPLACE", str(with_pflag_focused))
            .replace("WITH_PFLAG_SELECTED_REPLACE", str(with_pflag_selected))
            .replace("WITH_PFLAG_PREPRESSED_REPLACE", str(with_pflag_prepressed))
            .replace("WITH_PFLAG_HOVERED_REPLACE", str(with_pflag_hovered))
            .replace("WITH_PFLAG_ACTIVATED_REPLACE", str(with_pflag_activated))
            .replace("WITH_PFLAG_INVALIDATED_REPLACE", str(with_pflag_invalidated))
            .replace("WITH_PFLAG_DIRTY_MASK_REPLACE", str(with_pflag_dirty_mask))
            .replace("STRIPLINE_REPLACE", str(stripline))
            .replace("PRINT_CSV_REPLACE", str(int(1)))
            .replace("DEFAULTVALUE_REPLACE", str(defaultvalue))
        )

        return self.execute_sh_command(
            scripttoexecute,
            **kwargs,
        )[0]

    def get_uiautomator_element_dump(self, defaultvalue="null", **kwargs):
        scripttoexecute = (
            c.uiautomatorscript.replace(
                "ADD_TO_SCRIPT_REPLACE", str(c.uiautomatorscriptbasis)
            )
            .replace("PRINT_CSV_REPLACE", str(int(1)))
            .replace("DEFAULTVALUE_REPLACE", str(defaultvalue))
            .replace("SLEEPTIME_REPLACE", str(0))
        )
        return self.execute_sh_command(scripttoexecute, **kwargs)[0]

    @change_args_kwargs(
        args_and_function=(("file1", _escape_filepath), ("file2", _escape_filepath))
    )
    def compare_2_files(self, file1, file2, **kwargs):
        co = c.compare2files.replace("REPLACE_FILE_1", file1).replace(
            "REPLACE_FILE_2", file2
        )
        oi = self.execute_sh_command(co, **kwargs)
        return [
            [y[0], y[1].lstrip()]
            for y in [
                q.split(b": :::::::::::::::::::::::::::::::::::::::::::::::")
                for q in b"".join(oi[0]).split(
                    b"----------------------------------------------......."
                )
            ]
            if len(y) == 2
        ]

    def get_all_keyboards(self):
        return [
            x.strip().decode("utf-8")
            for x in self.execute_sh_command(c.ADB_SHELL_ALL_KEYBOARDS)[0]
        ]

    def install_adb_keyboard(
        self,
        url=r"https://github.com/senzhk/ADBKeyBoard/raw/master/ADBKeyboard.apk",
        **kwargs,
    ):
        purefile, filename, removefu = get_tmpfile(".apk")

        with requests.get(url) as r:
            keyb = r.content
            if r.status_code != 200:
                raise Exception(f"Could not download ADBKeyboard.apk from {url}")
            with open(filename, mode="wb") as f:
                f.write(keyb)
        kwargs = kwargs.copy()
        kwargs.update(invisibledict)
        subprocess.run(
            f"{self.adb_path} -s {self.device_serial} install {filename}",
            **kwargs,
        )

        while True:
            try:
                removefu()
                break
            except Exception:
                sleep(1)
                continue

    def get_active_keyboard(self, **kwargs):
        return (
            self.execute_sh_command(c.ADB_GET_DEFAULT_KEYBOARD, **kwargs)[0][0]
            .strip()
            .decode("utf-8")
        )

    def disable_keyboard(self, **kwargs):
        activekeyboard = self.get_active_keyboard(**kwargs)
        return self.execute_sh_command(
            c.ADB_DISABLE_KEYBOARD % activekeyboard,
            **kwargs,
        )

    def enable_keyboard(
        self, keyboard="com.android.inputmethod.latin/.LatinIME", **kwargs
    ):
        stdout1, stderr1 = self.execute_sh_command(
            c.ADB_ENABLE_KEYBOARD % keyboard, **kwargs
        )
        stdout2, stderr2 = self.execute_sh_command(
            c.ADB_SET_KEYBOARD % keyboard, **kwargs
        )
        allstdout = self._all_outputlist_to_one(
            stdout1,
            stdout2,
        )
        allstderr = self._all_outputlist_to_one(
            stderr1,
            stderr2,
        )
        return allstdout, allstderr

    def enable_adbkeyboard(self, **kwargs):
        return self.enable_keyboard(c.ADB_KEYBOARD_NAME, **kwargs)

    def is_keyboard_shown(self, **kwargs):
        q = b"".join(self.execute_sh_command(c.ADB_IS_KEYBOARD_SHOWN, **kwargs)[0])
        if b"mInputShown=true" in q:
            return True
        return False

    def input_text_adbkeyboard(self, text, **kwargs):
        charsb64 = base64.b64encode(text.encode("utf-8")).decode()
        return self.execute_sh_command(c.ADB_KEYBOARD_COMMAND % charsb64, **kwargs)

    def input_text(
        self,
        text,
        remove_accents=False,
        sleep_after_letter=(0, 0),
        input_device: valid_input_devices = "",
        **kwargs,
    ):
        if remove_accents:
            text = remove_accents_from_text(text)
        stdoutlist = []
        stderrlist = []
        splitext = split_text_in_chars_or_parts(text, sleep_after_letter)
        for c in splitext:
            cmd2send = format_input_command(input_device, action="text", command=c)

            stdout, stderr = self.execute_sh_command(
                cmd2send,
                **kwargs,
            )
            stdoutlist.extend(stdout)
            stderrlist.extend(stderr)
            sleep_random_time(sleep_after_letter)
        return [stdoutlist, stderrlist]

    def sh_input_dpad_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="dpad",
            ),
        )

    def sh_input_keyboard_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="keyboard",
            ),
        )

    def sh_input_mouse_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="mouse",
            ),
        )

    def sh_input_touchpad_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="touchpad",
            ),
        )

    def sh_input_gamepad_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="gamepad",
            ),
        )

    def sh_input_touchnavigation_text(
        self, text, sleeptime=(0.0, 0.0), remove_accents=False
    ):
        return self.input_text(
            text,
            sleeptime=sleeptime,
            remove_accents=remove_accents,
            input_device="touchnavigation",
        )

    def sh_input_joystick_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="joystick",
            ),
        )

    def sh_input_touchscreen_text(
        self, text, sleeptime=(0.0, 0.0), remove_accents=False
    ):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="touchscreen",
            ),
        )

    def sh_input_stylus_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="stylus",
            ),
        )

    def sh_input_trackball_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="trackball",
            ),
        )

    @change_args_kwargs(args_and_function=(("pathtoscan", _escape_filepath),))
    def get_file_dict(
        self,
        pathtoscan="/sdcard/",
        hidden=False,
        sepa="XXXÇÇÇXXX",
        wait_to_complete=1,
        **kwargs,
    ):
        # pathtoscan = strip_quotes_and_escape(pathtoscan)
        if hidden:
            add_to_find = ' -type f -iname ".*" '
        else:
            add_to_find = " "
        s1, s2 = self.execute_sh_command(
            f"""find {pathtoscan}{add_to_find}-exec stat -c "%i{sepa}%s{sepa}%A{sepa}%U{sepa}%G{sepa}%Y{sepa}%n" {{}} \;""",
            wait_to_complete=wait_to_complete,
            **kwargs,
        )
        splitfiles2 = [
            x.strip().decode("utf-8", "backslashreplace").split(sepa, maxsplit=6)
            for x in s1
        ]
        splitfiles = [(x[:6] + [x[-1].lstrip(".")]) for x in splitfiles2 if len(x) == 7]
        allfi = PunktDict({})
        for x in splitfiles:
            try:
                spli = (x[6]).strip("/").split("/")
                if len(spli) > 1:
                    fol = "/" + "/".join(spli[:-1])

                else:
                    fol = "/"
                fi = spli[-1]
                allfi[f"f{x[0]}"] = {}
                allfi[f"f{x[0]}"]["file_size"] = int(x[1])
                ditmp = get_file_rights(x[2])
                allfi[f"f{x[0]}"].update(ditmp)
                allfi[f"f{x[0]}"]["user_owner"] = x[3]
                allfi[f"f{x[0]}"]["group"] = x[4]
                allfi[f"f{x[0]}"]["modification_time"] = int(x[5])
                allfi[f"f{x[0]}"]["path"] = x[6]
                allfi[f"f{x[0]}"]["folder"] = fol
                allfi[f"f{x[0]}"]["pure_path"] = fi
                # allfi[f"f{x[0]}"]["is_hidden"] = "hidden"
                allfi[f"f{x[0]}"]["cat_file"] = FuExec(
                    fu=self.sh_cat_file, path=allfi[f"f{x[0]}"]["path"]
                )
                allfi[f"f{x[0]}"]["remove"] = FuExec(
                    fu=self.sh_remove_file, path=allfi[f"f{x[0]}"]["path"]
                )
                allfi[f"f{x[0]}"]["rename"] = FuExec(
                    self.sh_rename, allfi[f"f{x[0]}"]["path"]
                )
                allfi[f"f{x[0]}"]["grep"] = FuExec(
                    fu=self.sh_grep,
                    path=allfi[f"f{x[0]}"]["path"],
                    escape=True,
                    quote=False,
                    extended_regexp=True,
                    ignore_case=True,
                    recursively=False,
                    line_number=True,
                    invert_match=False,
                    files_with_matches=False,
                    count=False,
                )
            except Exception as fe:
                sys.stderr.write(f"{fe}\n")
        return allfi

    @change_args_kwargs(args_and_function=(("src", _escape_filepath),))
    def pull_folder(self, src, dst, **kwargs):
        kwargs.update({"disable_print_stdout": True, "wait_to_complete": 2})
        su = kwargs.get("su", False)
        if "su" in kwargs:
            del kwargs["su"]
        if not su:
            s1, s2 = self.execute_sh_command(f"(cd {src}; tar cf - .)", **kwargs)
        else:
            s1, s2 = self.execute_sh_command(
                f"(su -- cd {src}; su -- tar cf - .)", **kwargs
            )

        repla = self.format_output(s1)
        tar_data_bytes_io = io.BytesIO(repla)
        os.makedirs(dst, exist_ok=True)
        with tarfile.open(fileobj=tar_data_bytes_io, mode="r:") as tar:
            tar.extractall(path=dst)

    def sh_awk_calculator(self, expr, **kwargs):
        return float(
            self.execute_sh_command(c.ADB_SHELL_AWK_CALCULATOR % expr, **kwargs)[0][
                0
            ].strip()
        )

    import re

    @change_args_kwargs(args_and_function=(("src", _escape_filepath),))
    def sh_all_full_file_path_from_dir(self, folder, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_PURE_ABS_PATH_OF_FILES % folder, **kwargs
        )

    @change_args_kwargs(args_and_function=(("src", _escape_filepath),))
    def sh_pull_folder_with_cat(self, src, dst, **kwargs):
        folder2copy = "/" + src.strip("/ ") + "/"
        outfolder = dst.rstrip("/\\ ")

        so, se = self.sh_all_full_file_path_from_dir(folder2copy, **kwargs)
        for fi in so:
            try:
                file = fi.strip().decode("utf-8", "backslashreplace")
                shorterpath = file[len(folder2copy) :]
                outfol = os.path.normpath(
                    os.path.join(
                        outfolder, re.sub(r"[\\/]+", f"{os.sep}{os.sep}", shorterpath)
                    )
                )
                touch(outfol)
                catfi = self.sh_cat_file(file, **kwargs)
                with open(outfol, mode="wb") as fx:
                    fx.write(catfi)
            except Exception as fe:
                sys.stderr.write(f"\n{fe}\n")
                sys.stderr.flush()

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_get_treeview_of_folder(self, folder, **kwargs):
        if "print_stdout" not in kwargs:
            kwargs["print_stdout"] = False
        if "print_stderr" not in kwargs:
            kwargs["print_stderr"] = False

        s1, s2 = self.execute_sh_command(c.ADB_SHELL_GET_TREEVIEW % folder, **kwargs)
        s1 = [x.decode("utf-8", "backslashreplace").strip() for x in s1]
        return s1

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_get_lines_from_to_in_file(self, start, end, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_GET_LINES_IN_FILE % (int(start), int(end), path), **kwargs
        )

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_get_specific_line_from_a_file(self, no, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_SPECIFIC_LINE_IN_FILE % (int(no), path), **kwargs
        )

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_remove_specific_line_from_a_file(self, no, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_REMOVE_SPECIFIC_LINE_IN_FILE % (int(no), path), **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def chmod_all_files_in_folder(self, path, chmod, **kwargs):
        # newpath = strip_quotes_and_escape(path)
        return self.execute_sh_command(
            c.ADB_SHELL_CHMOD_ALL_FILES_IN_FOLDER % (path, int(chmod)), **kwargs
        )

    def sh_count_network_connections(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_COUNT_NETWORK_CONNECTIONS, **kwargs)

    @change_args_kwargs(args_and_function=(("path", _escape_filepath),))
    def sh_mkdir_and_cd(self, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CREATE_DICT_AND_CD % (path,), **kwargs
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_get_all_chmod_from_files_in_folder(self, folder, **kwargs):
        foldernew = folder.strip("/")
        return self.execute_sh_command(
            c.ADB_SHELL_GET_ALL_CHMOD_IN_FOLDER.replace("REPLACE_FOLDER", foldernew),
            **kwargs,
        )

    def sh_list_all_connected_ips(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ALL_CONNECTED_IPS, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_get_bios_info(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_BIOS_INFORMATION, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_wait_until_file_written_to_disk(self, file, interval, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CHECK_FILESIZE
            + f"\ncheck_if_finished_writing {file} {interval}\n",
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_ls_human_readable(self, folder, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_FILE_LISTING_HUMAN_READABLE.replace("REPLACEDIR", folder),
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_find_all_folder_full_path(self, folder, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_FIND_FULL_FILEPATH % folder, **kwargs
        )

    def sh_check_environment_vars(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_CHECK_ENVIRONMENT_VARS, **kwargs)

    def sh_printenv(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PRINTENV, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_freeze_proc(self, pid, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_FREEZE_PROC % str(int(pid)), **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_unfreeze_proc(self, pid, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_UNFREEZE_PROC % str(int(pid)), **kwargs
        )

    def sh_is_valid_float(self, n, **kwargs):
        cmd = (
            c.ADB_SHELL_IS_VALID_FLOAT
            + f"""
if [ $(count_char_in_string {n} .) -gt 1 ]; then
    echo 0
else
    if validfloat {n}; then
        echo 1
    else
        echo 0
    fi
fi
\n"""
        )
        so, se = self.execute_sh_command(cmd, **kwargs)
        return bool(int(so[0].strip()))

    def sh_is_valid_int(self, n, **kwargs):
        cmd = (
            c.ADB_SHELL_IS_VALID_INT
            + f"""
if validint {n}; then
    echo 1
else
    echo 0
fi\n"""
        )
        so, se = self.execute_sh_command(cmd, **kwargs)
        return bool(int(so[0].strip()))

    def rgb_values_of_area(
        self,
        start_x,
        start_y,
        end_x,
        end_y,
        screen_width=None,
        screen_height=None,
        **kwargs,
    ):
        if not screen_width or not screen_height:
            screen_width, screen_height = self.sh_get_resolution()
        if (
            start_x >= end_x
            or start_y >= end_y
            or end_x >= screen_width
            or end_y >= screen_height
        ):
            raise ValueError("No way to get that area")
        wholecommand = (
            c.RGB_VALUES_OF_AREA.replace("REPLACE_SCREEN_WIDTH", str(int(screen_width)))
            .replace("REPLACE_AREA_STARTX", str(int(start_x)))
            .replace("REPLACE_AREA_STARTY", str(int(start_y)))
            .replace("REPLACE_AREA_ENDX", str(int(end_x)))
            .replace("REPLACE_AREA_ENDY", str(int(end_y)))
        )
        kwargs.update({f"wait_to_complete": 0})
        stdo, stde = self.execute_sh_command(wholecommand, **kwargs)
        sizeofoutput = (end_x - start_x) * (end_y - start_y)
        while len(stdo) < sizeofoutput:
            sleep(0.001)
        finalv = []
        for v in stdo:
            finalv.append(clsrgb(*(int(x) for x in v.strip().split(maxsplit=4))))
        return finalv

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_hexdump(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_HEXDUMP % file, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_count_lines_in_file(self, file, **kwargs):
        stdo, stde = self.execute_sh_command(
            c.ADB_SHELL_COUNT_LINES_IN_FILE % file, **kwargs
        )
        fire = []
        for std in stdo:
            q, v = std.split(maxsplit=1)
            q = int(q)
            v = v.strip()
            fire.extend([q, v])
        return fire

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_reverse_file(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REVERSE_FILE % file, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_comment_out_line_in_file(self, n, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_COMMENT_OUT_LINE_IN_FILE % (n, file), **kwargs
        )

    def sh_tar_backup_of_folder_to_sdcard(
        self, foldertobackup, outputfolder="/sdcard/", **kwargs
    ):
        foldertobackup2 = strip_quotes_and_escape(foldertobackup)
        foldertobackupn = re.sub(r"\W+", "_", foldertobackup).strip("_")
        return self.execute_sh_command(
            f"""filename={outputfolder}{foldertobackupn}$(date "+%Y%m%d_%H%M%S").tar.gz\necho "$filename"\ntar -czvvf "$filename" {foldertobackup2}""",
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_ls_folder(self, folder="", **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LS_FOLDER % folder, **kwargs)

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_ls_fp(self, folder="", **kwargs):
        if folder:
            folder = "cd " + folder
        return self.execute_sh_command(
            c.ADB_SHELL_LS_FULL_PATH.replace("REPLACE_PATH", folder), **kwargs
        )

    def sh_get_md5_for_all_files(self, folder="", **kwargs):
        if folder:
            folder = "cd " + folder
        return self.execute_sh_command(
            c.ADB_SHELL_MD5_HASHES_FROM_ALL_FILES.replace("REPLACE_PATH", folder),
            **kwargs,
        )

    def sh_delete_all_files_in_folder_except_newest(self, folder="", **kwargs):
        if folder:
            folder = "cd " + folder
        return self.execute_sh_command(
            c.ADB_SHELL_DELETE_ALL_FILES_IN_FOLDER_EXCEPT_NEWEST.replace(
                "REPLACE_PATH", folder
            ),
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_list_extensions_in_folder(self, folder="", **kwargs):
        if folder:
            folder = "cd " + folder
        return self.execute_sh_command(
            c.ADB_SHELL_LIST_ALL_EXTENSIONS_IN_FOLDER.replace("REPLACE_PATH", folder),
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_ls_size(self, folder="", **kwargs):
        if folder:
            folder = "cd " + folder
        return self.execute_sh_command(
            c.ADB_LS_BY_FILESIZE.replace("REPLACE_PATH", folder), **kwargs
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_ls_by_mod_date(self, folder="", **kwargs):
        # path = strip_quotes_and_escape(folder)
        if folder:
            folder = "cd " + folder + "\n"
        return self.execute_sh_command(
            c.ADB_SHELL_LS_SORT_BY_MOD_DATE.replace("REPLACE_PATH", folder), **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_iptables(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_IPTABLES, **kwargs)

    def sh_get_kernel_infos(self, **kwargs):
        return re.split(
            r"^\s*$",
            b"".join(
                self.execute_sh_command(
                    c.ADB_SHELL_KERNEL_INFOS,
                    **kwargs,
                )[0]
            )
            .strip()
            .decode("utf-8", "backslashreplace"),
        )

    def sh_get_ip_from_host(self, url, **kwargs):
        stdo, stde = self.execute_sh_command(
            c.ADB_SHELL_GET_IP_FROM_HOST % url, **kwargs
        )
        if stdo:
            return stdo[0].strip().decode("utf-8", "backslashreplace")

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_newest_file_in_folder(self, folder, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_NEWEST_FILE_IN_FOLDER % folder, **kwargs
        )

    def sh_show_ips(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_IPS, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_print_file_with_linenumbers(self, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_PRINT_FILE_WITH_LINENUMBERS % file, **kwargs
        )

    def sh_abs_value_of_number(self, number, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_ABS_VALUE_OF_NUMBER % (int(number),), **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_get_details_from_pid(self, pid, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_GET_DETAILS_FROM_PROCESS % (int(pid),), **kwargs
        )

    def sh_netstat_tlnp(self):
        return [
            g
            for x in self.execute_sh_command(c.ADB_SHELL_NETSTAT_TLNP)[0]
            if len(g := (x.strip().split(maxsplit=6))) == 7
            and re.search(rb"^\d+", g[1])
        ]

    def sh_get_details_with_lsof(self, **kwargs):
        return self.execute_sh_command(c.ADB_GET_DETAILS_FROM_ALL_PROCS, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_kill_process_that_is_locking_a_file(self, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_KILL_A_PROCESS_THAT_IS_LOCKING_A_FILE % file, **kwargs
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_print_lines_of_file_with_at_least_length_n(self, file, n, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_PRINT_LINES_LONGER_THAN % (int(n), file), **kwargs
        )

    def sh_show_folders_in_PATH(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_FOLDER_IN_PATH_VAR, **kwargs)

    @change_args_kwargs(
        args_and_function=(("file1", _escape_filepath), ("file2", _escape_filepath))
    )
    def sh_compare_2_files(self, file1, file2, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_COMPARE_2_FILES % (file1, file2), **kwargs
        )

    def sh_substring_from_string(self, string, start, end, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_SUBSTRING_FROM_STRING % (string, start, end - start), **kwargs
        )

    def sh_rm_dry_run(self, args, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_RM_DRY_RUN % (args,), **kwargs)

    def sh_ipv4_interfaces(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_IPV4_INTERFACES, **kwargs)

    def sh_list_procs_cpu_usage(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_PROCS_CPU_USAGE, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_list_current_running_procs(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_CURRENT_RUNNING_PROCESSES, **kwargs)

    def sh_get_interfaces_and_mac(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_INTERFACES_AND_MAC, **kwargs)
        out = [
            g.decode("utf-8", "backslashreplace").split(maxsplit=1)
            for x in so
            if (g := x.strip())
        ]
        return out

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_list_files_newest_first(self, folder, **kwargs):
        so, se = self.execute_sh_command(
            c.ADB_SHELL_FILES_IN_FOLDER_NEWEST_FIRST % folder, **kwargs
        )
        return [
            y
            for y in [
                x.decode("utf-8", "backslashreplace").strip().split(maxsplit=6)
                for x in so
            ]
            if len(y) == 7
        ]

    @add_to_kwargs(
        v=(
            ("capture_stdout_stderr_first", True),
            ("global_cmd", False),
            ("wait_to_complete", 0.1),
        )
    )
    def sh_search_for_colors(self, colorlist, **kwargs):
        colorliststr = (
            "/ "
            + " | ".join([(to_rgb_hex(x)[2:] + "ff").lower() for x in colorlist])
            + " /"
        )

        so, se = self.execute_sh_command(
            c.ADB_SHELL_SEARCH_FOR_COLORS.replace("COLOR_REPLACE", colorliststr),
            **kwargs,
        )
        return [
            clsrgb(g[0], g[1], *convertcolor2rgb(g[2]))
            for x in so
            if len(g := x.strip().split(b",", maxsplit=2)) == 3
        ]

    def sh_upperstring_to_lowerstring(self, s, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_UPPER_TO_LOWER % (s,), **kwargs)

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_calculate_size_of_folders(self, folder, **kwargs):
        if folder:
            folder = "cd " + folder
        size = self.execute_sh_command(
            c.ADB_SHELL_SIZE_OF_FOLDERS.replace("REPLACE_PATH", folder), **kwargs
        )
        return [
            (int(g[0]), g[1])
            for x in size[0]
            if len(g := x.strip().split(maxsplit=1)) == 2
        ]

    def sh_number_of_cpus(self, **kwargs):
        return int(
            self.execute_sh_command(c.ADB_SHELL_NUMBER_OF_CPUS, **kwargs)[0][0].strip()
        )

    def sh_get_internal_ip_addr(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GET_INTERNAL_IPS, **kwargs)
        return [g.decode("utf-8", "backslashreplace") for x in so if (g := x.strip())]

    def sh_get_external_ip(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GET_EXTERNAL_IP, **kwargs)
        if so:
            return so[0].strip().decode("utf-8", "backslashreplace")
        else:
            so, se = self.execute_sh_command(c.ADB_SHELL_GET_EXTERNAL_IP2, **kwargs)
            if so:
                return so[0].strip().decode("utf-8", "backslashreplace")

    def sh_get_all_mac_addresses(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GET_ALL_MAC_ADDRESSES, **kwargs)
        return [g.decode("utf-8", "backslashreplace") for x in so if (g := x.strip())]

    def sh_number_of_tcp_connections(self, **kwargs):
        return int(
            self.execute_sh_command(c.ADB_SHELL_NUMBER_OF_TCP_CONNECTIONS, **kwargs)[0][
                0
            ].strip()
        )

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_append_line_to_file(self, line, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_APPEND_LINE_TO_FILE % (line, file), **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_dump_all_db_files(self, as_pandas=False, **kwargs):
        return self._sh_dump_db_files(
            c.ADB_SHELL_DUMP_ALL_DB_FILES, as_pandas=as_pandas, **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_dump_all_databases_in_data_data(self, as_pandas=False, **kwargs):
        return self._sh_dump_db_files(
            c.ADB_SHELL_DUMP_ALL_DATABASES_IN_DATA_DATA, as_pandas=as_pandas, **kwargs
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_delete_files_in_folder_older_than(
        self, folder, file_filter="*", date_distance="+1", **kwargs
    ):
        return self.execute_sh_command(
            c.ADB_SHELL_DELETE_FILES_IN_FOLDER_OLDER_THAN.replace(
                "REPLACEFOLDER", folder
            )
            .replace("REPLACEFILEFILTER", file_filter)
            .replace("REPLACEDISTANCE", date_distance),
            **kwargs,
        )

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_get_newest_file_in_folder_as_tar(
        self, folder, file_filter="*", tarpath="/ssdcard/newestar.tar.gz", **kwargs
    ):
        return self.execute_sh_command(
            c.ADB_SHELL_GET_NEWEST_FILE_IN_FOLDER_AS_TAR.replace(
                "REPLACEFOLDER", folder
            )
            .replace("REPLACEFILEFILTER", file_filter)
            .replace("REPLACETARPATH", tarpath),
            **kwargs,
        )

    def uiautomator_nice20(self, timeout=60, nice=True, su=True, as_pandas=False):
        niceadd = "nice -n -20 " if nice else ""
        dumpath = "/sdcard/window_dump.xml"
        self.sh_remove_file(dumpath)
        parser = etree.XMLParser()
        timeoutfinal = time.time() + timeout
        while True:
            if timeoutfinal < time.time():
                return {}
            try:
                so, se = self.execute_sh_command(
                    f"""
    getui(){{
    {niceadd}uiautomator dump 2>&1 >/dev/null
    }}
    getui
    cat {dumpath}""",
                    su=su,
                    capture_stdout_stderr_first=True,
                    wait_to_complete=0.1,
                    global_cmd=True,
                )
                #
                sox = [x for x in so if x.startswith(b"<?")][0]
                tree = etree.parse(
                    io.BytesIO(sox.rsplit(b">", maxsplit=1)[0] + b">"), parser
                )
                break
            except Exception as e:
                self.sh_remove_file(
                    dumpath,
                    su=su,
                    capture_stdout_stderr_first=True,
                    wait_to_complete=0.1,
                    global_cmd=True,
                )
                try:
                    print(so)
                except Exception:
                    pass
                time.sleep(0.5)
                sys.stderr.write(f"{e}")
                sys.stderr.flush()

        (
            ellis_children_hierachy,
            hashroot,
            hashcodesonly,
            ellis,
            ellis_parents,
            ellis_children,
        ) = _parsexmluiauto(tree)
        itemsdict = {}

        for key, item1 in ellis.items():
            item = item1["element"]
            try:
                allitems = (("tag", item.tag),) + tuple(item.items())

            except Exception:
                allitems = ((None, None),)
            itemsdict[key] = allitems
        rotation = -1
        itemsdictfinal = {}
        for k, v in itemsdict.items():
            newid = hashcodesonly[k]
            par = ellis_parents.get(k, None)
            chi = ellis_children.get(k, None)
            if su := {None, "rotation"}.intersection({n[0] for n in v}):
                if "rotation" in su:
                    for axs in v:
                        if axs[0] == "rotation":
                            rotation = int(axs[1])
                continue
            else:
                itemsdictfinal[newid] = dict(v)
            for key in itemsdictfinal[newid]:
                if itemsdictfinal[newid][key] == "true":
                    itemsdictfinal[newid][key] = True
                if itemsdictfinal[newid][key] == "false":
                    itemsdictfinal[newid][key] = False
            itemsdictfinal[newid]["rotation"] = rotation
            itemsdictfinal[newid]["all_parents"] = ()
            itemsdictfinal[newid]["all_children"] = ()
            itemsdictfinal[newid]["start_x"] = -1
            itemsdictfinal[newid]["start_y"] = -1
            itemsdictfinal[newid]["end_x"] = -1
            itemsdictfinal[newid]["end_y"] = -1
            itemsdictfinal[newid]["area"] = -1
            itemsdictfinal[newid]["center_x"] = -1
            itemsdictfinal[newid]["center_y"] = -1
            itemsdictfinal[newid]["width"] = -1
            itemsdictfinal[newid]["height"] = -1
            itemsdictfinal[newid]["ratio"] = -1
            try:
                itemsdictfinal[newid]["bounds"] = tuple(
                    map(
                        int,
                        flatten_everything(
                            numberreg.findall(itemsdictfinal[newid]["bounds"])
                        ),
                    )
                )
                itemsdictfinal[newid]["start_x"] = itemsdictfinal[newid]["bounds"][0]
                itemsdictfinal[newid]["start_y"] = itemsdictfinal[newid]["bounds"][1]
                itemsdictfinal[newid]["end_x"] = itemsdictfinal[newid]["bounds"][2]
                itemsdictfinal[newid]["end_y"] = itemsdictfinal[newid]["bounds"][3]
                itemsdictfinal[newid]["width"] = (
                    itemsdictfinal[newid]["end_x"] - itemsdictfinal[newid]["start_x"]
                )
                itemsdictfinal[newid]["height"] = (
                    itemsdictfinal[newid]["end_y"] - itemsdictfinal[newid]["start_y"]
                )
                itemsdictfinal[newid]["area"] = (
                    itemsdictfinal[newid]["width"] * itemsdictfinal[newid]["height"]
                )
                itemsdictfinal[newid]["center_x"] = itemsdictfinal[newid]["start_x"] + (
                    itemsdictfinal[newid]["width"] // 2
                )
                itemsdictfinal[newid]["center_y"] = itemsdictfinal[newid]["start_y"] + (
                    itemsdictfinal[newid]["height"] // 2
                )
                itemsdictfinal[newid]["ratio"] = (
                    itemsdictfinal[newid]["width"] / itemsdictfinal[newid]["height"]
                )

            except Exception:
                itemsdictfinal[newid]["bounds"] = ()
            try:
                if par:
                    itemsdictfinal[newid]["all_parents"] = tuple(
                        ii
                        for ii in (
                            sorted(
                                list(
                                    set(
                                        flatten_everything(
                                            [
                                                tuple([hashcodesonly[tt] for tt in t])
                                                for t in (
                                                    [
                                                        ellis_parents.get(k1, None)
                                                        for k1 in par
                                                    ]
                                                )
                                                if t
                                            ]
                                        )
                                    )
                                )
                            )
                        )
                        if ii not in [0, 1]
                    )
            except Exception:
                pass
            try:
                if chi:
                    itemsdictfinal[newid]["all_children"] = tuple(
                        ii
                        for ii in (
                            sorted(
                                list(
                                    set(
                                        flatten_everything(
                                            [
                                                tuple([hashcodesonly[tt] for tt in t])
                                                for t in (
                                                    [
                                                        ellis_children.get(k1, None)
                                                        for k1 in chi
                                                    ]
                                                )
                                                if t
                                            ]
                                        )
                                    )
                                )
                            )
                        )
                        if ii not in [0, 1]
                    )
            except Exception:
                pass
        if as_pandas:
            try:
                pd = importlib.import_module("pandas")
                return pd.DataFrame(itemsdictfinal).T
            except Exception as e:
                sys.stderr.write(f"{e}\n")
                sys.stderr.flush()
        return itemsdictfinal

    @add_to_kwargs(
        v=(
            ("su", True),
            ("global_cmd", False),
            ("wait_to_complete", 0),
            ("capture_stdout_stderr_first", False),
        )
    )
    def sh_disable_network_adapter(self, network, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_DISABLE_NETWORK_INTERFACE % network, **kwargs
        )

    def sh_get_linux_version(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LINUX_VERSION, **kwargs)

    def sh_get_cpu_info(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_CPU_INFO, **kwargs)

    def sh_get_mem_info(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_MEM_INFO, **kwargs)

    def sh_whoami(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WHOAMI, **kwargs)

    def sh_id(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_ID, **kwargs)

    def sh_get_user_groups(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_USER_GROUPS, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_get_filetype(self, file, **kwargs):
        return (
            self.execute_sh_command(c.ADB_SHELL_GET_FILETYPE % file, **kwargs)[0][0]
            .rsplit(b":", 1)[-1]
            .strip()
            .decode()
        )

    @add_to_kwargs(
        v=(
            ("su", True),
            ("global_cmd", False),
            ("wait_to_complete", 0),
            ("capture_stdout_stderr_first", False),
        )
    )
    def sh_enable_network_adapter(self, network, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_ENABLE_NETWORK_INTERFACE % network, **kwargs
        )

    @add_to_kwargs(v=(("su", True), ("print_stdout", False), ("wait_to_complete", 0)))
    def _sh_dump_db_files(self, command, as_pandas=False, **kwargs):
        dbfiles = self.execute_sh_command(command, **kwargs)
        sleep(10)
        oldlen = -1
        while oldlen < len(dbfiles[0]):
            oldlen = len(dbfiles[0])
            print(dbfiles)
            sleep(10)

        dumpdata = [
            b"path,table," + g.split(b",", maxsplit=2)[-1]
            for q in re.split(
                rb"^\s*Dumping\s*data\s*from.*:\s*$",
                b"".join(dbfiles[0]).replace(self.exitcommand.encode("utf-8"), b""),
                flags=re.M,
            )
            if (g := q.strip())
        ]
        if as_pandas:
            try:
                pd = importlib.import_module("pandas")
                pddfs = [
                    pd.read_csv(
                        io.StringIO(xx.decode("utf-8", "backslashreplace")),
                        header=0,
                        encoding="utf-8",
                        sep=",",
                        index_col=False,
                        encoding_errors="backslashreplace",
                        on_bad_lines="warn",
                        engine="python",
                    )
                    for xx in dumpdata
                ]
                return pddfs
            except Exception as e:
                sys.stderr.write(f"{e}\n")
        return dumpdata

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_cat_file_join_newlines(self, file, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CAT_FILE_JOIN_NEWLINES % file, **kwargs
        )

    def sh_check_open_ports(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_CHECK_OPEN_PORTS, **kwargs)

    def sh_show_touches(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHOW_TOUCHES, **kwargs)

    def sh_show_touches_not(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHOW_TOUCHES_NOT, **kwargs)

    @change_args_kwargs(args_and_function=(("folder", _escape_filepath),))
    def sh_count_files_in_folder(self, folder, **kwargs):
        folder = folder.rstrip("/") + "/"
        return int(
            self.execute_sh_command(
                c.ADB_SHELL_COUNT_FILES_IN_FOLDER % folder, **kwargs
            )[0][0].strip()
        )

    def sh_list_input_devices(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_INPUT_DEVICES, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_get_sendevent_input_devices(self, **kwargs):
        so, se = self.execute_sh_command(
            c.ADB_SHELL_GET_SENDEVENT_INPUT_DEVICES, **kwargs
        )
        return [
            x.strip().decode("utf-8", "backslashreplace").split(maxsplit=1) for x in so
        ]

    def sh_list_dev_input(self, **kwargs):
        return [
            f"/dev/input/{x.decode().strip()}"
            for x in self.sh_ls_folder("/dev/input", **kwargs)[0]
        ]

    def sh_get_all_props(self, **kwargs):
        return [
            [y[0].strip(b"[] ").decode(), y[1].strip(b"[]\n ").decode()]
            for y in [
                x.split(b": ", maxsplit=1)
                for x in self.execute_sh_command(c.ADB_SHELL_GETPROPS, **kwargs)[0]
            ]
        ]

    def sh_get_all_dumpsys_services(self, **kwargs):
        return [
            q.decode().strip()
            for q in self.execute_sh_command(
                c.ADB_SHELL_GET_ALL_SERVICES_FOR_DUMPSYS, **kwargs
            )[0]
        ]

    def sh_dumpsys_everything(self, **kwargs):
        alli = []
        alls = self.sh_get_all_dumpsys_services(**kwargs)
        for a in alls:
            sleep(0.1)
            alli.append([a, self.execute_sh_command(f"dumpsys {a} 2>/dev/null")[0]])
        return alli

    def sh_get_all_extra_options_from_dumpsys(self, **kwargs):
        extraoptions = []

        alli = []
        alls = self.sh_get_all_dumpsys_services(**kwargs)
        allcommands = []
        for a in alls:
            sleep(0.1)
            alli.append([self.execute_sh_command(f"dumpsys {a} 2>/dev/null")], **kwargs)
            sleep(0.1)
            alli[-1].append(self.execute_sh_command(f"dumpsys {a} -h"), **kwargs)
            allcommands.append(a)
        i = -1
        for p1, p2 in alli:
            i += 1
            if p1 != p2:
                if b" options:" in b"".join(p2[0]):
                    extraoptions.append([allcommands[i], p2])
        return extraoptions

    @add_to_kwargs(
        v=(
            ("su", True),
            ("wait_to_complete", 0),
            ("capture_stdout_stderr_first", False),
        )
    )
    def sh_sendevent_touch(self, x, y, inputdev, inputdevmax, width, height, **kwargs):
        command = (
            c.ADB_SHELL_SENDEVENT.replace("REPLACE_XCOORD", str(int(x)))
            .replace("REPLACE_YCOORD", str(int(y)))
            .replace("REPLACE_INPUTDEVICE", str(inputdev))
            .replace("REPLACE_MAX", str(int(inputdevmax)))
            .replace("REPLACE_DISPLAYWIDTH", str(int(width)))
            .replace("REPLACE_DISPLAYHEIGHT", str(int(height)))
        )
        return self.execute_sh_command(command, **kwargs)

    def sh_record_getevent(self, tmpfilegetevent="getevenfile"):
        tmpfilegetevent = tmpfilegetevent.strip("/")
        tmpfilegetevent = f"""/sdcard/{tmpfilegetevent}"""
        print(f"File will be saved: {tmpfilegetevent}")
        cmdcom = get_comspec()
        subprocess.run(
            f'''start {cmdcom} /k {self.adbpath} -s {self.device_serial} shell "getevent -t >'{tmpfilegetevent}'"''',
            shell=True,
        )
        return tmpfilegetevent

    def sh_record_getevent_as_binary_data(self, device, tmpfilegetevent):
        tmpfilegetevent = tmpfilegetevent.strip("/")
        tmpfilegetevent = f"""/sdcard/{tmpfilegetevent}"""
        print(f"File will be saved: {tmpfilegetevent}")
        device = device.rstrip("/")
        cmdcom = get_comspec()
        subprocess.run(
            f'''start {cmdcom} /k {self.adbpath} -s {self.device_serial} shell su -c "cat {device} > {tmpfilegetevent}"''',
            shell=True,
        )
        return tmpfilegetevent

    def convert_getevent_binary_data_to_decimal(self, path):
        sample_data = self.sh_cat_file(path)
        sample_data = sample_data[: (divmod(len(sample_data), 16)[0] * 16)]
        purebindata = []
        unpacked_data = [
            [struct.unpack("llHHI", g) + (g,)]
            if not purebindata.append((g := sample_data[i : i + 16]))
            else None
            for i in range(0, len(sample_data), 16)
        ]
        return purebindata, unpacked_data

    def sh_execute_sendevent_script(self, scriptpath):
        s = self.sh_cat_file(scriptpath)
        s = s.decode("utf-8")  # .splitlines()[:-6] + ['KILLME'])
        print(s)
        formatcmd = self.format_adb_command(s)
        p = subprocess.Popen(
            [self.adbpath, "-s", self.device_serial, "shell"],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            bufsize=0,
            **invisibledict,
        )
        p.stdin.write(formatcmd)
        p.stdin.close()
        for l in iter(p.stdout.readline, b""):
            print(l)
        try:
            p.stdout.close()
        except Exception:
            pass
        try:
            p.kill()
        except Exception:
            pass

        return p

    @add_to_kwargs(
        v=(
            ("su", True),
            ("capture_stdout_stderr_first", False),
            ("disable_print_stderr", True),
            ("wait_to_complete", 0),
        )
    )
    def sh_getevent_capture(self, device, iterations=1000, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_GETEVENT_WITH_COORDS.replace(
                "REPLACE_DEVICE", str(device)
            ).replace("REPLACE_ITER", str(iterations)),
            **kwargs,
        )

    def save_a_stuck_shell(self, **kwargs):
        kwargs.update(invisibledict)
        fo = self.format_adb_command(c.ADB_SHELL_SAVE_THE_SHELL)
        proc = subprocess.Popen(
            f'{self.adbpath} -s {self.device_serial} shell "{fo.decode().strip()}"',
            **kwargs,
        )
        try:
            outs, errs = proc.communicate(timeout=15)
        except Exception:
            proc.kill()
            outs, errs = proc.communicate()
        return outs, errs

    def get_all_sendevent_keys(self):
        s1 = self.sh_cat_file("/system/bin/toolbox", wait_to_complete=2, su=True)
        lines = re.split(b"\n", s1)
        lines = [line.decode("utf-8", "ignore").strip("\x00") for line in lines]
        output_lines = []
        key_reserved_index = False
        for i, line in enumerate(lines):
            if "KEY_RESERVED" in line:
                key_reserved_index = True
            if key_reserved_index:
                output_lines.extend(line.split("\x00"))
        output_lines2 = re.split("[^A-Z0-9_\\n]", "\n".join(output_lines))
        output_lines3 = [
            g for x in output_lines2 if len(g := x.strip()) > 4 and "_" in x
        ]
        output_lines4 = [
            [h for g in x.splitlines() if (len(h := g.strip().strip("_")) > 1)]
            for x in output_lines3
        ]
        output_lines5 = [x for x in output_lines4 if len(x) > 1]
        allevents = defaultdict(list)
        ii = 0
        for l in output_lines5:
            i = 0
            for ll in l:
                if ll in ["EV_VERSION"]:
                    continue
                if i == 83:
                    i = i + 1
                if ll == "BTN_MISC":
                    i = i + 10
                    continue
                allevents[ii].append([i, ll])
                i = i + 1

            ii += 1
        return allevents

    @add_to_kwargs(v=(("su", False), ("wait_to_complete", 0)))
    def exit_from_su_shell(self, **kwargs):
        ju = b""
        while b"REGULAR" not in ju:
            so, se = self.execute_sh_command(
                c.ADB_SHELL_EXIT_FROM_SU.replace("REPLACE_EXIT", self.exitcommand),
                **kwargs,
            )
            sleep(1)
            ju = b"".join(so) + b"".join(se)

    def sh_get_file_extension(self, path, **kwargs):
        so, se = self.execute_sh_command(
            c.ADB_SHELL_GET_FILE_EXTENSION.replace("FILEPATH", path), **kwargs
        )
        if so:
            return so[0].strip().decode()

    def sh_test_directory(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(c.ADB_SHELL_TEST_DIRECTORY % path, **kwargs)[0][
                    0
                ].strip()
            )
        )

    def sh_test_exists_in_any_form(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(
                    c.ADB_SHELL_TEST_EXISTS_IN_ANY_FORM % path, **kwargs
                )[0][0].strip()
            )
        )

    def sh_test_executable(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(c.ADB_SHELL_TEST_EXECUTABLE % path, **kwargs)[
                    0
                ][0].strip()
            )
        )

    def sh_test_regular_file(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(c.ADB_SHELL_TEST_REGULAR_FILE % path, **kwargs)[
                    0
                ][0].strip()
            )
        )

    def sh_test_readable(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(c.ADB_SHELL_TEST_READABLE % path, **kwargs)[0][
                    0
                ].strip()
            )
        )

    def sh_test_named_pipe(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(c.ADB_SHELL_TEST_NAMED_PIPE % path, **kwargs)[
                    0
                ][0].strip()
            )
        )

    def sh_test_block_device(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(c.ADB_SHELL_TEST_BLOCK_DEVICE % path, **kwargs)[
                    0
                ][0].strip()
            )
        )

    def sh_test_character_device(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(
                    c.ADB_SHELL_TEST_CHARACTER_DEVICE % path, **kwargs
                )[0][0].strip()
            )
        )

    def sh_test_link(self, path, **kwargs):
        return bool(
            int(
                self.execute_sh_command(
                    c.ADB_SHELL_TEST_CHARACTER_LINK % path, **kwargs
                )[0][0].strip()
            )
        )

    def sh_scrape_html(self, file_path, mainblocks, subblocks, **kwargs):
        try:
            cmd = (
                "cat %s | sed -r 's/(" % strip_quotes_and_escape(file_path)
                + (q := "|".join([h for h in mainblocks]))
                + f")/\\n\\1/g' | grep -E '({q})' | sed -r 's/("
                + "|".join([h for h in subblocks])
                + ")/\\n\\1/g' | grep -E "
                "'(" + "|".join([h for h in subblocks + mainblocks]) + ")'"
            )
            so, se = self.execute_sh_command(cmd, **kwargs)
            decoded = b"".join(so).decode("utf-8", "backslashreplace").strip()
            r = [
                v.start()
                for v in (
                    re.finditer("(" + "|".join([h for h in mainblocks]) + ")", decoded)
                )
            ]
            b2 = "(" + "|".join([h for h in subblocks + mainblocks]) + ")"
            result1 = list_split(l=decoded, indices_or_sections=r)
            result2 = [
                [j for j in q if j]
                for q in [
                    list_split(
                        l=ri,
                        indices_or_sections=[y.start() for y in re.finditer(b2, ri)],
                    )
                    for ri in result1
                    if ri
                ]
            ]
            return result2
        except Exception as fe:
            sys.stderr.write(f"{fe}")
            sys.stderr.flush()
            return []

    def sh_cd_and_search_string_in_files(self, path, query, **kwargs):
        path = strip_quotes_and_escape(path)

        so, se = self.execute_sh_command(
            c.ADB_SHELL_GOTO_DIR_AND_SEARCH_FOR_STRING % (f"cd {path}", query), **kwargs
        )
        if so:
            return [g for x in so if len(g := x.strip().split(b":", maxsplit=2)) == 3]

    def sh_get_md5sum(self, path, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_MD5SUM % path, **kwargs)
        if so:
            return so[0].strip().decode()

    def sh_realpath(self, path, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_REALPATH % path, **kwargs)
        if so:
            return so[0].strip().decode()

    def sh_dirname(self, path, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_DIRNAME % path, **kwargs)
        if so:
            return so[0].strip().decode()

    def sh_rename_file_to_md5(self, path, **kwargs):
        so, se = self.execute_sh_command(
            c.ADB_SHELL_RENAME_FILE_TO_MD5.replace("FINOPATH", path), **kwargs
        )
        if so:
            return so[0].strip().decode()

    def sh_get_size_of_terminal(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GET_SIZE_OF_TERMINAL, **kwargs)
        if so:
            return list(map(int, so[0].strip().split(b" x ")))

    # @add_to_kwargs(v=(("global_cmd", False),))

    def sh_get_file_with_tstamp(self, filename, ext, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_GET_FILE_WITH_TIMESTAMP.replace(
                "REPLACE_FILENAME", filename
            ).replace("REPLACE_EXT", ext),
            **kwargs,
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_disable_input_device(self, device, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_DISABLE_INPUT_DEVICE % device, **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_memory_dump(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SYSTEM_MEMORY_DUMP, **kwargs)

    def sh_get_cwd_of_procs(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_CWD_OF_PROCS, **kwargs)

    def sh_get_install_date(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_INSTALL_DATE, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_get_audio_playing_procs(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_AUDIO_PLAYING_PROCS, **kwargs)

    def sh_get_procs_with_open_connections(self, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_PROCS_WITH_OPEN_CONNECTIONS, **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_force_idle(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_FORCE_IDLE, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_unforce_idle(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_UNFORCE_IDLE, **kwargs)

    @add_to_kwargs(v=(("su", True),))
    def sh_nice(self, cmd, value=-19, **kwargs):
        return self.execute_sh_command(
            c.ADB_UIAUTOMATOR_NICE20 % (value, cmd), **kwargs
        )

    @add_to_kwargs(v=(("su", True),))
    def sh_get_current_focus(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_CURRENT_FOCUS, **kwargs)
        try:
            return so[0].decode().strip()
        except Exception as e:
            sys.stderr.write(f"{e}")
            sys.stderr.flush()

    def sh_grep_proc_top(self, grep, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_TOP_ALL_PIDS_FROM_PROC_GREP.replace("REPLACEGREP", grep),
            **kwargs,
        )

    def sh_am_i_su(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_AM_I_SU, **kwargs)
        if so:
            sostri = so[0].strip()
            return True if sostri == b"True" else False

    def sh_get_all_possible_activities(self, **kwargs):
        input_data = b"".join(
            self.execute_sh_command(c.ADB_SHELL_GET_ALL_POSSIBLE_ACTIVITIES, **kwargs)[
                0
            ][1:]
        ).decode("utf-8")
        return indent2dict(input_data, removespaces=True)

    @add_to_kwargs(v=(("su", True),))
    def sh_apps_using_internet(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_APPS_USING_INTERNET, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    @add_to_kwargs(v=(("su", True),))
    def sh_chmod_x(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_CHMOD_X % file, **kwargs)

    @change_args_kwargs(args_and_function=(("file", _escape_filepath),))
    def sh_execute_sh_script(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_EXECUTE_SH_SCRIPT % file, **kwargs)

    def sh_which_a(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WHICH_A % file, **kwargs)

    def sh_type(self, file, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_TYPE % file, **kwargs)

    @change_args_kwargs(
        args_and_function=(("src", _escape_filepath), ("dst", _escape_filepath))
    )
    @add_to_kwargs(v=(("su", True),))
    def sh_create_symbolic_link(self, src, dst, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CREATE_SYMBOLIC_LINK % (src, dst), **kwargs
        )

    def sh_show_used_diskspace(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SHOW_USED_DISKSPACE, **kwargs)

    def sh_show_used_memory(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SHOW_USED_MEMORY, **kwargs)

    def sh_reboot(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_REBOOT, **kwargs)

    def sh_jobs(self, **kwargs):
        return [
            [int(u[0].strip()), (u[1].strip())]
            for u in (
                zip(
                    self.execute_sh_command(c.ADB_SHELL_JOBS_P, **kwargs)[0],
                    self.execute_sh_command(c.ADB_SHELL_JOBS, **kwargs)[0],
                )
            )
        ]

    def sh_goto_next_sibling_folder(self, **kwargs):
        so, se = self.execute_sh_command(c.ADB_SHELL_GOTO_NEXT_SIBLING_FOLDER, **kwargs)
        if so:
            return so[0].strip()

    def sh_chr(self, char, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CHR.replace("REPLACE_CHAR", char), **kwargs
        )

    def parse_sendevent_keys(self):
        d1 = [
            "/dev/input/" + x.strip().decode()
            for x in self.sh_ls_folder("/dev/input")[0]
        ]
        d2 = {x: b"".join(self.execute_sh_command(f"getevent -p {x}")[0]) for x in d1}
        keysplitreg = re.compile(rb"\s+\b(\w+)\b\s+\(([^\)]+)\):")
        sireg = re.compile(rb"\b[a-f0-9]{4}\b")
        keynamereg = re.compile(b"^[A-Z_0-9]+$")
        did = {}
        for key, item in d2.items():
            did[key] = defaultdict(list)
            keysplit = keysplitreg.split(item)[1:]
            for i, k in enumerate(keysplit):
                try:
                    si = sireg.findall(k.strip())
                    if si:
                        did[key][activekey].append(si)
                    else:
                        if keynamereg.findall(k.strip()):
                            activekey = k.strip()
                except Exception:
                    break

        # pudi = PunktDict({})
        for key, item in did.items():
            devi = key.split("/")[-1]
            self.keyevents_sendevent[devi] = {}
            for key2, item2 in item.items():
                try:
                    eventtype = int(b"0x" + item2[0][0], base=16)
                except Exception as e:
                    sys.stderr.write(f"{e}")
                    sys.stderr.flush()
                    continue
                for key3 in item2[1]:
                    try:
                        key3 = int(b"0x" + key3, base=16)
                        downi = get_event_labels(eventtype, key3, value=1)
                        if "Unknown" in downi:
                            continue
                        keyeventtopress = downi[0]
                        wholecommand = f"""sendevent {key} {eventtype} {key3} 1\nsendevent {key} 0 0 0\nsleep %f\nsendevent {key} {eventtype} {key3} 0\nsendevent {key} 0 0 0"""
                        self.keyevents_sendevent[devi][
                            keyeventtopress
                        ] = SendEventKeyPress(
                            self.execute_sh_command,
                            wholecommand,
                            stripri=f"{key} {eventtype} {key3}",
                        )
                    except Exception as e:
                        sys.stderr.write(f"{e}")
                        sys.stderr.flush()

    def execute_adb_command(self, cmd, withid=True, **kwargs):
        if kwargs.get("to_83", False):
            if isinstance(cmd, str):
                cmd = convert_path_to_short(cmd)
            else:
                cmd = [convert_path_to_short(x) for x in cmd]
        if isinstance(cmd, list):
            cmd = " ".join(cmd)
        if withid:
            cmd = f"{self.adbpath} -s {self.device_serial} " + cmd
        else:
            cmd = f"{self.adbpath} " + cmd
        p = subprocess.run(cmd, capture_output=True, **invisibledict)
        return [p.stdout.splitlines(), p.stderr.splitlines()]

    def adb_reconnect(self):
        so, se = self.execute_adb_command(c.ADBEXE_RECONNECT, withid=True)
        timeout = time.time() + 3
        while self.isalive():
            if time.time() > timeout:
                break
            sleep(1)
        self.kill_proc()
        sleep(2)
        self._reconnect_device()
        return so, se

    def adb_root(self):
        so, se = self.execute_adb_command(c.ADBEXE_ROOT, withid=True)
        timeout = time.time() + 3
        while self.isalive():
            if time.time() > timeout:
                break
            sleep(1)
        if not self.isalive():
            self.kill_proc()
            sleep(2)
            self._reconnect_device()
        return so, se

    def adb_unroot(self):
        so, se = self.execute_adb_command(c.ADBEXE_UNROOT, withid=True)
        timeout = time.time() + 3
        while self.isalive():
            if time.time() > timeout:
                break
            sleep(1)
        self.kill_proc()
        sleep(2)
        self._reconnect_device()
        return so, se

    def adb_remount_as_rw(self):
        self.adb_root()
        so, se = self.execute_adb_command("remount")
        return so, se

    def adb_install(
        self,
        path,
        grand_permissions=True,
        replace=True,
        allow_test=True,
        allow_downgrade=False,
        to_83=True,
    ):
        args = []
        if replace:
            args.append("-r")
        if allow_test:
            args.append("-t")
        if allow_downgrade:
            args.append("-d")
        if grand_permissions:
            args.append("-g")
        if to_83:
            path = get_short_path_name(path)
        argslist = " ".join(args).strip()
        if not argslist:
            argslist = " "
        else:
            argslist = f" {argslist} "
        return self.execute_adb_command(f"install{argslist}{path}", withid=True)

    def adb_uninstall(self, package):
        return self.execute_adb_command(c.ADBEXE_UNINSTALL % package, withid=True)

    def adb_show_forwarded_ports(self):
        return self.execute_adb_command(c.ADBEXE_SHOW_FORWARDED_PORTS, withid=True)

    def adb_show_reversed_ports(self):
        return self.execute_adb_command(c.ADBEXE_SHOW_REVERSED_PORTS, withid=True)

    def adb_uinstall(self, package):
        return self.execute_adb_command(c.ADBEXE_UNINSTALL % package, withid=True)

    def write(
        self,
        cmd,
        wait_to_complete=0.1,
        convert_to_83=False,
        exitcommand="",
        commandtimeout=0,
    ):
        try:
            return super().write(
                cmd,
                wait_to_complete=wait_to_complete,
                convert_to_83=convert_to_83,
                exitcommand=exitcommand,
                commandtimeout=commandtimeout,
            )
        except OSError:
            self._reconnect_device()
            return super().write(
                cmd,
                wait_to_complete=wait_to_complete,
                convert_to_83=convert_to_83,
                exitcommand=exitcommand,
                commandtimeout=commandtimeout,
            )
            # raise e

    def _reconnect_device(self):
        subprocess.run(
            [self.adb_path, c.ADBEXE_CONNECT, self.device_serial], **invisibledict
        )
        super().__init__(
            self.adb_path,
            self.device_serial,
            use_busybox=self.use_busybox,
            connect_to_device=True,
            invisible=self.invisible,
            print_stdout=self.print_stdout,
            print_stderr=self.print_stderr,
            limit_stdout=self.limit_stdout,
            limit_stderr=self.limit_stderr,
            limit_stdin=self.limit_stdin,
            convert_to_83=self.convert_to_83,
            wait_to_complete=self.wait_to_complete,
            flush_stdout_before=self.flush_stdout_before,
            flush_stdin_before=self.flush_stdin_before,
            flush_stderr_before=self.flush_stderr_before,
            exitcommand=self.exitcommand,
            capture_stdout_stderr_first=self.capture_stdout_stderr_first,
        )

    def get_all_devices(self, **kwargs):
        alld = []
        kwargs.update({"to_83": False})
        try:
            return [
                q.decode().strip().split(maxsplit=2)
                for q in self.execute_adb_command(c.ADBEXE_DEVICES, withid=False)[0][
                    1:-1
                ]
            ]
        except Exception as fe:
            print(fe)
        return alld

    def adb_forward_port(self, port_device, port_pc):
        return self.execute_adb_command(
            c.ADBEXE_FORWARD_PORT % (str(int(port_device)), str(int(port_pc))),
            withid=True,
        )

    def adb_reverse_port(self, port_device, port_pc):
        return self.execute_adb_command(
            c.ADBEXE_REVERSE_PORT % (str(int(port_device)), str(int(port_pc))),
            withid=True,
        )

    def adb_remove_forwarded_port(self, port):
        return self.execute_adb_command(
            c.ADBEXE_REMOVE_FORWARDED_PORT % str(int(port)), withid=True
        )

    def adb_remove_reversed_port(self, port):
        return self.execute_adb_command(
            c.ADBEXE_REMOVE_REVERSED_PORT % str(int(port)), withid=True
        )

    def adb_pull(self, path_device, path_pc, escape_path=True):
        os.makedirs(path_pc, exist_ok=True)
        if escape_path:
            path_device = strip_quotes_and_escape(path_device)
        path_pc = f'"{path_pc}"'

        return self.execute_adb_command(
            c.ADBEXE_PULL % (path_device, path_pc), withid=True
        )

    def adb_push(self, path_pc, path_device, escape_path=True, to_83=False):
        if escape_path:
            path_device = strip_quotes_and_escape(path_device)
        self.sh_mkdir(path_device, exist_ok=True)
        if to_83:
            path_pc = get_short_path_name(path_pc)
        path_pc = f'"{path_pc}"'

        return self.execute_adb_command(
            c.ADBEXE_PUSH % (path_pc, path_device), withid=True
        )

    def netcatcopy(
        self,
        outputfolder,
        foldertodownload,
        tarpath="tar.exe",
        netcatpath="nc.exe",
        tmpfilename="taradbdownload.tar",
        removetar=True,
    ):
        r"""
        Copy files from a remote Android device to a local folder using netcat and tar.

        This function allows you to copy files from a specified folder on an Android device
        to a local directory on your computer. It uses netcat (nc) and tar to efficiently transfer
        and package the files.

        Args:
            outputfolder (str): The local directory where the copied files will be saved.
            foldertodownload (str): The path to the folder on the Android device that you want to copy.
            tarpath (str, optional): The path to the tar executable (default is "tar.exe").
            netcatpath (str, optional): The path to the netcat executable (default is "nc.exe").
            tmpfilename (str, optional): The temporary filename for the tar archive (default is "taradbdownload.tar").
            removetar: Whether to remove the tar file
            su (bool, optional): Whether to run commands with superuser privileges (default is True).

        Returns:
            list: A list of file paths that were successfully copied.

        Raises:
            OSError: If the specified tar or netcat executables are not found.
            FileNotFoundError: If the shell (cmd.exe) is not found.

        Note:
            This function requires ADB (Android Debug Bridge) and busybox to be installed on the
            Android device, and cygwin (with tar.exe and nc.exe) on Windows.

        Example:
            To copy files from an Android device to a local folder:
            copiedfiles self.netcatcopy(
            tarpath="tar.exe",
            netcatpath="nc.exe",
            outputfolder="c:\\testbackuo2", # will be created
            foldertodownload="/data/data/com.instagram.lite/",
            tmpfilename="taradbdownload.tar",
            su=True,
        )

        """
        su = True
        if not os.path.exists(tarpath):
            tarpath = shutil.which(tarpath)
            if not tarpath:
                raise OSError("tar.exe not found")
        if not os.path.exists(netcatpath):
            netcatpath = shutil.which(netcatpath)
            if not netcatpath:
                raise OSError("nc.exe not found")

        comspec = os.environ.get("ComSpec")
        if not comspec:
            system_root = os.environ.get("SystemRoot", "")
            comspec = os.path.join(system_root, "System32", "cmd.exe")
            if not os.path.isabs(comspec):
                raise FileNotFoundError(
                    "shell not found: neither %ComSpec% nor %SystemRoot% is set"
                )
        wholepath = os.path.join(outputfolder, tmpfilename)
        os.makedirs(outputfolder, exist_ok=True)
        port = get_free_port()

        self.adb_forward_port(self, port, port)
        so, se = self.execute_sh_command(
            f'cd {foldertodownload} && $(which busybox) nc -l -p {port} -e $(which busybox) tar -c . && echo "{self.exitcommand}"',
            wait_to_complete=0,
            capture_stdout_stderr_first=False,
            su=su,
        )
        p = subprocess.Popen(
            [comspec],
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            **invisibledict,
        )
        joinedpath = os.path.normpath(os.path.join(outputfolder, tmpfilename))
        p.stdin.write(f"{netcatpath} 127.0.0.1 {port} > {joinedpath}\n".encode())
        p.stdin.close()
        exitcommandbin = self.exitcommand.encode()

        while exitcommandbin not in b"".join(so):
            sleep(0.1)
            continue
        while True:
            try:
                os.rename(wholepath, wholepath)
                break
            except Exception:
                sleep(0.1)
                continue
        p.kill()
        pn = subprocess.run(
            f"{tarpath} -xvf {tmpfilename}",
            cwd=outputfolder,
            **invisibledict,
            capture_output=True,
        )
        if removetar:
            try:
                os.remove(wholepath)
            except Exception:
                pass
        self.adb_remove_forwarded_port(port)
        return [x for x in pn.stdout.splitlines() if x.startswith(b"./")]

    @add_to_kwargs(v=(("global_cmd", False),))
    def remove_stderr_stdout_tmpfiles_on_sdcard(self, **kwargs):
        self.execute_sh_command(c.ADB_SHELL_REMOVE_STDERR_TMPFILES, **kwargs)
        self.execute_sh_command(c.ADB_SHELL_REMOVE_STDOUT_TMPFILES, **kwargs)
        self.execute_sh_command(c.ADB_SHELL_REMOVE_STDERR_TMPFILES_G, **kwargs)
        self.execute_sh_command(c.ADB_SHELL_REMOVE_STDOUT_TMPFILES_G, **kwargs)

    def sh_show_fragments_on_screen(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_SHOW_FRAGMENTS_ON_SCREEN, **kwargs)

    def sh_get_settings_manager(self, **kwargs):
        allcats = ["secure", "system", "global"]
        pdi = PunktDict()
        for ca in allcats:
            pdi[ca] = PunktDict(
                dict(
                    [
                        (
                            cc[0],
                            {
                                "value": cc[1],
                                "get_value": PartialAdb(
                                    self.execute_sh_command,
                                    callback=format_partial_result,
                                    funame=f"()",
                                    args=(f"settings get {ca} {cc[0]}",),
                                    kwargs=kwargs,
                                ),
                                "put_value": PartialAdb(
                                    self.execute_sh_command,
                                    callback=format_partial_result,
                                    funame=f"()",
                                    args=(f"settings put {ca} {cc[0]}",),
                                    kwargs=kwargs,
                                ),
                            },
                        )
                        for cc in [
                            f
                            for f in [
                                x.decode("utf-8", "backslashreplace")
                                .strip()
                                .split("=", maxsplit=1)
                                for x in self.execute_sh_command(f"settings list {ca}")[
                                    0
                                ]
                            ]
                            if len(f) == 2
                        ]
                    ]
                )
            )

        return pdi

    @add_to_kwargs(v=(("su", True),))
    def sh_get_getprop_setprop_manager(self, **kwargs):
        def get_va(kvz, j):
            try:
                return kvz[j][2]
            except Exception:
                return None

        kvz = [
            [
                SettingsChanger(
                    p1=PartialAdb(
                        self.execute_sh_command,
                        callback=format_partial_result,
                        funame=f"()",
                        args=(f"setprop {z[0][1:-1]}",),
                        kwargs=kwargs,
                    ),
                    p2=PartialAdb(
                        self.execute_sh_command,
                        callback=format_partial_result,
                        funame=f"()",
                        args=(f'setprop {z[0][1:-1].split(".", maxsplit=1)[-1]}',),
                        kwargs=kwargs,
                    ),
                ),
                z[0][1:-1],
                z[1][1:-1],
            ]
            for z in [
                y.split(": ", maxsplit=1)
                for y in [
                    x.strip().decode("utf-8", "backslashreplace")
                    for x in self.execute_sh_command("getprop", **kwargs)[0]
                ]
            ]
        ]

        return PunktDict(
            [
                (
                    kvz[j][1].replace(".", "_"),
                    {
                        "setprop": kvz[j][0],
                        "value": get_va(kvz, j),
                    },
                )
                for j in range(len(kvz))
            ]
        )


def format_partial_result(stdout, stderr):
    if stdout:
        return stdout[0].decode("utf-8", "backslashreplace").strip()

    return ""


class PartialAdb:
    def __init__(self, fu, callback=None, funame="", args=None, kwargs=None):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        if not args:
            self.args = ()
        if not kwargs:
            self.kwargs = {}
        self.fu = fu
        self.last_command_ok = []
        self.funame = funame

    def __call__(self, *args, thisargsfirst=False, ignore_exceptions=True, **kwargs):
        if thisargsfirst:
            o = " ".join(list(map(str, (*args, *self.args))))
        else:
            o = " ".join(list(map(str, (*self.args, *args))))
        newkwargs = self.kwargs.copy()
        newkwargs.update(kwargs)
        try:
            v = self.fu(o, **kwargs)
            if callable(self.callback):
                v = self.callback(*v)
            self.last_command_ok.append(1)
            return v
        except Exception as e:
            if not ignore_exceptions:
                raise e
            self.last_command_ok.append(0)

    def __str__(self):
        return self.funame

    def __repr__(self):
        return self.__str__()


class FuExec:
    def __init__(self, fu, *oldargs, **oldkwargs):
        self.fu = fu
        self.args = oldargs
        self.kwargs = oldkwargs

    def __call__(self, *args, **kwargs):
        oldkwargs = self.kwargs.copy()
        oldkwargs.update(kwargs)
        return self.fu(*self.args, *args, **oldkwargs)

    def __str__(self):
        return "()"

    def __repr__(self):
        return "()"


class SendEventKeyPress:
    def __init__(self, fu, cmd, stripri):
        self.fu = fu
        self.cmd = cmd
        self.stripri = stripri

    def __call__(self, duration=0.0, **kwargs):
        kwargs.update({"su": True})
        return self.fu(self.cmd % duration, **kwargs)

    def __str__(self):
        return self.stripri

    def __repr__(self):
        return self.stripri


class SettingsChanger:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __call__(self, *args, **kwargs):
        self.p1(*args, **kwargs)
        self.p2(*args, **kwargs)


@cache
def get_file_rights(x):
    allfi = {
        "is_file": x[0] == "-",
        "is_folder": x[0] == "d",
        "is_link": x[0] == "l",
        "is_character_device_file": x[0] == "c",
        "is_block_device_file": x[0] == "b",
        "is_named_pipe": x[0] == "p",
        "is_socket": x[0] == "s",
        "owner_read": x[1] == "r",
        "owner_write": x[2] == "w",
        "owner_exec": x[3] == "x",
        "group_read": x[4] == "r",
        "group_write": x[5] == "w",
        "group_exec": x[6] == "x",
        "others_read": x[7] == "r",
        "others_write": x[8] == "w",
        "others_exec": x[9] == "x",
        "file_permissions": x,
    }

    return allfi


@cache
def get_comspec():
    comspec = os.environ.get("ComSpec")
    if not comspec:
        system_root = os.environ.get("SystemRoot", "")
        comspec = os.path.join(system_root, "System32", "cmd.exe")
        if not os.path.isabs(comspec):
            raise FileNotFoundError(
                "shell not found: neither %ComSpec% nor %SystemRoot% is set"
            )
    return comspec
