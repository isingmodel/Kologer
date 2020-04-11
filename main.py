import qt_text_ui as ui
import keyboard_recorder as kr
import mouse_recorder as mr
from pynput import keyboard
from multiprocessing import Process
from multiprocessing import Queue
import pickle as pkl
from queue import Empty
import time
from sys import exit as sysExit


def make_listener_run(listener):
    listener = kr.start_keyboard_logging("nothing")
    listener.join()


def get_data_from_queue(d_q):
    pynput_data = list()
    pyqt_data = list()
    while True:
        try:
            data = d_q.get(block=False)
            print(data)
            if data[0] == "pynput":
                pynput_data.append(data)
            elif data[0] == "pyqt":
                pyqt_data.append(data)

            elif data[0] == "exit":
                break
        except Empty:
            print("queue empty")
            pass
        time.sleep(0.02)
    with open("./temp_data/keyboard_recording.pkl", 'wb') as f_pynput:
        pkl.dump(pynput_data, f_pynput)
    with open("./temp_data/ui_data.pkl", 'wb') as f_ui:
        pkl.dump(pynput_data, f_ui)



if __name__ == "__main__":
    data_queue = Queue(maxsize=200)
    p_save = Process(target=get_data_from_queue, args=(data_queue,))
    p_save.start()
    p = Process(target=make_listener_run, args=(data_queue,))
    p.start()
    ui.execute_ui(data_queue)

