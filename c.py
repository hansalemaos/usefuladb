ADBEXE_RECONNECT = "reconnect"
ADBEXE_CONNECT = "connect"
ADBEXE_ROOT = "root"
ADBEXE_UNROOT = "unroot"
ADBEXE_SHOW_REVERSED_PORTS = "reverse --list"
ADBEXE_SHOW_FORWARDED_PORTS = "forward --list"
ADBEXE_UNINSTALL = "uninstall %s"
ADBEXE_DEVICES = "devices -l"
ADBEXE_FORWARD_PORT = "forward tcp:%s tcp:%s"
ADBEXE_REMOVE_FORWARDED_PORT = "forward --remove tcp:%s"
ADBEXE_REVERSE_PORT = "reverse tcp:%s tcp:%s"
ADBEXE_REMOVE_REVERSED_PORT = "reverse --remove tcp:%s"
ADBEXE_PUSH = "push %s %s"
ADBEXE_PULL = "pull %s %s"
ADB_SHELL_REALPATH = """realpath %s"""
ADB_SHELL_DIRNAME = "dirname %s"
ADB_SHELL_MD5SUM = """md5sum -b %s"""
ADB_SHELL_GET_FILE_EXTENSION = """filename="FILEPATH"\necho \"${filename##*.}\""""
ADB_SHELL_REMOVE_STDERR_TMPFILES = (
    r"cd /sdcard/ && find . -type f -name 'xxxstd*' -exec rm {} \;"
)
ADB_SHELL_REMOVE_STDOUT_TMPFILES = (
    r"cd /sdcard/ && find . -type f -name 'xxxxstd*' -exec rm {} \;"
)
ADB_SHELL_REMOVE_STDERR_TMPFILES_G = (
    r"cd /sdcard/ && find . -type f -name 'errortmp*' -exec rm {} \;"
)
ADB_SHELL_REMOVE_STDOUT_TMPFILES_G = (
    r"cd /sdcard/ && find . -type f -name 'outputtmp*' -exec rm {} \;"
)
ADB_SHELL_GET_USER_ROTATION = "settings get system user_rotation"
ADB_SHELL_CRATE_BACKUP = "cp %s{,.bak}"
ADB_SHELL_CHANGE_DICT = "cd %s"
ADB_SHELL_LS = "ls"
ADB_SHELL_EXIT_FROM_SU = f"""
#!/bin/bash    
while true; do
    if [ "$(whoami)" == "root" ]; then
      echo -n -e "ROOTUSER"
      echo REPLACE_EXIT
      exit
    else
        echo "REGULAR"
        break
    fi
done
            """
ADB_SHELL_GET_ALL_CHMOD_IN_FOLDER = f"""stat -c '%A %a %n' REPLACE_FOLDER*"""
ADB_SHELL_CHANGE_TO_PREV_WORKING_DICT = "cd -"
ADB_SHELL_EMPTY_FILE = "> %s"
ADB_SHELL_CAT_FILE = "cat %s"
ADB_SHELL_CREATE_NESTED_FOLDER = "mkdir -p %s"
ADB_SHELL_TOUCH = "touch %s"
ADB_SHELL_ALL_KEYBOARDS = "ime list -s -a"
ADB_SHELL_LIST_ALL_LISTENING_PORT_AND_PIDS = "netstat -tlnp"
ADB_GET_DEFAULT_KEYBOARD = f"settings get secure default_input_method"
ADB_LIST_ALL_KEYBOARDS = f"ime list -a"
ADB_ENABLE_KEYBOARD = f"ime enable %s"
ADB_DISABLE_KEYBOARD = f"ime disable %s"
ADB_SET_KEYBOARD = f"ime set %s"
ADB_IS_KEYBOARD_SHOWN = f"dumpsys input_method"
ADB_KEYBOARD_NAME = "com.android.adbkeyboard/.AdbIME"
ADB_SHOW_TOUCHES = "settings put system show_touches 1"
ADB_SHOW_TOUCHES_NOT = "settings put system show_touches 0"
ADB_KEYBOARD_COMMAND = f"am broadcast -a ADB_INPUT_B64 --es msg %s"
ADB_SELECTED_INPUT_METHOD = f"cmd settings put secure selected_input_method_subtype 0"
ADB_SHOW_IME_WITH_HARD_KEYBOARD = (
    f"cmd settings put secure show_ime_with_hard_keyboard 1"
)

ADB_SHELL_SWIPE = "input swipe %d %d %d %d %d"
ADB_INSTALL = "install %s"
ADB_UNINSTALL = "uninstall %s"
ADB_UNINSTALL_KEEP_DATA = "uninstall -k %s"
ADB_UPDATE_APP = "install -r %s"
ADB_PUSH_TO_FOLDER = "push %s %s"
ADB_SHELL_PATH_EXISTS = "if [ -e '%s' ]; then echo '1'; else echo '0'; fi"
ADB_SHELL_IS_FOLDER = f"ls -i -H -las -s -d %s"
ADB_SHELL_IS_FILE = """if [ -f "%s" ]; then
    echo 1
else
    echo 0
fi
"""
ADB_SHELL_MKDIR = f"mkdir -p %s"
ADB_SHELL_RENAME_FILE = "mv %s %s"
ADB_SHELL_DATE_SETTINGS = "am start -a android.settings.DATE_SETTINGS"
ADB_SHELL_APPLICATION_DEVELOPMENT_SETTINGS = (
    "am start -a com.android.settings.APPLICATION_DEVELOPMENT_SETTINGS"
)
ADB_SHELL_LOCATION_SOURCE_SETTINGS = (
    "am start -a android.settings.LOCATION_SOURCE_SETTINGS"
)
ADB_SHELL_MEMORY_CARD_SETTINGS = "am start -a android.settings.MEMORY_CARD_SETTINGS"
ADB_SHELL_LOCALE_SETTINGS = "am start -a android.settings.LOCALE_SETTINGS"
ADB_SHELL_SEARCH_SETTINGS = "am start -a android.search.action.SEARCH_SETTINGS"
ADB_SHELL_SETTINGS = "am start -a android.net.vpn.SETTINGS"
ADB_SHELL_ACCOUNT_SYNC_SETTINGS = "am start -a android.settings.ACCOUNT_SYNC_SETTINGS"
ADB_SHELL_DISPLAY_SETTINGS = "am start -a com.android.settings.DISPLAY_SETTINGS"
ADB_SHELL_INPUT_METHOD_SETTINGS = "am start -a android.settings.INPUT_METHOD_SETTINGS"
ADB_SHELL_SOUND_SETTINGS = "am start -a android.settings.SOUND_SETTINGS"
ADB_SHELL_WIFI_SETTINGS = "am start -a android.settings.WIFI_SETTINGS"
ADB_SHELL_APPLICATION_SETTINGS = "am start -a android.settings.APPLICATION_SETTINGS"
ADB_SHELL_ACCOUNT_SYNC_SETTINGS_ADD_ACCOUNT = (
    "am start -a android.settings.ACCOUNT_SYNC_SETTINGS_ADD_ACCOUNT"
)
ADB_SHELL_MANAGE_APPLICATIONS_SETTINGS = (
    "am start -a android.settings.MANAGE_APPLICATIONS_SETTINGS"
)
ADB_SHELL_SYNC_SETTINGS = "am start -a android.settings.SYNC_SETTINGS"
ADB_SHELL_DOCK_SETTINGS = "am start -a com.android.settings.DOCK_SETTINGS"
ADB_SHELL_ADD_ACCOUNT_SETTINGS = "am start -a android.settings.ADD_ACCOUNT_SETTINGS"
ADB_SHELL_SECURITY_SETTINGS = "am start -a android.settings.SECURITY_SETTINGS"
ADB_SHELL_DEVICE_INFO_SETTINGS = "am start -a android.settings.DEVICE_INFO_SETTINGS"
ADB_SHELL_WIRELESS_SETTINGS = "am start -a android.settings.WIRELESS_SETTINGS"
ADB_SHELL_SYSTEM_UPDATE_SETTINGS = "am start -a android.settings.SYSTEM_UPDATE_SETTINGS"
ADB_SHELL_MANAGE_ALL_APPLICATIONS_SETTINGS = (
    "am start -a android.settings.MANAGE_ALL_APPLICATIONS_SETTINGS"
)
ADB_SHELL_DATA_ROAMING_SETTINGS = "am start -a android.settings.DATA_ROAMING_SETTINGS"
ADB_SHELL_APN_SETTINGS = "am start -a android.settings.APN_SETTINGS"
ADB_SHELL_USER_DICTIONARY_SETTINGS = (
    "am start -a android.settings.USER_DICTIONARY_SETTINGS"
)
ADB_SHELL_VOICE_INPUT_OUTPUT_SETTINGS = (
    "am start -a com.android.settings.VOICE_INPUT_OUTPUT_SETTINGS"
)
ADB_SHELL_TTS_SETTINGS = "am start -a com.android.settings.TTS_SETTINGS"
ADB_SHELL_WIFI_IP_SETTINGS = "am start -a android.settings.WIFI_IP_SETTINGS"
ADB_SHELL_WEB_SEARCH_SETTINGS = "am start -a android.search.action.WEB_SEARCH_SETTINGS"
ADB_SHELL_BLUETOOTH_SETTINGS = "am start -a android.settings.BLUETOOTH_SETTINGS"
ADB_SHELL_AIRPLANE_MODE_SETTINGS = "am start -a android.settings.AIRPLANE_MODE_SETTINGS"
ADB_SHELL_INTERNAL_STORAGE_SETTINGS = (
    "am start -a android.settings.INTERNAL_STORAGE_SETTINGS"
)
ADB_SHELL_ACCESSIBILITY_SETTINGS = "am start -a android.settings.ACCESSIBILITY_SETTINGS"
ADB_SHELL_QUICK_LAUNCH_SETTINGS = (
    "am start -a com.android.settings.QUICK_LAUNCH_SETTINGS"
)
ADB_SHELL_PRIVACY_SETTINGS = "am start -a android.settings.PRIVACY_SETTINGS"
ADB_SHELL_DUMPSYS_INPUT = "dumpsys input"
ADB_SHELL_RESCAN_ALL_MEDIA = f"""find %s | while read f; do am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d \"file://${{f}}\"; done"""
ADB_SHELL_RESCAN_ONE_MEDIA = (
    f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d %s"
)
ADB_SHELL_LIST_USERS = "pm list users"

