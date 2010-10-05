#!/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2010 José de Paula Eufrásio Júnior <jose.junior@gmail.com>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import signal
import curses
import datetime
from curses import panel

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
    loads = [1, 4, 40]
    for load in loads:
        load = float(load)
        too_big = False
        if load > n_cpus * load_multiplier:
            too_big = True
            true_load = load
            load = n_cpus * load_multiplier
        if load <= n_cpus:
            prop = float(load) / n_cpus
            squares = prop * half_screen
            w_load.hline(initial_line,1,chr(219),int(squares))
            initial_line +=1
        elif load > n_cpus:
            prop = (float(load)) / (n_cpus * load_multiplier)
            squares = half_screen + (prop * half_screen)
            w_load.hline(initial_line,1,chr(219),int(squares - 2))
            if too_big:
               diff = int(true_load - load)
               end_line = x - (2 + len(str(diff)))
               w_load.addstr(initial_line, end_line, '+' + str(diff), 
                                curses.A_BOLD)
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
    w_header.addstr(1, 1, "Time:")
    w_header.addstr(1, 16, "Hostname:")
    w_header.addstr(2, 1, "Load Average:")
    w_header.addstr(1, 26, os.uname()[1], curses.A_BOLD)
    w_header.addstr(1, 7, str(datetime.datetime.now().strftime('%H:%M:%S')), 
                    curses.A_BOLD)
    w_header.addstr(2, 15, load, curses.A_BOLD)
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
    scr.timeout(int(delay) * 1000) # more responsive feeling than time.sleep
    curses.curs_set(0)
    scr.addstr(10,1, "Press: 'q' to exit.", curses.A_BOLD)
    w_header = curses.newwin(4, 0, 0, 0)
    w_load = curses.newwin(6,0,4,0)
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
    curses.endwin()

signal.signal(signal.SIGWINCH, signal.SIG_IGN)
curses.wrapper(main)
