# Rooted Android emulator lab

## Why an emulator, not a phone

You can snapshot, wipe, attach GDB to the *guest kernel*, and break things.
A physical phone with a locked bootloader is the wrong lab for kernel work.

## Option A — Android Studio AVD (recommended)

1. Install Android Studio + SDK + emulator.
2. Device Manager → Create Device → Pixel 7 / Pixel 8 class.
3. System image: **Google APIs** x86_64 or arm64. Avoid Play Store if you want `adb root`.
4. AVD name: `AetherLab`.

Launch:

```bash
emulator -avd AetherLab -writable-system -no-snapshot-load
adb wait-for-device
adb root
adb remount
adb shell id
# uid=0(root) gid=0(root)
```

You are now inside the Linux on that machine. Look around:

```bash
adb shell
uname -a
cat /proc/version
ls /sys /proc /dev
ps -A | head
```

That is the Linux we will *cover*, not delete.

### Play Store images (no adb root)

Start the emulator with QEMU's GDB stub:

```bash
emulator -avd AetherLab -qemu -s
```

Then [AERoot](https://github.com/quarkslab/AERoot):

```bash
pip install aeroot
aeroot daemon
# new adb shells are root
```

AERoot patches kernel credential structs in guest RAM through gdb. It is a lab tool, not a product feature.

## Option B — Genymotion Desktop

- Android 5–11 images: pre-rooted.
- Android 12+: toggle Root Access in Advanced Developer Tools (license may be required).
- Connect: `adb connect <ip>:5555` then `adb shell` → `su`.

## Option C — custom kernel + KernelSU (advanced)

Build AOSP common kernel, flash it into an AVD, boot KernelSU. This is how you later add *your* syscalls without throwing Linux away.
See projects such as KernelSU-Next and custom AVD kernel recipes.

## What "replacing Linux" looks like from a root shell

You do **not** `rm -rf /`. You:

1. Install Aether as a root daemon (`/data/local/aether`).
2. Make it the login shell (`adb shell` lands in Aether).
3. Have Aether spawn/kill processes instead of you typing `ps`/`kill`.
4. Later, hide zygote/launcher and let Aether own the UI.
5. Much later, kernel modules.

See REPLACE_LINUX.md.
