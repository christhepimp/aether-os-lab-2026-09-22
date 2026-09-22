# Replacing Linux — the honest map

"Replace Linux with an AI OS" is three different jobs. Do not mix them.

## Job 1 — Replace the *interface* (do this first)

The OS is whatever you talk to. If Aether is the only prompt, Aether *is* the OS
for you, even while Linux still schedules threads.

Deliverable in this repo: `python3 -m aether.cli`

## Job 2 — Replace *userspace* (do this second)

Android userspace = init, zygote, system_server, binders, surfaceflinger.
You replace these one daemon at a time with Aether agents that call the same
kernel syscalls.

This is how early Unix was replaced by later Unix: not by burning the kernel.

## Job 3 — Replace the *kernel* (do this last, maybe never)

A kernel must:
- talk to a virtio/goldfish virtual disk, net, GPU
- preempt tasks
- isolate address spaces
- handle interrupts

An LLM cannot do that in Python. If you want a custom kernel, start from Linux,
keep the drivers, and add Aether as a supervisor (seccomp, LSM, eBPF, KernelSU).
Writing a from-scratch kernel that boots on the Android emulator is a separate
repo and a separate decade.

## Why we start on an Android emulator

The emulator already gives you:
- a Linux kernel you can GDB
- root when you ask for it
- snapshots
- no bricked hardware

That is the right sandbox for Job 1 and Job 2.
