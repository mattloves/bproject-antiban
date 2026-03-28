[app]

title = B项目防封
package.name = antiban_cloud
package.domain = com.bproject

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.3.0

fullscreen = 1

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.archs = arm64-v8a,armeabi-v7a

android.meta_data = com.google.android.gms.version.@android/get_ad_unit_id

[buildozer]

log_level = 2

warn_on_root = 0

build_dir = ./.buildozer

bin_dir = ./bin
