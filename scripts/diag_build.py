# Wrapper для сборки в среде с заблокированным loopback TCP:
# генератор уроков исполняет тесты с asyncio.run, а Windows-эмуляция
# socket.socketpair (self-pipe event loop) зависает без сети.
import asyncio, socket

class _DummySock:
    def sendto(self, *a, **k): pass
    def send(self, *a, **k): pass
    def recv(self, *a, **k): return b'\x00'
    def setblocking(self, *a, **k): pass
    def close(self, *a, **k): pass
    def fileno(self): return -1

def _fake_make_self_pipe(self):
    self._csock = _DummySock()
    self._ssock = _DummySock()
    self._internal_fds = False

asyncio.proactor_events.BaseProactorEventLoop._make_self_pipe = _fake_make_self_pipe
asyncio.proactor_events.BaseProactorEventLoop._loop_self_reading = lambda self: None

exec(open(r'C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\assemble_academy.py', encoding='utf-8').read())
