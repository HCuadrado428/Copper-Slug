package com.copperslug.shim.eventbus.api;

/** En Copper Slug no hay bus del mod: los registros se cierran solos (DeferredRegister.register no hace nada). */
public interface IEventBus {
    IEventBus NINGUNO = new IEventBus() {};
}
