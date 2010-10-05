#!/bin/env python

import os
import sys
import time
import signal
import curses
import datetime
from curses import panel
# devel
import inspect

delay = 2.0
load_multiplier = 2

def get_load():
    raw_load = open('/proc/loadavg').readline()
    load = ', '.join(raw_load.split()[:3])
    return load

def get_cpus():
    cpus = 0
    for line in open('/proc/cpuinfo'):
        if line.strip().startswith('processor'):
            cpus += 1
    return cpus

def draw_load(scr, load, n_cpus):
    y, x = scr.getmaxyx()
    half_screen = x / 2
    prop = float(load) / n_cpus
    if load <= n_cpus:
        squares = prop * half_screen
    return '#'*int(squares)

def check_screen_size(x, y):
    if (x < 40) or (y < 10):
        raise Exception("Minimum terminal size is 40x10")
        sys.exit(2)

def update_header(p_header):
    w_header = p_header.window()
    w_header.erase()
    w_header.box()
    w_header.addstr(1, 1, "Load Average:", curses.A_BOLD)
    w_header.addstr(2, 1, "Number of CPUs:", curses.A_BOLD)
    w_header.addstr(3, 1, "Time:", curses.A_BOLD)
    w_header.addstr(1, 15, get_load())
    w_header.addstr(2, 17, str(get_cpus()))
    w_header.addstr(3, 8, str(datetime.datetime.now()))
    update_screen()

def update_screen():
    panel.update_panels()
    curses.doupdate()

def update_load(p_load):
    w_load = p_load.window()
    w_load.erase()
    w_load.box()
    update_screen()

def main(stdscr):
    scr = stdscr
    scr.nodelay(0)
    curses.curs_set(0)
    w_header = curses.newwin(5, 0, 0, 0)
    w_load = curses.newwin(0,0,5,0)
    p_header = panel.new_panel(w_header)
    p_load = panel.new_panel(w_load)
    update_header(p_header)
    update_load(p_load)
    while 1:
        ch = scr.getch()
        if ch == ord('q'):
            break
        else:
            y, x = scr.getmaxyx()
            check_screen_size(x, y)
            update_header(p_header)
            update_load(p_load)
            time.sleep(delay)
    curses.endwin()

signal.signal(signal.SIGWINCH, signal.SIG_IGN)
curses.wrapper(main)
