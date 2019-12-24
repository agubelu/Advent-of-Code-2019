from etc import intcode
from multiprocessing import Manager, Event
from multiprocessing.managers import RemoteError
from threading import Thread

def run_computer(i, queues, finished):
    comp = intcode.from_file("input/day23.txt")

    def get_packet(i):
        return -1 if queues[i].empty() else queues[i].get()
             
    comp.set_inputs([i, get_packet])
    comp.set_funcargs([i])

    if i != 50:
        # Regular computer
        while True:
            try:
                addr, x, y = comp.get_next_output(), comp.get_next_output(), comp.get_next_output()
                if addr == 255: addr = 50
                queues[addr].put([x, y], False)
            except RemoteError: pass  # Main process is closing
    else:
        # NAT
        last_msg = None, None
        cur_msg = queues[i].get()
        
        if not last_msg[0]:  # Prints parts 1
            print(cur_msg[1])

        while not finished.is_set():
            while not all(q.empty() for q in queues[:50]): 
                pass

            while not queues[i].empty(): 
                cur_msg = queues[i].get()

            if last_msg[1] == cur_msg[1]:
                print(cur_msg[1])  # Prints part 2
                finished.set()

            last_msg = cur_msg
            queues[0].put([cur_msg[0], cur_msg[1]])

if __name__ == "__main__":  # Required so that Windows doesn't complain
    manager = Manager()
    list_of_qs = [manager.Queue() for _ in range(51)]
    finished = Event()
    ps = [Thread(target=run_computer, args=(i, list_of_qs, finished), daemon=True) for i in range(51)]
    for p in ps: p.start()
    finished.wait()
