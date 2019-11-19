'''
    Utils for scripts

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
import sys, getopt, time, threading, subprocess

class Loader:
    '''
        Worker thread to create a spinner in the terminal

        Args:
                delay (float): The delay time on the spinner
    '''
    isBusy = False
    delay = 0.1

    BARS = '▁▂▃▄▅▆▇█▇▆▅▄▃▁'
    SPINNER = '/-|-\|'

    @staticmethod
    def loadingCursor():
        '''
            Static method to yield each phase of the spinner

            Yields:
                (str)
        '''
        while 1:
            for cursor in Loader.BARS: yield cursor

    def __init__(self, delay=None):
        self.loadingGenerator = self.loadingCursor()
        if delay and float(delay): self.delay = delay

    def loadingTask(self):
        '''
            The task to run in the thread
        '''
        while self.isBusy: # Will execute until interrupted
            sys.stdout.write(next(self.loadingGenerator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        '''
            A magic method to help use the `with` helper
        '''
        self.isBusy = True
        # Create a thread with the spinnerTask
        threading.Thread(target=self.loadingTask).start()

    def __exit__(self, exception, value, tb):
        '''
            Once the with code block has exeucted, exit
            Interrupting the threaed
        '''
        self.isBusy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

def execute_step(processList, errorMessage: str):
    '''
        Check process evaluates the CompletedProcess object from subprocess.run

        Args:
            completedProcess (CompletedProcess): The completed output from subprocess.run
            errorMessage (str): The error string to return
    '''
    with Loader(delay=0.2):
        completedProcess = subprocess.run(processList, capture_output=True)
    # Zero return code indicates success
    if completedProcess.returncode == 0:
        print("--\t[OK]")
        return
    # If not we have a failure so pass the stderr data
    print("--\t[Failed]")
    stdout = b'' if completedProcess.stdout is None else completedProcess.stdout
    stderr = b'' if completedProcess.stderr is None else completedProcess.stderr
    print("--\t[Debug]")
    for line in stdout.decode("utf-8").split("\n"):
        if not line:
            continue
        print("--\t[Debug] " + line)
    print("--\t[Error]")
    for line in stderr.decode("utf-8").split("\n"):
        if not line:
            continue
        print("--\t[Error] " + line)
    print("--\t[Ensure you are in the right directory]")
    exit()

# def get_options(args, *definitions):
#     options, remainder = getopt.getopt(
#         args,
#         ':'.join(o.getShort() for o in definitions),
#     )
#
# class Option:
#     def __init__(self, short, long):
#         self.short = short
#         self.long = long
#
#     def getShort(self):
#         return self.short
#
#     def getLong(self):
#         return self.long
