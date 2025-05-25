# Bematech Display Driver

Driver for controlling LCI v1.45 USB-based customer displays.

Currently tested working on:

Bematech LD9900UP-GY-CM

There is a 39 character limit when printing single messages to the display, as
printing a 40th character overflows line 2 to line 1, so we print 39 characters,
and on clear we print a 40th character to 'clear' the display.

Scrolling starts at the end of line 2, and wraps back to line 1 on scroll.
