from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from os.path import join, expanduser
import subprocess
from xdo import Xdo


def checkhistory():
    # return bash history in long text
    with open(join(expanduser('~'), '.bash_history'), 'r') as f:
        return f.read()

def copy2clip(txt):
    # Copies text to clipboard
    cmd='echo "'+txt.strip()+'" | xclip -sel c'
    return subprocess.check_call(cmd, shell=True)

def sendkeys(xdo, *keys):
    # send keystrokes for xdo
    for k in keys: xdo.send_keysequence_window(0, k.encode())

class MyCustomCompleter(Completer):
    def __init__(self, data_list):
        self.data_list = data_list
        self.data_dict = dict(data_list)

    def get_completions(self, document, complete_event):
        matches = [name for name in self.data_dict.keys() if document.text in name]
        for m in matches:
            yield Completion(m, 
                start_position=-len(document.text_before_cursor), 
                display = m, display_meta = self.data_dict[m])
        

def main():
    xdo = Xdo()
    
    data_list = checkhistory().split('\n')
    data_list = list(zip(data_list, [ str(i) for i in range(len(data_list))]))

    mycompleter = MyCustomCompleter(data_list)
    answer = prompt('>', completer = mycompleter)
    print('ID: %s' % answer)
    copy2clip(answer)
    sendkeys(xdo, 'ctrl+Shift+v')