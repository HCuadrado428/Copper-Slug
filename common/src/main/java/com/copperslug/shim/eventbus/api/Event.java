package com.copperslug.shim.eventbus.api;

/** Base de los eventos del shim. */
public class Event {
    private boolean cancelado;

    public boolean isCancelable() {
        return false;
    }

    public void setCanceled(boolean c) {
        cancelado = c;
    }

    public boolean isCanceled() {
        return cancelado;
    }
}
