"""Golden folder G1 (recording-files/SPEC.md Appendix A): a capture-only take, in the cases `take` and `confirmed_key`.

Each value of this file is synthetic. The cameras and the audio follow one list of events: a click
and a flash each 500 ms. The fit of each file is the ground truth that made its rows.
"""

from __future__ import annotations

from pathlib import Path

from goldgen import common

TAKE = {
    "rec": "g01_synthetic_take",
    "take_uuid": "00000000000040008000000000000001",
    "take_start_host_ns": 1_000_000_000_000,
    "take_start_utc_ns": 946_684_800_000_000_000,  # 2000-01-01T00:00:00Z
    "utc_offset_min": 0,
    "clock": "windows_qpc",
    "clock_hz": 10_000_000,
}
FRAMES = 90
EVENTS_NS = [100_000_000 + j * 500_000_000 for j in range(6)]
MAX_EVENT_ERROR_NS = 1_000_000  # SFT-729

AUDIO_T0_NS, AUDIO_PERIOD_FS = 12_345_678, 20_833_350_000
BLOCK_SAMPLES, BLOCKS = 4800, 30


def _camera(index: int, t0_ns: int, period_ps: int, first_source: int, dropped: int | None, **config) -> dict:
    """A camera with its frames on the lattice t0_ns + d * period_ps. `dropped` is a step with no frame."""
    steps = [d for d in range(FRAMES + (dropped is not None)) if d != dropped]
    fitted = [common.video_fitted_ns(t0_ns, period_ps, d) for d in steps]
    flashes = [min(range(FRAMES), key=lambda p: abs(fitted[p] - event)) for event in EVENTS_NS]
    assert all(abs(fitted[p] - event) < MAX_EVENT_ERROR_NS for p, event in zip(flashes, EVENTS_NS))
    rows = [
        (
            first_source + d,
            t + 4_000_000 + p * 104_729 % 1_000_003,  # the frame arrives 4 ms to 5 ms after its fitted time
            t + p * 7_919 % 100_001 - 50_000 if index == 0 else None,  # only camera 0 has a driver time
        )
        for p, (d, t) in enumerate(zip(steps, fitted))
    ]
    return config | {
        "rate": (30, 1), "width": 64, "height": 48, "display_rotation": 0, "shade": 40 * index,
        "t0_ns": t0_ns, "period_ps": period_ps, "flash_positions": flashes, "rows": rows,
        "requested": {
            "width": 64, "height": 48, "framerate": 30, "capture_format": "MJPG", "exposure_mode": "manual",
        },
        "exposure_step": None,
    }  # fmt: skip


def _device(index: int, serial: str | None, os_device_id: str | None) -> dict:
    return {
        "model": f"Synthetic Camera Model {index}",
        "os_name": f"Synthetic Camera {index}",
        "vendor_id": "ffff",
        "product_id": f"000{index + 1}",
        "serial": serial,
        "port_path": f"FAKE-PORT-{index}",
        "os_device_id": os_device_id,
        "backend": "media_foundation",
        "os_index": index,
    }


def cameras() -> list[dict]:
    # Camera 0 has a usable serial (form 1 of SFF-752). Camera 1 has none, so its key has the port
    # form (form 2), although it also has an OS device identifier (form 3).
    return [
        _camera(
            0, 33_483_200, 33_333_400_000, 1000, None,
            camera_key=common.camera_key("ffff:0001:serial:FAKE-SERIAL-A"),
            user_name="Fake camera A",
            key_origin="computed",
            device=_device(0, "FAKE-SERIAL-A", None),
            controls={"exposure_us": {"value": 4000, "auto": False}, "gain": {"value": 32, "auto": False}},
        ),
        _camera(
            1, 33_133_500, 33_333_250_000, 500, 40,
            camera_key=common.camera_key("ffff:0002:port:FAKE-PORT-1"),
            user_name=None,
            key_origin="computed",
            device=_device(1, None, "FAKE-OS-DEVICE-1"),
            controls={"exposure_us": {"value": None, "auto": None}},
        ),
    ]  # fmt: skip


def audio() -> dict:
    def fitted(n: int) -> int:
        return common.audio_fitted_ns(AUDIO_T0_NS, AUDIO_PERIOD_FS, 0, n)

    clicks = [round((event - AUDIO_T0_NS) * 10**6 / AUDIO_PERIOD_FS) for event in EVENTS_NS]
    assert all(abs(fitted(n) - event) < MAX_EVENT_ERROR_NS for n, event in zip(clicks, EVENTS_NS))
    return {
        "config": {"device_name": "Synthetic Microphone", "host_api": "Windows WASAPI", "device_channels": 1},
        "t0_ns": AUDIO_T0_NS,
        "period_fs": AUDIO_PERIOD_FS,
        "click_samples": clicks,
        "rows": [
            (
                b * BLOCK_SAMPLES,
                BLOCK_SAMPLES,
                fitted((b + 1) * BLOCK_SAMPLES) + 2_000_000 + b * 7_919 % 500_009,  # after the last sample
                fitted(b * BLOCK_SAMPLES) + b * 31 % 2_001 - 1_000,
            )
            for b in range(BLOCKS)
        ],
    }


def build(out: Path) -> None:
    """Write the two cases of G1 into `out`, each with its two expected results and its truth file."""
    confirmed = cameras()
    # The user confirmed camera 1 after a move from another port. It keeps the key of the old port.
    confirmed[1] |= {"camera_key": common.camera_key("ffff:0002:port:FAKE-PORT-9"), "key_origin": "confirmed_by_user"}
    for case, case_cameras in (("take", cameras()), ("confirmed_key", confirmed)):
        case_audio = audio()
        facts = common.write_take(out / case, TAKE, case_cameras, case_audio)
        for scope in ("full", "player"):
            result = common.expected_result(facts, scope)
            (out / f"{case}.{scope}.json").write_bytes(common.canonical_json(result))
        truth = {
            "audio": {"name": facts["files"][-1]["name"], "click_samples": case_audio["click_samples"]},
            "cameras": [
                {"name": item["name"], "flash_positions": camera["flash_positions"]}
                for item, camera in zip(facts["files"], case_cameras)
            ],
        }
        (out / f"{case}.truth.json").write_bytes(common.canonical_json(truth))