ADB_SHELL_SCREEN_COMPAT_ON = "am screen-compat on %s"
ADB_SHELL_SCREEN_COMPAT_OFF = "am screen-compat off %s"
ADB_SHELL_ENABLE_NOTIFICATIONS = "settings put global heads_up_notifications_enabled 1"
ADB_SHELL_DISABLE_NOTIFICATIONS = "settings put global heads_up_notifications_enabled 0"
ADB_SHELL_REMOVE_FILE = f"rm -f %s"
ADB_SHELL_UNPACK_TAR = "tar xvf %s"
ADB_SHELL_MEMDUMP = memdumpfunction = (
    r"""
getmemdump() {
    cat /proc/$1/maps | grep -v -E "rw-p.*deleted\)" | grep -E "rw-p.*" | awk '{print $1}' | (
        IFS="-"
        while read a b; do
            adec=$(printf "%d\n" 0x"$a")
            bdec=$(printf "%d\n" 0x"$b")
            si=$((bdec - adec))
            fina="/sdcard/$1_mem_$a.bin"
            echo "$fina"
            echo "$adec"
            echo "$bdec"
            echo "$si"
            dd if=/proc/$1/mem ibs=1 obs="$si" skip="$adec" count="$si" of="$fina"
            cat "$fina"
            rm -f "$fina"
        done
    )
}
getmemdump"""
    + "\n\n"
)

ADB_GET_imsi = "service call iphonesubinfo 7 i32 2"
ADB_GET_imei = "service call iphonesubinfo 3 i32 2"
ADB_GET_sims = "service call iphonesubinfo 11 i32 2"

ADB_IMEI_MULTI1 = r"""service call iphonesubinfo 4 i32 2 | awk -F "'" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS="""
ADB_IMEI_MULTI2 = r"""service call iphonesubinfo 4 i32 1 | awk -F "'" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS="""

ADB_IMEI_ANDROID14 = """service call iphonesubinfo 1 s16 com.android.shell | cut -c 52-66 | tr -d '.[:space:]'"""
ADB_SHELL_CLEAR_PACKAGE = "pm clear %s"
ADB_SHELL_STILL_IMAGE_CAMERA = "am start -a android.media.action.STILL_IMAGE_CAMERA"
ADB_SHELL_MAKE_CALL = "am start -a android.intent.action.CALL -d tel:%s"
ADB_SHELL_DUMPSYS_ACTIVITY_SETTINGS = "dumpsys activity settings"
ADB_SHELL_DUMPSYS_ACTIVITY_ALLOWED_ASSOCIATIONS = (
    "dumpsys activity allowed-associations"
)
ADB_SHELL_SAVE_THE_SHELL = """
pids=$(ps -a | grep -v grep | grep -E -o "([0-9]{1,}) (.*)$" | grep -v 'sh' | awk '{print $1}')
for pid in $pids; do
  kill -9 $pid
done
        """
ADB_SHELL_DUMPSYS_ACTIVITY_INTENTS = "dumpsys activity intents"
ADB_SHELL_DUMPSYS_ACTIVITY_BROADCASTS = "dumpsys activity broadcasts"
ADB_SHELL_DUMPSYS_ACTIVITY_BROADCAST_STATS = "dumpsys activity broadcast-stats"
ADB_SHELL_DUMPSYS_ACTIVITY_PROVIDERS = "dumpsys activity providers"
ADB_SHELL_DUMPSYS_ACTIVITY_PERMISSIONS = "dumpsys activity permissions"
ADB_SHELL_DUMPSYS_ACTIVITY_SERVICES = "dumpsys activity services"
ADB_SHELL_DUMPSYS_ACTIVITY_RECENTS = "dumpsys activity recents"
ADB_SHELL_DUMPSYS_ACTIVITY_LASTANR = "dumpsys activity lastanr"
ADB_SHELL_DUMPSYS_ACTIVITY_STARTER = "dumpsys activity starter"
ADB_SHELL_DUMPSYS_ACTIVITY_ACTIVITIES = "dumpsys activity activities"
ADB_SHELL_DUMPSYS_ACTIVITY_EXIT_INFO = "dumpsys activity exit-info"
ADB_SHELL_DUMPSYS_ACTIVITY_PROCESSES = "dumpsys activity processes"
ADB_SHELL_DUMPSYS_ACTIVITY_LRU = "dumpsys activity lru"
ADB_SHELL_PM_DUMP = "pm dump %s"
ADB_SHELL_GET_WM_SIZE = "wm size"
ADB_SHELL_CHANGE_WM_SIZE = "wm size %sx%s"
ADB_SHELL_WM_RESET_SIZE = "wm size reset"
ADB_SHELL_GET_WM_DENSITY = "wm density"
ADB_SHELL_CHANGE_WM_DENSITY = "wm density %s"
ADB_SHELL_WM_RESET_DENSITY = "wm density reset"
ADB_SHELL_LIST_FEATURES = "pm list features"
ADB_SHELL_PWD = "pwd"
ADB_SHELL_LIST_SERVICES = "service list"
ADB_SHELL_PS_A_T_L_Z = "ps -A -T -l -Z"
ADB_SHELL_OPEN_URL = "am start -a android.intent.action.VIEW -d %s"
ADB_SHELL_GET_NTP_SERVER = "settings get global ntp_server"
ADB_SHELL_SET_NTP_SERVER = 'settings put global ntp_server "%s"'
ADB_SHELL_PM_LIST_PACKAGES_F_I_U = "pm list packages -f -i -U"
ADB_SHELL_PM_LIST_PACKAGES_3 = "pm list packages -3"
ADB_SHELL_PM_LIST_PACKAGES_S = "pm list packages -s"
ADB_SHELL_MOUNT = "mount"
ADB_SHELL_CAT = "cat %s"
ADB_SHELL_SCREENCAP = "screencap -p"
ADB_SHELL_SCREENCAPRAW = "screencap"
ADB_SHELL_REMOUNT_ALL_RW = "mount -o remount,rw /"
ADB_SHELL_REMOUNT_ALL_RO = "mount -o remount,rw /"
ADB_SHELL_REMOVE_DATA_CACHE = r"mount -o remount,rw /; rm -r -f /data/cache"
ADB_SHELL_REMOVE_DALVIK_CACHE = r"mount -o remount,rw /; rm -r -f /data/dalvik-cache"
ADB_SHELL_REMOVE_USER_CACHE = r'mount -o remount,rw /; for cache in /data/user*/*/*/cache/*; do rm -rf "$cache"; done'
ADB_SHELL_GET_ANDROID_VERSION = "getprop ro.build.version.release"
ADB_SHELL_NETSTAT = r"netstat -n -W -p -a -e"
ADB_SHELL_START_PACKAGE = f"monkey -p %s 1"
ADB_SHELL_EXPAND_NOTIFICATIONS = "cmd statusbar expand-notifications"
ADB_SHELL_EXPAND_SETTINGS = "cmd statusbar expand-settings"
ADB_SHELL_RESOLVE_ACTIVITY_BRIEF = "cmd package resolve-activity --brief %s"
ADB_SHELL_RESOLVE_ACTIVITY = "cmd package resolve-activity %s"
ADB_SHELL_LIST_PERMISSION_GROUPS = "pm list permission-groups"
ADB_SHELL_DUMPSYS_WINDOW = "dumpsys window"
ADB_SHELL_INPUT_TAP = "input tap %s %s"
ADB_SHELL_INPUT_DPAD_TAP = "input dpad tap %s %s"
ADB_SHELL_INPUT_KEYBOARD_TAP = "input keyboard tap %s %s"
ADB_SHELL_INPUT_MOUSE_TAP = "input mouse tap %s %s"
ADB_SHELL_INPUT_TOUCHPAD_TAP = "input touchpad tap %s %s"
ADB_SHELL_INPUT_GAMEPAD_TAP = "input gamepad tap %s %s"
ADB_SHELL_INPUT_TOUCHNAVIGATION_TAP = "input touchnavigation tap %s %s"
ADB_SHELL_INPUT_JOYSTICK_TAP = "input joystick tap %s %s"
ADB_SHELL_INPUT_TOUCHSCREEN_TAP = "input touchscreen tap %s %s"
ADB_SHELL_INPUT_STYLUS_TAP = "input stylus tap %s %s"
ADB_SHELL_INPUT_TRACKBALL_TAP = "input trackball tap %s %s"
ADB_SHELL_INPUT_DPAD_SWIPE = "input dpad swipe %s %s %s %s %s"
ADB_SHELL_INPUT_DPAD_DRAGANDDROP = "input dpad draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_DPAD_ROLL = "input dpad roll %s %s"
ADB_SHELL_INPUT_KEYBOARD_SWIPE = "input keyboard swipe %s %s %s %s %s"
ADB_SHELL_INPUT_KEYBOARD_DRAGANDDROP = "input keyboard draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_KEYBOARD_ROLL = "input keyboard roll %s %s"
ADB_SHELL_INPUT_MOUSE_SWIPE = "input mouse swipe %s %s %s %s %s"
ADB_SHELL_INPUT_MOUSE_DRAGANDDROP = "input mouse draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_MOUSE_ROLL = "input mouse roll %s %s"
ADB_SHELL_INPUT_TOUCHPAD_SWIPE = "input touchpad swipe %s %s %s %s %s"
ADB_SHELL_INPUT_TOUCHPAD_DRAGANDDROP = "input touchpad draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_TOUCHPAD_ROLL = "input touchpad roll %s %s"
ADB_SHELL_INPUT_GAMEPAD_SWIPE = "input gamepad swipe %s %s %s %s %s"
ADB_SHELL_INPUT_GAMEPAD_DRAGANDDROP = "input gamepad draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_GAMEPAD_ROLL = "input gamepad roll %s %s"
ADB_SHELL_INPUT_TOUCHNAVIGATION_SWIPE = "input touchnavigation swipe %s %s %s %s %s"
ADB_SHELL_INPUT_TOUCHNAVIGATION_DRAGANDDROP = (
    "input touchnavigation draganddrop %s %s %s %s %s"
)
ADB_SHELL_INPUT_TOUCHNAVIGATION_ROLL = "input touchnavigation roll %s %s"
ADB_SHELL_INPUT_JOYSTICK_SWIPE = "input joystick swipe %s %s %s %s %s"
ADB_SHELL_INPUT_JOYSTICK_DRAGANDDROP = "input joystick draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_JOYSTICK_ROLL = "input joystick roll %s %s"
ADB_SHELL_INPUT_TOUCHSCREEN_SWIPE = "input touchscreen swipe %s %s %s %s %s"
ADB_SHELL_INPUT_TOUCHSCREEN_DRAGANDDROP = "input touchscreen draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_TOUCHSCREEN_ROLL = "input touchscreen roll %s %s"
ADB_SHELL_INPUT_STYLUS_SWIPE = "input stylus swipe %s %s %s %s %s"
ADB_SHELL_INPUT_STYLUS_DRAGANDDROP = "input stylus draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_STYLUS_ROLL = "input stylus roll %s %s"
ADB_SHELL_INPUT_TRACKBALL_SWIPE = "input trackball swipe %s %s %s %s %s"
ADB_SHELL_INPUT_TRACKBALL_DRAGANDDROP = "input trackball draganddrop %s %s %s %s %s"
ADB_SHELL_INPUT_TRACKBALL_ROLL = "input trackball roll %s %s"
ADB_SHELL_GET_PIDOF = "pidof %s"
ADB_SHELL_AM_FORCE_STOP = "am force-stop %s"
ADB_SHELL_KILLALL_9 = "killall -9 %s"
ADB_SHELL_AM_KILL = "am kill %s"
ADB_SHELL_PKILL = "pkill %s"

