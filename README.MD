# A collection of useful adb commands

## pip install usefuladb

```python
# Tested against Android 9 / Bluestacks / Python 11 / Windows 10
# Please be aware that Android commands and
# their behavior can vary across different Android
# versions, custom ROMs, and devices. Consequently,
# some commands or methods may not function as
# expected on specific devices or Android versions.
# Moreover, certain advanced operations may
# necessitate root access, which is not universally
# available.
#
# It is advisable to thoroughly test and customize
# your commands and methods according to the
# unique specifications of your device and the
# Android version it runs. Keep in mind that
# Android is a dynamic platform, and commands and
# behaviors may change over time.
# Additionally, when executing commands,
# particularly those requiring elevated privileges,
# it's essential to consider the security
# and permission model of the Android device
from time import sleep

from usefuladb import AdbControl

# To connect to all devices at once, you can use this static method (Windows only):
AdbControl.connect_to_all_tcp_devices_windows(
    adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
)
# Blocking Shell
# - Waits until stderr/stdout have finished processing.
# - if you run "cd /sdcard/" and then another command "ls", for example, you will see the contents of /sdcard/.
# - If you switch to su, you will remain in the superuser mode.
# - Commands are not base64 encoded
blocking_shell = AdbControl(
    adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
    device_serial="127.0.0.1:5555",
    use_busybox=False,  # uses busybox to decode base64
    connect_to_device=True,
    invisible=True,  # windows only - doesn't open a shell window, when you compile the code with nuitka, for example
    print_stdout=True,
    print_stderr=True,
    limit_stdout=3,  # limits the history of shellcommands - can be checked at blocking_shell.stdout
    limit_stderr=3,  # limits the history of shellcommands - can be checked at blocking_shell.stderr
    limit_stdin=None,  # limits the history of shellcommands - can be checked at blocking_shell.stdin
    convert_to_83=True,  # converts the adb path to 8.3 on Windows
    wait_to_complete=0,  # doesn't matter if global_cmd is True
    flush_stdout_before=True,  # flushes the history in  blocking_shell.stdout
    flush_stdin_before=True,  # flushes the history in blocking_shell.stderr
    flush_stderr_before=True,  # flushes the history in  blocking_shell.stdin
    exitcommand="xxxCOMMANDxxxDONExxx",
    # Written using echo at the end of every command to determine when the output is finished.
    capture_stdout_stderr_first=True,  # doesn't matter if global_cmd is True
    global_cmd=True,  # global, because variables/su status/dirs stay
    global_cmd_timeout=10,  # if a command doesn't return stderr/stdout in a given time
)
# Blocking Subshell
# - Waits until stderr/stdout have finished processing.
# - Commands are base64 encoded.
# - All commands are executed within a subshell using a pipeline like base64command | base64 -d | sh.
# - For example, if you run "cd /sdcard/" and then another command like "ls," you will see the contents of the root directory '/' instead of '/sdcard'.
# - Note that 'su' is only valid for a single command.
blocking_subshell = AdbControl(
    adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
    device_serial="127.0.0.1:5555",
    use_busybox=False,  # Use busybox to decode base64 (if needed)
    connect_to_device=True,
    invisible=True,
    # Windows only - This option prevents the shell window from opening, e.g., when compiling the code with Nuitka.
    print_stdout=True,
    print_stderr=True,
    limit_stdout=3,  # Limit the history of shell commands (can be checked at blocking_shell.stdout)
    limit_stderr=3,  # Limit the history of shell commands (can be checked at blocking_shell.stderr)
    limit_stdin=None,  # Limit the history of shell commands (can be checked at blocking_shell.stdin)
    convert_to_83=True,  # Converts the adb path to 8.3 format on Windows
    wait_to_complete=0.1,  # Time to wait for command completion - only valid with capture_stdout_stderr_first=False
    flush_stdout_before=True,  # Flushes the history in blocking_shell.stdout before executing a command
    flush_stdin_before=True,  # Flushes the history in blocking_shell.stderr before executing a command
    flush_stderr_before=True,  # Flushes the history in blocking_shell.stdin before executing a command
    exitcommand="xxxCOMMANDxxxDONExxx",
    # Written using echo at the end of every command to determine when the output is finished
    capture_stdout_stderr_first=True,  # Blocks the process until the execution of a command is finished
    global_cmd=False,
    global_cmd_timeout=5,
)
# Non-blocking Subshell
# - Does not wait until stderr/stdout have finished processing.
# - Commands are base64 encoded.
# - All commands are executed within a subshell using a pipeline like base64command | base64 -d | sh.
# - For example, if you run "cd /sdcard/" and then another command like "ls," you will see the contents of the root directory '/' instead of '/sdcard'.
# - Note that 'su' is only valid for a single command.

nonblocking_subshell = AdbControl(
    adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
    device_serial="127.0.0.1:5555",
    use_busybox=False,  # Use busybox to decode base64 (if needed)
    connect_to_device=True,
    invisible=True,
    # Windows only - This option prevents the shell window from opening, e.g., when compiling the code with Nuitka.
    print_stdout=True,
    print_stderr=True,
    limit_stdout=3,  # Limit the history of shell commands (can be checked at blocking_shell.stdout)
    limit_stderr=3,  # Limit the history of shell commands (can be checked at blocking_shell.stderr)
    limit_stdin=None,  # Limit the history of shell commands (can be checked at blocking_shell.stdin)
    convert_to_83=True,  # Converts the adb path to 8.3 format on Windows
    wait_to_complete=0,  # Time to wait for command completion - only valid with capture_stdout_stderr_first=False
    flush_stdout_before=True,  # Flushes the history in blocking_shell.stdout before executing a command
    flush_stdin_before=True,  # Flushes the history in blocking_shell.stderr before executing a command
    flush_stderr_before=True,  # Flushes the history in blocking_shell.stdin before executing a command
    exitcommand="xxxCOMMANDxxxDONExxx",
    # Written using echo at the end of every command to determine when the output is finished
    capture_stdout_stderr_first=False,  # Blocks the process until the execution of a command is finished
    global_cmd=False,
    global_cmd_timeout=5,
)

executecmds = False
if executecmds:
    # The AdbControl module stays connected to an adb instance throughout its usage.
    # It continuously reads from stdout, stderr, and writes to stdin.
    # A typical way to execute adb commands is as follows:
    # adb.exe -s DEVICE shell ls /sdcard/
    # The problem with this approach is that it generates significant overhead for each command.

    # This module executes 'adb.exe -s DEVICE shell' right at the beginning when you create the instance
    # and keeps the shell open. This approach minimizes overhead, as the executable is run only once
    # and remains in a standby mode.

    # The core functionality of this module is provided by the AdbControl.execute_sh_command method.
    # Most commands are executed using this method.

    # You can use blocking_shell.execute_sh_command to run any command, and it returns a list of lists.
    # The first element is the stdout, and the second is stderr.
    stdout, stderr = blocking_shell.execute_sh_command("ls /sdcard/")
    # stderr
    # Out[5]: []
    # stdout
    # ....
    #  b'1753_mem_12c00000.bin\r\n',
    #  b'1753_mem_74d74000.bin\r\n',
    #  b'1753_mem_74ecd000.bin\r\n',
    #  b'1753_mem_77d75000.bin\r\n',
    #  b'1753_mem_ce771000.bin\r\n',
    # ...
    # If you encounter any problems with deadlocks, you can use the non-blocking version mentioned above:
    stdout, stderr = nonblocking_subshell.execute_sh_command("ls /sdcard/")

    # You don't have to create a new instance; you can temporarily switch to the non-blocking version:
    stdout, stderr = blocking_shell.execute_sh_command(
        "ls /sdcard/",
        capture_stdout_stderr_first=False,
        global_cmd=False,
        wait_to_complete=0,
    )

    # Or switch to the subshell blocking version temporarily:
    stdout, stderr = blocking_shell.execute_sh_command(
        "ls /sdcard/",
        capture_stdout_stderr_first=True,
        global_cmd=False,
        wait_to_complete=0.1,
    )

    # These are the available keyword arguments that can be used to temporarily adjust the configuration:
    # - disable_print_stdout
    # - disable_print_stderr
    # - wait_to_complete
    # - flush_stdout_before
    # - flush_stdin_before
    # - flush_stderr_before
    # - exitcommand
    # - su
    # - commandtimeout
    # - escape_filepath
    # - escape_filepath
    # - capture_stdout_stderr_first
    # - global_cmd

    # stderr
    # Out[5]: []
    # stdout
    # ....
    #  b'1753_mem_12c00000.bin\r\n',
    #  b'1753_mem_74d74000.bin\r\n',
    #  b'1753_mem_74ecd000.bin\r\n',
    #  b'1753_mem_77d75000.bin\r\n',
    #  b'1753_mem_ce771000.bin\r\n',
    # ...

    # All commands using the blocking and non-blocking subshell are converted to
    # base64 and sent to the device for decoding and execution.

    # For example, when you execute this command:
    blocking_subshell.execute_sh_command("ls /data/data")

    # It is executed as:
    # b'echo ZXhlYyAzPiYxIDQ+JjIgMT4vc2RjYXJkL3h4eHhzdGRvdXQxNjk4NzU0ODk5LjY4MjUzMzcudHh0IDI+L3NkY2FyZC94eHhzdGRlcnIxNjk4NzU0ODk5LjY4MjUzMzcudHh0CmxzIC9kYXRhL2RhdGEKZXhlYyAxPiYzIDI+JjQKY2F0IC9zZGNhcmQveHh4eHN0ZG91dDE2OTg3NTQ4OTk5LjY4MjUzMzcudHh0CmxzIC9kYXRhL2RhdGEKZXhlYyAxPiY1IDI+JjYKY2F0IC9zZGNhcmQveHh4c3RkZXJyMTY5ODc1NDg5OS42ODI1MzM3LnR4dCA+JjYKcm0gLWYgL3NkY2FyZC94eHh4c3Rkb3V0MTY5ODc1NDg5OS42ODI1MzM3LnR4dCA+IC9kZXYvbnVsbCAyPiYxCnJtIC1mIC9zZGNhcmQveHh4c3RkZXJyMTY5ODc1NDg5OS42ODI1MzM3LnR4dCA+IC9kZXYvbnVsbCAyPiYxCmVjaG8geHh4Q09NTUFORHh4eERPTkV4eHgK | base64 -d | sh\n'

    # You can decode it as:
    # base64.b64decode(b'ZXhlYyAzPiYxIDQ+JjIgMT4vc2RjYXJkL3h4eHhzdGRvdXQxNjk4NzU0ODk5LjY4MjUzMzcudHh0IDI+L3NkY2FyZC94eHhzdGRlcnIxNjk4NzU0ODk5LjY4MjUzMzcudHh0CmxzIC9kYXRhL2DmRhdGEKZXhlYyAxPiYzIDI+JjQKY2F0IC9zZGNhcmQveHh4eHN0ZG91dDE2OTg3NTQ4OTk5LjY4MjUzMzcudHh0CmxzIC9kYXRhL2DmRhdGEKZXhlYyAxPiY1IDI+JjYKY2F0IC9zZGNhcmQveHh4c3RkZXJyMTY5ODc1NDg5OS42ODI1MzM3LnR4dCA+JjYKcm0gLWYgL3NkY2FyZC94eHh4c3Rkb3V0MTY5ODc1NDg5OS42ODI1MzM3LnR4dCA+IC9kZXYvbnVsbCAyPiYxCnJtIC1mIC9zZGNhcmQveHh4c3RkZXJyMTY5ODc1NDg5OS42ODI1MzM3LnR4dCA+IC9kZXYvbnVsbCAyPiYxCmVjaG8geHh4Q09NTUFORHh4eERPTkV4eHgK')

    # As you can see, stdout and stderr are temporarily redirected and printed at the end to ensure that the entire output is captured.
    # This is essential to avoid closing adb.exe to minimize overhead.

    # If you encounter problems or deadlocks while executing commands this way, you can execute them as non-blocking commands.
    # To do this, set the kwargs `capture_stdout_stderr_first=False` and `wait_to_complete=0`.
    # and global_cmd to false
    stdout, stderr = nonblocking_subshell.execute_sh_command(
        "ls /data/data",
        capture_stdout_stderr_first=False,
        wait_to_complete=0,
        global_cmd=False,
    )

    # This is the command that was executed non-blocking:
    # base64.b64decode(b'bHMgL2RhdGEvZGF0YQplY2hvIHh4eENPTU1BTkR4eHhET05FeHh4Cg==')

    # You can convert any command to base64 using the `AdbControl.format_adb_command` method:
    blocking_shell.format_adb_command(
        cmd="ls /sdcard/", su=False, exitcommand="DONE", errors="strict"
    )

    # You can also convert any command to base64 and execute a command for screen capture using
    # `blocking_shell.format_adb_command_screen_capture`:
    blocking_shell.format_adb_command_screen_capture(
        cmd="ls /sdcard/", su=False, exitcommand="DONE", errors="strict"
    )
    # Out[4]: b'echo bHMgL3NkY2FyZC8KZWNobyBET05FCg== | base64 -d | sh\n'

    # blocking shell commands are executed like this:
    blocking_shell.execute_sh_command(r"ls")

    # b'#!/bin/bash\nexec 2>/sdcard/errortmp16989591673106961.txt\nexec 1>/sdcard/outputtmp16989591673106961.txt\nls\nexec 1>&-\nexec 2>&-\n\necho -n -e xxxCOMMANDxxxDONExxx>> /sdcard/outputtmp16989591673106961.txt\necho -n -e xxxCOMMANDxxxDONExxx >> /sdcard/errortmp16989591673106961.txt\n'
    # for each new instance, there are new tempfiles, to delete all of them, you can use:
    blocking_shell.remove_stderr_stdout_tmpfiles_on_sdcard()

    # Using the non blocking modus is useful if you want to execute commands at the same time:

    # Creating a new AdbControl instance
    instance2 = AdbControl(
        adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
        device_serial="127.0.0.1:5555",
        use_busybox=False,  # Use busybox to decode base64 if needed
        connect_to_device=True,
        invisible=True,
        # Windows only - Prevents the opening of a shell window when compiling the code with Nuitka, for example
        print_stdout=True,
        print_stderr=True,
        limit_stdout=3,  # Limits the history of shell commands - can be checked at blocking_shell.stdout
        limit_stderr=3,  # Limits the history of shell commands - can be checked at blocking_shell.stderr
        limit_stdin=None,  # Limits the history of shell commands - can be checked at blocking_shell.stdin
        convert_to_83=True,  # Converts the adb path to 8.3 format on Windows
        wait_to_complete=0,  # Time to wait for command completion - 0 means non blocking
        flush_stdout_before=True,  # Flushes the history in blocking_shell.stdout
        flush_stdin_before=True,  # Flushes the history in blocking_shell.stderr
        flush_stderr_before=True,  # Flushes the history in blocking_shell.stdin
        exitcommand="xxxCOMMANDxxxDONExxx",
        # Written using echo at the end of every command to determine when the output is finished
        capture_stdout_stderr_first=False,  # Doesn't block the process until the execution of a command is finished
        global_cmd=False,
        global_cmd_timeout=5,
    )

    # Execute two commands simultaneously in a non-blocking way
    # Keep in mind that the stdout/stderr list might grow even after returning
    stdout1, stderr1 = nonblocking_subshell.execute_sh_command(
        "ls -R /",
        capture_stdout_stderr_first=False,
        su=True,
        wait_to_complete=0,
        global_cmd=False,
    )
    print(len(stdout1))

    stdout2, stderr2 = instance2.execute_sh_command(
        "ls -R /sdcard/",
        capture_stdout_stderr_first=False,
        wait_to_complete=0,
        global_cmd=False,
    )
    print(len(stdout2))

    sleep(0.1)
    print(len(stdout1), len(stdout2))

    # This creates some crazy swipe effect:

    stdout1, stderr1 = nonblocking_subshell.execute_sh_command(
        "input swipe 100 300 200 800 2000",
        capture_stdout_stderr_first=False,
        su=True,
        wait_to_complete=0,
        global_cmd=False,
    )
    print(len(stdout1))

    stdout2, stderr2 = instance2.execute_sh_command(
        "input swipe 400 300 600 800 2000",
        capture_stdout_stderr_first=False,
        wait_to_complete=0,
        global_cmd=False,
    )
    print(len(stdout2))
    stdout1, stderr1 = nonblocking_subshell.execute_sh_command(
        "input swipe 100 300 200 800 2000",
        capture_stdout_stderr_first=False,
        su=True,
        wait_to_complete=0,
        global_cmd=False,
    )
    print(len(stdout1))

    stdout2, stderr2 = instance2.execute_sh_command(
        "input swipe 400 300 600 800 2000",
        capture_stdout_stderr_first=False,
        wait_to_complete=0,
        global_cmd=False,
    )
    print(len(stdout2))

    # Commands can include special characters, but spaces, quotes, etc., must be escaped:
    blocking_shell.execute_sh_command(r"cat /sdcard/bxx\ ab\ bcçc/xxx222\ d.txt")
    nonblocking_subshell.execute_sh_command(r"cat /sdcard/bxx\ ab\ bcçc/xxx222\ d.txt")
    blocking_subshell.execute_sh_command(r"cat /sdcard/bxx\ ab\ bcçc/xxx222\ d.txt")

    # You can escape characters like this. This method is used in several functions but not all,
    # as it might escape characters that shouldn't be escaped:
    from usefuladb import strip_quotes_and_escape

    blocking_shell.execute_sh_command(
        rf"cat {strip_quotes_and_escape('/sdcard/bxx ab bcçc/xxx222 d.txt')}"
    )

    # You can execute the command as bytes, but avoid using this unless necessary:
    blocking_shell.execute_sh_command(b"ls /sdcard/")
    blocking_shell.execute_sh_command(
        b"cat /sdcard/bxx\\ ab\\ bc\xc3\xa7c/xxx222\\ d.txt"
    )

    # Many adb commands are available as ready-to-use functions, so you don't have to worry about escaping and other details.
    # For example, to cat a file, you can use:
    blocking_shell.sh_cat_file(
        "/sdcard/bxx ab bcçc/xxx222 d.txt"
    )  # Escaping is done automatically, and quotes are stripped - either you escape or put it in quotes but not both :).

    # The significant advantage of using base64 encoding is the ability to execute bash scripts:
    nonblocking_subshell.execute_sh_command(
        """#!/bin/bash
    i=0
    while true; do
        i=$((i + 1))
        ls /sdcard/
        sleep 1.0
        if [ "$i" -gt 5 ]; then
            break
        fi
    done
    """
    )

    # You can also execute scripts as bytes:
    blocking_subshell.execute_sh_command(
        b"""#!/bin/bash
    i=0
    while true; do
        i=$((i + 1))
        ls /sdcard
        sleep 0.1
        if [ "$i" -gt 5 ]; then
            break
        fi
    done
    """
    )

    # Note that there is a potential risk when executing bash scripts with blocking_shell since the commands are not encoded to
    # base64. However, this risk should be manageable if you use caution and only execute trusted scripts.

    # A disadvantage of base64 is that the "cd" command, for example,
    # is only valid within one command since all commands are executed in a subshell:
    blocking_subshell.sh_change_to_dir("/sdcard/")
    # Out[12]: [[], []]
    blocking_subshell.execute_sh_command("ls")
    # This command prints the content of "/", not "/sdcard/"
    # To achieve the desired behavior, you have to use:
    blocking_subshell.execute_sh_command("cd /sdcard/ && ls")

    # To execute a command with superuser (su) privileges:
    blocking_subshell.execute_sh_command("ls /data/data")  # not working
    # Out[3]: [[], [b'ls: /data/data: Permission denied\r\n']]

    blocking_subshell.execute_sh_command("ls /data/data", su=True)  # working now
    # Out[4]:
    # [[b'android\r\n',
    #   b'android.ext.services\r\n',
    #   b'com.android.adbkeyboard\r\n',
    #   b'com.android.bookmarkprovider\r\n',
    #   b'com.android.camera2\r\n',

    # You can execute a shell script with superuser privileges in the same way:
    blocking_shell.execute_sh_command(
        b"""
    #!/bin/bash
    i=0
    while true; do
        i=$((i + 1))
        ls /data/data
        sleep 0.1
        if [ "$i" -gt 5 ]; then
            break
        fi
    done
    """,
        su=True,
    )

    # Piping is also possible:
    blocking_shell.execute_sh_command(
        r'dumpsys -t 1000000 | grep -E "com\.google\.android.{0,10}"'
    )

    # Here are some additional methods I've added to save time when working with ADB.
    # These methods can be used to perform various operations.

    # Create a new file using the sh_touch method:
    blocking_shell.sh_touch(
        "/sdcard/i dont exist yet/me neither/i have spëçiäl chars.txt"
    )
    # Out[6]: [[], []]
    nonblocking_subshell.sh_touch(
        "/sdcard/i dont exist yet/me neither/i have spëçiäl chars2.txt"
    )
    # Out[7]: [[], []]
    blocking_subshell.sh_touch(
        "/sdcard/i dont exist yet/me neither/i have spëçiäl chars3.txt"
    )
    # Out[8]: [[], []]

    # Append a line to an existing file using the sh_append_line_to_file method:
    blocking_shell.sh_append_line_to_file(
        "did it work?", "/sdcard/i dont exist yet/me neither/i have spëçiäl chars.txt"
    )
    # Out[7]: [[b'did it work?\r\n'], []]

    # Read the content of a file using the sh_cat_file method:
    file_content = blocking_shell.sh_cat_file(
        "/sdcard/i dont exist yet/me neither/i have spëçiäl chars.txt"
    )
    # Out[8]: b'did it work?\n'

    # To perform these operations with superuser (su) privileges, you can add the su=True parameter:
    blocking_shell.sh_touch(
        "/data/data/i dont exist yet/me neither/i have spëçiäl chars.txt", su=True
    )
    blocking_shell.sh_append_line_to_file(
        "did it work?",
        "/data/data/i dont exist yet/me neither/i have spëçiäl chars.txt",
        su=True,
    )

    catstuff = blocking_shell.sh_cat_file(
        "/data/data/i dont exist yet/me neither/i have spëçiäl chars.txt", su=True
    )
    # Out[10]: b'did it work?\n'
    # As you might have noticed, blocking_shell.sh_cat_file returns binary data, and \r\n is already replaced with \n.
    # Due to the post-processing involved, it's not recommended to use nonblocking_subshell in this case, as the data
    # might not be complete.
    catstuff = nonblocking_subshell.sh_cat_file(
        "/data/data/i dont exist yet/me neither/i have spëçiäl chars1.txt", su=True
    )

    # List the contents of a folder with superuser privileges:
    blocking_shell.sh_ls_folder("/data/data/i dont exist yet/me neither/", su=True)
    # Out[11]: [[b'i have sp\xc3\xab\xc3\xa7i\xc3\xa4l chars.txt\r\n'], []]

    # Additional methods to open various Android settings:
    blocking_shell.sh_open_date_settings()
    blocking_shell.sh_open_settings()
    blocking_shell.sh_open_application_development_settings()
    blocking_shell.sh_open_location_source_settings()
    blocking_shell.sh_open_memory_card_settings()
    blocking_shell.sh_open_locale_settings()
    blocking_shell.sh_open_search_settings()
    blocking_shell.sh_open_account_sync_settings()
    blocking_shell.sh_open_display_settings()
    blocking_shell.sh_open_input_method_settings()
    blocking_shell.sh_open_sound_settings()
    blocking_shell.sh_open_wifi_settings()
    blocking_shell.sh_open_application_settings()
    blocking_shell.sh_open_account_sync_settings_add_account()
    blocking_shell.sh_open_manage_applications_settings()
    blocking_shell.sh_open_sync_settings()
    blocking_shell.sh_open_dock_settings()
    blocking_shell.sh_open_add_account_settings()
    blocking_shell.sh_open_security_settings()
    blocking_shell.sh_open_device_info_settings()
    blocking_shell.sh_open_wireless_settings()
    blocking_shell.sh_open_system_update_settings()
    blocking_shell.sh_open_manage_all_applications_settings()
    blocking_shell.sh_open_data_roaming_settings()
    blocking_shell.sh_open_apn_settings()
    blocking_shell.sh_open_user_dictionary_settings()
    blocking_shell.sh_open_voice_input_output_settings()
    blocking_shell.sh_open_tts_settings()
    blocking_shell.sh_open_wifi_ip_settings()
    blocking_shell.sh_open_web_search_settings()
    blocking_shell.sh_open_bluetooth_settings()
    blocking_shell.sh_open_airplane_mode_settings()
    blocking_shell.sh_open_internal_storage_settings()
    blocking_shell.sh_open_accessibility_settings()
    blocking_shell.sh_open_quick_launch_settings()
    blocking_shell.sh_open_privacy_settings()

    # Display orientation using ScreenOrientation: https://developer.android.com/reference/androidx/browser/trusted/ScreenOrientation
    display_orientation = blocking_shell.sh_get_display_orientation()
    # Out[14]: 0

    # Additional keypress events methods have been added for convenience:

    blocking_shell.k_app_switch(longpress=True)
    blocking_shell.k_app_switch(longpress=True)
    blocking_shell.k_app_switch(longpress=False)
    blocking_shell.k_app_switch(longpress=False)
    blocking_shell.k_app_switch()
    blocking_shell.k_brightness_down()
    blocking_shell.k_brightness_up()
    blocking_shell.k_contacts()
    blocking_shell.k_copy()
    blocking_shell.k_cut()
    blocking_shell.k_home()
    blocking_shell.k_page_down()
    blocking_shell.k_page_up()
    blocking_shell.k_paste()
    blocking_shell.k_power()
    blocking_shell.k_search()
    blocking_shell.k_sleep()
    blocking_shell.k_tab()
    blocking_shell.k_volume_down()
    blocking_shell.k_volume_up()
    blocking_shell.k_volume_mute()
    blocking_shell.k_wakeup()

    # You can execute any other keypress like this:
    blocking_shell.keyevents.KEYCODE_P.longpress.keyboard()
    blocking_shell.keyevents.KEYCODE_PAGE_DOWN.press.keyboard()
    blocking_shell.keyevents.KEYCODE_P.longpress.touchpad()
    blocking_shell.keyevents.KEYCODE_P.longpress.gamepad()
    blocking_subshell.keyevents.KEYCODE_P.longpress.touchpad()
    nonblocking_subshell.keyevents.KEYCODE_P.longpress.touchpad()

    # Push files with spaces and special characters into [non-]existing folders.
    # This method sends the data using stdin and base64 encoding, rather than using adb.exe push.

    blocking_shell.push(
        r"C:\Users\hansc\Downloads\RobloxPlayerInstaller (6).exe",
        "/sdcard/not existing path/çççö",
    )
    # Note: The non-blocking subshell is not recommended for this operation.
    # You can use the blocking_subshell for file pushes.
    nonblocking_subshell.push(
        r"C:\Users\hansc\Downloads\RobloxPlayerInstaller (6).exe",
        "/sdcard/not existing path/çççö1",
    )
    blocking_subshell.push(
        r"C:\Users\hansc\Downloads\RobloxPlayerInstaller (6).exe",
        "/sdcard/not existing path/çççö2",
    )
    # Check if the file was successfully created in the specified folder:
    blocking_shell.sh_ls_folder("/sdcard/not existing path/çççö")
    # Out[23]: [[b'RobloxPlayerInstaller (6).exe\r\n'], []]

    # Check if the file exists using sh_file_exists method:
    file_exists = blocking_shell.sh_file_exists(
        r"/sdcard/not existing path/çççö/RobloxPlayerInstaller (6).exe"
    )
    # Out[24]: True

    # Note: Using the non-blocking version is not recommended for checking file existence.
    # It may result in a early response, leading to potential errors.
    # Instead, use the blocking_subshell for file existence checks.
    file_exists = blocking_subshell.sh_file_exists(
        r"/sdcard/not existing path/çççö/RobloxPlayerInstaller (6).exe"
    )
    # ....
    #     return bool(int(stdout[0].strip().decode("utf-8")))
    #                     ~~~~~~^^^
    # IndexError: list index out of range
    # 1

    # The file can also be pulled, but it is essentially the same as what cat is doing:
    # Don't use the non blocking variation here!
    filedata = blocking_shell.pull(
        r"/sdcard/not existing path/çççö/RobloxPlayerInstaller (6).exe"
    )
    with open("c:\\robloxinstall.exe", mode="wb") as f:
        f.write(filedata)

    # Remove the file using sh_remove_file method:
    blocking_shell.sh_remove_file(
        r"/sdcard/not existing path/çççö/RobloxPlayerInstaller (6).exe"
    )
    blocking_subshell.sh_remove_file(
        r"/sdcard/not existing path/çççö1/RobloxPlayerInstaller (6).exe"
    )
    # This is a great usecase for the non blocking version if don't care much about the stdout/stderr.
    nonblocking_subshell.sh_remove_file(
        r"/sdcard/not existing path/çççö2/RobloxPlayerInstaller (6).exe"
    )

    # Check if the file was successfully removed:
    blocking_shell.sh_file_exists(
        r"/sdcard/not existing path/çççö/RobloxPlayerInstaller (6).exe"
    )
    # Out[12]: False

    # Rescan a single file to show up in the gallery:
    blocking_shell.push(
        r"C:\asgasdfasdfasdf.png",
        "/sdcard/Download",
    )
    blocking_shell.sh_rescan_one_media("/sdcard/Download/asgasdfasdfasdf.png")

    # You can also push and pull entire folders:
    blocking_shell.pull_folder("/sdcard/Download", "c:\\babababaxx")

    # Push a folder from the local machine to the device:
    blocking_shell.push_folder(r"C:\qqqqqqqqqqqq", "/sdcard/")

    # You might encounter some errors, but you can ignore them, as 'tar' tries to execute 'chown,' which is not permitted.
    # Out[20]:
    # ([b'./\r\n',
    #   b'./asgasdfasdfasdf.png\r\n',
    #   b'./ba.html\r\n',
    #   b'./baba.png\r\n',
    #   b'./babaxx2.mhtml\r\n',
    #   b'./bibi.png\r\n',
    #   b'./bibixx.png\r\n',
    #   b'./datetmp.log\r\n',
    #   b'./tmp5j75s57u.tar\r\n'],
    #  [b"tar: chown 0:0 '.': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './asgasdfasdfasdf.png': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './ba.html': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './baba.png': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './babaxx2.mhtml': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './bibi.png': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './bibixx.png': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './datetmp.log': Operation not permitted\r\n",
    #   b"tar: chown 0:0 './tmp5j75s57u.tar': Operation not permitted\r\n",
    #   b'rm: tmpqp5_mrdt.tar: No such file or directory\r\n'])

    # List users on the device:
    users = blocking_shell.sh_list_users()
    # ['UserInfo{0:Owner:13} running']

    # NOTIFICATIONS:

    # Enable and disable heads-up notifications:
    blocking_shell.sh_enable_heads_up_notifications()
    blocking_shell.sh_disable_heads_up_notifications()

    # Open the camera to take a photo:
    blocking_shell.sh_still_image_camera()
    # Out[13]: [[b'Starting: Intent { act=android.media.action.STILL_IMAGE_CAMERA }\r\n'], []]

    # Make a call:
    blocking_shell.sh_make_call("+5511989782756")

    # Dumpsys:

    blocking_shell.sh_dumpsys_activity_settings()
    blocking_shell.sh_dumpsys_activity_allowed_associations()
    blocking_shell.sh_dumpsys_activity_intents()
    blocking_shell.sh_dumpsys_activity_broadcasts()
    blocking_shell.sh_dumpsys_activity_broadcast_stats()
    blocking_shell.sh_dumpsys_activity_providers()
    blocking_shell.sh_dumpsys_activity_permissions()
    blocking_shell.sh_dumpsys_activity_services()
    blocking_shell.sh_dumpsys_activity_recents()
    blocking_shell.sh_dumpsys_activity_lastanr()
    blocking_shell.sh_dumpsys_activity_starter()
    blocking_shell.sh_dumpsys_activity_activities()
    blocking_shell.sh_dumpsys_activity_exit_info()
    blocking_shell.sh_dumpsys_activity_processes()
    blocking_shell.sh_dumpsys_activity_lru()

    # Dump package information for a specific package (e.g., com.roblox.client):
    blocking_shell.sh_pm_dump("com.roblox.client")

    # Screen-related operations:

    # Get the screen width and height:
    w, h = blocking_shell.sh_get_wm_size()
    # this one is better:
    width, height = blocking_shell.sh_get_resolution()

    # Change the screen resolution to 960x540:
    blocking_shell.sh_change_wm_size(960, 540)

    # Reset the screen resolution to its default:
    blocking_shell.sh_wm_reset_size()

    # Get the current screen density:
    blocking_shell.sh_get_wm_density()

    # Change the screen density to 160:
    blocking_shell.sh_change_wm_density(160)

    # Reset the screen density to its default:
    blocking_shell.sh_wm_reset_density()

    # List device features and present working directory (pwd):
    blocking_shell.sh_list_features()
    blocking_shell.sh_pwd()

    # Create a directory with nested subdirectories on the device:
    blocking_shell.sh_mkdir("/sdcard/bobo/baba/bibix/not existing/me neither")
    # Out[7]: [[], []]

    # List the contents of a specific folder on the device:
    blocking_shell.sh_ls_folder("/sdcard/bobo/baba/bibix")
    # Out[6]: [[b'not existing\r\n'], []]

    # Create a directory and change into it (not necessary if the next command is not going to be launched in the folder):
    blocking_shell.sh_mkdir_and_cd("/sdcard/bibi")

    # Check if a folder exists on the device:
    folder_exists = blocking_shell.sh_is_folder("/sdcard/bobo/baba/bibix/")
    # Out[4]: True

    # Exit from the superuser (su) shell (only valid for blocking_shell):
    blocking_shell.exit_from_su_shell()

    # List available services on the device:
    blocking_shell.sh_list_services()
    # [[b'Found services:\r\n',
    #   b'0\tsip: [android.net.sip.ISipService]\r\n',
    #   b'1\tcarrier_config: [com.android.internal.telephony.ICarrierConfigLoader]\r\n',

    # Open a URL in a web browser:
    blocking_shell.sh_open_url("https://www.google.com")
    # Out[7]: [[b'Starting: Intent { act=android.intent.action.VIEW dat=https://www.google.com/... }\r\n'], []]

    # Get the NTP (Network Time Protocol) server information:
    blocking_shell.sh_get_ntp_server()
    # Out[8]: [[b'null\r\n'], []]

    # List installed packages on the device:
    blocking_shell.sh_pm_list_packages_f_i_u()
    blocking_shell.sh_pm_list_packages_3()
    blocking_shell.sh_pm_list_packages_s()

    # Show mounted devices on the device:
    blocking_shell.sh_mount()

    # The 'su' (superuser) mode is automatically set to true here because it is necessary to obtain this data.
    # This applies to some other methods as well.

    # Get IMEI, IMSI, and SIM information (valid until Android 9):
    imei, imsi, sim = blocking_shell.get_imei_imsi_sim()
    # For devices with more than one SIM card, get IMEIs:
    a, b = blocking_shell.get_imeis_multidevices()
    # Get IMEI information for Android 14 (but also works on Android 9):
    imei = blocking_shell.get_imei_android_14()

    # Verify that the file copy operations were successful:
    blocking_shell.sh_ls_folder("/sdcard/Download2")
    # Out[21]:
    # [[b'Nearby Share\r\n',
    #   b'asgasdfasdfasdf.png\r\n',
    #   b'ba.html\r\n',
    #   b'baba.png\r\n',
    #   b'babaxx2.mhtml\r\n',
    #   b'bibi.png\r\n',
    #   b'bibixx.png\r\n',
    #   b'datetmp.log\r\n',
    #   b'tmp5j75s57u.tar\r\n',
    #   b'tmpqp5_mrdt.tar\r\n'],
    #  []]

    # Change the display orientation to the specified value (in this case, new_orientation=1).
    blocking_shell.sh_change_display_orientation(new_orientation=1)

    # Perform random actions on the specified app:
    blocking_shell.sh_do_random_actions(
        p=("com.spotify.music",),  # Package name for the target app
        c=(),  # Use this to specify component
        v=10,  # Number of random actions to perform
        # Set other options as needed to control the behavior of random actions.
    )
    blocking_shell.sh_do_random_actions(
        p=("com.spotify.music",),
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
    )

    # Start the "com.android.chrome" package (launch the Chrome app).
    blocking_shell.sh_start_package("com.android.chrome")

    # Expand the notifications panel and settings panel.
    blocking_shell.sh_expand_notifications()
    blocking_shell.sh_expand_settings()

    # Resolve activity details for the "com.android.chrome" package.
    stdout, stderr = blocking_shell.sh_resolve_activity("com.android.chrome")
    # Out[16]:
    # [b'priority=0 preferredOrder=0 match=0x108000 specificIndex=-1 isDefault=true\r\n',
    #  b'ActivityInfo:\r\n',
    #  b'  name=com.google.android.apps.chrome.Main\r\n',
    #  b'  packageName=com.android.chrome\r\n',
    #  b'  splitName=chrome\r\n',
    #  b'  enabled=true exported=true directBootAw

    # The result is a list of information about the specified activity.

    # Resolve a brief summary of activity details for the "com.android.chrome" package.
    stdout, stderr = blocking_shell.sh_resolve_activity_brief("com.android.chrome")

    # List permission groups on the device.
    blocking_shell.sh_list_permission_groups()
    # Out[14]:
    # [[b'permission group:com.google.android.gms.permission.CAR_INFORMATION\r\n',
    #   b'permission group:android.permission-group.CONTACTS\r\n',
    #   b'permission group:android.permission-group.PHONE\r\n',

    # Dump the window manager state.
    blocking_shell.sh_dumpsys_window()

    # Check if the screen is locked.
    blocking_shell.sh_is_screen_locked()
    # Out[12]: False

    # Simulate a tap at coordinates (500, 500)
    blocking_shell.sh_input_tap(500, 500)

    # Simulate a tap using the DPAD controller at coordinates (500, 500)
    blocking_shell.sh_input_dpad_tap(500, 500)

    # Simulate a tap using the keyboard at coordinates (500, 500)
    blocking_shell.sh_input_keyboard_tap(500, 500)

    # Simulate a tap using the mouse at coordinates (500, 500)
    blocking_shell.sh_input_mouse_tap(500, 500)

    # Simulate a tap using the touchpad at coordinates (500, 500)
    blocking_shell.sh_input_touchpad_tap(500, 500)

    # Simulate a tap using a gamepad at coordinates (500, 500)
    blocking_shell.sh_input_gamepad_tap(500, 500)

    # Simulate a tap using touch navigation at coordinates (500, 500)
    blocking_shell.sh_input_touchnavigation_tap(500, 500)

    # Simulate a tap using a joystick at coordinates (500, 500)
    blocking_shell.sh_input_joystick_tap(500, 500)

    # Simulate a tap using the touchscreen at coordinates (500, 500)
    blocking_shell.sh_input_touchscreen_tap(500, 500)

    # Simulate a tap using a stylus at coordinates (500, 500)
    blocking_shell.sh_input_stylus_tap(500, 500)

    # Simulate a tap using a trackball at coordinates (500, 500)
    blocking_shell.sh_input_trackball_tap(500, 500)

    # Simulate typing "bibib" using the DPAD input method
    blocking_shell.sh_input_dpad_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using the keyboard input method
    blocking_shell.sh_input_keyboard_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "ççççç" using the keyboard input method and remove accents
    blocking_shell.sh_input_keyboard_text(
        "ççççç", sleeptime=(0.0, 0.0), remove_accents=True
    )

    # Simulate typing "bibib" using the mouse input method
    blocking_shell.sh_input_mouse_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using the touchpad input method
    blocking_shell.sh_input_touchpad_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using a gamepad input method
    blocking_shell.sh_input_gamepad_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using touch navigation input method
    blocking_shell.sh_input_touchnavigation_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using a joystick input method
    blocking_shell.sh_input_joystick_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using the touchscreen input method
    blocking_shell.sh_input_touchscreen_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using a stylus input method
    blocking_shell.sh_input_stylus_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    # Simulate typing "bibib" using a trackball input method
    blocking_shell.sh_input_trackball_text(
        "bibib", sleeptime=(0.0, 0.0), remove_accents=False
    )

    blocking_shell.sh_input_dpad_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_dpad_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_dpad_roll(x=10, y=300)
    blocking_shell.sh_input_keyboard_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_keyboard_drag_and_drop(
        x0=300, y0=100, x1=500, y1=500, t=1.0
    )
    blocking_shell.sh_input_keyboard_roll(x=10, y=300)
    blocking_shell.sh_input_mouse_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_mouse_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_mouse_roll(x=10, y=300)
    blocking_shell.sh_input_touchpad_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_touchpad_drag_and_drop(
        x0=300, y0=100, x1=500, y1=500, t=1.0
    )
    blocking_shell.sh_input_touchpad_roll(x=10, y=300)
    blocking_shell.sh_input_gamepad_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_gamepad_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_gamepad_roll(x=10, y=300)
    blocking_shell.sh_input_touchnavigation_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_touchnavigation_drag_and_drop(
        x0=300, y0=100, x1=500, y1=500, t=1.0
    )
    blocking_shell.sh_input_touchnavigation_roll(x=10, y=300)
    blocking_shell.sh_input_joystick_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_joystick_drag_and_drop(
        x0=300, y0=100, x1=500, y1=500, t=1.0
    )
    blocking_shell.sh_input_joystick_roll(x=10, y=300)
    blocking_shell.sh_input_touchscreen_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_touchscreen_drag_and_drop(
        x0=300, y0=100, x1=500, y1=500, t=1.0
    )
    blocking_shell.sh_input_touchscreen_roll(x=10, y=300)
    blocking_shell.sh_input_stylus_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_stylus_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_stylus_roll(x=10, y=300)
    blocking_shell.sh_input_trackball_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
    blocking_shell.sh_input_trackball_drag_and_drop(
        x0=300, y0=100, x1=500, y1=500, t=1.0
    )
    blocking_shell.sh_input_trackball_roll(x=10, y=300)

    # Simulate a long tap using the DPAD input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_dpad_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using the keyboard input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_keyboard_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using the mouse input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_mouse_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using the touchpad input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_touchpad_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using a gamepad input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_gamepad_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using touch navigation input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_touchnavigation_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using a joystick input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_joystick_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using the touchscreen input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_touchscreen_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using a stylus input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_stylus_longtap(x=304, y=360, t=1.0)

    # Simulate a long tap using a trackball input method at coordinates (304, 360) for 1.0 seconds
    blocking_shell.sh_input_trackball_longtap(x=304, y=360, t=1.0)

    # A little file manager
    # Get a dictionary of files and folders in the '/sdcard/Download' directory
    filedict = blocking_shell.get_file_dict("/sdcard/Download")

    # filedict
    # Out[4]:
    # {'f6': {'file_size': 12288,
    #   'is_file': False,
    #   'is_folder': True,
    #   'is_link': False,
    #   'is_character_device_file': False,
    #   'is_block_device_file': False,
    #   'is_named_pipe': False,
    #   'is_socket': False,
    #   'owner_read': True,
    #   'owner_write': True,
    #   'owner_exec': True,
    #   'group_read': True,
    #   'group_write': True,
    #   'group_exec': True,
    #   'others_read': False,
    #   'others_write': False,
    #   'others_exec': True,
    #   'file_permissions': 'drwxrwx--x',
    #   'user_owner': 'root',
    #   'group': 'sdcard_rw',
    #   'modification_time': 1698766942,
    #   'path': '/sdcard/Download',
    #   'folder': '/sdcard',
    #   'pure_path': 'Download',
    #   'cat_file': (),
    #   'remove': (),
    #   'rename': (),
    #   'grep': ()},
    #  'f190907': {'file_size': 6147735,
    #   'is_file': True,
    #   'is_folder': False,
    #   'is_link': False,
    #   'is_character_device_file': False,
    #   'is_block_device_file': False,
    #   'is_named_pipe': False,
    #   'is_socket': False,
    #   'owner_read': True,
    #   'owner_write': True,
    #   'owner_exec': False,
    #   'group_read': True,
    #   'group_write': True,
    #   'group_exec': False,
    #   'others_read': False,
    #   'others_write': False,
    #   'others_exec': False,
    #   'file_permissions': '-rw-rw----',
    #   'user_owner': 'root',
    #   'group': 'sdcard_rw',
    #   'modification_time': 1698268016,
    #   'path': '/sdcard/Download/babaxx2.mhtml',
    #   'folder': '/sdcard/Download',
    #   'pure_path': 'babaxx2.mhtml',
    #   'cat_file': (),
    #   'remove': (),
    #   'rename': (),
    #   'grep': ()},

    # Iterate through files and folders in the dictionary
    for filename, file_info in filedict.items():
        if file_info["is_file"]:
            # For each file, print its contents using the cat_file() method
            print(file_info.cat_file())

        # Alternatively, you can search for files matching a regex pattern (e.g., '.mhtml')
        if file_info["is_file"] and file_info.regex_search(r"\.mhtml"):
            print(file_info.cat_file())

        # You can also use the grep() method to search for specific text within files
        if file_info["is_file"] and file_info.regex_search(r"\.mhtml"):
            print(file_info.grep("Odds"))

        # You can also rename and remove files and folders as needed

    # Change the permissions of all files in the '/sdcard/Download' directory to 644 (needs su)
    blocking_shell.chmod_all_files_in_folder("/sdcard/Download", 644)

    # Copy the entire '/sdcard/Download' directory to another location, e.g., '/sdcard/Download8'
    # Ignore chown errors if they occur
    # Out[37]:
    # [[b'./\r\n',
    #   b'./babaxx2.mhtml\r\n',
    #   b'./bibi.png\r\n',
    #   b'./ba.html\r\n',
    #   b'./asgasdfasdfasdf.png\r\n',
    #   b'./baba.png\r\n',
    #   b'./bibixx.png\r\n',
    #   b'./datetmp.log\r\n',
    #   b'./tmp5j75s57u.tar\r\n'],
    #  [b"tar: chown 0:1015 '.': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './babaxx2.mhtml': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './bibi.png': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './ba.html': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './asgasdfasdfasdf.png': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './baba.png': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './bibixx.png': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './datetmp.log': Operation not permitted\r\n",
    #   b"tar: chown 0:1015 './tmp5j75s57u.tar': Operation not permitted\r\n"]]

    blocking_shell.sh_ls_folder("/sdcard/Download9")
    # Out[39]:
    # [[b'asgasdfasdfasdf.png\r\n',
    #   b'ba.html\r\n',
    #   b'baba.png\r\n',
    #   b'babaxx2.mhtml\r\n',
    #   b'bibi.png\r\n',
    #   b'bibixx.png\r\n',
    #   b'datetmp.log\r\n',
    #   b'tmp5j75s57u.tar\r\n'],
    #  []]

    # Normalize the text 'bibixxççx' and send it as a single input.
    blocking_shell.input_text(
        "bibixxççx", remove_accents=True, sleep_after_letter=(0, 0)
    )

    # Send each letter of 'bibixxççx' individually with a sleep interval between letters.
    blocking_shell.input_text(
        "bibixxççx", remove_accents=True, sleep_after_letter=(0, 1)
    )

    # Install the ADB Keyboard app, which allows you to send Unicode characters. "https://github.com/senzhk/ADBKeyBoard/raw/master/ADBKeyboard.apk" and installs it
    blocking_shell.install_adb_keyboard()

    # Send the text 'bababöäß' using the ADB Keyboard app.
    blocking_shell.input_text_adbkeyboard("bababöäß")

    # Disable the current keyboard.
    blocking_shell.disable_keyboard()

    # Enable the previously installed ADB Keyboard.
    blocking_shell.enable_keyboard()

    # Re-enable the ADB Keyboard for sending Unicode characters.
    blocking_shell.enable_adbkeyboard()

    # Get the active keyboard and verify that it's 'com.android.adbkeyboard/.AdbIME'.
    blocking_shell.get_active_keyboard()

    # Disable the ADB Keyboard, which will revert to the default keyboard.
    blocking_shell.disable_keyboard()

    # Enable touch animation on the device.
    blocking_shell.sh_show_touches()

    # Disable touch animation, which is better for automation purposes.
    blocking_shell.sh_show_touches_not()

    # Disable printing of standard output.
    blocking_shell.disable_stdout_print()

    # Enable printing of standard error.
    blocking_shell.enable_stderr_print()

    # Enable printing of standard output.
    blocking_shell.enable_stdout_print()

    # Get activity element dump in CSV format, which is useful for automation with multiple devices.
    # The more you disable 1->0, the faster it gets
    blocking_shell.get_activity_element_dump(
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
    )

    # Much faster and usually enough to identify elements
    blocking_shell.get_activity_element_dump(
        defaultvalue="null",
        stripline=1,
        with_class=1,
        with_mid=0,
        with_hashcode=0,
        with_elementid=0,
        with_visibility=0,
        with_focusable=0,
        with_enabled=0,
        with_drawn=0,
        with_scrollbars_horizontal=0,
        with_scrollbars_vertical=0,
        with_clickable=0,
        with_long_clickable=0,
        with_context_clickable=0,
        with_pflag_is_root_namespace=0,
        with_pflag_focused=0,
        with_pflag_selected=0,
        with_pflag_prepressed=0,
        with_pflag_hovered=0,
        with_pflag_activated=0,
        with_pflag_invalidated=0,
        with_pflag_dirty_mask=0,
    )
    # Output from get_activity_element_dump is a CSV format representing activity elements.

    # [b'IS_ACTIVE,ELEMENT_INDEX,START_X,START_Y,CENTER_X,CENTER_Y,AREA,END_X,END_Y,WIDTH,HEIGHT,START_X_RELATIVE,START_Y_RELATIVE,END_X_RELATIVE,END_Y_RELATIVE,PARENTSINDEX,ELEMENT_ID,MID,HASHCODE,VISIBILITY,FOCUSABLE,ENABLED,DRAWN,SCROLLBARS_HORIZONTAL,SCROLLBARS_VERTICAL,CLICKABLE,LONG_CLICKABLE,CONTEXT_CLICKABLE,CLASSNAME,PFLAG_IS_ROOT_NAMESPACE,PFLAG_FOCUSED,PFLAG_SELECTED,PFLAG_PREPRESSED,PFLAG_HOVERED,PFLAG_ACTIVATED,PFLAG_INVALIDATED,PFLAG_DIRTY_MASK,LINE_STRIPPED\r\n',
    #  b'"0","0","0","0","800","450","1440000","1600","900","1600","900","0","0","1600","900","|","null","9536b93","null","I","null","E","D","null","null","null","null","null","rB1","null","null","null","null","null","null","I","null","rB1{9536b93 I.ED..... ......I. 0,0-1600,900"\r\n',
    #  b'"800","1","0","0","800","450","1440000","1600","900","1600","900","0","0","1600","900","|","null","e911b96","null","V","null","E","null","null","null","null","null","null","android.widget.LinearLayout","null","null","null","null","null","null","null","null","android.widget.LinearLayout{e911b96 V.E...... ........ 0,0-1600,900"\r\n',
    #  b'"800","2","0","0","0","0","0","0","0","0","0","0","0","0","0","|1|","android:id/action_mode_bar_stub","9fdc7d0","102018a","G","null","E","null","null","null","null","null","null","android.view.ViewStub","null","null","null","null","null","null","I","null","android.view.ViewStub{9fdc7d0 G.E...... ......I. 0,0-0,0 #102018a android:id/action_mode_bar_stub"\r\n',
    #

    # Get a UI Automator element dump in CSV format. The device does the parsing using a shell script.
    # Output is a CSV that can be read using pandas.
    blocking_shell.get_uiautomator_element_dump(defaultvalue="null")
    # [b'INDEX,TEXT,RESOURCE_ID,CLASS,PACKAGE,CONTENT_DESC,CHECKABLE,CHECKED,CLICKABLE,ENABLED,FOCUSABLE,FOCUSED,SCROLLABLE,LONG_CLICKABLE,PASSWORD,SELECTED,BOUNDS,STARTX,ENDX,STARTY,ENDY,CENTER_X,CENTER_Y,AREA,WIDTH,HEIGHT\r\n',
    #  b'"null","null","null","android.widget.FrameLayout","com.android.chrome","null","false","false","false","true","false","false","false","false","false","false","0 0 1600 900","0","1600","0","900","800","450","1440000","1600","900"\r\n',
    #  b'"android:id/content","null","null","android.widget.LinearLayout","com.android.chrome","null","false","false","false","true","false","false","false","false","false","false","0 0 1600 900","0","1600","0","900","800","450","1440000","1600","900"\r\n',

    # Obtain a list of all available keys for the sendevent command.
    blocking_shell.get_all_sendevent_keys()
    # [[1, 'KEY_RESERVED'],
    #    [2, 'KEY_W'],
    #    [3, 'KEY_I'],
    #    [4, 'KEY_F6'],
    #    [5, 'KEY_KP9'],
    #    [6, 'KEY_102ND'],
    #    [7, 'KEY_VOLUMEUP'],
    #    [8, 'KEY_CALC'],
    #    [9, 'KEY_PROG3'],
    #    [10, 'BTN_DIGI'],
    #    [11, 'BTN_TOUCH'],
    #    [12, 'KEY_OK'],

    # You can also use sendevents to send keystrokes (needs su)
    blocking_shell.parse_sendevent_keys()  # need to be parsed first
    # After the parsing, they can be used like this:
    blocking_shell.keyevents_sendevent.event3.KEY_A(
        0.8, wait_to_complete=0, capture_stdout_stderr_first=False
    )
    blocking_shell.keyevents_sendevent.event3.KEY_B(
        1, wait_to_complete=0, capture_stdout_stderr_first=False
    )

    # Get a memory dump from a specific process (e.g., process with PID 1979). Note that this may take some time to complete.
    blocking_shell.get_memdump_from_process(1979)

    # Start a subprocess with elevated privileges (su) and attempt to kill all user-started processes.
    # This doesn't always work
    blocking_shell.save_a_stuck_shell()

    # Check if the keyboard is currently shown.
    blocking_shell.is_keyboard_shown()

    # Check if the ADB server is still alive.
    blocking_shell.isalive()

    # Access keyevents for different input methods (gamepad and keyboard).
    blocking_shell.keyevents.KEYCODE_E.press.gamepad()
    blocking_shell.keyevents.KEYCODE_E.press.keyboard()

    # Kill the ADB instance.
    blocking_shell.kill_proc()

    # List all listening ports along with their associated PIDs.
    blocking_shell.list_all_listening_ports_and_pid()

    # Open an ADB shell in cmd.exe.
    blocking_shell.open_adb_shell()

    # You can use the rgb_values_of_area function to obtain the RGB values in a specified area on the screen.
    # This function retrieves the RGB values within the defined area (between coordinates (x1, y1) and (x2, y2)). The result includes a list of XYRGB
    # This calculation is done directly on the device, no screenshots are transferred.
    coordsofcolours = blocking_shell.rgb_values_of_area(200, 200, 220, 320)
    #  XYRGB(x=215, y=249, r=254, g=254, b=254),
    #  XYRGB(x=216, y=249, r=254, g=254, b=254),
    #  XYRGB(x=217, y=249, r=254, g=254, b=254),
    #  XYRGB(x=218, y=249, r=254, g=254, b=254),
    #  XYRGB(x=219, y=249, r=254, g=254, b=254),

    # Some stuff for scripting:
    # Calculate the absolute value of a number.
    blocking_shell.sh_abs_value_of_number(-444)

    # Use an AWK calculator to perform mathematical calculations.
    blocking_shell.sh_awk_calculator("13.5*3")

    # Convert a string from uppercase to lowercase.
    blocking_shell.sh_upperstring_to_lowerstring("OOOXxx")

    # Extract a substring from a given string.
    blocking_shell.sh_substring_from_string("abcdef", 2, 4)

    # Terminate a specified Android package (com.android.chrome) using multiple methods,
    # as there is no one-fits-all command.
    blocking_shell.kill_package("com.android.chrome")

    # After calling `kill_package`, the following commands are executed one after another to forcefully stop the package:
    stdout, stderr = blocking_shell.sh_force_stop(
        package, **kwargs
    )  # Use the `am force-stop` command.
    stdout, stderr = blocking_shell.sh_kill(
        package, **kwargs
    )  # Use the `kill` command.
    stdout, stderr = blocking_shell.sh_killall9(
        package, **kwargs
    )  # Use the `killall -9` command.
    stdout, stderr = blocking_shell.sh_am_kill(
        package, **kwargs
    )  # Use the `am kill` command.
    stdout, stderr = blocking_shell.sh_pkill(
        package, **kwargs
    )  # Use the `pkill` command.

    # Concatenate the contents of a file (/sdcard/window_dump.xml) without newlines.
    blocking_shell.sh_cat_file_join_newlines("/sdcard/window_dump.xml")

    # Check for open ports on the device.
    blocking_shell.sh_check_open_ports()

    # Clear data and cache for a specified Android package (com.android.chrome).
    blocking_shell.sh_clear_package("com.android.chrome")
    # Output: [[b'Success\r\n'], []]

    # Compare two files (/sdcard/window_dump.xml and /sdcard/window_dump2.xml).
    blocking_shell.sh_compare_2_files(
        "/sdcard/window_dump.xml", "/sdcard/window_dump2.xml"
    )

    # Start a new instance of logcat and capture the output in `stdout` while suppressing `stderr`.
    newinstance, stdout, stderr = blocking_shell.start_logcat(
        print_stdout=True, print_stderr=False
    )

    # Create a fast backup of a SQLite database in the same folder - /sdcard/your_sqlite.db.bak
    blocking_shell.sh_create_bak_of_file("/sdcard/your_sqlite.db")

    # Delete the content of a file, but not the file itself:
    # Create a file first using uiautomator
    blocking_shell.execute_sh_command("uiautomator dump")
    # Output: [[b'UI hierarchy dumped to: /sdcard/window_dump.xml\r\n'], []]
    blocking_shell.sh_empty_file("/sdcard/window_dump.xml")
    # Output: [[], []]
    blocking_shell.sh_cat_file("/sdcard/window_dump.xml")
    # Output: b''

    # Capture a raw screen image
    raw_screen_data = blocking_shell.sh_screencap()

    # To convert the data to a numpy array and save as a PNG:
    # cv2.imwrite('c:\\TESTADBRAWSCREENSHOT.PNG', np.frombuffer(raw_screen_data, dtype=np.uint8)[16:].reshape((900, 1600, 4))[...,[2,1,0]])

    # Capture a PNG screen image
    png_screen_data = blocking_shell.sh_screencap_png()

    # To convert the data to a numpy array:
    # cv2.imdecode(np.frombuffer(png_screen_data, np.uint8), cv2.IMREAD_COLOR)

    # Capture the UI hierarchy using uiautomator dump
    blocking_shell.execute_sh_command("uiautomator dump")

    # Use 'grep' to search for lines matching the specified pattern in a file
    blocking_shell.sh_grep(
        r"bounds=......",
        "/sdcard/window_dump.xml",
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

    blocking_shell.sh_netstat()

    # Remove Dalvik cache, data cache, and user cache using 'su' command
    blocking_shell.sh_remove_dalvik_cache()
    blocking_shell.sh_remove_data_cache()
    blocking_shell.sh_remove_user_cache()

    # Remount the system as read-write or read-only
    # Note: Not working for the next command yet, since all commands are executed in a subshell.
    blocking_shell.sh_remount_all_rw()
    blocking_shell.sh_remount_all_ro()
    # If you know how to fix that, let me know. Use this for now: .
    blocking_shell.execute_sh_command(
        "su -c 'mount --all -o remount,rw -t vfat; echo \"bibi\" > /data/baba.txt'"
    )

    # Enable or disable screen compatibility mode for the specified app (com.spotify.music)
    blocking_shell.sh_screen_compat_on("com.spotify.music")
    blocking_shell.sh_screen_compat_off()

    # Rename a file from '/sdcard/window_dump.xml' to '/sdcard/window_dumpxx.xml'
    blocking_shell.sh_rename("/sdcard/window_dump.xml", "/sdcard/window_dumpxx.xml")

    # Check if the path '/sdcard/window_dumpxx.xml' is a file
    blocking_shell.sh_is_file("/sdcard/window_dumpxx.xml")
    # Output: True

    # Get the RGB value at a specific coordinate (200, 300) on the device
    rgb_value = blocking_shell.sh_get_rgb_value_at(200, 300)
    # Output: (35, 37, 39)

    # List all installed keyboards on the device
    keyboard_list = blocking_shell.get_all_keyboards()
    # Output: ['com.android.inputmethod.latin/.LatinIME', 'com.android.adbkeyboard/.AdbIME']

    # Get the tree view of the '/sdcard/' directory
    tree_view_sdcard = blocking_shell.sh_get_treeview_of_folder("/sdcard/")
    # Out[10]:
    # ['|-',
    #  '|-20231024',
    #  '|-AUTOMAT',
    #  '|---tmpaam24gbf',
    #  '|-Android',
    #  '|---data',
    #  '|-----com.android.camera2',
    #  '|-------cache',
    #  '|-------files',
    #  '|-----com.android.chrome',

    # Get the tree view of the '/data/data' directory with superuser privileges (for protected directories)
    tree_view_data_data = blocking_shell.sh_get_treeview_of_folder(
        "/data/data", su=True
    )

    # Get lines 0 to 3 from the '/etc/hosts' file with superuser privileges
    lines_0_to_3 = blocking_shell.sh_get_lines_from_to_in_file(
        0, 3, "/etc/hosts", su=True
    )
    # Out[13]:
    # [[b'127.0.0.1       localhost\r\n',
    #   b'::1             ip6-localhost\r\n',
    #   b'127.0.0.1       coinhive.com\r\n'],
    #  []]

    # Get a specific line (line 3) from the '/etc/hosts' file with superuser privileges
    specific_line = blocking_shell.sh_get_specific_line_from_a_file(
        3, "/etc/hosts", su=True
    )
    #     # [[b'127.0.0.1       coinhive.com\r\n'], []]

    # Remove a specific line (line 0) from the '/sdcard/window_dump.xml' file
    blocking_shell.sh_remove_specific_line_from_a_file(0, "/sdcard/window_dump.xml")

    # Check the contents of the '/sdcard/window_dump.xml' file after removing a specific line
    file_contents = blocking_shell.sh_cat_file("/sdcard/window_dump.xml")
    # Out[22]: b''

    # Count the network connections and display the status of each connection
    network_connections = blocking_shell.sh_count_network_connections()
    # Out[23]:
    # [[b'      6 CLOSE_WAIT\r\n',
    #   b'      7 ESTABLISHED\r\n',
    #   b'      2 LISTEN\r\n',
    #   b'      1 TIME_WAIT\r\n'],
    #  []]

    # Get the chmod permissions of files in the '/sdcard/' directory
    chmod_permissions_sdcard = blocking_shell.sh_get_all_chmod_from_files_in_folder(
        "/sdcard/"
    )
    # Out[24]:
    # [[b'-rw-rw---- 660 /sdcard/ \r\n',
    #   b'-rw-rw---- 660 /sdcard/(rev)\r\n',
    #   b'-rw-rw---- 660 /sdcard/(tr\r\n',
    #   b'-rw-rw---- 660 /sdcard/-1_threads.notifications.db_text.txt\r\n',
    #   b'-rw-rw---- 660 /sdcard/1753_mem_12c00000.bin\r\n',
    #   b'-rw-rw---- 660 /sdcard/1753_mem_74d74000.bin\r\n',
    #   b'-rw-rw---- 660 /sdcard/1753_mem_74ecd000.bin\r\n',
    #   b'-rw-rw---- 660 /sdcard/1753_mem_77d75000.bin\r\n',
    #   b'-rw-rw---- 660 /sdcard/1753_mem_ce771000.bin\r\n',

    # List all connected IP addresses
    connected_ips = blocking_shell.sh_list_all_connected_ips()
    # Out[25]:
    # [[b'\r\n',
    #   b'128.116.127.8\r\n',
    #   b'128.116.45.3\r\n',
    #   b'23.61.138.153\r\n',
    #   b'5.226.179.25\r\n'],
    #  []]
    # Get BIOS information (root only)
    bios_info = blocking_shell.sh_get_bios_info()
    # [[b'RSD PTR \r\n',
    #   b'innotek GmbH\r\n',
    #   b'VirtualBox\r\n',
    #   b'12/01/2006\r\n',
    #   b'innotek GmbH\r\n',
    #   b'VirtualBox\r\n',
    #   b'Virtual Machine\r\n',
    #   b'Oracle Corporation\r\n',

    # Display a hex dump of the specified file
    hex_dump = blocking_shell.sh_hexdump("/sdcard/window_dumpxx.xml")
    # Out[29]:
    # [[b"0000000   <   ?   x   m   l       v   e   r   s   i   o   n   =   '   1\r\n",
    #   b"0000010   .   0   '       e   n   c   o   d   i   n   g   =   '   U   T\r\n",
    #   b"0000020   F   -   8   '       s   t   a   n   d   a   l   o   n   e   =\r\n",
    #   b"0000030   '   y   e   s   '       ?   >   <   h   i   e   r   a   r   c\r\n",

    # Count the number of lines in the '/etc/hosts' file (root only)
    line_count = blocking_shell.sh_count_lines_in_file("/etc/hosts", su=True)
    # Out[31]: [3, b'/etc/hosts']

    # Get kernel information (root only)
    kernel_info = blocking_shell.sh_get_kernel_infos()

    # Get the IP address from the hostname 'google.com'
    ip_address = blocking_shell.sh_get_ip_from_host("google.com")
    # Out[34]: '142.251.128.14'

    # Get the newest file in the '/sdcard/' folder
    newest_file = blocking_shell.sh_newest_file_in_folder("/sdcard/")
    # Out[35]: [[b'/sdcard/dumpdata.tmp\r\n'], []]

    # Print the '/etc/hosts' file with line numbers (root only)
    hosts_file_lines = blocking_shell.sh_print_file_with_linenumbers(
        "/etc/hosts", su=True
    )
    # Out[3]:
    # [[b'1:127.0.0.1       localhost\r\n',
    #   b'2:::1             ip6-localhost\r\n',
    #   b'3:127.0.0.1       coinhive.com\r\n'],
    #  []]

    # Display a detailed process overview
    process_overview = blocking_shell.sh_ps_a_t_l_z()

    # Get details of a process with PID 1737
    details_of_pid_1737 = blocking_shell.sh_get_details_from_pid(1737)
    # [[b'COMMAND     PID       USER   FD      TYPE             DEVICE  SIZE/OFF       NODE NAME\r\n',
    #   b'logd       1737       logd  cwd       DIR                0,2      1000          2 /\r\n',
    #   b'logd       1737       logd  rtd       DIR                0,2      1000          2 /\r\n',
    #   b'logd       1737       logd  txt       REG                8,1    186648     265642 /system/bin/logd\r\n',
    #   b'logd       1737       logd  mem       REG                8,1    186648     265642 /system/bin/logd\r\n',
    #   b'logd       1737       logd  mem       REG                8,1     15056     264521 /system/lib64/libnetd_client.so\r\n',
    #   b'logd       1737       logd  mem       REG                8,1     23448     263965 /system/lib64/libcap.so\r\n',
    #   b'logd       1737       logd  mem       REG                8,1     73472     264133 /system/lib64/libbase.so\r\n',
    #   b'logd       1737       logd  mem       REG                8,1     43928     264178 /system/lib64/libsysutils.so\r\n',

    # Show network connections in a detailed format
    netstat_details = blocking_shell.sh_netstat_tlnp()
    # [[b'tcp',
    #   b'29289',
    #   b'0',
    #   b'10.0.2.15:42398',
    #   b'5.226.179.25:443',
    #   b'CLOSE_WAIT',
    #   b'-'],

    # Dump detailed process information with 'lsof' command (root only)
    detailed_process_info = blocking_shell.sh_get_details_with_lsof(su=True)
    blocking_shell.sh_get_details_with_lsof(su=True)
    # [[b'COMMAND     PID       USER   FD      TYPE             DEVICE  SIZE/OFF       NODE NAME\r\n',
    #   b'init          1       root  cwd       DIR                0,2      1000          2 /\r\n',
    #   b'init          1       root  rtd       DIR                0,2      1000          2 /\r\n',
    #   b'init          1       root  txt       REG                0,2   2409528       7182 /init\r\n',
    #   b'init          1       root  mem       REG                0,2   2409528       7182 /init\r\n',
    #   b'init          1       root  mem       REG               0,16    131072       8407 /dev/__properties__/properties_serial\r\n',

    # Display detailed network output, including IP addresses
    network_ip_info = blocking_shell.sh_show_ips()

    # Terminate a process that is locking a file at a specified path (root only)
    blocking_shell.sh_kill_process_that_is_locking_a_file("...some path", su=True)

    # Print lines of the '/etc/hosts' file that have at least 26 characters
    long_lines_in_hosts_file = (
        blocking_shell.sh_print_lines_of_file_with_at_least_length_n(
            "/etc/hosts", 26, su=True
        )
    )
    # Out[16]:
    # [[b'::1             ip6-localhost\r\n', b'127.0.0.1       coinhive.com\r\n'],
    #  []]

    # Show folders in the PATH environment variable (non-root)
    folders_in_path = blocking_shell.sh_show_folders_in_PATH(su=False)
    # Out[18]:
    # [[b'/sbin\r\n',
    #   b'/system/sbin\r\n',
    #   b'/system/bin\r\n',
    #   b'/system/xbin\r\n',
    #   b'/odm/bin\r\n',
    #   b'/vendor/bin\r\n',
    #   b'/vendor/xbin\r\n'],
    #  []]

    # Dry run of removing files matching the pattern '/sdcard/Download/*' (root only)
    # This command shows the files that would be removed without actually deleting them.
    dry_run_remove_files = blocking_shell.sh_rm_dry_run("/sdcard/Download/*")
    # Out[21]:
    # [[b'rm /sdcard/Download/Nearby Share /sdcard/Download/ba.html /sdcard/Download/baba.png /sdcard/Download/babaxx2.mhtml /sdcard/Download/bibi.png /sdcard/Download/bibixx.png /sdcard/Download/datetmp.log /sdcard/Download/tmp5j75s57u.tar\r\n'],
    #  []]

    # List IPv4 network interfaces and their associated IP addresses
    ipv4_interfaces = blocking_shell.sh_ipv4_interfaces()
    # Out[22]: [[b'lo 127.0.0.1\r\n', b'eth0 10.0.2.15\r\n'], []]

    # List processes and their CPU usage
    processes_cpu_usage = blocking_shell.sh_list_procs_cpu_usage()
    # Out[23]:
    # [[b'UID            PID  PPID C STIME TTY          TIME CMD\r\n',
    #   b'u0_a60       10218  1790 10 12:53:42 ?    00:19:24 com.roblox.client\r\n',
    #   b'u0_i2         8596  2178 3 11:30:32 ?     00:07:34 com.android.chrome:sandboxed_process0\r\n',
    #   b'u0_a31        8628  1791 2 11:30:33 ?     00:04:49 com.android.chrome:privileged_process0\r\n',
    #   b'system        1811     1 1 10:10:57 ?     00:01:59 surfaceflinger\r\n',
    #   b'system        1958  1790 0 10:10:58 ?     00:00:57 system_server\r\n',
    #   b'audioserver   1805     1 0 10:10:57 ?     00:00:31 audioserver\r\n',

    # List currently running processes
    running_processes = blocking_shell.sh_list_current_running_procs()
    # Out[24]:
    # [[b' 0.0     1 init\r\n',
    #   b' 0.0     2 [kthreadd]\r\n',
    #   b' 0.0     3 [rcu_gp]\r\n',
    #   b' 0.0     4 [rcu_par_gp]\r\n',
    #   b' 0.0     6 [kworker/0:0H-kblockd]\r\n',

    blocking_shell.sh_get_interfaces_and_mac()
    # Out[25]:
    # [['dummy0', 'ae:9c:a5:bd:92:cf'],
    #  ['eth0', '08:00:27:0e:38:b3'],
    #  ['ip6tnl0', '00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00'],

    # List files in the '/sdcard/Download' directory, sorted by newest first
    # The output includes details like permissions, owner, size, date, and file name.
    newest_files = blocking_shell.sh_list_files_newest_first("/sdcard/Download")
    # Out[26]:
    # [['-rw-rw----',
    #   '1',
    #   'root',
    #   'sdcard_rw',
    #   '10240',
    #   '2023-10-29',
    #   '20:48 tmp5j75s57u.tar'],
    #  ['-rw-rw----',
    #   '1',
    #   'root',
    #   'sdcard_rw',
    #   '294188',
    #   '2023-10-25',
    #   '18:06 baba.png'],

    # Get the number of CPUs on the device
    number_of_cpus = blocking_shell.sh_number_of_cpus()
    # Out[28]: 4

    # Get the internal IP addresses of the device (loopback and local network)
    internal_ip_addresses = blocking_shell.sh_get_internal_ip_addr()
    # Out[29]: ['127.0.0.1', '10.0.2.15']

    # Get the external IP address of the device (requires an internet connection)
    external_ip_address = blocking_shell.sh_get_external_ip()
    # Out[30]: '189.XXXXXXX'

    # Get the MAC addresses of all network interfaces on the device
    mac_addresses = blocking_shell.sh_get_all_mac_addresses()
    # Out[31]: ['ae:9c:a5:bd:92:cf', '08:00:27:0e:38:b3']

    # Get the number of active TCP connections on the device
    number_of_tcp_connections = blocking_shell.sh_number_of_tcp_connections()

    # Dump all files with a '.db' extension on the entire system
    db_files_list = blocking_shell.sh_dump_all_db_files(as_pandas=False)

    # Dump all databases in the 'data/data' directory (not limited to '.db' files)
    databases_in_data_data = blocking_shell.sh_dump_all_databases_in_data_data(
        as_pandas=False
    )

    # Count the number of files in the '/sdcard' directory
    number_of_files_in_sdcard = blocking_shell.sh_count_files_in_folder("/sdcard")
    # Out[33]: 826

    # List input devices, including details like device names and supported events
    input_devices = blocking_shell.sh_list_input_devices()
    # Out[34]:
    # [[b'add device 1: /dev/input/event6\r\n',
    #   b'  name:     "Android Power Button"\r\n',
    #   b'  events:\r\n',
    #   b'    KEY (0001): KEY_POWER             KEY_WAKEUP           \r\n',
    #   b'  input props:\r\n',
    #   b'    <none>\r\n', ......

    # Get the input devices that are candidates for sending touch events using sendevent
    sendevent_input_devices = blocking_shell.sh_get_sendevent_input_devices()
    # Out[35]: [['/dev/input/event4', '32767'], ['/dev/input/event5', '65535']]

    # Use the previously obtained data to execute a touch event using sendevent
    blocking_shell.sh_sendevent_touch(
        x=600,  # X coordinate
        y=400,  # Y coordinate
        inputdev="event4",  # Input device (without '/dev/input/')
        inputdevmax=32767,  # Maximum value from sh_get_sendevent_input_devices()
        width=1600,  # Screen width
        height=900,  # Screen height
    )

    # On a Windows system, open a new cmd.exe window to record getevent data
    # This is necessary to capture events, and the data will be saved to the 'myeventfile' file
    blocking_shell.sh_record_getevent(tmpfilegetevent="myeventfile")

    # View the contents of the recorded event data file located at '/sdcard/myeventfile'
    captured_event_data = blocking_shell.sh_cat_file("/sdcard/myeventfile")

    # Record getevent data as binary from the specified device, e.g., '/dev/input/event4', and save it to 'somefilename'
    outputpath = blocking_shell.sh_record_getevent_as_binary_data(
        device="/dev/input/event4", tmpfilegetevent="somefilename"
    )

    # Pause execution until the user presses Enter to continue
    input("Press enter when ready")

    # Convert the binary getevent data into decimal values
    # 'purebindata' can be sent to the device to execute the commands (e.g., using https://github.com/hansalemaos/geteventplayback)
    purebindata, alldata = blocking_shell.convert_getevent_binary_data_to_decimal(
        outputpath
    )

    fi = blocking_shell.sh_record_getevent(tmpfilegetevent="getevenfile2")
    # File will be saved: /sdcard/getevenfile2
    # fi
    # Out[5]: '/sdcard/getevenfile2'

    # Exit the 'su' shell (superuser mode), if it was previously entered
    blocking_shell.exit_from_su_shell()

    # Capture events from a specified input device, e.g., 'event4', with better timestamp formatting
    stdout, stderr = blocking_shell.sh_getevent_capture(
        "event3", 1000, disable_print_stdout=False
    )

    # The captured data includes event timestamps and coordinates (x, y)

    #   1698717226            0        54020            4            0
    #      3473411        23642        24106        25920            0   x= 1154
    #       316164            0            3           54        19633   y=  539
    #   1698717226            0        54020            4            0
    #       131072            0        24106        25920            0
    #       316164            0            0            0            0
    #   1698717226            0        55679            4            0
    #      3473411        23679        24106        25920            0   x= 1156
    #       317823            0            3           54        19568   y=  537
    #   1698717226            0        55679            4            0
    #       131072            0        24106        25920            0
    #       317823            0            0            0            0
    #   1698717226            0        56899            4            0
    #      3473411        23679        24106        25920            0   x= 1156
    #       319043            0            3           54        19568   y=  537
    #   1698717226            0        56899            4            0
    #       131072            0        24106        25920            0
    #       319043            0            0            0            0
    #   1698717226            0        23086            5            0

    # On Windows, open a new cmd.exe shell in a separate window
    blocking_shell.open_adb_shell()
    version = blocking_shell.sh_get_android_version()
    blocking_shell.get_all_devices()

    print(version)

    blocking_shell.execute_adb_command(
        f"-s {blocking_shell.device_serial} reverse tcp:1300 tcp:1600"
    )

    # muuuuch faster than adb pull / adb shell cat
    # Requirements: Windows / Cygwin (with nc.exe and tar.exe)
    # busybox on the Android device and su
    blocking_shell.netcatcopy(
        tarpath="tar.exe",
        netcatpath="nc.exe",
        outputfolder="c:\\testbackuo3",  # will be created
        foldertodownload="/data/data/com.instagram.lite/",
        tmpfilename="taradbdownload.tar",
    )

    # Some non shell ADB commands
    blocking_shell.adb_reconnect()
    blocking_shell.adb_root()
    blocking_shell.adb_remount_as_rw()

    blocking_shell.adb_install(
        path=r"C:\Users\hansc\Downloads\Opera Mini_ Fast Web Browser_72.0.2254.67482_Apkpure.apk",
        grand_permissions=True,
        replace=True,
        allow_test=True,
        allow_downgrade=False,
        to_83=True,
    )
    packname = [
        x.strip().split(b":")[-1].decode("utf-8")
        for x in blocking_shell.sh_pm_list_packages_3()[0]
        if b"opera" in x
    ][0]
    blocking_shell.adb_uninstall(packname)
    blocking_shell.adb_unroot()

    # port forwarding
    blocking_shell.adb_forward_port(6000, 6100)
    blocking_shell.adb_reverse_port(9000, 9100)
    p1 = blocking_shell.adb_show_forwarded_ports()
    p2 = blocking_shell.adb_show_reversed_ports()
    print(p1)
    print(p2)
    blocking_shell.adb_remove_forwarded_port(6000)
    blocking_shell.adb_remove_reversed_port(9000)
    p1 = blocking_shell.adb_show_forwarded_ports()
    p2 = blocking_shell.adb_show_reversed_ports()
    print(p1)
    print(p2)
    # [[b'127.0.0.1:5555 tcp:6000 tcp:6100', b''], []]
    # [[b'host-9 tcp:9000 tcp:9100', b''], []]
    # [[b''], []]
    # [[b''], []]
    s01, s02 = blocking_shell.adb_pull(
        path_device="/sdcard/window_dump.xml",
        path_pc="C:\\PUSHEDTEST",
        escape_path=True,
    )
    s03, s04 = blocking_shell.adb_push(
        path_pc=r"C:\Users\hansc\Downloads\1633637532_Royale High Candy Autofarm .webp",
        path_device="/sdcard/Download",
        escape_path=True,
        to_83=False,
    )
    blocking_shell.sh_get_file_extension("/sdcard/window_dump.xml")
    #  'xml'
    blocking_shell.sh_get_md5sum(path="/sdcard/window_dump.xml")
    # '027001170290b3415144019a4c3db567'
    blocking_shell.sh_realpath(path="/sdcard/window_dump.xml")
    # '/storage/emulated/0/window_dump.xml'
    blocking_shell.sh_dirname(path="/sdcard/window_dump.xml")
    blocking_shell.execute_sh_command("uiautomator dump")
    blocking_shell.sh_rename_file_to_md5("/sdcard/window_dump.xml")
    #  '/sdcard/09e1ad07ae0c4f3df822e18977c2fd3f.xml'
    blocking_shell.sh_get_size_of_terminal()
    # : [80, 24]
    blocking_shell.sh_change_to_dir("/sdcard/Download")
    print(blocking_shell.sh_ls())
    blocking_shell.sh_change_to_prev_working_dir()
    print(blocking_shell.sh_ls())

    blocking_shell.sh_create_file_with_content("bibi baba", "/sdcard/çç ççtest.txt")
    # Out[7]: [[], []]
    blocking_shell.sh_cat_file("/sdcard/çç ççtest.txt")
    # Out[8]: b'bibi baba'
    # with binary data:
    blocking_shell.sh_create_file_with_content(b"bibi baba", "/sdcard/çç ççötest.txt")
    # Out[9]: [[], []]
    blocking_shell.sh_cat_file("/sdcard/çç ççötest.txt")
    # Out[10]: b'bibi baba'

    blocking_shell.sh_ping_one_time("www.google.com")
    # Out[3]:
    # [[b'PING www.google.com (142.250.218.68) 56(84) bytes of data.\r\n',
    #   b'\r\n',
    #   b'--- www.google.com ping statistics ---\r\n',
    #   b'1 packets transmitted, 1 received, 0% packet loss, time 0ms\r\n',
    #   b'rtt min/avg/max/mdev = 16.937/16.937/16.937/0.000 ms\r\n'],
    #  []]
    blocking_shell.sh_create_file_with_content(
        b"   bibi\n    baba\n ddd", "/sdcard/çç ççötest.txt"
    )

    fiu = blocking_shell.sh_cat_file_without_leading_whitespaces(
        "/sdcard/çç ççötest.txt"
    )

    # This does only work wit blocking_shell, the subshells can't set vars
    print(fiu)
    sh_variable_existsv = blocking_shell.sh_variable_exists("bibi", global_cmd=True)
    print(sh_variable_existsv)
    blocking_shell.execute_sh_command_global("bibi=5")
    sh_variable_existsv2 = blocking_shell.sh_variable_exists("bibi", global_cmd=True)
    print(sh_variable_existsv2)

    # Another way to call the blocking_shell
    blocking_shell.execute_sh_command_global("ls")

    blocking_shell.sh_get_file_with_tstamp("testfile", ".tar.gz")
    blocking_shell.sh_memory_dump()
    blocking_shell.sh_ls_fp("/sdcard/")
    blocking_shell.sh_iptables()
    blocking_shell.sh_reverse_file("/sdcard/your_sqlite_text.txt")

    blocking_shell.sh_append_to_file(
        filedata="bbabab babab", path="/sdcard/çç ççötest.txt"
    )
    blocking_shell.sh_echo_rev("My name is John")
    blocking_shell.sh_netstat_ip_group()
    # Out[3]:
    # [[b'      1 142.251.128.106\n',
    #   b'      1 142.251.128.42\n',
    #   b'      1 142.251.129.202\n',
    #   b'      3 142.251.128.10\n'],
    #  []]
    blocking_shell.sh_process_tree()
    # [[b'init(1)-+-Binder:1755_2(1755)-+-sdcard(2143)-+-{sdcard}(2148)\n',
    #   b'        |                     |              |-{sdcard}(2149)\n',
    #   b'        |                     |              `-{sdcard}(2150)\n',
    #   b'        |                     |-{Binder:1755_1}(1757)\n',
    #   b'        |                     |-{Binder:1755_2}(1758)\n',
    #   b'        |                     |-{Binder:1755_3}(1759)\n',
    #   b'        |                     `-{Binder:1755_4}(1790)\n',
    #   b'        |-Binder:1792_2(1792)-+-ip6tables-resto(1848)\n',
    blocking_shell.sh_list_hdds()
    blocking_shell.sh_cat_file_without_leading_whitespaces("/sdcard/çç ççötest.txt")
    blocking_shell.sh_list_hdds_real()
    blocking_shell.sh_lsof_filehandles()
    blocking_shell.sh_list_exe_in_path()
    blocking_shell.sh_free_memory()
    blocking_shell.sh_ls_size("/sdcard/Download")
    # Out[3]:
    # [[b'-rw-rw---- 1 root sdcard_rw       0 2023-10-21 20:31 ba.html\n',
    #   b'total 6444\n',
    #   b'-rw-rw---- 1 root sdcard_rw      21 2023-10-24 22:48 datetmp.log\n',
    #   b'-rw-rw---- 1 root sdcard_rw      46 2023-10-25 17:57 bibixx.png\n',
    #   b'-rw-rw---- 1 root sdcard_rw    5696 2023-10-25 18:06 bibi.png\n',
    #   b'-rw-rw---- 1 root sdcard_rw   10240 2023-10-29 20:48 tmp5j75s57u.tar\n',
    #   b'-rw-rw---- 1 root sdcard_rw   28682 2023-11-01 19:34 1633637532_Royale High Candy Autofarm .webp\n',
    #   b'-rw-rw---- 1 root sdcard_rw   92590 2023-10-31 12:42 asgasdfasdfasdf.png\n',
    #   b'-rw-rw---- 1 root sdcard_rw  294188 2023-10-25 18:06 baba.png\n',
    #   b'-rw-rw---- 1 root sdcard_rw 6147735 2023-10-25 18:06 babaxx2.mhtml\n']
    # The day your device came alive
    blocking_shell.sh_get_install_date()
    blocking_shell.sh_get_audio_playing_procs()
    blocking_shell.sh_get_kernel_infos()
    blocking_shell.sh_get_procs_with_open_connections()
    blocking_shell.sh_chr("77")
    blocking_shell.sh_list_extensions_in_folder("/sdcard/Download")
    # Out[3]:
    # [[b'      1 html\n',
    #   b'      1 log\n',
    #   b'      1 mhtml\n',
    #   b'      1 tar\n',
    #   b'      1 webp\n',
    #   b'      4 png\n'],
    blocking_shell.sh_comment_out_line_in_file(2, "/sdcard/your_sqlite_text.txt")
    blocking_shell.sh_cat_file("/sdcard/your_sqlite_text.txt")
    blocking_shell.sh_tar_backup_of_folder_to_sdcard("/sdcard/Download")
    # b'#!/bin/bash\nexec 2>/sdcard/errortmp16989042186992085.txt\nexec 1>/sdcard/outputtmp16989042186992085.txt\ncd /sdcard/Download\nfind . -type f -exec md5sum {} \\;\nexec 1>&-\nexec 2>&-\n\necho -n -e xxxCOMMANDxxxDONExxx>> /sdcard/outputtmp16989042186992085.txt\necho -n -e xxxCOMMANDxxxDONExxx >> /sdcard/errortmp16989042186992085.txt\n'
    # Out[3]:
    # [[b'bdb92ce5db632c499f8c1d52b6bcff13  ./babaxx2.mhtml\n',
    #   b'6f44a9d7667d8e166cb5d5cbbb674709  ./bibi.png\n',
    #   b'd41d8cd98f00b204e9800998ecf8427e  ./ba.html\n',
    blocking_shell.sh_delete_all_files_in_folder_except_newest("/sdcard/Download9")
    blocking_shell.sh_apps_using_internet()
    blocking_shell.sh_goto_next_sibling_folder()
    blocking_shell.sh_cd_and_search_string_in_files("/sdcard/Download", "html")

    # This method has to be executed with blocking_subshell - base64 - due to some chars in the script
    coords = blocking_subshell.sh_search_for_colors(
        colorlist=[(183, 28, 28)], global_cmd=False
    )
    size = blocking_shell.sh_calculate_size_of_folders("/sdcard/")
    # [(4, b'20231024/'), (8, b'AUTOMAT/'), (1045336, b'Android/'), (344, b'DCIM/'), (6460, b'Download/'), (100, b'Download2/'), (8, b'Download4/'), (96, b'Download9/'), (4, b'REPLACE_BINFOLDER/'), (16, b'a/'),


```