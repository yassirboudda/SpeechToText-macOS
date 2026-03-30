"""Settings dialog using tkinter (macOS)."""

import tkinter as tk
from tkinter import ttk
import threading


def show_settings(app):
    """Show the settings window."""
    win = tk.Toplevel() if tk._default_root else tk.Tk()
    win.title('SpeechToText — Settings')
    win.geometry('460x320')
    win.resizable(False, False)
    win.configure(bg='#1e1e2e')

    # Force focus
    win.attributes('-topmost', True)
    win.lift()
    win.focus_force()

    key_tested = [bool(app.api_key)]
    testing = [False]

    # ── Header ──
    tk.Label(win, text='⚙  Settings', font=('Helvetica', 16, 'bold'),
             bg='#1e1e2e', fg='#cdd6f4').pack(pady=(16, 8))
    ttk.Separator(win).pack(fill='x', padx=20)

    # ── API Key ──
    tk.Label(win, text='Mistral API Key', font=('Helvetica', 11, 'bold'),
             bg='#1e1e2e', fg='#a6adc8', anchor='w').pack(fill='x', padx=20, pady=(12, 4))

    key_frame = tk.Frame(win, bg='#1e1e2e')
    key_frame.pack(fill='x', padx=20)

    key_var = tk.StringVar(value=app.api_key or '')
    key_entry = tk.Entry(key_frame, textvariable=key_var, show='•',
                         font=('Helvetica', 12), bg='#181825', fg='#cdd6f4',
                         insertbackground='#cdd6f4', relief='flat', bd=6)
    key_entry.pack(side='left', fill='x', expand=True)

    show_var = tk.BooleanVar(value=False)

    def toggle_show():
        key_entry.config(show='' if show_var.get() else '•')

    show_btn = tk.Checkbutton(key_frame, text='👁', variable=show_var,
                               command=toggle_show, bg='#313244', fg='#a6adc8',
                               selectcolor='#7c3aed', relief='flat', bd=2,
                               font=('Helvetica', 12))
    show_btn.pack(side='right', padx=(4, 0))

    # ── Test row ──
    test_frame = tk.Frame(win, bg='#1e1e2e')
    test_frame.pack(fill='x', padx=20, pady=(6, 0))

    test_status = tk.Label(test_frame, text='', font=('Helvetica', 10),
                           bg='#1e1e2e', fg='#6c7086', anchor='w')

    def on_key_change(*args):
        key_tested[0] = False
        test_status.config(text='')
        save_btn.config(state='disabled')

    key_var.trace_add('write', on_key_change)

    def do_test():
        key = key_var.get().strip()
        if not key:
            test_status.config(text='Enter an API key first', fg='#f38ba8')
            return
        if testing[0]:
            return
        testing[0] = True
        test_btn.config(state='disabled')
        test_status.config(text='Testing…', fg='#a6adc8')

        def bg():
            from speechtotext.transcriber import test_api_key
            ok, error = test_api_key(key)
            win.after(0, lambda: on_result(ok, error))

        def on_result(ok, error):
            testing[0] = False
            test_btn.config(state='normal')
            if ok:
                key_tested[0] = True
                test_status.config(text='✓ API key is valid', fg='#a6e3a1')
                save_btn.config(state='normal')
            else:
                key_tested[0] = False
                test_status.config(text=f'✗ {error}', fg='#f38ba8')
                save_btn.config(state='disabled')

        threading.Thread(target=bg, daemon=True).start()

    test_btn = tk.Button(test_frame, text='🔍 Test Key', command=do_test,
                         bg='#313244', fg='#a78bfa', relief='flat', bd=4,
                         font=('Helvetica', 11, 'bold'), cursor='hand2')
    test_btn.pack(side='left')
    test_status.pack(side='left', padx=(10, 0), fill='x', expand=True)

    # ── Separator ──
    ttk.Separator(win).pack(fill='x', padx=20, pady=(12, 0))

    # ── Auto type toggle ──
    tk.Label(win, text='Behavior', font=('Helvetica', 11, 'bold'),
             bg='#1e1e2e', fg='#a6adc8', anchor='w').pack(fill='x', padx=20, pady=(8, 4))

    auto_frame = tk.Frame(win, bg='#1e1e2e')
    auto_frame.pack(fill='x', padx=20)

    tk.Label(auto_frame, text='Auto "Type at Cursor" after transcription',
             bg='#1e1e2e', fg='#cdd6f4', font=('Helvetica', 11),
             anchor='w').pack(side='left', fill='x', expand=True)

    auto_var = tk.BooleanVar(value=app.auto_type)
    auto_check = tk.Checkbutton(auto_frame, variable=auto_var,
                                 bg='#1e1e2e', selectcolor='#7c3aed',
                                 activebackground='#1e1e2e')
    auto_check.pack(side='right')

    # ── Buttons ──
    btn_frame = tk.Frame(win, bg='#1e1e2e')
    btn_frame.pack(fill='x', padx=20, pady=(16, 16), side='bottom')

    def on_save():
        app.apply_settings(key_var.get().strip(), auto_var.get())
        win.destroy()

    def on_cancel():
        win.destroy()

    tk.Button(btn_frame, text='Cancel', command=on_cancel,
              bg='#313244', fg='#a78bfa', relief='flat', bd=4,
              font=('Helvetica', 11, 'bold'), cursor='hand2',
              width=12).pack(side='left', expand=True, padx=(0, 5))

    save_btn = tk.Button(btn_frame, text='💾 Save', command=on_save,
                         bg='#7c3aed', fg='white', relief='flat', bd=4,
                         font=('Helvetica', 11, 'bold'), cursor='hand2',
                         width=12,
                         state='normal' if key_tested[0] else 'disabled')
    save_btn.pack(side='right', expand=True, padx=(5, 0))

    # Allow save if key is unchanged
    if app.api_key and key_var.get().strip() == app.api_key:
        save_btn.config(state='normal')

    win.mainloop() if not tk._default_root else None
