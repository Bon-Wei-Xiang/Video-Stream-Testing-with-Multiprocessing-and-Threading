  Video Stream Testing

Video Stream Testing with Multiprocessing and Threading
=======================================================

Overview
--------

This code allows you to test your PC's capacity for handling multiple video streams simultaneously. It leverages Python's `multiprocessing` and `threading` libraries to efficiently read, display, and manage multiple video streams, showcasing how many video streams your system can handle concurrently. The code can split video processing tasks across multiple processes, with each process managing a subset of videos.


![example](example.gif)

Features
--------

*   **Parallel Processing**: Uses multiprocessing to assign video tasks across multiple CPU cores.
*   **Threaded Execution**: Utilizes threading to separate video reading and displaying tasks for each video.
*   **Queue Management**: Manages frames using queues to balance load and ensure smooth video playback.

Requirements
------------

*   Python 3.x
*   OpenCV (`cv2`) installed via:
    
        pip install opencv-python==4.8.0
    

Code Usage
----------

### Command-Line Arguments

The code accepts the following command-line arguments:

*   `--videos`: List of video file paths to process. Multiple files can be added by separating each path with a space.
*   `--processes`: Number of processes to handle the videos. This defines how many CPU processes will be used.

### Running the Code

To execute the code, use the following command:

    python script_name.py --videos <video1.mp4> <video2.mp4> <video3.mp4> --processes <num_processes>

Replace `<video1.mp4>`, `<video2.mp4>`, etc., with the paths to your video files, and `<num_processes>` with the desired number of processes to use.

**Example:**

    python script_name.py --videos test.mp4 car3.mp4 car3_night.mp4 car1.mp4 --processes 4

### Code Structure

*   **`Video` Class**: Manages individual video streams. Uses threading to separate the video reading and displaying tasks.
*   **`VideoAgent` Class**: Manages a set of video streams assigned to a process. Each `VideoAgent` handles multiple `Video` objects and synchronizes their display.
*   **`Controller` Class**: Splits videos across processes, creating multiple `VideoAgent` instances, each handling a subset of the video list.
*   **`args_parser` Function**: Parses command-line arguments using `argparse` to set up video paths and process count.

### Closing a Video Stream

Press **'c'** in the video window to close a specific video stream.