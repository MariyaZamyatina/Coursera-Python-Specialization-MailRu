# Синхронизация потоков, блокировки
# dead lock

import threading


a = threading.RLock()
b = threading.RLock()


def foo():
    try:
        # захватить блокировку
        a.acquire()
        b.acquire()
    finally:
        # освободить блокировку
        # неправильная последовательность освобождения
        # лучше использовать контекстный менеджер
        a.release()
        b.release()