ADB_SCRIPT_GET_RGB_VALUE_AT_COORD = R"""#!/bin/bash
get_width_height() {
    local -n stringarraywidthheight=$1
    stringarraywidthheight=()
    screen_width=$(wm size | grep -oE '[0-9]+x[0-9]+$')
    stringarraywidthheight=()
    dlim="x"
    splitstringdelim stringarraywidthheight "$screen_width" "$dlim"
    echo "${stringarraywidthheight[0]}"
    echo "${stringarraywidthheight[1]}"
}

splitstringdelim() {
    local -n stringarray="$1"
    inputstring=$2
    sep=$3
    allfilessplit=$(tr "$sep" '\r' <<<"$inputstring")
    array=($(echo $allfilessplit | sed 's/\r/\n/g'))
    for l in "${array[@]}"; do
        stringarray+=("$l")
    done
}

get_rgb_value_at_coords() {
    x_coord="$1"
    y_coord="$2"
    screen_width="$3"
    local -n rgbresults="$4"

    color_depth_bytes=4
    offset_bytes=$(((y_coord * screen_width + x_coord) * color_depth_bytes))
    offset_bytes=$((offset_bytes - color_depth_bytes))
    offset_bytes=$((offset_bytes + 16))
    screencap /sdcard/dumpdata.tmp
    rgbdata=$(hexdump -n 4 -s $offset_bytes -e '"%%07.8_Ad\n"' -e'4/1 "%%d "" "' /sdcard/dumpdata.tmp)
    IFS=" " read -r r g b alpha offset_dec <<<"$rgbdata"
    coldepth=$((screen_width * color_depth_bytes))
    y=$((offset_dec / coldepth))
    x=$((offset_dec %% coldepth))
    x=$((x - 16))
    x=$((x / color_depth_bytes))
    rgbresults[0]="$x"
    rgbresults[1]="$y"
    rgbresults[2]="$r"
    rgbresults[3]="$g"
    rgbresults[4]="$b"
}

screen_width=%s
screen_height=%s
allrgbresults=()
x_coordinate=%s
y_coordinate=%s
while true; do
  get_rgb_value_at_coords $x_coordinate $y_coordinate "$screen_width" allrgbresults
  echo "${allrgbresults[0]},${allrgbresults[1]},${allrgbresults[2]},${allrgbresults[3]},${allrgbresults[4]}"
  unset allrgbresults
  break
done"""


activityelementsbasic = r"""
while true; do
    execute_all
    if [ "$print_csv" -gt 0 ]; then
        echo "$ALL_COLUMNS"
        for row in "${INDEX_ARRAY[@]}"; do
            #echo "----------------------------"
            for column in "${COLUMNS[@]}"; do
                indexarray=$((row + column))
                #echo -n "$row ${NAMESCOLUMNS[column]}"
                echo -n "\"${array_elements[indexarray]}\""
                if [ "$column" != "$ARRAY_MAX_INDEX" ]; then
                    echo -n ","
                fi
            done
            echo ""
        done
    fi
    unset INDEX_ARRAY
    unset array_elements
    break
done

"""

