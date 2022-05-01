import random
import enum
from termcolor import cprint
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time

class Status(enum.Enum):
    CREATED = 0
    PROCESSED = 1
    DONE = 2

def run_process(proc):
    def running():
        time.sleep(proc['burst_time']/100.0)
    for _ in track(range(100), description='[yellow] {} is running.'.format(proc['name'])):
        running()

class Priority:
    def __init__(self,num_of_process) -> None:
        self.num_of_process = num_of_process
        self._generate()
    def _generate(self):
        process_list = []
        prior = [i+1 for i in range(self.num_of_process)]
        for i in range(self.num_of_process):
            r_time = random.randint(1,11)
            prty = random.choice(prior)
            prior.remove(prty)
            tmp = {
                'name' : 'Process {}'.format(i+1),
                'burst_time': r_time,
                'priority' : prty,
                'status' : Status.CREATED,
            }
            process_list.append(tmp)
        process_list.sort(key=lambda x: x["priority"],reverse=True)
        self.process_list = process_list
            

    def simulate(self):
        self.show_queue_status()
        end_time = 0
        print("\n")
        cprint("\t\tSTART SIMULATION SCHEDULER.", "red")
        print("\n")
        for index,each in enumerate(self.process_list):
            self.process_list[index]["status"] = Status.PROCESSED
            end_time += self.process_list[index]["burst_time"]
            self.process_list[index]["end_time"] = end_time
            self.show_queue_status()
            run_process(each)
            cprint("{} has been terminated.\n".format(self.process_list[index]["name"]), "green")
            self.process_list[index]["status"] = Status.DONE

        self.show_queue_status()
        turn_around_average = self._turn_arround()
        wait_time_avergae = self._wait_time()
        self.show_queue_status(final=True)
        cprint("[+] Turn arround time average {} s".format(turn_around_average),"green")
        cprint("[+] Waiting time average {} s".format(wait_time_avergae),"green")



    def show_queue_status(self, final=False):
        if final:
            table = Table(title="LOGGING")
            table.add_column("Process name", style="blue", justify="right")
            table.add_column("Burst time (s)", style="cyan",justify="center")
            table.add_column("Priority",style="magenta", justify="center")
            table.add_column("Completion time (s)", style="purple", justify="center")
            table.add_column("Waiting time (s)", style="purple", justify="center")
            for each in self.process_list:                
                table.add_row(
                    each["name"],
                    str(each["burst_time"]),
                    str(each["priority"]),
                    str(each["end_time"]),
                    str(each["wait_time"])
                )
            console = Console()
            console.print(table)
            pass
        else:
            table = Table(title="READY QUEUE")
            table.add_column("Process name", style="blue", justify="right")
            table.add_column("Burst time (s)", style="cyan",justify="center")
            table.add_column("Priority",style="magenta", justify="center")
            table.add_column("Status", style="green", justify="center")
            for each in self.process_list:
                show_status = ""
                if each["status"] == Status.CREATED:
                    show_status = "Created"
                if each["status"] == Status.PROCESSED:
                    show_status = "Processed"
                if each["status"] == Status.DONE:
                    show_status = "DONE"
                    
                table.add_row(
                    each["name"],
                    str(each["burst_time"]),
                    str(each["priority"]),
                    show_status
                )
            console = Console()
            console.print(table)


    def _turn_arround(self):
        turn_around_time = 0
        for index, _ in enumerate(self.process_list):
            # end_time - arrival time
            turn_around_time += self.process_list[index]["end_time"]
            # make sense as I assume the arrival time are the same
            self.process_list[index]["turn_around"] = self.process_list[index]["end_time"]
        return float(turn_around_time / self.num_of_process)

    def _wait_time(self):
        wait_time = 0
        for index, _ in enumerate(self.process_list):
            # turn around - burst time
            wait_t = self.process_list[index]["turn_around"] - self.process_list[index]["burst_time"]
            self.process_list[index]["wait_time"] = wait_t
            wait_time += wait_t
        return float(wait_time/self.num_of_process)