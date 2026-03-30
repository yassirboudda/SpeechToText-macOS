"""Visual editor window using tkinter (macOS)."""

import tkinter as tk
import subprocess


def show_editor(app):
    """Show the visual editor window."""
    win = tk.Toplevel() if tk._default_root else tk.Tk()
    win.title('SpeechToText — Editor')
    win.geometry('420x400')
    win.resizable(True, True)
    win.configure(bg='#1e1e2e')
    win.attributes('-topmost', True)
    win.lift()

    # ── Header ──
    tk.Label(win, text='🎤  Transcription Editor', font=('Helvetica', 16, 'bold'),
             bg='#1e1e2e', fg='#cdd6f4').pack(pady=(16, 8))

    # ── Text area ──
    text_frame = tk.Frame(win, bg='#313244', bd=1)
    text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 6))

    text_widget = tk.Text(text_frame, wrap='word', font=('Helvetica', 13),
                          bg='#181825', fg='#cdd6f4', insertbackground='#cdd6f4',
                          relief='flat', bd=8, undo=True)
    text_widget.pack(fill='both', expand=True)
    text_widget.insert('1.0', app.transcription or '')

    scrollbar = tk.Scrollbar(text_widget, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    def sync_back(*args):
        text = text_widget.get('1.0', 'end-1c').strip()
        app.update_transcription_from_editor(text)

    text_widget.bind('<<Modified>>', lambda e: (sync_back(), text_widget.edit_modified(False)))

    # ── Status ──
    status_var = tk.StringVar(value='Edit transcription text above')
    tk.Label(win, textvariable=status_var, font=('Helvetica', 10),
             bg='#1e1e2e', fg='#6c7086', anchor='w').pack(fill='x', padx=20)

    # ── Buttons ──
    btn_frame = tk.Frame(win, bg='#1e1e2e')
    btn_frame.pack(fill='x', padx=20, pady=(6, 16))

    def on_copy():
        text = text_widget.get('1.0', 'end-1c').strip()
        if text:
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            status_var.set('Copied to clipboard!')
        else:
            status_var.set('Nothing to copy')

    def on_type():
        text = text_widget.get('1.0', 'end-1c').strip()
        if not text:
            status_var.set('Nothing to type')
            return
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        win.withdraw()
        win.after(700, lambda: _paste_and_show(win))

    def _paste_and_show(w):
        script = 'tell application "System Events" to keystroke "v" using command down'
        subprocess.run(['osascript', '-e', script], timeout=5, check=False)

    def on_delete():
        text_widget.delete('1.0', 'end')
        app.update_transcription_from_editor('')
        status_var.set('Transcription deleted')

    tk.Button(btn_frame, text='📋 Copy', command=on_copy,
              bg='#313244', fg='#a78bfa', relief='flat', bd=4,
              font=('Helvetica', 11, 'bold'), cursor='hand2').pack(side='left', expand=True, fill='x', padx=(0, 4))

    tk.Button(btn_frame, text='⌨ Type at Cursor', command=on_type,
              bg='#7c3aed', fg='white', relief='flat', bd=4,
              font=('Helvetica', 11, 'bold'), cursor='hand2').pack(side='left', expand=True, fill='x', padx=4)

    tk.Button(btn_frame, text='🗑 Delete', command=on_delete,
              bg='#313244', fg='#ef4444', relief='flat', bd=4,
              font=('Helvetica', 11, 'bold'), cursor='hand2').pack(side='left', expand=True, fill='x', padx=(4, 0))

    win.mainloop() if not tk._default_root else None
