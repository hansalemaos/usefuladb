import os
import subprocess
import sys
import time
import regex as re
from adbeasykey import AdbEasyKey, invisibledict, get_short_path_name
from flatten_everything import flatten_everything
from punktdict import PunktDict, dictconfig
from touchtouch import touch

c = sys.modules[__name__]
c.ADB_SHELL_SWIPE = "input swipe %d %d %d %d %d"
c.ADB_INSTALL = "install %s"
c.ADB_UNINSTALL = "uninstall %s"
c.ADB_UNINSTALL_KEEP_DATA = "uninstall -k %s"
c.ADB_UPDATE_APP = "install -r %s"
c.ADB_PUSH_TO_FOLDER = "push %s %s"
c.ADB_SHELL_PATH_EXISTS = "if [ -e '%s' ]; then echo '1'; else echo '0'; fi"
c.ADB_SHELL_IS_FOLDER = f"ls -i -H -las -s -d %s"
c.ADB_SHELL_MKDIR = f"mkdir -p %s"
c.ADB_SHELL_RENAME_FILE = "mv %s %s"
c.ADB_SHELL_TOUCH = "touch %s"
c.ADB_SHELL_DATE_SETTINGS = "am start -a android.settings.DATE_SETTINGS"
c.ADB_SHELL_APPLICATION_DEVELOPMENT_SETTINGS = (
    "am start -a com.android.settings.APPLICATION_DEVELOPMENT_SETTINGS"
)
c.ADB_SHELL_LOCATION_SOURCE_SETTINGS = (
    "am start -a android.settings.LOCATION_SOURCE_SETTINGS"
)
c.ADB_SHELL_MEMORY_CARD_SETTINGS = "am start -a android.settings.MEMORY_CARD_SETTINGS"
c.ADB_SHELL_LOCALE_SETTINGS = "am start -a android.settings.LOCALE_SETTINGS"
c.ADB_SHELL_SEARCH_SETTINGS = "am start -a android.search.action.SEARCH_SETTINGS"
c.ADB_SHELL_SETTINGS = "am start -a android.net.vpn.SETTINGS"
c.ADB_SHELL_ACCOUNT_SYNC_SETTINGS = "am start -a android.settings.ACCOUNT_SYNC_SETTINGS"
c.ADB_SHELL_DISPLAY_SETTINGS = "am start -a com.android.settings.DISPLAY_SETTINGS"
c.ADB_SHELL_INPUT_METHOD_SETTINGS = "am start -a android.settings.INPUT_METHOD_SETTINGS"
c.ADB_SHELL_SOUND_SETTINGS = "am start -a android.settings.SOUND_SETTINGS"
c.ADB_SHELL_WIFI_SETTINGS = "am start -a android.settings.WIFI_SETTINGS"
c.ADB_SHELL_APPLICATION_SETTINGS = "am start -a android.settings.APPLICATION_SETTINGS"
c.ADB_SHELL_ACCOUNT_SYNC_SETTINGS_ADD_ACCOUNT = (
    "am start -a android.settings.ACCOUNT_SYNC_SETTINGS_ADD_ACCOUNT"
)
c.ADB_SHELL_MANAGE_APPLICATIONS_SETTINGS = (
    "am start -a android.settings.MANAGE_APPLICATIONS_SETTINGS"
)
c.ADB_SHELL_SYNC_SETTINGS = "am start -a android.settings.SYNC_SETTINGS"
c.ADB_SHELL_DOCK_SETTINGS = "am start -a com.android.settings.DOCK_SETTINGS"
c.ADB_SHELL_ADD_ACCOUNT_SETTINGS = "am start -a android.settings.ADD_ACCOUNT_SETTINGS"
c.ADB_SHELL_SECURITY_SETTINGS = "am start -a android.settings.SECURITY_SETTINGS"
c.ADB_SHELL_DEVICE_INFO_SETTINGS = "am start -a android.settings.DEVICE_INFO_SETTINGS"
c.ADB_SHELL_WIRELESS_SETTINGS = "am start -a android.settings.WIRELESS_SETTINGS"
c.ADB_SHELL_SYSTEM_UPDATE_SETTINGS = (
    "am start -a android.settings.SYSTEM_UPDATE_SETTINGS"
)
c.ADB_SHELL_MANAGE_ALL_APPLICATIONS_SETTINGS = (
    "am start -a android.settings.MANAGE_ALL_APPLICATIONS_SETTINGS"
)
c.ADB_SHELL_DATA_ROAMING_SETTINGS = "am start -a android.settings.DATA_ROAMING_SETTINGS"
c.ADB_SHELL_APN_SETTINGS = "am start -a android.settings.APN_SETTINGS"
c.ADB_SHELL_USER_DICTIONARY_SETTINGS = (
    "am start -a android.settings.USER_DICTIONARY_SETTINGS"
)
c.ADB_SHELL_VOICE_INPUT_OUTPUT_SETTINGS = (
    "am start -a com.android.settings.VOICE_INPUT_OUTPUT_SETTINGS"
)
c.ADB_SHELL_TTS_SETTINGS = "am start -a com.android.settings.TTS_SETTINGS"
c.ADB_SHELL_WIFI_IP_SETTINGS = "am start -a android.settings.WIFI_IP_SETTINGS"
c.ADB_SHELL_WEB_SEARCH_SETTINGS = (
    "am start -a android.search.action.WEB_SEARCH_SETTINGS"
)
c.ADB_SHELL_BLUETOOTH_SETTINGS = "am start -a android.settings.BLUETOOTH_SETTINGS"
c.ADB_SHELL_AIRPLANE_MODE_SETTINGS = (
    "am start -a android.settings.AIRPLANE_MODE_SETTINGS"
)
c.ADB_SHELL_INTERNAL_STORAGE_SETTINGS = (
    "am start -a android.settings.INTERNAL_STORAGE_SETTINGS"
)
c.ADB_SHELL_ACCESSIBILITY_SETTINGS = (
    "am start -a android.settings.ACCESSIBILITY_SETTINGS"
)
c.ADB_SHELL_QUICK_LAUNCH_SETTINGS = (
    "am start -a com.android.settings.QUICK_LAUNCH_SETTINGS"
)
c.ADB_SHELL_PRIVACY_SETTINGS = "am start -a android.settings.PRIVACY_SETTINGS"
c.ADB_SHELL_DUMPSYS_INPUT = "dumpsys input"
c.ADB_SHELL_RESCAN_ALL_MEDIA = f"""find %s | while read f; do am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d \"file://${{f}}\"; done"""
c.ADB_SHELL_RESCAN_ONE_MEDIA = (
    f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d %s"
)
c.ADB_SHELL_LIST_USERS = "pm list users"

