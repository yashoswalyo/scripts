import ffmpeg
import json
import os
import subprocess

video_directory = "/path/to/videos"

vpaths = []
print("[+] Cooking ./input.txt")
input = open("./input.txt", "w")
for dirpath, dirnames, filenames in os.walk(video_directory):
    filenames.sort(key=str.casefold)
    for f in filenames:
        # if f.lower().endswith('mp4'):
        # print(os.path.join(dirpath, f))
        vpaths.append(f"file '{os.path.join(dirpath, f)}'")
input.writelines("\n".join(vpaths))
input.close()

print("[+] Serving merged video in ./output dir.")
muxcmd = []
muxcmd.append("ffmpeg")
muxcmd.append("-f")
muxcmd.append("concat")
muxcmd.append("-safe")
muxcmd.append("0")
# for i in range(len(vpaths)):
muxcmd.append("-i")
muxcmd.append("./input.txt")
muxcmd.append("-map")
muxcmd.append("0:v")
muxcmd.append("-map")
muxcmd.append("0:a")
muxcmd.append("-c:v")
muxcmd.append("copy")
muxcmd.append("-c:a")
muxcmd.append("copy")
muxcmd.append("./output/merged.mkv")

subprocess.call(muxcmd)
