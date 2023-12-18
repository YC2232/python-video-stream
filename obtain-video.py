import requests
import json
import cv2
def get_rtsp_stream_url(url, channel_code, stream_type=0):
    payload = json.dumps({
        "channelCode": channel_code,
        "streamType": stream_type
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)


    # 检查响应状态
    if response.status_code == 200:
        # 解析 JSON 响应
        response_data = response.json()
        # 提取并返回 URL
        return response_data.get('data', {}).get('url', None)

    else:
        print(f"Error: Unable to fetch URL, Status Code: {response.status_code}")
        return None


def open_video_stream(stream_url, resize_factor=0.5, new_fps=30):
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        exit()

    # 获取视频原始帧率和尺寸
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 调整分辨率和帧率
    width = int(original_width * resize_factor)
    height = int(original_height * resize_factor)
    fps = min(new_fps, original_fps)

    # 使用 H.264 编解码器
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter("my-file.mp4", fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 调整帧的尺寸
        resized_frame = cv2.resize(frame, (width, height))

        out.write(resized_frame)
        cv2.imshow("Frame", resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()



def main():
    # rtsp_url = "http://1.192.171.31:19480/hik/petrol/camera/video/rtsp"
    # channel_code = "00099c0d928f4cde95dd48148651d115"
    #
    # rtsp_stream_url = get_rtsp_stream_url(rtsp_url, channel_code)
    #
    # if rtsp_stream_url:
    #     print("RTSP Stream URL:", rtsp_stream_url)
    # else:
    #     print("Failed to get RTSP Stream URL.")
    #
    # open_video_stream(rtsp_stream_url)
    open_video_stream("rtmp://mobliestream.c3tv.com:554/live/goodtv.sdp")


if __name__ == "__main__":
    main()