c.ADB_SHELL_SCREEN_COMPAT_ON = "am screen-compat on %s"
c.ADB_SHELL_SCREEN_COMPAT_OFF = "am screen-compat off %s"
c.ADB_SHELL_ENABLE_NOTIFICATIONS = (
    "settings put global heads_up_notifications_enabled 1"
)
c.ADB_SHELL_DISABLE_NOTIFICATIONS = (
    "settings put global heads_up_notifications_enabled 0"
)
c.ADB_SHELL_REMOVE_FILE = f"rm -f %s"
c.ADB_SHELL_CLEAR_PACKAGE = "pm clear %s"
c.ADB_SHELL_STILL_IMAGE_CAMERA = "am start -a android.media.action.STILL_IMAGE_CAMERA"
c.ADB_SHELL_MAKE_CALL = "am start -a android.intent.action.CALL -d tel:%s"
c.ADB_SHELL_DUMPSYS_ACTIVITY_SETTINGS = "dumpsys activity settings"
c.ADB_SHELL_DUMPSYS_ACTIVITY_ALLOWED_ASSOCIATIONS = (
    "dumpsys activity allowed-associations"
)
c.ADB_SHELL_DUMPSYS_ACTIVITY_INTENTS = "dumpsys activity intents"
c.ADB_SHELL_DUMPSYS_ACTIVITY_BROADCASTS = "dumpsys activity broadcasts"
c.ADB_SHELL_DUMPSYS_ACTIVITY_BROADCAST_STATS = "dumpsys activity broadcast-stats"
c.ADB_SHELL_DUMPSYS_ACTIVITY_PROVIDERS = "dumpsys activity providers"
c.ADB_SHELL_DUMPSYS_ACTIVITY_PERMISSIONS = "dumpsys activity permissions"
c.ADB_SHELL_DUMPSYS_ACTIVITY_SERVICES = "dumpsys activity services"
c.ADB_SHELL_DUMPSYS_ACTIVITY_RECENTS = "dumpsys activity recents"
c.ADB_SHELL_DUMPSYS_ACTIVITY_LASTANR = "dumpsys activity lastanr"
c.ADB_SHELL_DUMPSYS_ACTIVITY_STARTER = "dumpsys activity starter"
c.ADB_SHELL_DUMPSYS_ACTIVITY_ACTIVITIES = "dumpsys activity activities"
c.ADB_SHELL_DUMPSYS_ACTIVITY_EXIT_INFO = "dumpsys activity exit-info"
c.ADB_SHELL_DUMPSYS_ACTIVITY_PROCESSES = "dumpsys activity processes"
c.ADB_SHELL_DUMPSYS_ACTIVITY_LRU = "dumpsys activity lru"
c.ADB_SHELL_PM_DUMP = "pm dump %s"
c.ADB_SHELL_GET_WM_SIZE = "wm size"
c.ADB_SHELL_CHANGE_WM_SIZE = "wm size %sx%s"
c.ADB_SHELL_WM_RESET_SIZE = "wm size reset"
c.ADB_SHELL_GET_WM_DENSITY = "wm density"
c.ADB_SHELL_CHANGE_WM_DENSITY = "wm density %s"
c.ADB_SHELL_WM_RESET_DENSITY = "wm density reset"
c.ADB_SHELL_LIST_FEATURES = "pm list features"
c.ADB_SHELL_PWD = "pwd"
c.ADB_SHELL_LIST_SERVICES = "service list"
c.ADB_SHELL_PS_A_T_L_Z = "ps -A -T -l -Z"
c.ADB_SHELL_OPEN_URL = "am start -a android.intent.action.VIEW -d %s"
c.ADB_SHELL_GET_NTP_SERVER = "settings get global ntp_server"
c.ADB_SHELL_SET_NTP_SERVER = 'settings put global ntp_server "%s"'
c.ADB_SHELL_PM_LIST_PACKAGES_F_I_U = "pm list packages -f -i -U"
c.ADB_SHELL_PM_LIST_PACKAGES_3 = "pm list packages -3"
c.ADB_SHELL_PM_LIST_PACKAGES_S = "pm list packages -s"
c.ADB_SHELL_MOUNT = "mount"
c.ADB_SHELL_CAT = "cat %s"
c.ADB_SHELL_SCREENCAP = "screencap -p"
c.ADB_SHELL_REMOUNT_ALL_RW = "mount --all -o remount,rw -t vfat"
c.ADB_SHELL_REMOUNT_ALL_RO = "mount --all -o remount,ro -t vfat"
c.ADB_SHELL_REMOVE_DATA_CACHE = "rm -r -f /data/cache"
c.ADB_SHELL_REMOVE_DALVIK_CACHE = "rm -r -f /data/dalvik-cache"
c.ADB_SHELL_REMOVE_USER_CACHE = (
    r'for cache in /data/user*/*/*/cache/*; do rm -rf "$cache"; done'
)
c.ADB_SHELL_NETSTAT = r"netstat -n -W -p -a -e"
c.ADB_SHELL_START_PACKAGE = f"monkey -p %s 1"
c.ADB_SHELL_EXPAND_NOTIFICATIONS = "cmd statusbar expand-notifications"
c.ADB_SHELL_EXPAND_SETTINGS = "cmd statusbar expand-settings"
c.ADB_SHELL_RESOLVE_ACTIVITY_BRIEF = "cmd package resolve-activity --brief %s"
c.ADB_SHELL_RESOLVE_ACTIVITY = "cmd package resolve-activity %s"
c.ADB_SHELL_LIST_PERMISSION_GROUPS = "pm list permission-groups"
c.ADB_SHELL_DUMPSYS_WINDOW = "dumpsys window"
c.ADB_SHELL_INPUT_TAP = "input tap %s %s"
c.ADB_SHELL_INPUT_DPAD_TAP = "input dpad tap %s %s"
c.ADB_SHELL_INPUT_KEYBOARD_TAP = "input keyboard tap %s %s"
c.ADB_SHELL_INPUT_MOUSE_TAP = "input mouse tap %s %s"
c.ADB_SHELL_INPUT_TOUCHPAD_TAP = "input touchpad tap %s %s"
c.ADB_SHELL_INPUT_GAMEPAD_TAP = "input gamepad tap %s %s"
c.ADB_SHELL_INPUT_TOUCHNAVIGATION_TAP = "input touchnavigation tap %s %s"
c.ADB_SHELL_INPUT_JOYSTICK_TAP = "input joystick tap %s %s"
c.ADB_SHELL_INPUT_TOUCHSCREEN_TAP = "input touchscreen tap %s %s"
c.ADB_SHELL_INPUT_STYLUS_TAP = "input stylus tap %s %s"
c.ADB_SHELL_INPUT_TRACKBALL_TAP = "input trackball tap %s %s"
c.ADB_SHELL_INPUT_DPAD_SWIPE = "input dpad swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_DPAD_DRAGANDDROP = "input dpad draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_DPAD_ROLL = "input dpad roll %s %s"
c.ADB_SHELL_INPUT_KEYBOARD_SWIPE = "input keyboard swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_KEYBOARD_DRAGANDDROP = "input keyboard draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_KEYBOARD_ROLL = "input keyboard roll %s %s"
c.ADB_SHELL_INPUT_MOUSE_SWIPE = "input mouse swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_MOUSE_DRAGANDDROP = "input mouse draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_MOUSE_ROLL = "input mouse roll %s %s"
c.ADB_SHELL_INPUT_TOUCHPAD_SWIPE = "input touchpad swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_TOUCHPAD_DRAGANDDROP = "input touchpad draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_TOUCHPAD_ROLL = "input touchpad roll %s %s"
c.ADB_SHELL_INPUT_GAMEPAD_SWIPE = "input gamepad swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_GAMEPAD_DRAGANDDROP = "input gamepad draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_GAMEPAD_ROLL = "input gamepad roll %s %s"
c.ADB_SHELL_INPUT_TOUCHNAVIGATION_SWIPE = "input touchnavigation swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_TOUCHNAVIGATION_DRAGANDDROP = (
    "input touchnavigation draganddrop %s %s %s %s %s"
)
c.ADB_SHELL_INPUT_TOUCHNAVIGATION_ROLL = "input touchnavigation roll %s %s"
c.ADB_SHELL_INPUT_JOYSTICK_SWIPE = "input joystick swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_JOYSTICK_DRAGANDDROP = "input joystick draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_JOYSTICK_ROLL = "input joystick roll %s %s"
c.ADB_SHELL_INPUT_TOUCHSCREEN_SWIPE = "input touchscreen swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_TOUCHSCREEN_DRAGANDDROP = (
    "input touchscreen draganddrop %s %s %s %s %s"
)
c.ADB_SHELL_INPUT_TOUCHSCREEN_ROLL = "input touchscreen roll %s %s"
c.ADB_SHELL_INPUT_STYLUS_SWIPE = "input stylus swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_STYLUS_DRAGANDDROP = "input stylus draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_STYLUS_ROLL = "input stylus roll %s %s"
c.ADB_SHELL_INPUT_TRACKBALL_SWIPE = "input trackball swipe %s %s %s %s %s"
c.ADB_SHELL_INPUT_TRACKBALL_DRAGANDDROP = "input trackball draganddrop %s %s %s %s %s"
c.ADB_SHELL_INPUT_TRACKBALL_ROLL = "input trackball roll %s %s"
splitos_reg_u = re.compile(r"[\\/]+", flags=re.I)
splitos_reg_b = re.compile(rb"[\\/]+", flags=re.I)
screenres_reg_cur = re.compile(rb"\bcur=(\d+)x(\d+)\b")
screenres_reg = re.compile(rb"\bcur=(\d+)x(\d+)\b")

