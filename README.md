# Aether OS Lab (2026-09-22)

**Goal:** make an operating system that *is* an AI — not an AI app sitting on Android.

**Reality check:** you cannot delete Linux from a running Android emulator and drop in a brand-new kernel in one weekend. Android *is* Linux (Goldfish/Ranchu kernel + userspace). Replacing the kernel is a multi-year systems project. What you *can* do now is take a **rooted emulator**, get a real root shell into that Linux, and grow an **AI control plane** that becomes the OS from the user's point of view: it owns processes, files, permissions, intent, and the shell.

This repo is that lab.

## Architecture

```
You  -->  Aether Kernel (userspace AI)  -->  Android userspace  -->  Linux kernel  -->  QEMU
```

- Phase 0 (this repo): AI userspace kernel on your PC + rooted AVD scripts.
- Phase 1: run Aether inside the emulator as a root daemon.
- Phase 2: Aether is the only shell / launcher you talk to.
- Phase 3: optional KernelSU / custom modules.
- Phase 4: a new kernel. Not this week.

## Rooted emulator (the lab)

Recommended: Android Studio AVD, **Google APIs** image (not Play Store).

```bash
emulator -avd AetherLab -writable-system -qemu -s
adb root && adb remount
```

Play Store images: [AERoot](https://github.com/quarkslab/AERoot) can root `adbd` via the QEMU GDB stub.
Genymotion Desktop: Android 11 and below are pre-rooted; newer images can be rooted in settings.

Gaming emulators (BlueStacks / LDPlayer / Nox) can be rooted but hide the kernel. Bad lab.

Details: [docs/EMULATOR.md](docs/EMULATOR.md) and [docs/REPLACE_LINUX.md](docs/REPLACE_LINUX.md).

## Run Aether on this machine

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 -m aether.cli
```

## License

MIT. Research only.
