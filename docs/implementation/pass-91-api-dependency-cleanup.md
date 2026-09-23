# Pass 91 — API dependency cleanup

The acquisition audit route now uses the concrete acquisition-event repository through the normal module import boundary. The dynamic import workaround from the first API wiring is removed.