dictconfig.allow_nested_attribute_creation = False
dictconfig.allow_nested_key_creation = False
dictconfig.convert_all_dicts_recursively = True
regcomp_no = re.compile(rb"^\d+$")


def _get_n_adb_screenshots(
    adb_path,
    deviceserial,
    sleeptime=None,
    n=1,
):
    read, write = os.pipe()
    nbin = str(n).encode()
    if sleeptime is None:
        subcommand = (
            b"n=0; while (( n++ < "
            + nbin
            + b" )); do "
            + b"screencap -p\n"
            + b"echo oioioioioioioioi"
            + b"; done"
        )
    else:
        subcommand = (
            b"n=0; while (( n++ < "
            + nbin
            + b" )); do "
            + b"screencap -p\n"
            + b"echo oioioioioioioioi\nsleep "
            + str(sleeptime).encode()
            + b"; done"
        )

    os.write(write, subcommand)
    os.close(write)

    wholbilist = []
    try:
        with subprocess.Popen(
            f"{adb_path} -s {deviceserial} shell",
            stdin=read,
            stdout=subprocess.PIPE,
            universal_newlines=False,
            stderr=subprocess.DEVNULL,
            shell=False,
            **invisibledict,
        ) as popen:
            for stdout_line in iter(popen.stdout.readline, b""):
                try:
                    wholbilist.append(stdout_line)
                    if stdout_line.endswith(b"oioioioioioioioi\r\n"):
                        wholbilist[-1] = wholbilist[-1][:-18]
                        yield b"".join(wholbilist).replace(b"\r\n", b"\n")
                        wholbilist.clear()

                except Exception as fe:
                    print(fe)
    except KeyboardInterrupt:
        pass


