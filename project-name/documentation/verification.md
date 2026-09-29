# Verification

- Node asset tests pass for sixteen original scoped GLBs and four rendered portraits.
- Production Vite build passes using the repository Pages subpath.
- Chrome WebGPU browser playthrough: two independent clients, duplicate Valkyries, unique colored rings/labels, keyboard movement, focus release and local pause.
- Complete level through keyboard only: all altars, key, victory, then replay.
- Natural defeat, replay, offline disconnect/retry, unsupported WebGPU message.
- 390x844 mobile emulation: no horizontal overflow, joystick, concurrent attack, touch release and cancellation. Physical touch hardware untested.
- Shared backend v0.5.0: 15 regression tests and live production integration checks pass. See server verification record.
- Screenshots are captured from the actual runtime. The visual target is separately labeled conceptual artwork.

## Public release evidence

- Release v0.0.3 targets f7c0c88e8efd58c47cd4c2c54647b747a332de51.
- Release workflow: https://github.com/SamuelAsherRivello/babylon-lite-gauntlet-clone-3d/actions/runs/36613779302
- Pages deployment: https://github.com/SamuelAsherRivello/babylon-lite-gauntlet-clone-3d/actions/runs/36613843700
- Public version.txt and rendered HUD both show 0.0.3.
- Two public clients joined, switched through all four classes, and shared duplicate wizard/valkyrie identities with distinct colors.

Public full-level keyboard playthrough, victory, restart and mobile emulation also passed with zero uncaught browser errors. browser-verification.json records the public URL and timestamp.
