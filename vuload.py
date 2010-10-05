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

delay = 3.0
load_multiplier = 4

def get_load():
    raw_load = open('/proc/loadavg').readline()
    load = raw_load.split()[:3]
    return load

def get_cpus():
    cpus = 0
    for line in open('/proc/cpuinfo'):
        if line.strip().startswith('processor'):
            cpus += 1
    return cpus

def draw_load(p_load, loads):
    n_cpus = get_cpus()
    w_load = p_load.window()
    y, x = w_load.getmaxyx()
    half_screen = x / 2
    initial_line = 2
    w_load.addstr(1, 1, "0", curses.A_BOLD)
    w_load.addstr(1, half_screen, str(n_cpus), curses.A_BOLD)
    w_load.addstr(1, x - (1 + len(str(n_cpus * load_multiplier))), 
                        str(n_cpus * load_multiplier), curses.A_BOLD)
    for load in loads:
        if float(load) <= n_cpus:
            prop = float(load) / n_cpus
            squares = prop * half_screen
            w_load.hline(initial_line,1,chr(219),int(squares))
            initial_line +=1
        elif float(load) > n_cpus:
            prop = (float(load)) / (n_cpus * load_multiplier)
            squares = half_screen + (prop * half_screen)
            w_load.hline(initial_line,1,chr(219),int(squares - 1))
            initial_line +=1

def check_screen_size(x, y):
    if (x < 40) or (y < 10):
        raise Exception("Minimum terminal size is 40x10")
        sys.exit(2)

def update_header(p_header):
    raw_load = get_load()
    load = ', '.join(raw_load)
    w_header = p_header.window()
    w_header.erase()
    w_header.box()
    w_header.addstr(1, 1, "Load Average:", curses.A_BOLD)
    w_header.addstr(2, 1, "Number of CPUs:", curses.A_BOLD)
    w_header.addstr(3, 1, "Time:", curses.A_BOLD)
    w_header.addstr(1, 15, load)
    w_header.addstr(2, 17, str(get_cpus()))
    w_header.addstr(3, 8, str(datetime.datetime.now()))
    update_screen()

def update_load(p_load):
    w_load = p_load.window()
    w_load.erase()
    w_load.box()
    draw_load(p_load, get_load())
    update_screen()

def update_screen():
    panel.update_panels()
    curses.doupdate()

def main(stdscr):
    scr = stdscr
    scr.nodelay(1)
    curses.curs_set(0)
    w_header = curses.newwin(5, 0, 0, 0)
    w_load = curses.newwin(6,0,5,0)
    p_header = panel.new_panel(w_header)
    p_load = panel.new_panel(w_load)
    update_header(p_header)
    update_load(p_load)
    while 1:
        time.sleep(delay)
        ch = scr.getch()
        if ch == ord('q'):
            break
        else:
            y, x = scr.getmaxyx()
            check_screen_size(x, y)
            update_header(p_header)
            update_load(p_load)
    curses.endwin()

signal.signal(signal.SIGWINCH, signal.SIG_IGN)
curses.wrapper(main)
