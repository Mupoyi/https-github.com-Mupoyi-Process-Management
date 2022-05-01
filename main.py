import sys
from algorithms.Priority import Priority

if __name__ == '__main__':
    try:
        num_process = int(input("Enter number of process : "))
    except:
        print("[X] Please enter an integer, run again python main.py")
        sys.exit(0)
    p = Priority(num_process)
    p.simulate()
    