activityelements = r"""
#!/bin/bash
fileout="/sdcard/dumpsys_output.txt"
filex="/sdcard/filenames_output.txt"
filenamesmatch="/sdcard/match_filenames.txt"
rm -f "$fileout"
rm -f "$filex"
rm -f "$filenamesmatch"
with_class=WITH_CLASS_REPLACE
with_mid=WITH_MID_REPLACE
with_hashcode=WITH_HASHCODE_REPLACE
with_elementid=WITH_ELEMENTID_REPLACE
with_visibility=WITH_VISIBILITY_REPLACE
with_focusable=WITH_FOCUSABLE_REPLACE
with_enabled=WITH_ENABLED_REPLACE
with_drawn=WITH_DRAWN_REPLACE
with_scrollbars_horizontal=WITH_SCROLLBARS_HORIZONTAL_REPLACE
with_scrollbars_vertical=WITH_SCROLLBARS_VERTICAL_REPLACE
with_clickable=WITH_CLICKABLE_REPLACE
with_long_clickable=WITH_LONG_CLICKABLE_REPLACE
with_context_clickable=WITH_CONTEXT_CLICKABLE_REPLACE
with_pflag_is_root_namespace=WITH_PFLAG_IS_ROOT_NAMESPACE_REPLACE
with_pflag_focused=WITH_PFLAG_FOCUSED_REPLACE
with_pflag_selected=WITH_PFLAG_SELECTED_REPLACE
with_pflag_prepressed=WITH_PFLAG_PREPRESSED_REPLACE
with_pflag_hovered=WITH_PFLAG_HOVERED_REPLACE
with_pflag_activated=WITH_PFLAG_ACTIVATED_REPLACE
with_pflag_invalidated=WITH_PFLAG_INVALIDATED_REPLACE
with_pflag_dirty_mask=WITH_PFLAG_DIRTY_MASK_REPLACE
stripline=STRIPLINE_REPLACE
defaultval="DEFAULTVALUE_REPLACE"
print_csv=PRINT_CSV_REPLACE

only_active=1

IS_ACTIVE=0
ELEMENT_INDEX=1
START_X=2
START_Y=3
CENTER_X=4
CENTER_Y=5
AREA=6
END_X=7
END_Y=8
WIDTH=9
HEIGHT=10
START_X_RELATIVE=11
START_Y_RELATIVE=12
END_X_RELATIVE=13
END_Y_RELATIVE=14
PARENTSINDEX=15
ELEMENT_ID=16
MID=17
HASHCODE=18
VISIBILITY=19
FOCUSABLE=20
ENABLED=21
DRAWN=22
SCROLLBARS_HORIZONTAL=23
SCROLLBARS_VERTICAL=24
CLICKABLE=25
LONG_CLICKABLE=26
CONTEXT_CLICKABLE=27
CLASSNAME=28
PFLAG_IS_ROOT_NAMESPACE=29
PFLAG_FOCUSED=30
PFLAG_SELECTED=31
PFLAG_PREPRESSED=32
PFLAG_HOVERED=33
PFLAG_ACTIVATED=34
PFLAG_INVALIDATED=35
PFLAG_DIRTY_MASK=36
LINE_STRIPPED=37
ARRAY_WIDTH=38
ARRAY_MAX_INDEX=$((ARRAY_WIDTH - 1))
INDEX_ARRAY=()
array_elements=()
COLUMNS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37)
NAMESCOLUMNS=(IS_ACTIVE ELEMENT_INDEX START_X START_Y CENTER_X CENTER_Y AREA END_X END_Y WIDTH HEIGHT START_X_RELATIVE START_Y_RELATIVE END_X_RELATIVE END_Y_RELATIVE PARENTSINDEX ELEMENT_ID MID HASHCODE VISIBILITY FOCUSABLE ENABLED DRAWN SCROLLBARS_HORIZONTAL SCROLLBARS_VERTICAL CLICKABLE LONG_CLICKABLE CONTEXT_CLICKABLE CLASSNAME PFLAG_IS_ROOT_NAMESPACE PFLAG_FOCUSED PFLAG_SELECTED PFLAG_PREPRESSED PFLAG_HOVERED PFLAG_ACTIVATED PFLAG_INVALIDATED PFLAG_DIRTY_MASK LINE_STRIPPED)
ALL_COLUMNS="IS_ACTIVE,ELEMENT_INDEX,START_X,START_Y,CENTER_X,CENTER_Y,AREA,END_X,END_Y,WIDTH,HEIGHT,START_X_RELATIVE,START_Y_RELATIVE,END_X_RELATIVE,END_Y_RELATIVE,PARENTSINDEX,ELEMENT_ID,MID,HASHCODE,VISIBILITY,FOCUSABLE,ENABLED,DRAWN,SCROLLBARS_HORIZONTAL,SCROLLBARS_VERTICAL,CLICKABLE,LONG_CLICKABLE,CONTEXT_CLICKABLE,CLASSNAME,PFLAG_IS_ROOT_NAMESPACE,PFLAG_FOCUSED,PFLAG_SELECTED,PFLAG_PREPRESSED,PFLAG_HOVERED,PFLAG_ACTIVATED,PFLAG_INVALIDATED,PFLAG_DIRTY_MASK,LINE_STRIPPED"
process_matches() {
    rm -f "$fileout"
    rm -f "$filex"
    rm -f "$filenamesmatch"
    dumpsys activity top -c >"$fileout"
    awk '/View Hierarchy:/ {
        output = $0
        next
    }
    output {
        output = output "\n" $0
    }
    /Looper/ {
        if (output) {
            # Process and print each match separately
            # print "Match found:"
            print output

            # Save each match to a separate file
            match_file = "/sdcard/match_" NR ".txt"
            print output > match_file
            close(match_file)

            # Save the filename to a separate file
            print match_file > "/sdcard/match_filenames.txt"

            output = ""
        }
    }' "$fileout" >"$filex"
}

trim() {
    local var="$1"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    var="${var//\"/}"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo "$var"
}

process_result() {
    resultx="$1"
    groups=("$resultx")
    classname=''
    defaultvalue="$2"
    if [ -z "$resultx" ]; then
        classname="$defaultvalue"
    else
        for group in "${groups[@]}"; do
            classname="${classname} ${group}"
        done
    fi
    classnamestriped=$(trim "$classname")
    if [ "$classnamestriped" = "" ]; then
        classnamestriped="$defaultval"
    fi
    echo "$classnamestriped"
}
execute_all() {
    process_matches
    match_filenames_names=()
    filecounter=0
    while IFS= read -r filename; do
        match_filenames_names+=("$filename")
        filecounter=$((filecounter + 1))
        sed -i '1,2d' "$filename"
        sed -i '$d' "$filename"
    done <"$filenamesmatch"
    filecountermain=0
    isactivemainwindow=0
    element_index=0
    for file in "${match_filenames_names[@]}"; do
        filecountermain=$((filecountermain + 1))
        if [ "$only_active" -gt 0 ]; then
            if [ "$filecountermain" -lt "$filecounter" ]; then
                rm -f "$file"
                continue
            fi
        fi
        if [ "$filecountermain" -ge "$filecounter" ]; then
            isactivemainwindow=$((isactivemainwindow + 1))
        fi
        file_len=$(wc -l <"$file")
        file_contents=$(<"$file")
        rm -f "$file"
        output_array_coords=()
        output_array_lines=()
        output_array_index=()
        output_array_coords_start_x=()
        output_array_coords_start_y=()
        output_array_coords_end_x=()
        output_array_coords_end_y=()
        output_array_count=()
        output_array_index_rev=()
        output_array_coords_rev=()
        output_array_lines_rev=()
        output_array_coords_start_x_rev=()
        output_array_coords_start_y_rev=()
        output_array_coords_end_x_rev=()
        output_array_coords_end_y_rev=()
        output_array_count_rev=()
        i=0
        j="$file_len"
        while IFS= read -r line0; do
            j=$((j - 1))
            line0="${line0%?} "
            lxa=$(echo "$line0" | awk '{ for (i=1; i<=NF; i++) if ($i ~ /^[0-9,-]+$/) print $i }' || echo "0 0 0 0")
            lxa2=$(echo "$lxa" | sed -n -E 's/[^0-9]*([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]*/\1 \2 \3 \4/p' || echo "0 0 0 0")
            string0="$line0"
            count0="${#string0}"
            string0="${string0#"${string0%%[![:space:]]*}"}"
            count0=$((count0 - ${#string0}))
            output_array_coords+=("$lxa2")
            output_array_lines+=("$string0")
            output_array_index+=("$i")
            output_array_count+=("$count0")
            output_array_index_rev+=("$j")
            IFS=" " read -r startx_temp1 starty_temp1 endx1 endy1 <<<"$lxa2"
            output_array_coords_start_x+=("$startx_temp1")
            output_array_coords_start_y+=("$starty_temp1")
            output_array_coords_end_x+=("$endx1")
            output_array_coords_end_y+=("$endy1")
            i=$((i + 1))
        done <<<"$file_contents"
        for element in "${output_array_index_rev[@]}"; do
            output_array_coords_rev+=("${output_array_coords[element]}")
            output_array_lines_rev+=("${output_array_lines[element]}")
            output_array_coords_start_x_rev+=("${output_array_coords_start_x[element]}")
            output_array_coords_start_y_rev+=("${output_array_coords_start_y[element]}")
            output_array_coords_end_x_rev+=("${output_array_coords_end_x[element]}")
            output_array_coords_end_y_rev+=("${output_array_coords_end_y[element]}")
            output_array_count_rev+=("${output_array_count[element]}")
        done
        indexrevcounter=0
        reversecounterchecker=$((file_len - 1))
        resultmid="$defaultval"
        result_visibility="$defaultval"
        result_focusable="$defaultval"
        result_enabled="$defaultval"
        result_drawn="$defaultval"
        result_scrollbars_horizontal="$defaultval"
        result_scrollbars_vertical="$defaultval"
        result_clickable="$defaultval"
        result_long_clickable="$defaultval"
        result_context_clickable="$defaultval"
        resultclass="$defaultval"
        result_pflag_is_root_namespace="$defaultval"
        result_pflag_focused="$defaultval"
        result_pflag_selected="$defaultval"
        result_pflag_prepressed="$defaultval"
        result_pflag_hovered="$defaultval"
        result_pflag_activated="$defaultval"
        result_pflag_invalidated="$defaultval"
        result_pflag_dirty_mask="$defaultval"
        for element in "${output_array_index[@]}"; do
            line0="${output_array_lines[element]}"
            startx0="${output_array_coords_start_x[element]}"
            starty0="${output_array_coords_start_y[element]}"
            count0="${output_array_count[element]}"
            indexrevcounter=$((indexrevcounter - indexrevcounter))
            parents='|'
            for element1 in "${output_array_index[@]}"; do
                indexrev="${output_array_index_rev[element1]}"
                indexrevcounter=$((indexrevcounter + 1))
                if [ "$indexrev" -lt "$element" ]; then
                    startx1="${output_array_coords_start_x_rev[element1]}"
                    starty1="${output_array_coords_start_y_rev[element1]}"
                    endx1="${output_array_coords_end_x_rev[element1]}"
                    endy1="${output_array_coords_end_y_rev[element1]}"
                    count1="${output_array_count_rev[element1]}"
                    if [ "$count1" -lt "$count0" ]; then
                        parents="${parents}${indexrev}|"
                        count0=$((count1 + 0))
                        startx0=$((startx0 + startx1))
                        starty0=$((starty0 + starty1))
                    fi
                fi
                if [ "$indexrevcounter" -eq "$reversecounterchecker" ]; then
                    relativexstart="${output_array_coords_start_x[element]}"
                    relativeystart="${output_array_coords_start_y[element]}"
                    relativexend="${output_array_coords_end_x[element]}"
                    relativeyend="${output_array_coords_end_y[element]}"
                    relativexend=$((relativexend - relativexstart))
                    relativeyend=$((relativeyend - relativeystart))
                    absxend=$((startx0 + relativexend))
                    absyend=$((starty0 + relativeyend))
                    width=$((absxend - startx0))
                    height=$((absyend - starty0))
                    area=$((width * height))
                    centerx=$((width / 2 + startx0))
                    centery=$((height / 2 + starty0))
                    relativexend="${output_array_coords_end_x[element]}"
                    relativeyend="${output_array_coords_end_y[element]}"
                    if [ "$with_class" -gt 0 ]; then
                        classsearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*([^[:space:]]+)\{.*/\1/p')
                        resultclass=$(process_result "$classsearch" "$defaultval")
                    fi
                    if [ "$with_mid" -gt 0 ]; then
                        midsearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{([a-fA-F0-9]+)[[:space:]]+.*/\1/p')
                        resultmid=$(process_result "$midsearch" "$defaultval")
                    fi
                    if [ "$with_hashcode" -gt 0 ]; then
                        hashcodesearch=$(echo "$line0" | sed -n -E 's/^[^#]+[[:space:]]+#([a-f0-9]+)[[:space:]]+.*/\1/p')
                        resulthashcode=$(process_result "$hashcodesearch" "$defaultval")
                    fi
                    if [ "$with_elementid" -gt 0 ]; then
                        elementidsearch=$(echo "$line0" | sed -n -E 's/^[^:]+[[:space:]]+([^[:space:]]+:[^[:space:]]+)\}?.*/\1/p')
                        resultelementid=$(process_result "$elementidsearch" "$defaultval")
                    fi
                    execute_first_flag=$((with_visibility + with_focusable + with_enabled + with_drawn + with_scrollbars_horizontal + with_scrollbars_vertical + with_clickable + with_long_clickable + with_context_clickable))
                    if [ "$execute_first_flag" -gt 0 ]; then
                        firstimesearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{[a-fA-F0-9]+[[:space:]]+([A-Z.]{8,9})[[:space:]]+.*/\1/p')
                    fi
                    if [ "$with_visibility" -gt 0 ]; then
                        visibility_search=$"${firstimesearch:0:1}"
                        if [ "$visibility_search" = "." ]; then
                            visibility_search="$defaultval"
                        fi

                        result_visibility="$visibility_search"
                    fi
                    if [ "$with_focusable" -gt 0 ]; then
                        focusable_search=$"${firstimesearch:1:1}"
                        if [ "$focusable_search" = "." ]; then
                            focusable_search="$defaultval"
                        fi

                        result_focusable="$focusable_search"
                    fi
                    if [ "$with_enabled" -gt 0 ]; then
                        enabled_search=$"${firstimesearch:2:1}"
                        if [ "$enabled_search" = "." ]; then
                            enabled_search="$defaultval"
                        fi

                        result_enabled="$enabled_search"
                    fi
                    if [ "$with_drawn" -gt 0 ]; then
                        drawn_search=$"${firstimesearch:3:1}"
                        if [ "$drawn_search" = "." ]; then
                            drawn_search="$defaultval"
                        fi

                        result_drawn="$drawn_search"
                    fi
                    if [ "$with_scrollbars_horizontal" -gt 0 ]; then
                        scrollbars_horizontal_search=$"${firstimesearch:4:1}"
                        if [ "$scrollbars_horizontal_search" = "." ]; then
                            scrollbars_horizontal_search="$defaultval"
                        fi

                        result_scrollbars_horizontal="$scrollbars_horizontal_search"
                    fi
                    if [ "$with_scrollbars_vertical" -gt 0 ]; then
                        scrollbars_vertical_search=$"${firstimesearch:5:1}"
                        if [ "$scrollbars_vertical_search" = "." ]; then
                            scrollbars_vertical_search="$defaultval"
                        fi

                        result_scrollbars_vertical="$scrollbars_vertical_search"
                    fi
                    if [ "$with_clickable" -gt 0 ]; then
                        clickable_search=$"${firstimesearch:6:1}"
                        if [ "$clickable_search" = "." ]; then
                            clickable_search="$defaultval"
                        fi

                        result_clickable="$clickable_search"
                    fi
                    if [ "$with_long_clickable" -gt 0 ]; then
                        long_clickable_search=$"${firstimesearch:7:1}"
                        if [ "$long_clickable_search" = "." ]; then
                            long_clickable_search="$defaultval"
                        fi

                        result_long_clickable="$long_clickable_search"
                    fi
                    if [ "$with_context_clickable" -gt 0 ]; then
                        if [ ${#firstimesearch} -gt 8 ]; then
                            context_clickable_search=$"${firstimesearch:8:1}"
                            if [ "$context_clickable_search" = "." ]; then
                                context_clickable_search="$defaultval"
                                result_context_clickable="$context_clickable_search"

                            fi
                        fi
                    fi
                    execute_second_flag=$((with_pflag_is_root_namespace + with_pflag_focused + with_pflag_selected + with_pflag_prepressed + with_pflag_hovered + with_pflag_activated + with_pflag_invalidated + with_pflag_dirty_mask))
                    if [ "$execute_second_flag" -gt 0 ]; then
                        secondtimesearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{[a-fA-F0-9]+[[:space:]]+[A-Z.]{8,9}[[:space:]]+([A-Z.]{8}).*/\1/p')
                    fi
                    if [ "$with_pflag_is_root_namespace" -gt 0 ]; then
                        pflag_is_root_namespace_search=$"${secondtimesearch:0:1}"
                        if [ "$pflag_is_root_namespace_search" = "." ]; then
                            pflag_is_root_namespace_search="$defaultval"
                        fi

                        result_pflag_is_root_namespace="$pflag_is_root_namespace_search"
                    fi
                    if [ "$with_pflag_focused" -gt 0 ]; then
                        pflag_focused_search=$"${secondtimesearch:1:1}"
                        if [ "$pflag_focused_search" = "." ]; then
                            pflag_focused_search="$defaultval"
                        fi

                        result_pflag_focused="$pflag_focused_search"
                    fi
                    if [ "$with_pflag_selected" -gt 0 ]; then
                        pflag_selected_search=$"${secondtimesearch:2:1}"
                        if [ "$pflag_selected_search" = "." ]; then
                            pflag_selected_search="$defaultval"
                        fi

                        result_pflag_selected="$pflag_selected_search"
                    fi
                    if [ "$with_pflag_prepressed" -gt 0 ]; then
                        pflag_prepressed_search=$"${secondtimesearch:3:1}"
                        if [ "$pflag_prepressed_search" = "." ]; then
                            pflag_prepressed_search="$defaultval"
                        fi

                        result_pflag_prepressed="$pflag_prepressed_search"
                    fi
                    if [ "$with_pflag_hovered" -gt 0 ]; then
                        pflag_hovered_search=$"${secondtimesearch:4:1}"
                        if [ "$pflag_hovered_search" = "." ]; then
                            pflag_hovered_search="$defaultval"
                        fi

                        result_pflag_hovered="$pflag_hovered_search"
                    fi
                    if [ "$with_pflag_activated" -gt 0 ]; then
                        pflag_activated_search=$"${secondtimesearch:5:1}"
                        if [ "$pflag_activated_search" = "." ]; then
                            pflag_activated_search="$defaultval"
                        fi

                        result_pflag_activated="$pflag_activated_search"
                    fi
                    if [ "$with_pflag_invalidated" -gt 0 ]; then
                        pflag_invalidated_search=$"${secondtimesearch:6:1}"
                        if [ "$pflag_invalidated_search" = "." ]; then
                            pflag_invalidated_search="$defaultval"
                        fi

                        result_pflag_invalidated="$pflag_invalidated_search"
                    fi
                    if [ "$with_pflag_dirty_mask" -gt 0 ]; then
                        pflag_dirty_mask_search=$"${secondtimesearch:7:1}"
                        if [ "$pflag_dirty_mask_search" = "." ]; then
                            pflag_dirty_mask_search="$defaultval"
                        fi

                        result_pflag_dirty_mask="$pflag_dirty_mask_search"
                    fi
                    if [ "$stripline" -gt 0 ]; then
                        #line0stripped=$(echo "$line0" | tr -d '[:space:]|')
                        line0stripped=$(trim "$line0")
                    else
                        line0stripped="$line0"
                    fi
                    INDEX_ARRAY+=($((element_index * ARRAY_WIDTH)))
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((IS_ACTIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_INDEX))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((AREA))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((WIDTH))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PARENTSINDEX))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_ID))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((MID))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HASHCODE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((VISIBILITY))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ENABLED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((DRAWN))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_HORIZONTAL))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_VERTICAL))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CONTEXT_CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLASSNAME))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_IS_ROOT_NAMESPACE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_FOCUSED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_SELECTED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_PREPRESSED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_HOVERED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_ACTIVATED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_INVALIDATED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_DIRTY_MASK))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LINE_STRIPPED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((IS_ACTIVE))))]=1
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_INDEX))))]="$element"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X))))]="$startx0"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y))))]="$starty0"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$centerx"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$centery"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((AREA))))]="$area"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X))))]="$absxend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y))))]="$absyend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((WIDTH))))]="$width"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$height"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X_RELATIVE))))]="$relativexstart"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y_RELATIVE))))]="$relativeystart"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X_RELATIVE))))]="$relativexend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y_RELATIVE))))]="$relativeyend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PARENTSINDEX))))]="$parents"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_ID))))]="$resultelementid"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((MID))))]="$resultmid"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HASHCODE))))]="$resulthashcode"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((VISIBILITY))))]="$result_visibility"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$result_focusable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ENABLED))))]="$result_enabled"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((DRAWN))))]="$result_drawn"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_HORIZONTAL))))]="$result_scrollbars_horizontal"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_VERTICAL))))]="$result_scrollbars_vertical"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$result_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$result_long_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CONTEXT_CLICKABLE))))]="$result_context_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLASSNAME))))]="$resultclass"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_IS_ROOT_NAMESPACE))))]="$result_pflag_is_root_namespace"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_FOCUSED))))]="$result_pflag_focused"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_SELECTED))))]="$result_pflag_selected"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_PREPRESSED))))]="$result_pflag_prepressed"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_HOVERED))))]="$result_pflag_hovered"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_ACTIVATED))))]="$result_pflag_activated"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_INVALIDATED))))]="$result_pflag_invalidated"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_DIRTY_MASK))))]="$result_pflag_dirty_mask"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LINE_STRIPPED))))]="$line0stripped"
                    element_index=$((element_index + 1))
                fi
            done
        done
    done
}
ADD_TO_SCRIPT_REPLACE

"""