def get_imei_imsi_sim(adb_path, deviceserial):
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

    imsi = (
        subprocess.run(
            f"""\"{adb_path}\" -s {deviceserial} shell su -c \'service call iphonesubinfo 7 i32 2\'""",
            capture_output=True,
            shell=False,
            **invisibledict,
        )
    ).stdout
    imei = (
        subprocess.run(
            f"""\"{adb_path}\" -s {deviceserial} shell su -c \'service call iphonesubinfo 3 i32 2\'""",
            capture_output=True,
            shell=False,
            **invisibledict,
        )
    ).stdout
    sims = (
        subprocess.run(
            f"""\"{adb_path}\" -s {deviceserial} shell su -c \'service call iphonesubinfo 11 i32 2\'""",
            capture_output=True,
            shell=False,
            **invisibledict,
        )
    ).stdout
    imsi = get_codes(v=imsi)
    imei = get_codes(v=imei)
    sims = get_codes(v=sims)
    return imei, imsi, sims


def split_os_sep(p):
    if isinstance(p, bytes):
        return splitos_reg_b.split(p)
    if isinstance(p, str):
        return splitos_reg_u.split(p)
    return p


def join_path_android(*args):
    argslist = list(args)
    p = "/".join(argslist)
    return splitos_reg_u.sub(p, "/")


def strip_quotes_and_escape(s):
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


def cat_copy(
    adb_path,
    deviceserial,
    files,
    folder=None,
    return_content=True,
    maintain_date=True,
    escape_path=True,
    filesep="FileXXXFile:",
):
    if escape_path:
        files = [strip_quotes_and_escape(x) for x in files]
    allfi = " ".join(files)
    read, write = os.pipe()
    filesepbin = filesep.encode("utf-8")
    subcommand = f"""files=({allfi})

    for file in "${{files[@]}}"
    do

        cat "$file"
        modified_date=$(stat -c %y "$file")
        echo "{filesep}$modified_date:::$file"
    done""".encode(
        "utf-8"
    )

    os.write(write, subcommand)
    os.close(write)

    wholbilist = []
    if folder:
        folder = folder.strip("\\/")
    try:
        with subprocess.Popen(
            f"{adb_path} -s {deviceserial} shell",
            stdin=read,
            stdout=subprocess.PIPE,
            universal_newlines=False,
            stderr=subprocess.DEVNULL,
            shell=False,
            **invisibledict,
        ) as popen:
            for stdout_line in iter(popen.stdout.readline, b""):
                try:
                    if stdout_line.startswith(filesepbin):
                        a_filename = (
                            stdout_line[len(filesepbin) :]
                            .decode("utf-8", "backslashreplace")
                            .strip()
                        )
                        last_modified_date, a_filename = a_filename.split(
                            ":::", maxsplit=1
                        )
                        if maintain_date:
                            last_modified_date = time.mktime(
                                time.strptime(
                                    last_modified_date[:26], "%Y-%m-%d %H:%M:%S.%f"
                                )
                            )
                        filecontent = b"".join(wholbilist).replace(b"\r\n", b"\n")
                        if return_content:
                            yield [a_filename, last_modified_date, filecontent]
                        if folder:
                            try:
                                joined = os.path.normpath(
                                    os.path.join(folder, a_filename.strip("\\/"))
                                )
                                touch(joined)
                                with open(joined, mode="wb") as f:
                                    f.write(filecontent)
                                if maintain_date:
                                    os.utime(
                                        joined, (last_modified_date, last_modified_date)
                                    )
                            except Exception as fe:
                                try:
                                    sys.stderr.write(f"ERROR: {a_filename}\n")
                                except Exception as e:
                                    pass
                        wholbilist.clear()
                    else:
                        wholbilist.append(stdout_line)

                except Exception as fe:
                    sys.stderr.write(f"ERROR: {fe}\n")
    except KeyboardInterrupt:
        pass


