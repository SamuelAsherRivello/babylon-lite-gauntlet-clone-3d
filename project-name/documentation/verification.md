# Verification

- Node asset tests pass for sixteen original scoped GLBs and four rendered portraits.
- Production Vite build passes using the repository Pages subpath.
- Chrome WebGPU browser playthrough: two independent clients, duplicate Valkyries, unique colored rings/labels, keyboard movement, focus release and local pause.
- Complete level through keyboard only: all altars, key, victory, then replay.
- Natural defeat, replay, offline disconnect/retry, unsupported WebGPU message.
- 390x844 mobile emulation: no horizontal overflow, joystick, concurrent attack, touch release and cancellation. Physical touch hardware untested.
- Shared backend v0.5.0: 15 regression tests and live production integration checks pass. See server verification record.
- Screenshots are captured from the actual runtime. The visual target is separately labeled conceptual artwork.