uiautomatorscriptbasis = r"""
while true; do
    outputuidump=$(uiautomator dump 2>&1 >/dev/null)
    if [ -n "$outputuidump" ]; then
        continue
    fi
    parse_uiautomator
    if [ "$print_csv" -gt 0 ]; then
        echo "$ALL_COLUMNS"
        for row in "${INDEX_ARRAY[@]}"; do
            for column in "${COLUMNS[@]}"; do
                indexarray=$((row + column))
                echo -n "\"${array_elements[indexarray]}\""
                if [ "$column" != "$ARRAY_MAX_INDEX" ]; then
                    echo -n ","
                fi
            done
            echo ""
        done
    fi
    unset INDEX_ARRAY
    unset array_elements
    break
done        
        """

uiautomatorscript = r"""
#!/bin/bash
INDEX=0
TEXT=1
RESOURCE_ID=2
CLASS=3
PACKAGE=4
CONTENT_DESC=5
CHECKABLE=6
CHECKED=7
CLICKABLE=8
ENABLED=9
FOCUSABLE=10
FOCUSED=11
SCROLLABLE=12
LONG_CLICKABLE=13
PASSWORD=14
SELECTED=15
BOUNDS=16
STARTX=17
ENDX=18
STARTY=19
ENDY=20
CENTER_X=21
CENTER_Y=22
AREA=23
WIDTH=24
HEIGHT=25
ARRAY_WIDTH=26
ARRAY_MAX_INDEX=$((ARRAY_WIDTH - 1))
COLUMNS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25)
NAMESCOLUMNS=(INDEX TEXT RESOURCE_ID CLASS PACKAGE CONTENT_DESC CHECKABLE CHECKED CLICKABLE ENABLED FOCUSABLE FOCUSED SCROLLABLE LONG_CLICKABLE PASSWORD SELECTED BOUNDS STARTX ENDX STARTY ENDY CENTER_X CENTER_Y AREA WIDTH HEIGHT)
ALL_COLUMNS="INDEX,TEXT,RESOURCE_ID,CLASS,PACKAGE,CONTENT_DESC,CHECKABLE,CHECKED,CLICKABLE,ENABLED,FOCUSABLE,FOCUSED,SCROLLABLE,LONG_CLICKABLE,PASSWORD,SELECTED,BOUNDS,STARTX,ENDX,STARTY,ENDY,CENTER_X,CENTER_Y,AREA,WIDTH,HEIGHT"
array_elements=()
INDEX_ARRAY=()
print_csv=PRINT_CSV_REPLACE
defaultval="DEFAULTVALUE_REPLACE"

trim() {
    local var="$1"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}
parse_uiautomator() {
    grep -o -E '<([A-Za-z_:]|[^\x00-\x7F])([A-Za-z0-9_:.-]|[^\x00-\x7F])*([ \n\t\r]+([A-Za-z_:]|[^\x00-\x7F])([A-Za-z0-9_:.-]|[^\x00-\x7F])*([ \n\t\r]+)?=([ \n\t\r]+)?("[^<"]*"|'\''[^<'\'']*'\''))*([ \n\t\r]+)?/?>?' /sdcard/window_dump.xml | grep -o -E '([a-zA-Z0-9\-]+)=(("[^"]*")|('\''[^'\'']*'\''))' | awk '{ printf "\"AAAA%sQQQQ", $1, ""} END { print "\n" }' | sed 's/QQQQ"AAAA/\nQQQQAAAA/g' | sed 's/AAAAindex=/\nQQQQAAAANEWELEMENT="EE"\nQQQQAAAAindex=/g' >/sdcard/outputui.txt
    file_contents=$(<"/sdcard/outputui.txt")
    j=0
    i=0
    while IFS= read -r line0; do
        keyx=$(echo "$line0" | sed -n -E 's/QQQQAAAA([^=]+)=\"([^\"]*)\"?/\1/p')
        if [ "$keyx" = "boundsQQQQ" ]; then
            keyx="bounds"
        fi
        valx=$(echo "$line0" | sed -n -E 's/QQQQAAAA([^=]+)=\"([^\"]*)\"?/\2/p')
        valx=$(trim "$valx")
        if [ "$valx" = "" ]; then
            valx="$defaultval"
        fi
        if [ "$keyx" = "NEWELEMENT" ]; then
            iar=$((j * ARRAY_WIDTH))
            INDEX_ARRAY+=("$iar")
            j=$((j + 1))
            i=$((j - 1))
            array_elements[$((i * $((ARRAY_WIDTH)) + $((INDEX))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((TEXT))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((RESOURCE_ID))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLASS))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PACKAGE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CONTENT_DESC))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENABLED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SCROLLABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PASSWORD))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SELECTED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((BOUNDS))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTX))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDX))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTY))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDY))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((AREA))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((WIDTH))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$defaultval"
        fi
        if [ "$keyx" = "index" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((INDEX))))]="$valx"
        fi
        if [ "$keyx" = "text" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((TEXT))))]="$valx"
        fi
        if [ "$keyx" = "resource-id" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((RESOURCE_ID))))]="$valx"
        fi
        if [ "$keyx" = "class" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLASS))))]="$valx"
        fi
        if [ "$keyx" = "package" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PACKAGE))))]="$valx"
        fi
        if [ "$keyx" = "content-desc" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CONTENT_DESC))))]="$valx"
        fi
        if [ "$keyx" = "checkable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKABLE))))]="$valx"
        fi
        if [ "$keyx" = "checked" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKED))))]="$valx"
        fi
        if [ "$keyx" = "clickable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$valx"
        fi
        if [ "$keyx" = "enabled" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENABLED))))]="$valx"
        fi
        if [ "$keyx" = "focusable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$valx"
        fi
        if [ "$keyx" = "focused" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSED))))]="$valx"
        fi
        if [ "$keyx" = "scrollable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SCROLLABLE))))]="$valx"
        fi
        if [ "$keyx" = "long-clickable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$valx"
        fi
        if [ "$keyx" = "password" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PASSWORD))))]="$valx"
        fi
        if [ "$keyx" = "selected" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SELECTED))))]="$valx"
        fi
        if [ "$keyx" = "bounds" ]; then
            lxa2y=$(echo "$valx" | sed -n -E 's/[^0-9]*\[([0-9]+),([0-9]+)\]\[([0-9]+),([0-9]+)\][^0-9]*/\1 \2 \3 \4/p' || echo "0 0 0 0")
            array_elements[$((i * $((ARRAY_WIDTH)) + $((BOUNDS))))]="$lxa2y"
            IFS=" " read -r startxtmp startytmp endxtmp endytmp <<<"$lxa2y"
            widthx=$((endxtmp - startxtmp))
            heighty=$((endytmp - startytmp))
            area=$((widthx * heighty))
            centerx=$((widthx / 2 + startxtmp))
            centery=$((heighty / 2 + startytmp))
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTX))))]="$startxtmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDX))))]="$endxtmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTY))))]="$startytmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDY))))]="$endytmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$centerx"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$centery"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((AREA))))]="$area"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((WIDTH))))]="$widthx"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$heighty"
        fi
    done <<<"$file_contents"
}
ADD_TO_SCRIPT_REPLACE
"""

