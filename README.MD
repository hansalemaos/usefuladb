# A collection of useful adb commands 

## Tested against Windows / Python 3.11 / Anaconda

## pip install usefuladb

```python

import re
import regex
from usefuladb import AdbCommands

adbpath = r"C:\Android\android-sdk\platform-tools\adb.exe"
serial_number = "127.0.0.1:5555"
uadb = AdbCommands(
    adbpath, serial_number, use_busybox=False
)  # if use_busybox is True, busybox will be used to decode the base64-encoded command

uadb.connect_to_device_ps()
stdout, stderr = uadb.sh_swipe(10, 10, 300, 400, 1.2, ps=True)
stdout1, stderr1 = uadb.sh_swipe(10, 10, 300, 400, 1.2, ps=False)
stdout2, stderr2 = uadb.adb_install(
    r"C:\Users\hansc\Downloads\instagram-lite-365-0-0-12-53.apk", ps=True
)
stdout3, stderr3 = uadb.adb_install(
    r"C:\Users\hansc\Downloads\AdAway-6.1.1-20230  620.apk", ps=False
)
uadb.adb_push(
    r"C:\Users\hansc\Downloads\FiddlerSetup (1).exe", "/sdcard/test1.exe", ps=True
)
uadb.adb_push(
    r"C:\Users\hansc\Downloads\FiddlerSetup (1).exe", "/sdcard/test1.exe", ps=False
)
print(uadb.sh_file_exists("/sdcard/test1.exe", ps=True))
print(uadb.sh_file_exists("/sdcard/test1.exe", ps=False))
print(uadb.sh_file_exists("/sdcard/test11.exe", ps=True))
print(uadb.sh_file_exists("/sdcard/test11.exe", ps=False))
print(uadb.sh_is_folder("/sdcard/", ps=True))
print(uadb.sh_is_folder("/sdcard/", ps=False))
uadb.sh_rename(src="/sdcard/test1.exe", dst='"/sdcard/t es t1.exe"', ps=True)
uadb.sh_rename(src="/sdcard/test1.exe", dst='"/sdcard/t es t1.exe"', ps=False)
uadb.adb_push_to_file_path(
    r"C:\Users\hansc\Downloads\AdAway-6.1.1-20230  620.apk",
    "/sdcard/baba/bubu",
    ps=True,
)
uadb.adb_push_to_file_path(
    r"C:\Users\hansc\Downloads\AdAway-6.1.1-20230  620.apk",
    "/sdcard/baba/bubu2",
    ps=False,
)
uadb.sh_touch("/sdcard/bab bcçc/xxx.txt", ps=False)
uadb.sh_touch("/sdcard/bab bcc/xxx.txt", ps=True)
uadb.sh_open_date_settings()
uadb.sh_open_application_development_settings()
uadb.sh_open_location_source_settings()
uadb.sh_open_memory_card_settings()
uadb.sh_open_locale_settings()
uadb.sh_open_search_settings()
uadb.sh_open_settings()
uadb.sh_open_account_sync_settings()
uadb.sh_open_display_settings()
uadb.sh_open_input_method_settings()
uadb.sh_open_sound_settings()
uadb.sh_open_wifi_settings()
uadb.sh_open_application_settings()
uadb.sh_open_account_sync_settings_add_account()
uadb.sh_open_manage_applications_settings()
uadb.sh_open_sync_settings()
uadb.sh_open_dock_settings()
uadb.sh_open_add_account_settings()
uadb.sh_open_security_settings()
uadb.sh_open_device_info_settings()
uadb.sh_open_wireless_settings()
uadb.sh_open_system_update_settings()
uadb.sh_open_manage_all_applications_settings()
uadb.sh_open_data_roaming_settings()
uadb.sh_open_apn_settings()
uadb.sh_open_user_dictionary_settings()
uadb.sh_open_voice_input_output_settings()
uadb.sh_open_tts_settings()
uadb.sh_open_wifi_ip_settings()
uadb.sh_open_web_search_settings()
uadb.sh_open_bluetooth_settings()
uadb.sh_open_airplane_mode_settings()
uadb.sh_open_internal_storage_settings()
uadb.sh_open_accessibility_settings()
uadb.sh_open_quick_launch_settings()
uadb.sh_open_privacy_settings()
print(uadb.sh_get_display_orientation())
uadb.k_app_switch(ps=True, longpress=True)
uadb.k_app_switch(ps=False, longpress=True)
uadb.k_app_switch(ps=True, longpress=False)
uadb.k_app_switch(ps=False, longpress=False)
uadb.k_app_switch()
uadb.k_brightness_down()
uadb.k_brightness_up()
uadb.k_contacts()
uadb.k_copy()
uadb.k_cut()
uadb.k_home()
uadb.k_page_down()
uadb.k_page_up()
uadb.k_paste()
uadb.k_power()
uadb.k_search()
uadb.k_sleep()
uadb.k_tab()
uadb.k_volume_down()
uadb.k_volume_up()
uadb.k_volume_mute()
uadb.k_wakeup()
uadb.adb_push_to_file_path(
    r"C:\Users\hansc\Downloads\avatar-gen11080ba46e2948ca0f20c6c9463f302e.jpg",
    "/sdcard/DCIM",
)
uadb.adb_push(
    r"C:\Users\hansc\Downloads\avatar-gen11080ba46e2948ca0f20c6c9463f302e.jpg",
    "/sdcard/DCIM/testpic.jpg",
)
uadb.sh_rescan_one_media("/sdcard/DCIM/testpic.jpg", ps=True)
uadb.sh_rescan_one_media("/sdcard/DCIM/testpic.jpg", ps=False)
uadb.sh_list_users(ps=True)
uadb.sh_list_users(ps=False)
uadb.sh_enable_heads_up_notifications()
uadb.sh_disable_heads_up_notifications()
uadb.sh_remove_file("/sdcard/test with space.pdf", ps=True)
uadb.sh_remove_file("/sdcard/t es t1.exe", ps=False)
uadb.sh_still_image_camera(ps=True)
uadb.sh_still_image_camera(ps=False)
uadb.sh_make_call("+5511989782756")
uadb.sh_dumpsys_activity_settings()
uadb.sh_dumpsys_activity_allowed_associations()
uadb.sh_dumpsys_activity_intents()
uadb.sh_dumpsys_activity_broadcasts()
uadb.sh_dumpsys_activity_broadcast_stats()
uadb.sh_dumpsys_activity_providers()
uadb.sh_dumpsys_activity_permissions()
uadb.sh_dumpsys_activity_services()
uadb.sh_dumpsys_activity_recents()
uadb.sh_dumpsys_activity_lastanr()
uadb.sh_dumpsys_activity_starter()
uadb.sh_dumpsys_activity_activities()
uadb.sh_dumpsys_activity_exit_info()
uadb.sh_dumpsys_activity_processes()
uadb.sh_dumpsys_activity_lru()
uadb.sh_pm_dump("com.android")
uadb.sh_get_wm_size()
uadb.sh_change_wm_size(960, 540)
uadb.sh_wm_reset_size()
uadb.sh_get_wm_density()
uadb.sh_change_wm_density(160)
uadb.sh_wm_reset_density()
uadb.sh_list_features()
uadb.sh_pwd()
uadb.sh_list_services()
uadb.sh_ps_a_t_l_z()
uadb.sh_open_url("https://www.goolge.com")
uadb.sh_get_ntp_server()
# uadb.sh_set_ntp_server()
uadb.sh_pm_list_packages_f_i_u()
uadb.sh_pm_list_packages_3()
uadb.sh_pm_list_packages_s()
uadb.sh_mount()
imei, imsi, sim = uadb.sh_get_imei_imsi_sim()
fi = uadb.sh_cat_get_file("/sdcard/DCIM/testpic.jpg", ps=True)
print(fi)
fi = uadb.sh_cat_get_file("/sdcard/DCIM/testpic.jpg", ps=False)
print(fi)

uadb.adb_pull(
    src="/sdcard/DCIM/testpic.jpg", dst="c:\\fooo2 xxxx\\bababa.jpg", ps=False
)
uadb.adb_pull(
    src="/sdcard/DCIM/testpic.jpg", dst="c:\\fooo2 xxxx\\bababa2.jpg", ps=True
)
uadb.adb_push(
    r"C:\Users\hansc\Downloads\avatar-gen11080ba46e2948ca0f20c6c9463f302e.jpg",
    "/sdcard/DCIM",
)
uadb.adb_push(
    r"C:\Users\hansc\Downloads\FiddlerSetup (1).exe", "/sdcard/bibibu", ps=True
)
uadb.adb_push_to_file_path(
    r"C:\Users\hansc\Downloads\avatar-gen11080ba46e2948ca0f20c6c9463f302e.jpg",
    "/sdcard/DCIM/somepic.jpg",
)
uadb.adb_push_to_file_path(
    r"C:\Users\hansc\Downloads\FiddlerSetup (1).exe",
    "/sdcard/bibibu/xx/exefile.exe",
    ps=True,
)
uadb.adb_pull_to_folder_nested(
    "/sdcard/bibibu/FiddlerSetup (1).exe", "c:\\new folder test"
)
uadb.sh_change_display_orientation(new_orientation=1)
uadb.sh_do_random_actions("com.roblox.client")
uadb.sh_change_display_orientation(new_orientation=0)
width, height = uadb.sh_get_resolution()
uadb.sh_start_package("com.roblox.client")
uadb.sh_expand_notifications()
uadb.sh_expand_settings()
stdout, stderr = uadb.sh_resolve_activity("com.roblox.client")
stdout, stderr = uadb.sh_resolve_activity_brief("com.roblox.client")
uadb.sh_list_permission_groups()
uadb.sh_dumpsys_window()
uadb.sh_is_screen_locked()
uadb.sh_input_tap(500, 500)
uadb.sh_input_dpad_tap(500, 500)
uadb.sh_input_keyboard_tap(500, 500)
uadb.sh_input_mouse_tap(500, 500)
uadb.sh_input_touchpad_tap(500, 500)
uadb.sh_input_gamepad_tap(500, 500)
uadb.sh_input_touchnavigation_tap(500, 500)
uadb.sh_input_joystick_tap(500, 500)
uadb.sh_input_touchscreen_tap(500, 500)
uadb.sh_input_stylus_tap(500, 500)
uadb.sh_input_trackball_tap(500, 500)
uadb.sh_input_dpad_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_keyboard_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_mouse_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_touchpad_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_gamepad_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_touchnavigation_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_joystick_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_touchscreen_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_stylus_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_trackball_text("bibib", sleeptime=(0.0, 0.0), remove_accents=False)
uadb.sh_input_dpad_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_dpad_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_dpad_roll(x=10, y=300)
uadb.sh_input_keyboard_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_keyboard_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_keyboard_roll(x=10, y=300)
uadb.sh_input_mouse_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_mouse_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_mouse_roll(x=10, y=300)
uadb.sh_input_touchpad_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_touchpad_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_touchpad_roll(x=10, y=300)
uadb.sh_input_gamepad_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_gamepad_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_gamepad_roll(x=10, y=300)
uadb.sh_input_touchnavigation_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_touchnavigation_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_touchnavigation_roll(x=10, y=300)
uadb.sh_input_joystick_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_joystick_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_joystick_roll(x=10, y=300)
uadb.sh_input_touchscreen_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_touchscreen_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_touchscreen_roll(x=10, y=300)
uadb.sh_input_stylus_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_stylus_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_stylus_roll(x=10, y=300)
uadb.sh_input_trackball_swipe(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_trackball_drag_and_drop(x0=300, y0=100, x1=500, y1=500, t=1.0)
uadb.sh_input_trackball_roll(x=10, y=300)
uadb.keyevents.KEYCODE_A.longpress_ps.touchpad()
uadb.sh_input_dpad_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_dpad_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_keyboard_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_keyboard_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_mouse_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_mouse_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_touchpad_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_touchpad_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_gamepad_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_gamepad_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_touchnavigation_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_touchnavigation_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_joystick_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_joystick_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_touchscreen_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_touchscreen_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_stylus_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_stylus_longtap(x=304, y=360, t=1.0, ps=True)
uadb.sh_input_trackball_longtap(x=304, y=360, t=1.0, ps=False)
uadb.sh_input_trackball_longtap(x=304, y=360, t=1.0, ps=True)
shots = list(uadb.get_n_screenshots(n=10, sleeptime=None))
d = uadb.get_all_devices()
print(d)
fi = uadb.manage_files("/sdcard/")
md = fi.regex_filepath_search(r"bet.*\.mhtml", flags=re.I)
# md.f85.cat_file()
md[list(md.keys())[0]].cat_file()
md[list(md.keys())[0]].pull_nested("c:\\nestedfo")
md[list(md.keys())[0]].pull("c:\\nestedfo")
md[list(md.keys())[0]].rename("/sdcard/bubuxa.html")
fi = fi.update_list()
md = fi.regex_filepath_search(r"bet.*\.mhtml", flags=re.I)
md[list(md.keys())[0]].remove()
fi = fi.update_list()
allfi = [
    x
    for x in fi.cat_copy_multiple_files(
        folder="c:\\copyofandroid",
        regcomp=regex.compile(r"bet.*\.mhtml", flags=regex.I),
        return_content=True,
        maintain_date=True,
        escape_path=True,
    )
]

ma = fi.grep_search_multiple_files(
    reg=r"\bGre",
    match_file=regex.compile(r"bet.*\.mhtml", flags=re.I),
    escape=True,
    quote=False,
    extended_regexp=True,
    ignore_case=True,
    invert_match=False,
)
backgroundproc = uadb.sh_start_while_loop_activity_check(
    activity_regex="message_paragraph_1",
    positive_action="input tap 1130 620",
    negative_action="input tap 1407 131",
    sleep_time=100,
)

```