class AdbBackground:
    def __init__(self, proc):
        self.proc = proc

    def __str__(self):
        return str(self.proc)

    def __repr__(self):
        return repr(self.proc)

    def kill(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        try:
            self.proc.stdout.close()
        except Exception:
            pass
        try:
            self.proc.stderr.close()
        except Exception:
            pass
        try:
            self.proc.kill()
        except Exception:
            pass


def do_something_when_activity_found(
    adb_path,
    deviceserial,
    activity_regex,
    positive_action,
    negative_action,
    sleep_time=1.0,
    **kwargs,
):
    read, write = os.pipe()
    cmd = f"""
while true
do
	if dumpsys activity top -c | grep -q -E "{activity_regex}"; then
		{positive_action}
	else
		{negative_action}
    fi
	sleep {sleep_time}
done	    
    """
    subcommand = cmd.encode()
    os.write(write, subcommand)
    os.close(write)
    kwargs.update(invisibledict)
    kwargs.update(
        {"stdin": read, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    )
    return AdbBackground(
        subprocess.Popen(
            f"{adb_path} -s {deviceserial} shell",
            **kwargs,
        )
    )


class AdbCommands(AdbEasyKey):
    def __init__(
        self,
        adb_path,
        device_serial,
        ps=False,
        to_83=True,
        timeout=0,
        sleeptime=0.05,
        su=False,
        add_exit=True,
        print_stdout=True,
        print_stderr=True,
        decode_stdout_print=True,
        use_busybox=False,
        longpress=False,
    ):
        super().__init__(adb_path, device_serial, use_busybox)
        self.default_settings = {
            "timeout": timeout,
            "sleeptime": sleeptime,
            "su": su,
            "add_exit": add_exit,
            "print_stdout": print_stdout,
            "print_stderr": print_stderr,
            "decode_stdout_print": decode_stdout_print,
            "to_83": to_83,
            "ps": ps,
            "longpress": longpress,
        }

    def sh_start_while_loop_activity_check(
        self, activity_regex, positive_action, negative_action, sleep_time=1.0
    ):
        return do_something_when_activity_found(
            adb_path=self.adbpath,
            deviceserial=self.device_serial,
            activity_regex=activity_regex,
            positive_action=positive_action,
            negative_action=negative_action,
            sleep_time=sleep_time,
        )

    def sh_multiple_cat_copy(
        self,
        files,
        folder=None,
        return_content=True,
        maintain_date=True,
        escape_path=True,
        filesep="FileXXXFile:",
    ):
        yield from cat_copy(
            self.adb_path,
            self.device_serial,
            files=files,
            folder=folder,
            return_content=return_content,
            maintain_date=maintain_date,
            escape_path=escape_path,
            filesep=filesep,
        )

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

    def get_n_screenshots(self, n=1, sleeptime=None):
        yield from _get_n_adb_screenshots(
            self.adbpath, self.device_serial, sleeptime=sleeptime, n=n
        )

    def get_all_devices(self, **kwargs):
        alld = {}
        kwargs.update({"to_83": False})
        try:
            alld = [
                ["device_name:" + y[0]]
                + re.search(r"^([^:]+:[^\s:]+)+", y[1]).allcaptures()[-1]
                for y in [
                    q.decode().strip().split(maxsplit=1)
                    for q in self.execute_adb_command("devices -l", **kwargs)[0][1:-1]
                ]
            ]
            alld = [[h.split(":", maxsplit=1) for h in q] for q in alld]
            alld = {
                k: {vv[0].strip().replace(" ", "_"): vv[1] for vv in v}
                for k, v in enumerate([q for q in alld])
            }
        except Exception as fe:
            print(fe)
        return alld

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

    def sh_input_dpad_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="dpad",
            ),
        )

    def sh_input_keyboard_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="keyboard",
            ),
        )

    def sh_input_mouse_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="mouse",
            ),
        )

    def sh_input_touchpad_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="touchpad",
            ),
        )

    def sh_input_gamepad_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="gamepad",
            ),
        )

    def sh_input_touchnavigation_text(
        self, text, sleeptime=(0.0, 0.0), remove_accents=False
    ):
        return self.input_text_subprocess(
            text,
            sleeptime=sleeptime,
            remove_accents=remove_accents,
            input_device="touchnavigation",
        )

    def sh_input_joystick_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
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
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="touchscreen",
            ),
        )

    def sh_input_stylus_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="stylus",
            ),
        )

    def sh_input_trackball_text(self, text, sleeptime=(0.0, 0.0), remove_accents=False):
        return (
            self.input_text_subprocess(
                text,
                sleeptime=sleeptime,
                remove_accents=remove_accents,
                input_device="trackball",
            ),
        )

    def sh_dumpsys_window(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_DUMPSYS_WINDOW, **kwargs)

    def sh_input_tap(self, x, y, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_INPUT_TAP % (int(x), int(y)), **kwargs
        )

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

    def sh_change_display_orientation(self, new_orientation=1, **kwargs):
        format222 = new_orientation

        if format222 == "horizontal_upside_down" or format222 == 2:
            format_einfuegen = 2

        elif format222 == "vertical" or format222 == 1:
            format_einfuegen = 1

        elif format222 == "horizontal" or format222 == 0:
            format_einfuegen = 0

        elif format222 == "vertical_upside_down" or format222 == 3:
            format_einfuegen = 3
        else:
            format_einfuegen = 0
        orientierung = self.sh_get_display_orientation(**kwargs)
        cmds = [
            f"""content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0""",
            f"""settings put system accelerometer_rotation 0""",
            f"""content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:{format_einfuegen}""",
        ]
        for cmd in cmds:
            stdo, stde = self.execute_sh_command(cmd, **kwargs)
        newscreen = self.sh_get_display_orientation(**kwargs)
        return {"old": orientierung, "new": newscreen}

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

    def sh_remove_user_cache(self, **kwargs):
        kwargs.update({"su": True})
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_USER_CACHE, **kwargs)

    def sh_remove_dalvik_cache(self, **kwargs):
        kwargs.update({"su": True})
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_DALVIK_CACHE, **kwargs)

    def sh_remove_data_cache(self, **kwargs):
        kwargs.update({"su": True})
        return self.execute_sh_command(c.ADB_SHELL_REMOVE_DATA_CACHE, **kwargs)

    def sh_remount_all_rw(self, **kwargs):
        kwargs.update({"su": True})
        return self.execute_sh_command(c.ADB_SHELL_REMOUNT_ALL_RW, **kwargs)

    def sh_remount_all_ro(self, **kwargs):
        kwargs.update({"su": True})
        return self.execute_sh_command(c.ADB_SHELL_REMOUNT_ALL_RO, **kwargs)

    def sh_screencap(self, **kwargs):
        kwargs.update({"print_stdout": False, "sleeptime": 0.00001})
        return b"".join(self.execute_sh_command(c.ADB_SHELL_SCREENCAP, **kwargs)[0])

    def adb_pull(self, src, dst, **kwargs):
        os.makedirs(dst, exist_ok=True)
        kwargs.update({"to_83": False})
        foldershort = get_short_path_name(dst)
        return self.execute_adb_command(f'pull "{src}" {foldershort}', **kwargs)

    def adb_pull_to_folder_nested(self, src, dst, **kwargs):
        kwargs.update({"to_83": False})
        srcfolder = os.sep.join(split_os_sep(src)[:-1])
        destfolder = os.path.normpath(
            os.path.join(dst.strip("\\/"), srcfolder.strip("\\/"))
        )
        os.makedirs(destfolder, exist_ok=True)
        foldershort = get_short_path_name(destfolder)
        self.execute_adb_command(f'pull "{src}" {foldershort}', **kwargs)

    def sh_cat_get_file(self, path, **kwargs):
        kwargs.update({"print_stdout": False})
        return b"".join(
            self.execute_sh_command(
                c.ADB_SHELL_CAT % strip_quotes_and_escape(path), **kwargs
            )[0]
        )

    def sh_get_imei_imsi_sim(self, **kwargs):
        return get_imei_imsi_sim(self.adbpath, self.device_serial)

    def sh_pm_dump(self, package, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PM_DUMP % package, **kwargs)

    def sh_get_wm_size(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_WM_SIZE, **kwargs)

    def sh_change_wm_size(self, width, height, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CHANGE_WM_SIZE % (width, height), **kwargs
        )

    def sh_wm_reset_size(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WM_RESET_SIZE, **kwargs)

    def sh_get_wm_density(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_GET_WM_DENSITY, **kwargs)

    def sh_change_wm_density(self, density, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_CHANGE_WM_DENSITY % density, **kwargs
        )

    def sh_wm_reset_density(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_WM_RESET_DENSITY, **kwargs)

    def sh_list_features(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_FEATURES, **kwargs)

    def sh_pwd(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PWD, **kwargs)

    def sh_list_services(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_LIST_SERVICES, **kwargs)

    def sh_ps_a_t_l_z(self, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_PS_A_T_L_Z, **kwargs)

    def sh_open_url(self, url, **kwargs):
        format_url
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

    def sh_remove_file(self, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_REMOVE_FILE % strip_quotes_and_escape(path), **kwargs
        )

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

    def sh_rescan_one_media(self, path, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_RESCAN_ONE_MEDIA % strip_quotes_and_escape(path), **kwargs
        )

    def _press_keyevent(self, k, **kwargs):
        kwargsdict = self.default_settings.copy()
        kwargsdict.update(kwargs)
        del kwargsdict["to_83"]
        ps = kwargsdict["ps"]
        del kwargsdict["ps"]
        longpress = kwargsdict.get("longpress")
        del kwargsdict["longpress"]
        if ps:
            if longpress:
                return self.keyevents[k].longpress_ps(**kwargsdict)
            else:
                return self.keyevents[k].press_ps(**kwargsdict)
        else:
            if longpress:
                return self.keyevents[k].longpress_subproc(**kwargsdict)
            else:
                return self.keyevents[k].press_subproc(**kwargsdict)

    def k_hide_keyboard(self, **kwargs):
        return self._press_keyevent("KEYCODE_ESCAPE", **kwargs)

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

    def sh_get_display_orientation(self, **kwargs):
        stdo, stde = self.execute_sh_command(c.ADB_SHELL_DUMPSYS_INPUT, **kwargs)
        return int(
            [x for x in stdo if b"SurfaceOrientation" in x][0]
            .strip()
            .split(b":")[-1]
            .strip()
        )

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
        folderpath = strip_quotes_and_escape("/".join(path.split("/")[:-1]))
        self.sh_mkdir(folderpath, **kwargs)
        return self.execute_sh_command(
            c.ADB_SHELL_TOUCH % strip_quotes_and_escape(path), **kwargs
        )

    def sh_rename(self, src, dst, **kwargs):
        src = strip_quotes_and_escape(src)
        dst = strip_quotes_and_escape(dst)
        return self.execute_sh_command(c.ADB_SHELL_RENAME_FILE % (src, dst), **kwargs)

    def sh_mkdir(self, path, **kwargs):
        return self.execute_sh_command(c.ADB_SHELL_MKDIR % path, **kwargs)

    def sh_is_folder(self, path, **kwargs):
        result, stde = self.execute_sh_command(c.ADB_SHELL_IS_FOLDER % path, **kwargs)
        isfolder = False
        try:
            if re.findall(rb"^\d+\s+\d+\s+d", result[0])[0]:
                isfolder = True
        except Exception:
            pass
        return isfolder

    def sh_swipe(self, x0, y0, x1, y1, t, **kwargs):
        return self.execute_sh_command(
            c.ADB_SHELL_SWIPE % (int(x0), int(y0), int(x1), int(y1), int(t * 1000)),
            **kwargs,
        )

    def sh_file_exists(self, path, **kwargs):
        stdout, stderr = self.execute_sh_command(
            c.ADB_SHELL_PATH_EXISTS % path, **kwargs
        )
        return bool(int(stdout[0].strip().decode("utf-8")))

    def adb_push(self, src, dst, **kwargs):
        shortsrc = get_short_path_name(src)
        shortsrc_pure_file = split_os_sep(shortsrc)[-1]
        longsrc_pure_file = split_os_sep(src)[-1]
        dst_file_short = dst.rstrip("/") + "/" + shortsrc_pure_file
        dst_file_long = dst.rstrip("/") + "/" + longsrc_pure_file
        kwargs.update({"to_83": False})
        stdoutlist = []
        stderrlist = []
        stdo, stde = self.execute_sh_command(
            c.ADB_SHELL_MKDIR % strip_quotes_and_escape(dst), **kwargs
        )
        stdoutlist.extend(stdo)
        stderrlist.extend(stde)

        stdo, stde = self.execute_adb_command(f"push {shortsrc} {dst}", **kwargs)
        stdoutlist.extend(stdo)
        stderrlist.extend(stde)
        stdo, stde = self.sh_rename(
            strip_quotes_and_escape(dst_file_short),
            strip_quotes_and_escape(dst_file_long),
            **kwargs,
        )
        stdoutlist.extend(stdo)
        stderrlist.extend(stde)
        return stdoutlist, stderrlist

    def adb_push_to_file_path(self, src, dst, **kwargs):
        dstexe = dst
        dst = "/".join(dst.split("/")[:-1])
        shortsrc = get_short_path_name(src)
        shortsrc_pure_file = split_os_sep(shortsrc)[-1]
        dst_file_short = dst.rstrip("/") + "/" + shortsrc_pure_file
        kwargs.update({"to_83": False})
        stdoutlist = []
        stderrlist = []
        stdo, stde = self.execute_sh_command(
            c.ADB_SHELL_MKDIR % strip_quotes_and_escape(dst), **kwargs
        )
        stdoutlist.extend(stdo)
        stderrlist.extend(stde)
        stdo, stde = self.execute_adb_command(f"push {shortsrc} {dst}", **kwargs)
        stdoutlist.extend(stdo)
        stderrlist.extend(stde)
        stdo, stde = self.sh_rename(
            strip_quotes_and_escape(dst_file_short),
            strip_quotes_and_escape(dstexe),
            **kwargs,
        )
        stdoutlist.extend(stdo)
        stderrlist.extend(stde)
        return stdoutlist, stderrlist

    def adb_install(self, path, **kwargs):
        return self.execute_adb_command(c.ADB_INSTALL % path, **kwargs)

    def adb_uninstall(self, path, **kwargs):
        return self.execute_adb_command(c.ADB_UNINSTALL % path, **kwargs)

    def adb_uninstall_keep_data(self, path, **kwargs):
        return self.execute_adb_command(c.ADB_UNINSTALL_KEEP_DATA % path, **kwargs)

    def adb_update_app(self, path, **kwargs):
        return self.execute_adb_command(c.ADB_UNINSTALL_KEEP_DATA % path, **kwargs)

    def execute_sh_command(self, cmd, **kwargs):
        kwargsdict = self.default_settings.copy()
        kwargsdict.update(kwargs)
        del kwargsdict["to_83"]
        ps = kwargsdict["ps"]
        del kwargsdict["ps"]
        del kwargsdict["longpress"]

        if ps:
            return self.adb_shell_ps(cmd, **kwargsdict)
        else:
            return self.adb_shell_subprocess(cmd, **kwargsdict)

    def execute_adb_command(self, cmd, **kwargs):
        kwargsdict = self.default_settings.copy()
        kwargsdict.update(kwargs)
        del kwargsdict["su"]
        del kwargsdict["add_exit"]
        ps = kwargsdict["ps"]
        del kwargsdict["ps"]
        del kwargsdict["longpress"]

        if ps:
            return self.adb_ps(cmd, **kwargsdict)
        else:
            return self.adb_subprocess(cmd, **kwargsdict)

    def open_adb_shell(self):
        subprocess.run(
            f'start cmd /k "{self.adbpath}" -s {self.device_serial} shell', shell=True
        )

    def manage_files(
        self,
        path,
        hidden=True,
        escape_path=True,
        quote_path=False,
        sepa="XXXÇÇÇXXX",
        add_to_find=(),
        **kwargs,
    ):
        return ListFiles(
            adb=self,
            path=path,
            hidden=hidden,
            escape_path=escape_path,
            quote_path=quote_path,
            sepa=sepa,
            add_to_find=add_to_find,
            **kwargs,
        )


