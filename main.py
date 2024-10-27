import argparse
import cv2
import threading, multiprocessing

class Video:
    def __init__(self, video_path: str, window_name: str, show_sync_switch):
        self.__VD = cv2.VideoCapture(video_path)
        self.__queue = multiprocessing.Queue(maxsize=30)
        self.start_switch = threading.Barrier(2)
        self.close_switch = threading.Event()
        self.__window_name = window_name
        self.show_sync_switch = show_sync_switch

    def __read_video(self):
        self.start_switch.wait()
        while not self.close_switch.is_set():
            ret, frame = self.__VD.read()
            if ret:
                self.__queue.put(frame)
            else:
                break
        self.__VD.release()
        self.__close()
        return

    def __show_video(self):
        self.start_switch.wait()
        self.show_sync_switch.wait()
        while not self.close_switch.is_set():
            if self.__queue.qsize() > 0:
                frame = self.__queue.get()
                if cv2.waitKey(1) & 0xff == ord('c'):
                    break
                cv2.imshow(f"{self.__window_name}", frame)
        self.__close()
        return

    def __close(self):
        if not self.close_switch.is_set():
            self.close_switch.set()
            self.__clear_queue()

    def __clear_queue(self):
        while self.__queue.qsize() > 0:
            self.__queue.get()
        print(f"{self.__window_name} closed")
        return

    def start(self):
        print(f"{self.__window_name} start")
        read_video = threading.Thread(target=self.__read_video, daemon=True)
        show_video = threading.Thread(target=self.__show_video)
        read_video.start()
        show_video.start()
        return


class VideoAgent:
    def __init__(self, number_of_video: list, video_name: list, name: str):
        self.__number_of_video = number_of_video
        self.__video_name = video_name
        self.__name = name
        self.show_lock = multiprocessing.Barrier(len(number_of_video))

    def start_video(self):
        print(f"Video Agent {self.__name} start")
        videos = [Video(video_path=i, window_name=f"{self.__video_name[idx]}", show_sync_switch=self.show_lock) for idx, i in
                  enumerate(self.__number_of_video)]
        for i in videos:
            i.start()
        return

    def start(self):
        multiprocessing.Process(target=self.start_video).start()
        return


class Controller:
    def __init__(self, video_list: list, num_of_process: int):
        self.__video_list = video_list
        self.__num_of_process = num_of_process
        self.__video_split_list, self.__video_name_split_list = self.__split_video()
        self.video_agent_list = [
            VideoAgent(number_of_video=self.__video_split_list[i], video_name=self.__video_name_split_list[i],
                       name=f"Agent {i}") for i in range(len(self.__video_split_list))]

    def __split_video(self) -> tuple:
        video_split_list = self.split_list(self.__video_list, self.__num_of_process)
        video_name_split_list = [[f"Process : {i} Video : {j}" for j in range(len(video_list))]
                                 for i, video_list in enumerate(video_split_list)]

        handle_videos_per_process = len(self.__video_list) / self.__num_of_process
        print(f"number of video : {len(self.__video_list)}")
        print(f"number of process : {self.__num_of_process}")
        print(f"each process handle : {int(handle_videos_per_process)} Videos")
        if isinstance(handle_videos_per_process, float):
            print(f"last process handle : {len(video_split_list[-1])} video")
        return video_split_list, video_name_split_list

    def split_list(self, input_list, num_splits):
        split_length = len(input_list) // num_splits
        remainder = len(input_list) % num_splits
        splits = []
        start = 0

        for i in range(num_splits):
            end = start + split_length + (1 if i < remainder else 0)
            splits.append(input_list[start:end])
            start = end

        return splits

    def start(self):
        for i in self.video_agent_list:
            i.start()

def args_parser():
    parser = argparse.ArgumentParser(description="Video processing with multiprocessing and threading.")
    parser.add_argument("--videos", nargs="+", required=True, help="List of video file paths to process.")
    parser.add_argument("--processes", type=int, required=True, help="Number of processes to handle videos.")

    args = parser.parse_args()

    video = args.videos
    number_of_process = args.processes

    return video, number_of_process

if __name__ == "__main__":
    video, number_of_process = args_parser()
    try:
        a = Controller(video, number_of_process)
        a.start()
    except Exception as e:
        import traceback
        traceback.print_exc()