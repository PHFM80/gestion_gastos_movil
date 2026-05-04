[app]

title = Control Gastos
package.name = controlgastos
package.domain = org.D&T

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,db,sqlite,csv

version = 0.1

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 35
android.minapi = 23
android.ndk = 25b

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
