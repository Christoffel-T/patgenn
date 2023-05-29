from classes import *
import threading
import psutil
import subprocess

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        Variables.Misc.state_break = True
        try:
            root.destroy()
            print('FloatingText_closed')
        except:
            print('error')
            sys.exit()

for proc in psutil.process_iter(['name']):
    if proc.name() == 'chrome.exe':
        # Show message box
        messagebox.showinfo('Message', 'Cannot run this script because Google Chrome is running. '
                                       'Please close Google Chrome to run this script.'
                                       '\n(Check also in the Task Manager)')
        print('Chrome is running.')
        sys.exit()

subprocess.Popen(['start', 'cmd', '/k', 'python', 'gsheets_upload.py'], shell=True)
Variables.Misc.state_break = False
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
ft = FloatingText(root)

ft.update_text(f'Initializing...\nPlease restart the script if this process took too long to complete.')
mainfunction = MainFunction(floating_text_obj=ft, root=root)
thread = threading.Thread(target=mainfunction.f_main1())
thread.start()
root.mainloop()
thread.join()
time.sleep(0.5)
# input('\nPress [Enter] to exit the script. \nWARNING: This will also close the Chrome browser window. So please make sure you are done with the websites before exiting.\n')
mainfunction.driver.quit()
sys.exit()