class ListFiles:
    def __init__(
        self,
        adb,
        path,
        hidden=True,
        escape_path=True,
        quote_path=False,
        sepa="XXXÇÇÇXXX",
        add_to_find=(),
        **kwargs,
    ):
        pathtoscan = path
        self.original_path = path
        self.escapedpath = ""
        self.escape_path = escape_path
        self.quote_path = quote_path
        self.sepa = sepa
        self.add_to_find = add_to_find
        self.kwdict = kwargs
        self.hidden = hidden
        if escape_path:
            self.escapedpath = strip_quotes_and_escape(path)
            pathtoscan = self.escapedpath
        if quote_path:
            pathtoscan = f'"{pathtoscan}"'
        kwargs.update({"print_stdout": False})
        if add_to_find:
            add_to_find = " " + "".join(list(add_to_find)) + " "
        else:
            add_to_find = " "
        self.files = dict(
            h
            for h in (
                (f"f{x[0]}", self._get_file_dict(x, hidden=False))
                for x in (
                    y.decode("utf-8", "backslashreplace")
                    .strip()
                    .split(sepa, maxsplit=6)
                    for y in adb.execute_sh_command(
                        f"""find {pathtoscan}{add_to_find}-exec stat -c "%i{sepa}%s{sepa}%A{sepa}%U{sepa}%G{sepa}%Y{sepa}%n" {{}} \;""",
                        **kwargs,
                    )[0]
                )
            )
            if h[1]
        )
        if hidden:
            self.files.update(
                dict(
                    h
                    for h in (
                        (f"f{x[0]}", self._get_file_dict(x, hidden=True))
                        for x in (
                            y.decode("utf-8", "backslashreplace")
                            .strip()
                            .split(sepa, maxsplit=6)
                            for y in adb.execute_sh_command(
                                f"""find {pathtoscan}{add_to_find}-name '.*' -exec stat -c "%i{sepa}%s{sepa}%A{sepa}%U{sepa}%G{sepa}%Y{sepa}%n" {{}} \;""",
                                **kwargs,
                            )[0]
                        )
                    )
                    if h[1]
                )
            )
        self.files = PunktDict(self.files)
        self.adb = adb

    def update_list(self):
        return self.__class__(
            adb=self.adb,
            path=self.original_path,
            hidden=self.hidden,
            escape_path=self.escape_path,
            quote_path=self.quote_path,
            sepa=self.sepa,
            add_to_find=self.add_to_find,
            **self.kwdict,
        )

    def __str__(self):
        return f"original: {self.original_path}\nescaped: {self.escapedpath}\nitems: {len(self.files)}"

    def __repr__(self):
        return self.__str__()

    def _get_file_dict(self, x, hidden=False):
        try:
            spli = (x[6]).strip("/").split("/")
            if len(spli) > 1:
                fol = "/" + "/".join(spli[:-1])

            else:
                fol = "/"
            fi = spli[-1]
            d = {
                "file_size": int(x[1]),
                "is_file": x[2][0] == "-",
                "is_folder": x[2][0] == "d",
                "is_link": x[2][0] == "l",
                "is_character_device_file": x[2][0] == "c",
                "is_block_device_file": x[2][0] == "b",
                "is_named_pipe": x[2][0] == "p",
                "is_socket": x[2][0] == "s",
                "owner_read": x[2][1] == "r",
                "owner_write": x[2][2] == "w",
                "owner_exec": x[2][3] == "x",
                "group_read": x[2][4] == "r",
                "group_write": x[2][5] == "w",
                "group_exec": x[2][6] == "x",
                "others_read": x[2][7] == "r",
                "others_write": x[2][8] == "w",
                "others_exec": x[2][9] == "x",
                "file_permissions": (x[2]),
                "user_owner": (x[3]),
                "group": (x[4]),
                "modification_time": int(x[5]),
                "path": (x[6]),
                "folder": fol,
                "pure_path": fi,
                "is_hidden": hidden,
            }
            d["cat_file"] = lambda **kwargs: self.adb.sh_cat_get_file(
                d["path"], **kwargs
            )
            d["pull_nested"] = lambda dst, **kwargs: self.adb.adb_pull_to_folder_nested(
                src=d["path"], dst=dst, **kwargs
            )
            d["pull"] = lambda dst, **kwargs: self.adb.adb_pull(
                src=d["path"], dst=dst, **kwargs
            )
            d["grep"] = lambda reg, **kwargs: self.adb.sh_grep(
                reg,
                path=d["path"],
                escape=kwargs.pop("escape") if "escape" in kwargs else True,
                quote=kwargs.pop("quote") if "quote" in kwargs else False,
                extended_regexp=kwargs.pop("extended_regexp")
                if "extended_regexp" in kwargs
                else True,
                ignore_case=kwargs.pop("ignore_case")
                if "ignore_case" in kwargs
                else True,
                recursively=False,
                line_number=kwargs.pop("line_number")
                if "line_number" in kwargs
                else True,
                invert_match=kwargs.pop("invert_match")
                if "invert_match" in kwargs
                else False,
                files_with_matches=kwargs.pop("files_with_matches")
                if "files_with_matches" in kwargs
                else False,
                count=kwargs.pop("count") if "count" in kwargs else False,
                **kwargs,
            )
            d["remove"] = lambda **kwargs: self.adb.sh_remove_file(
                path=d["path"], **kwargs
            )
            d["rename"] = lambda dst, **kwargs: self.adb.sh_rename(
                src=d["path"], dst=dst, **kwargs
            )
            return d
        except Exception as fe:
            sys.stderr.write(f"{x} {fe}")
        return {}

    def get_all_files(self, regcomp=".*"):
        if isinstance(regcomp, str):
            regcomp = re.compile(regcomp)
        ids_files = [
            (y[1].path, y[0])
            for y in self.files.items()
            if y[1]["is_file"] and regcomp.search(y[1]["path"])
        ]

        return ids_files

    def grep_search_multiple_files(
        self,
        reg,
        match_file=".*",
        escape=True,
        quote=False,
        extended_regexp=True,
        ignore_case=True,
        invert_match=False,
        **kwargs,
    ):
        regcomp = re.compile(match_file)
        ids_files = self.get_all_files(regcomp=regcomp)

        results = [
            [
                v[0].decode("utf-8", "backslashreplace"),
                int(v[1]) if regcomp_no.search(v[1]) else v[1],
                v[2],
            ]
            for v in [
                q.split(b":", maxsplit=2)
                for q in self.adb.sh_grep(
                    reg,
                    [x[0] for x in ids_files],
                    escape=escape,
                    quote=quote,
                    extended_regexp=extended_regexp,
                    ignore_case=ignore_case,
                    recursively=False,
                    line_number=True,
                    invert_match=invert_match,
                    files_with_matches=False,
                    count=False,
                    **kwargs,
                )[0]
            ]
            if len(v) == 3
        ]
        ids_files_lookup = dict(ids_files)
        allres = {}
        for r in results:
            try:
                allres[ids_files_lookup[r[0]]] = dict(
                    self.files[ids_files_lookup[r[0]]].items()
                )
                allres[ids_files_lookup[r[0]]]["regex_results"] = results[1:]
            except Exception as fe:
                print(fe)
        return allres

    def cat_copy_multiple_files(
        self,
        folder=None,
        regcomp=".*",
        return_content=True,
        filesep="FileXXXFile:",
        maintain_date=True,
        escape_path=True,
    ):
        allfi = [(x[0]) for x in self.get_all_files(regcomp=regcomp)]
        yield from self.adb.sh_multiple_cat_copy(
            files=allfi,
            folder=folder,
            return_content=return_content,
            filesep=filesep,
            maintain_date=maintain_date,
            escape_path=escape_path,
        )

    def regex_filepath_search(self, reg, flags=re.I):
        if isinstance(reg, str):
            reg = re.compile(reg, flags=flags)

        return PunktDict({k: v for k, v in self.files.items() if reg.search(v["path"])})
