#!/bin/env python

import os
import sys
import time
import signal
import curses
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

def update_screen(scr):
    scr_y, scr_x = scr.getmaxyx()
    scr.addstr(10, 20, "%s, %s" % (scr_x, scr_y))
    load_avg = get_load()
    scr.addstr(1, 15, get_load())
    scr.addstr(2, 17, str(get_cpus()))
    scr.addstr(2, 17, str(get_cpus()))
    scr.addstr(3, 8, str(delay))
    scr.addstr(5, 1, draw_load(scr, 2, get_cpus()))
    scr.refresh()

def main(stdscr, **kwargs):
    scr = stdscr
    scr_y, scr_x = scr.getmaxyx()
    if (scr_x < 40) or (scr_y < 10):
        raise Exception("Minimum terminal size is 40x10")
        sys.exit(2)
    curses.curs_set(0)
    scr.nodelay(1)
    scr.addstr(1, 1, "Load Average:", curses.A_BOLD)
    scr.addstr(2, 1, "Number of CPUS:", curses.A_BOLD)
    scr.addstr(3, 1, "Delay:", curses.A_BOLD)

    while 1:
        ch = scr.getch()
        if ch == ord('q'):
            break
        else:
            update_screen(scr)
            time.sleep(delay)

    curses.endwin()

signal.signal(signal.SIGWINCH, signal.SIG_IGN)
curses.wrapper(main)
