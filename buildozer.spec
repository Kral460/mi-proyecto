[app]

title = ConversorAudio
package.name = conversoraudio
package.domain = org.conversor.audio

source.dir = .
source.include_exts = py,kv,png,jpg

version = 1.0

requirements = python3,kivy,plyer

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

log_level = 2

[buildozer]

warn_on_root = 1
