import serial
import time
from collections import deque

class LCIScrollDisplay:
    def __init__(self, port: str):
        self.port = port
        self.ser = serial.Serial(port, baudrate=9600, timeout=1)
        self.buffer = [' '] * 40  # Internal buffer for full display (40 characters)
        self.message_active = False  # Track if a message is currently on screen
        self.queue = deque()  # Queue of messages to display

    def write(self, full_text: str):
        """
        Writes a message to the display.
        If a message is already on screen, send a space to position 40 first
        to wrap the cursor back to position 1.
        Then send 39 characters.
        """
        if self.message_active:
            self.ser.write(b' ')
            time.sleep(0.01)

        padded = full_text[:39].ljust(39)
        self.buffer = list(padded)
        self._flush()
        self.message_active = True

    def queue_message(self, message: str):
        """
        Adds a message to the display queue.
        """
        self.queue.append(message)

    def process_queue(self, delay: float = 2.0):
        """
        Displays all messages in the queue with an optional delay between them.
        """
        while self.queue:
            message = self.queue.popleft()
            self.write(message)
            time.sleep(delay)

    def update(self, position: int, text: str):
        """
        Updates the display buffer at a specific position (0–39),
        then re-flushes the display.
        """
        for i, char in enumerate(text):
            if 0 <= position + i < 40:
                self.buffer[position + i] = char
        self._flush()

    def scroll(self, text: str, delay: float = 0.2):
        """
        Scrolls the text across the 40-character FIFO window.
        """
        padded = list(' ' * 40 + text + ' ' * 40)
        for i in range(len(padded) - 39):
            self.buffer = padded[i:i + 40]
            self._flush()
            time.sleep(delay)

    def scroll_file(self, filepath: str, delay: float = 0.2):
        """
        Reads a file and scrolls its contents across the display.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    self.scroll(line.strip(), delay=delay)
        except Exception as e:
            print(f"Error reading file: {e}")

    def clear(self):
        """
        Clears the display buffer and screen.
        """
        self.buffer = [' '] * 40
        self._flush()
        self.message_active = False
        time.sleep(0.05)  # Allow time for display to reset

    def _flush(self):
        self.ser.write(''.join(self.buffer).encode('ascii'))

    def close(self):
        self.ser.write(b' ')  # Force wrap to position 1
        time.sleep(0.01)
        self.ser.close()
