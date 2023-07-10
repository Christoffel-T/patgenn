from classes import *

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        Variables.Misc.state_break = True
        try:
            root.destroy()
            print('FloatingText_closed')
        except:
            print('error')
            sys.exit()

Variables.Misc.state_break = False
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
ft = FloatingText(root)

ft.update_text(f'Initializing...\nPlease restart the script if this process took too long to complete.')
mainfunction = MainFunction(floating_text_obj=ft, root=root)

mainfunction.f_open_chrome()
for i in range(3):
    mainfunction.f_open_position(direction='SHORT', full=False)
    time.sleep(1)