compare2files = """
#!/bin/bash
splitlines_file(){
local -n oarra="$1"
filex=$2
file_contentscx=$(<"$filex")
while IFS= read -r line; do
    oarra+=("$line")
done <<<"$file_contentscx"
}

swap_arrays() {
    local -n arr1="$1"
    local -n arr2="$2"
    tmp1=()
    tmp2=()
    for liney in "${arr1[@]}"; do
        tmp1+=("$liney")
    done
    for liney in "${arr2[@]}"; do
        tmp2+=("$liney")
    done
    unset arr1
    unset arr2
    for liney in "${tmp2[@]}"; do
        arr1+=("$liney")
    done
    for liney in "${tmp1[@]}"; do
        arr2+=("$liney")
    done
}


get_unique_and_common_strings(){
  file1="$1"
  file2="$2"
  local -n unique_to_file1="$3"
  local -n unique_to_file2="$4"
  local -n in_file1_and_file2="$5"


file1_array=()
splitlines_file file1_array "$file1"
file2_array=()
splitlines_file file2_array "$file2"
for path1 in "${file1_array[@]}"; do
    found=false
    for path2 in "${file2_array[@]}"; do
        if [ "$path1" = "$path2" ]; then
            found=true
            in_file1_and_file2+=("$path1")
            break
        fi
    done
    if [ "$found" = false ]; then
        unique_to_file1+=("$path1")
    fi
done
for path1 in "${file2_array[@]}"; do
    found=false
    for path2 in "${file1_array[@]}"; do
        if [ "$path1" = "$path2" ]; then
            found=true
            break
        fi
    done
    if [ "$found" = false ]; then
        unique_to_file2+=("$path1")
    fi
done
}

file1="REPLACE_FILE_1"
file2="REPLACE_FILE_2"
unique_file1=()
unique_file2=()
commonfiles=()
get_unique_and_common_strings "$file1" "$file2" unique_file1 unique_file2 commonfiles

echo "----------------------------------------------.......Unique to $file1: :::::::::::::::::::::::::::::::::::::::::::::::"
for path in "${unique_file1[@]}"; do
    echo "$path"
done
echo "----------------------------------------------.......Unique to $file2: :::::::::::::::::::::::::::::::::::::::::::::::"
for path in "${unique_file2[@]}"; do
    echo "$path"
done
echo "----------------------------------------------.......in file 1 and 2  $file2: :::::::::::::::::::::::::::::::::::::::::::::::"
for path in "${commonfiles[@]}"; do
    echo "$path"
done

"""
ADB_SHELL_AWK_CALCULATOR = 'calc(){ awk "BEGIN{ print $* }" ;}\ncalc %s'
ADB_SHELL_GET_TREEVIEW = rf"""(ls %s -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/')"""
ADB_SHELL_GET_LINES_IN_FILE = r"""sed -n '%s,%sp' %s"""
ADB_SHELL_SPECIFIC_LINE_IN_FILE = r"""sed -n %sp %s"""
ADB_SHELL_REMOVE_SPECIFIC_LINE_IN_FILE = r"""sed -i %sd %s"""
ADB_SHELL_CHMOD_ALL_FILES_IN_FOLDER = r"find %s -type f -exec chmod %s {} \;"
ADB_SHELL_COUNT_NETWORK_CONNECTIONS = (
    R"""netstat -ant | awk '{print $NF}' | grep -v '[a-z]' | sort | uniq -c"""
)
ADB_SHELL_CREATE_DICT_AND_CD = """md () { mkdir -p "$@" && cd "$@"; }\nmd %s"""
ADB_SHELL_ALL_CONNECTED_IPS = """netstat -lantp | grep ESTABLISHED |awk '{print $5}' | awk -F: '{print $1}' | sort -u"""
ADB_SHELL_GET_BIOS_INFORMATION = (
    R"""dd if=/dev/mem bs=1k skip=768 count=256 2>/dev/null | strings -n 8"""
)

RGB_VALUES_OF_AREA = r"""
#!/bin/bash

generate_format2() {
    local readqty="$1"
    echo "$readqty/1 \"%03d,\""
}
split_string_into_chunks() {
    string=$1
    chunksize=$2
    local -n oarraxyz="$3"
    while IFS= read -n "$chunksize" -d '' char; do
        if is_string_empty "$char"; then
            continue
        fi
        oarraxyz+=("$char")
    done <<<"$string"
}
strip_string_both_sides() {
    local var="$1"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}

is_string_empty() {
    str=$1
    trimmed_str=$(strip_string_both_sides "$str")

    if [ -z "$trimmed_str" ]; then
        return 0
    else
        return
    fi
}
get_part_of_region() {
    start_x=$1
    start_y=$2
    end_x=$3
    end_y=$4
    chunkarray=()
    screen_width=$5
    rm -f "$dumpdata"
    screencap "$dumpdata"
    color_depth_bytes=4
    startabs=$((start_x * color_depth_bytes))
    endabs=$((end_x * color_depth_bytes))
    trashoffset=16
    endabs=$((endabs + trashoffset))
    startabs=$((startabs + trashoffset))
    screenwidthtimescolordepth=$((screen_width * color_depth_bytes))
    readqty=$((endabs - startabs))
    while [ "$start_y" -lt "$end_y" ]; do
        offset_start=$((start_y * screenwidthtimescolordepth))
        endabs=$((startabs + offset_start + readqty))
        format="$(generate_format2 "$readqty")"
        area_hexdump=$(hexdump -n "$readqty" -s "$offset_start" -e "$format" "$dumpdata")
        #area_hexdump="$(strip_string_both_sides "$area_hexdump")"
        split_string_into_chunks "$area_hexdump" 16 chunkarray
        counter=$((start_x + 0))
        for colorcomplete in "${chunkarray[@]}"; do
            v1="${colorcomplete:0:3}"
            v2="${colorcomplete:4:3}"
            v3="${colorcomplete:8:3}"
            v4="$counter"
            v5="$start_y"
            echo "$v4 $v5 $v1 $v2 $v3"
            counter=$((counter + 1))
        done
        unset chunkarray
        unset area_hexdump
        start_y=$((start_y + 1))
    done

}
dumpdata="/sdcard/dumpdata.tmp"
screen_width=REPLACE_SCREEN_WIDTH
start_x=REPLACE_AREA_STARTX
start_y=REPLACE_AREA_STARTY
end_x=REPLACE_AREA_ENDX
end_y=REPLACE_AREA_ENDY
get_part_of_region $start_x $start_y $end_x $end_y $screen_width
"""
ADB_SHELL_HEXDUMP = "hexdump -c %s"
ADB_SHELL_COUNT_LINES_IN_FILE = "wc -l %s"
ADB_SHELL_LS_FOLDER = "ls %s"
ADB_SHELL_KERNEL_INFOS = r"""lsmod | cut -d' ' -f1 | xargs modinfo | egrep '^file|^desc|^dep' | sed -e'/^dep/s/$/\n/g'"""
ADB_SHELL_GET_IP_FROM_HOST = (
    R"""ping -c 1 %s | egrep -m1 -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'"""
)
ADB_SHELL_NEWEST_FILE_IN_FOLDER = R"""newest () { DIR=${1:-'.'};  CANDIDATE=`find $DIR -type f|head -n1`; while [[ ! -z $CANDIDATE ]]; do BEST=$CANDIDATE; CANDIDATE=`find $DIR -newer "$BEST" -type f|head -n1`; done; echo "$BEST"; }; newest %s"""
ADB_SHELL_GET_IPS = "ip addr show"
ADB_SHELL_PRINT_FILE_WITH_LINENUMBERS = R"""grep -n "^" %s"""
ADB_SHELL_ABS_VALUE_OF_NUMBER = """abs_value=%s; echo ${abs_value#-}"""
ADB_SHELL_GET_DETAILS_FROM_PROCESS = """lsof -p$! %s"""
ADB_SHELL_NETSTAT_TLNP = "netstat -tlnp"
ADB_GET_DETAILS_FROM_ALL_PROCS = "lsof"
ADB_KILL_A_PROCESS_THAT_IS_LOCKING_A_FILE = """fuser -k %s"""
ADB_SHELL_PRINT_LINES_LONGER_THAN = """awk 'length>%s' %s"""
ADB_SHELL_FOLDER_IN_PATH_VAR = """echo "${PATH//:/$\'\\\\n\'}\""""
ADB_SHELL_COMPARE_2_FILES = "cmp %s %s"
ADB_SHELL_SUBSTRING_FROM_STRING = """var='%s'; echo ${var:%s:%s}"""
ADB_SHELL_RM_DRY_RUN = "echo rm %s"
ADB_SHELL_IPV4_INTERFACES = R"""ifconfig -a| awk '/^wlan|^eth|^lo/ {;a=$1;FS=":"; nextline=NR+1; next}{ if (NR==nextline) { split($2,b," ")}{ if ($2 ~ /[0-9]\./) {print a,b[1]}; FS=" "}}'"""
ADB_SHELL_LIST_PROCS_CPU_USAGE = """ps -ef --sort=-%cpu"""
ADB_SHELL_CURRENT_RUNNING_PROCESSES = """ps -eo pcpu,pid,args | sort -n"""
ADB_SHELL_INTERFACES_AND_MAC = R"""for f in /sys/class/net/*; do echo -e "$(basename $f)\t\t$(cat $f/address)"; done"""
ADB_SHELL_FILES_IN_FOLDER_NEWEST_FIRST = """ls -lt %s"""
ADB_SHELL_UPPER_TO_LOWER = """echo %s | tr '[:upper:]' '[:lower:]'"""
ADB_SHELL_NUMBER_OF_CPUS = """grep "processor" /proc/cpuinfo | wc -l"""
ADB_SHELL_GET_INTERNAL_IPS = R"""ifconfig $devices | grep "inet addr" | sed 's/.*inet addr:\([0-9\.]*\).*/\1/g'"""
ADB_SHELL_GET_EXTERNAL_IP = """wget -qO- ifconfig.me/ip"""
ADB_SHELL_GET_EXTERNAL_IP2 = "wget -O - -q icanhazip.com"

