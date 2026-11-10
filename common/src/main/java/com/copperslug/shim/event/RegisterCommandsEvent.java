package com.copperslug.shim.event;

import com.copperslug.shim.eventbus.api.Event;
import com.mojang.brigadier.CommandDispatcher;
import net.minecraft.commands.CommandBuildContext;
import net.minecraft.commands.CommandSourceStack;

public class RegisterCommandsEvent extends Event {
    private final CommandDispatcher<CommandSourceStack> d;
    private final CommandBuildContext ctx;

    public RegisterCommandsEvent(CommandDispatcher<CommandSourceStack> d, CommandBuildContext ctx) {
        this.d = d;
        this.ctx = ctx;
    }

    public CommandDispatcher<CommandSourceStack> getDispatcher() {
        return d;
    }

    public CommandBuildContext getBuildContext() {
        return ctx;
    }
}
