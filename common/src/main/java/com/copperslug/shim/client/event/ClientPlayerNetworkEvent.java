package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;

public class ClientPlayerNetworkEvent extends Event {
    public static class LoggingOut extends ClientPlayerNetworkEvent {}

    public static class LoggingIn extends ClientPlayerNetworkEvent {}
}