ADB_SHELL_GET_ALL_MAC_ADDRESSES = (
    R"""ifconfig -a| grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"""
)
ADB_SHELL_NUMBER_OF_TCP_CONNECTIONS = '''netstat -an|grep -ci "tcp.*established"'''
ADB_SHELL_APPEND_LINE_TO_FILE = """echo "%s" | tee -a %s"""
ADB_SHELL_DUMP_ALL_DB_FILES = R"""#!/bin/bash
find / -type f -iname "*.db" | while read -r dbfile; do
    filename=\$(basename \"\$dbfile\")
    
    # Get a list of all table names in the database
    table_names=\$(sqlite3 \"\$dbfile\" '.tables')

    for table_name in \$table_names; do
        echo \"Dumping data from \$dbfile as CSV for table \$table_name:\"
        outputfile=\"/sdcard/\${filename}_\${table_name}_text.csv\"
        sqlite3 \"\$dbfile\" <<EOF | awk -F \"|\" -v file=\"\$dbfile\" -v table=\"\$table_name\" 'BEGIN {OFS=\",\"} {print file, table, \$1, \$2, \$3, \$4, \$5, \$6, \$7}'
.headers on
.mode list
.output stdout
SELECT * FROM \"\$table_name\";
.quit
EOF
    done
    rm -f /sdcard/*_text.csv
done

"""
ADB_SHELL_DUMP_ALL_DATABASES_IN_DATA_DATA = R"""
#!/bin/bash
find /data/data -type f | while read -r dbfile; do
    filename=\$(basename \"\$dbfile\")
    
    # Get a list of all table names in the database
    table_names=\$(sqlite3 \"\$dbfile\" '.tables')

    for table_name in \$table_names; do
        echo \"Dumping data from \$dbfile as CSV for table \$table_name:\"
        outputfile=\"/sdcard/\${filename}_\${table_name}_text.csv\"
        sqlite3 \"\$dbfile\" <<EOF | awk -F \"|\" -v file=\"\$dbfile\" -v table=\"\$table_name\" 'BEGIN {OFS=\",\"} {print file, table, \$1, \$2, \$3, \$4, \$5, \$6, \$7}'
.headers on
.mode list
.output stdout
SELECT * FROM \"\$table_name\";
.quit
EOF
    done
    rm -f /sdcard/*_text.csv
done

"""
ADB_SHELL_CAT_FILE_JOIN_NEWLINES = '''cat %s | tr "\\\\n", " "'''
ADB_SHELL_CHECK_OPEN_PORTS = """netstat -plnt"""
ADB_SHELL_COUNT_FILES_IN_FOLDER = """find %s -maxdepth 1 -type f | wc -l"""
ADB_SHELL_LIST_INPUT_DEVICES = """getevent -pl"""
ADB_SHELL_GET_SENDEVENT_INPUT_DEVICES = R"""
#!/bin/bash
input_dir="/dev/input/"
for event_file in "$input_dir"event*; do
    if [ -e "$event_file" ]; then
        numeric_value=$(getevent -lp "$event_file" | awk -F'[[:space:]]max[[:space:]]|:' '/max/ { split($3, parts, ","); if (parts[1] != " value 0") print parts[1] }')
        if [[ -n "$numeric_value" ]]; then
            echo "$event_file $numeric_value"
        fi
    fi
done
"""
ADB_SHELL_SENDEVENT = R"""
#!/bin/bash
formatbinary() {
    int1=$1
    int2=$2
    int3=$3
    int4=$4
    int5=$5
    da=$(printf "\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x" $((int1 & 0xFF)) $((int1 >> 8 & 0xFF)) $((int1 >> 16 & 0xFF)) $((int1 >> 24 & 0xFF)) $((int2 & 0xFF)) $((int2 >> 8 & 0xFF)) $((int2 >> 16 & 0xFF)) $((int2 >> 24 & 0xFF)) $((int3 & 0xFF)) $((int3 >> 8 & 0xFF)) $((int4 & 0xFF)) $((int4 >> 8 & 0xFF)) $((int5 & 0xFF)) $((int5 >> 8 & 0xFF)) $((int5 >> 16 & 0xFF)) $((int5 >> 24 & 0xFF)))
    echo -n -e "$da" >>"$tmpfile"
}
x=REPLACE_XCOORD
y=REPLACE_YCOORD
inputdev="REPLACE_INPUTDEVICE"
inputdevmax=REPLACE_MAX
width=REPLACE_DISPLAYWIDTH
height=REPLACE_DISPLAYHEIGHT
tmpfile=/sdcard/sendeventtmp.bin
formatbinary 1 2 0 2 0
formatbinary 1 2 0 0 0
formatbinary 1 2 3 53 $((x * inputdevmax / width))
formatbinary 1 2 0 2 0
formatbinary 1 2 0 0 0
formatbinary 1 2 3 54 $((y * inputdevmax / height))
formatbinary 1 2 0 2 0
formatbinary 1 2 0 0 0
formatbinary 1 2 0 2 0
formatbinary 1 2 0 0 0
formatbinary 1 2 3 53 $((x * inputdevmax / width))
formatbinary 1 2 0 2 0
formatbinary 1 2 0 0 0
formatbinary 1 2 3 54 $((y * inputdevmax / height))
formatbinary 1 2 0 2 0
formatbinary 1 2 0 0 0
formatbinary 1 2 0 2 0
formatbinary 1 2 0 0 0
exec 3>"/dev/input/$inputdev"
cat "$tmpfile" >&3
exec 3>&-
sendevent /dev/input/$inputdev 0 0 0
sendevent /dev/input/$inputdev 0 2 0
sendevent /dev/input/$inputdev 0 0 0
rm -f "$tmpfile"
"""

ADB_SHELL_SENDEVENT_GETEVENT_SCRIPT = R"""
#!/bin/bash
tmpfilegetevent="REPLACE_TMPFILEGETEVENT"
tmpfilesendevent="REPLACE_TMPFILESENDEVENT"
devinput="REPLACE_DEVINPUT"
scriptname="REPLACE_SCRIPTNAME"
binfolder="REPLACE_BINFOLDER"
blocksize=REPLACE_BLOCKSIZE

capture_data_file="/sdcard/$tmpfilegetevent"
tmpfile="/sdcard/$tmpfilesendevent"
ev="/dev/input/$devinput"
scrif="/sdcard/$scriptname"
tmpfilesfolder="/sdcard/$binfolder"
mkdir -p "$tmpfilesfolder"

startcapture() {
    rm -f "$capture_data_file"
    getevent -t >"$capture_data_file"
}

removetmpfiles() {
    rm -f "$tmpfile"
    rm -f "$capture_data_file"
}

formatbinary() {
    int1=$1
    int2=$2
    int3=$3
    int4=$4
    int5=$5
    da=$(printf "\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x\\x%02x" $((int1 & 0xFF)) $((int1 >> 8 & 0xFF)) $((int1 >> 16 & 0xFF)) $((int1 >> 24 & 0xFF)) $((int2 & 0xFF)) $((int2 >> 8 & 0xFF)) $((int2 >> 16 & 0xFF)) $((int2 >> 24 & 0xFF)) $((int3 & 0xFF)) $((int3 >> 8 & 0xFF)) $((int4 & 0xFF)) $((int4 >> 8 & 0xFF)) $((int5 & 0xFF)) $((int5 >> 8 & 0xFF)) $((int5 >> 16 & 0xFF)) $((int5 >> 24 & 0xFF)))
    echo -n -e "$da" >>"$tmpfile"
}

executescript() {
    cat "$scrif"
    script_content=$(<"$scrif")
    eval "$script_content" #2>/dev/null
}

getevent2sendevent() {
    rm -f "$tmpfile"
    rm -f "$scrif"
    limitnumber=1.0
    foundstarttime=0
    no=0
    bi=0
    cat >$scrif <<EOF
#!/bin/bash
exec 3>"$ev"
EOF
    while IFS= read -r line; do
        IFS=" " read -r trash time event code1 code2 value <<<"$line"
        if [[ ${trash:0:1} != "[" ]]; then
            continue
        fi
        event="${event%?}"
        if [[ "$event" != "$ev" ]]; then
            continue
        fi
        if [[ "$foundstarttime" -eq 0 ]]; then
            first_timestamp="${time%%]*}"
            first_timestamp="${first_timestamp#"["}"
            first_timestamp="${first_timestamp%" "]}"
            #first_timestamp=$(printf "%.10f" $first_timestamp)
            starttime="$first_timestamp"
            foundstarttime=$((foundstarttime + 1))

        fi
        #time=$(printf "%.10f" $time)
        time="${time%?}"
        code1=$((16#$code1))
        code2=$((16#$code2))
        value=$((16#$value))
        #timediff=$((time - starttime))
        timediff="$(awk "BEGIN { print $time - $starttime }")"
        starttime="$time"
        #starttime=$((time + 0))
        formatbinary 1 2 $code1 $code2 $value
        newfi="$tmpfilesfolder/$no"
        rm -f $newfi
        #bi=$((bi + timediff))
        bi="$(awk "BEGIN { print $bi + $timediff }")"
        no=$((no + 1))
        echo "$event $code1 $code2 $value $bi"
        if [ $((no % blocksize)) -eq 0 ]; then
            echo "------------------------------------------"
            if (( $(awk -v num1="$bi" -v num2="$limitnumber" 'BEGIN {print (num1 > num2)}') )); then
                bi=0.1
            fi
            cat >>$scrif <<EOF
cat "$newfi" >&3
echo "$newfi"
sleep $bi
EOF
            bi=0
            #bi2=0
            mv "$tmpfile" "$newfi"

        fi
    done <"$capture_data_file"
    cat >>$scrif <<EOF
exec 3>&-
sendevent "$ev" 0 0 0
sendevent "$ev" 0 2 0
sendevent "$ev" 0 0 0
EOF
}

"""

ADB_SHELL_SENDEVENT_SCRIPT = """
executescript() {
    cat "$scrif"
    script_content=$(<"$scrif")
    eval "$script_content"
}
scrif="REPLACE_SCRIPTPATH"
executescript

"""

