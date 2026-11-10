package com.copperslug.shim.fml.event.lifecycle;

import com.copperslug.shim.eventbus.api.Event;

/** Arranque del cliente (con los registros ya cerrados). enqueueWork lo hace en el momento: ya va en el hilo principal. */
public class FMLClientSetupEvent extends Event {
    public void enqueueWork(Runnable r) {
        r.run();
    }
}
