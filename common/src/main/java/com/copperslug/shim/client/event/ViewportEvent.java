package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.client.Camera;

public class ViewportEvent extends Event {
    public static class ComputeCameraAngles extends ViewportEvent {
        private final Camera cam;
        private final double pt;
        private float yaw, pitch, roll;

        public ComputeCameraAngles(Camera cam, double pt, float yaw, float pitch, float roll) {
            this.cam = cam;
            this.pt = pt;
            this.yaw = yaw;
            this.pitch = pitch;
            this.roll = roll;
        }

        public Camera getCamera() {
            return cam;
        }

        public double getPartialTick() {
            return pt;
        }

        public float getYaw() {
            return yaw;
        }

        public void setYaw(float v) {
            yaw = v;
        }

        public float getPitch() {
            return pitch;
        }

        public void setPitch(float v) {
            pitch = v;
        }

        public float getRoll() {
            return roll;
        }

        public void setRoll(float v) {
            roll = v;
        }
    }
}
