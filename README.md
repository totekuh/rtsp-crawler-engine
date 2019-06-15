# rtsp-crawler-engine

# IMPORTANT! RTSP probing is running through a tor proxy, you should probably do the same.
# IMPORTANT! If you are using a masscan to locate the streams, please note that masscan is using it's own TCP/IP stack, so it will ignore your proxy. To avoid this and keep your anonymity safe, you can try to init your scans via VPN connection with packets masquerading.

# There are different ways to obtain the cameras:
# 1. blindly scan the internet and locate open streams:
./masscan_to_rtsp.py --masscan 10.0.0.0/8 --output masscan_results.txt
# 1.1 do an aggressive scan:
./masscan_to_rtsp.py --masscan 10.0.0.0/8 --aggressive --output masscan_results.txt

# 1.2 probe the results
torify ./rtsp_probe.py --batch-list masscan_results.txt --output probe_result.json


# 2. Get the cameras from the Shodan API and feed them into the crawler. You should be a member of Shodan to export their results.

# 2.1 consume the shodan JSON export to extract and probe cameras:
torify ./rtsp_probe.py --batch-json shodan-export.json --output probe_result.json

# 3 stream retrieved cameras to the backend API:
torify ./rtsp_probe.py --batch-list masscan_results.txt --output probe_result.json --import http://localhost/camera/stream


# You can use rtsp_probe.py to continuously stream a single camera:
torify ./rtsp_probe.py --url rtsp://10.10.10.10:554 --stream
