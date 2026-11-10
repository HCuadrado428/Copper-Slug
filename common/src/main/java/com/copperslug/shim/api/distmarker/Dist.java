package com.copperslug.shim.api.distmarker;

public enum Dist {
    CLIENT, DEDICATED_SERVER;

    public boolean isClient() {
        return this == CLIENT;
    }
}