ADB_SHELL_GETEVENT_WITH_COORDS = R"""
#!/bin/bash
# Define a function to get the screen width and height.
get_width_height() {
    local -n stringarraywidthheight=$1
    stringarraywidthheight=()

    # Use 'wm size' to get the screen dimensions, extract only the resolution part (e.g., '1920x1080').
    screen_width=$(wm size | grep -oE '[0-9]+x[0-9]+$')
    stringarraywidthheight=()
    dlim="x"

    # Call 'splitstringdelim' to split the screen width into an array.
    splitstringdelim stringarraywidthheight "$screen_width" "$dlim"
    echo "${stringarraywidthheight[0]}"
    echo "${stringarraywidthheight[1]}"
}

# Define a function to split a string into an array using a delimiter.
splitstringdelim() {
    local -n stringarray="$1"
    inputstring=$2
    sep=$3
    allfilessplit=$(tr "$sep" '\r' <<<"$inputstring")
    array=($(echo $allfilessplit | sed 's/\r/\n/g'))

    # Add the split parts to the provided array.
    for l in "${array[@]}"; do
        stringarray+=("$l")
    done
}

# Define a function to pad a string to a specified width with spaces.
padval() {
    padded="$2"
    width=$1
    while [ ${#padded} -lt "$width" ]; do
        padded=" ${padded}"
    done
    echo "$padded"
}

# Define a function to capture touch screen events from a specific input device.
capture_screen() {
    widthheight=()
    get_width_height widthheight
    screen_w="${widthheight[0]}"
    screen_h="${widthheight[1]}"
    inputdev="/dev/input/$1"
    input_dir="/dev/input/"

    # Loop through event files in the input directory to find the specified input device.
    for event_file in "$input_dir"event*; do
        if [ "$event_file" == "$inputdev" ]; then
            # Extract the maximum numeric value from 'getevent -lp' output.
            numeric_value=$(getevent -lp "$event_file" | awk -F'[[:space:]]max[[:space:]]|:' '/max/ { split($3, parts, ","); if (parts[1] != " value 0") print parts[1] }')
            if [[ -n "$numeric_value" ]]; then
                inputdevmax="$numeric_value"
                break
            fi
        fi
    done

    # Capture input from the specified input device and process the data - bytes in right order.
    cat "$inputdev" | dd bs=16 count="$2" | xxd -c 16 | while read hexdata; do
        hexstring1="${hexdata:17:2}${hexdata:15:2}${hexdata:12:2}${hexdata:10:2}"
        hexstring2="${hexdata:27:2}${hexdata:25:2}${hexdata:22:2}${hexdata:20:2}"
        hexstring3="${hexdata:32:2}${hexdata:30:2}"
        hexstring4="${hexdata:37:2}${hexdata:35:2}"
        hexstring5="${hexdata:47:2}${hexdata:45:2}${hexdata:42:2}${hexdata:40:2}"

        # Pad hexadecimal numbers to 12 characters and convert to decimal.
        decnum5=$(padval 12 $((16#${hexstring5})))
        decnum4=$(padval 12 $((16#${hexstring4})))
        decnum3=$(padval 12 $((16#${hexstring3})))
        decnum2=$(padval 12 $((16#${hexstring2})))
        decnum1=$(padval 12 $((16#${hexstring1})))

        # Calculate and print the coordinates based on the input device's maximum value.
        if [ "$decnum2" -gt 0 ]; then
            coord1=$(padval 5 $((decnum2 * screen_w / inputdevmax)))
            coord1="x=$coord1"
        elif [ "$decnum5" -gt 0 ]; then
            coord1=$(padval 5 $((decnum5 * screen_h / inputdevmax)))
            coord1="y=$coord1"
        else
            coord1="        "
        fi

        echo "$decnum1 $decnum2 $decnum3 $decnum4 $decnum5   $coord1"
    done
}

# Call the capture_screen function to capture touch screen events from 'event4' device for 100,000 iterations.
capture_screen REPLACE_DEVICE REPLACE_ITER

"""
ADB_SHELL_RENAME_FILE_TO_MD5 = """
#!/bin/bash
filename="FINOPATH"
extension=${filename##*.}
md5s=$(md5sum -b "$filename")
dirn=$(dirname "$filename")
wholepath="$dirn/$md5s.$extension"
mv "$filename" "$wholepath"
echo "$wholepath"
"""
ADB_SHELL_GET_SIZE_OF_TERMINAL = "echo $COLUMNS x $LINES"
ADB_SHELL_REMOVE_NEWLINES_FROM_FILE_AND_CAT = R"""tr -d "\n" <"%s" | cat"""
ADB_SHELL_ONE_TIME_PING = """ping -q -c 1 %s"""
ADB_SHELL_CAT_FILE_WITHOUT_LEADING_WHITESPACES = (
    """cat %s | sed -e 's/^[ \\\\t]*//;s/[ \\\\t]*$//'"""
)
ADB_SHELL_VARIABLE_EXISTS = '''[ -z "$%s" ] && echo "0" || echo "1"'''
ADB_SHELL_GET_FILE_WITH_TIMESTAMP = """
get_file_with_tstamp(){
    echo "$1$(date '+_%Y_%m_%d_%H_%M_%S_%N')$2"
}
fi=$(get_file_with_tstamp "REPLACE_FILENAME" "REPLACE_EXT")
echo "$fi"
"""
ADB_SHELL_SYSTEM_MEMORY_DUMP = R"""hexdump -e '90/1 "%_p" "\n"' /dev/mem"""

ADB_SHELL_GET_CWD_OF_PROCS = """
#!/bin/bash
for proc_path in /proc/*/cwd; do
    pid=$(basename "$(dirname "$proc_path")")
    cwd=$(readlink "$proc_path")
    echo "$pid - $cwd"
done
"""
ADB_SHELL_LS_FULL_PATH = """REPLACE_PATH\nls | sed s#^#$(pwd)/#"""
ADB_SHELL_LS_SORT_BY_MOD_DATE = (
    """REPLACE_PATHfind -type f -print0 | xargs -r0 stat -c %y\\ %n | sort"""
)
ADB_SHELL_IPTABLES = "iptables -nL -v --line-numbers"
ADB_SHELL_REVERSE_FILE = """cat %s | sed '1!G;h;$!d'"""
ADB_SHELL_ECHO_BACKWARDS = "echo %s|rev"
ADB_SHELL_NETSTAT_IP_GROUP = """netstat -ntu | awk ' $5 ~ /^[0-9]/ {print $5}' | cut -d: -f1 | sort | uniq -c | sort -n"""
ADB_SHELL_PSTREE = "pstree -p"
ADB_SHELL_LIST_HDS = """awk '/d.[0-9]/{print $4}' /proc/partitions"""
ADB_SHELL_LIST_HDDS_REAL = "ls /sys/bus/scsi/devices"
ADB_SHELL_SORT_AND_UNIQUE = "sort %s | uniq"
ADB_SHELL_LSOF_FILEHANDLES = (
    """lsof | awk '{print $1}' | sort | uniq -c | sort -rn | head"""
)
ADB_SHELL_LIST_ALL_EXE_IN_PATH = """ls `echo $PATH | sed 's/:/ /g'`"""
ADB_SHELL_FREE_MEMORY = """grep '^MemFree:' /proc/meminfo | awk '{ mem=($2)/(1024) ; printf "%0.0f \\n", mem }'"""
ADB_LS_BY_FILESIZE = "REPLACE_PATH\nls -l | sort -nk5"
ADB_SHELL_GET_INSTALL_DATE = """ls -lct /etc/ | tail -1 | awk '{print $6, $7}'"""
ADB_SHELL_GET_AUDIO_PLAYING_PROCS = """lsof | grep pcm"""
ADB_SHELL_GET_KERNEL_INFOS = """awk '{print $1}' "/proc/modules" | xargs modinfo | awk '/^(filename|desc|depends)/'"""
ADB_SHELL_PROCS_WITH_OPEN_CONNECTIONS = """netstat -ntauple"""
ADB_SHELL_CHR = (
    """chr () { printf \\\\$(($1/64*100+$1%64/8*10+$1%8)); }\nchr REPLACE_CHAR"""
)
ADB_SHELL_LIST_ALL_EXTENSIONS_IN_FOLDER = """REPLACE_PATH\nfind . -type f | awk -F'.' '{print $NF}' | sort| uniq -c | sort -g"""
ADB_SHELL_COMMENT_OUT_LINE_IN_FILE = """sed -i '%s s/^/#/' %s"""
ADB_SHELL_MD5_HASHES_FROM_ALL_FILES = (
    """REPLACE_PATH\nfind . -type f -exec md5sum {} \;"""
)
ADB_SHELL_SIZE_OF_FOLDERS = "REPLACE_PATH\ndu -ks */"
ADB_SHELL_DELETE_ALL_FILES_IN_FOLDER_EXCEPT_NEWEST = (
    """REPLACE_PATH\nls -pt1 | sed '/.*\//d' | sed 1d | xargs rm"""
)
ADB_SHELL_APPS_USING_INTERNET = (
    """netstat -lantp | grep -i stab | awk -F/ '{print $2}' | sort | uniq"""
)
ADB_SHELL_GOTO_NEXT_SIBLING_FOLDER = (
    '''cd ../"$(ls -F ..|grep '/'|grep -B1 `basename $PWD`|head -n 1)"\necho "$PWD"'''
)
ADB_SHELL_GOTO_DIR_AND_SEARCH_FOR_STRING = (
    """%s\nfind . -type f -print | xargs grep -n %s"""
)
ADB_SHELL_SEARCH_FOR_COLORS = R"""
get_width_height() {
    local -n stringarraywidthheight=$1
    stringarraywidthheight=()
    screen_width=$(wm size | grep -oE '[0-9]+x[0-9]+$')
    stringarraywidthheight=()
    dlim="x"
    splitstringdelim stringarraywidthheight "$screen_width" "$dlim"
    echo "${stringarraywidthheight[0]}"
    echo "${stringarraywidthheight[1]}"
}
splitstringdelim() {
    local -n stringarray="$1"
    inputstring=$2
    sep=$3
    allfilessplit=$(tr "$sep" '\r' <<<"$inputstring")
    array=($(echo $allfilessplit | sed 's/\r/\n/g'))

    # Add the split parts to the provided array.
    for l in "${array[@]}"; do
        stringarray+=("$l")
    done
}
widthheight=()
get_width_height widthheight
screen_w="${widthheight[0]}"
screen_h="${widthheight[1]}"

screencap | xxd -g 4 -c 4 | awk 'COLOR_REPLACE' | cut -b 1-8,10-18 | while read line; do
    first_number="0x${line%% *}"
    decimal_number=$(printf "%d" "$first_number")
    decimal_number=$((decimal_number - 12))
    decimal_number=$((decimal_number / 4))
    cox=$((decimal_number / screen_w))
    coy=$((decimal_number % screen_w))
    li=${line#* }
    lip=${li:0:6}
    echo "$coy,$cox,$lip"
done

"""

