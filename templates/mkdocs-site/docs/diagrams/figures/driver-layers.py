"""The three layers of a HardFOC driver: hardware-agnostic core, communication interface, platform port.

Reads: From top to bottom. The application calls the driver object. The driver turns each call into register or
command transactions and never touches the hardware itself. The communication interface is the small set of
methods the driver calls (transfer, GPIO, delay). The platform port implements them with the MCU's SDK. Below it
is the chip. A repository replaces this hand-placed figure with one whose data() reads the real class and method
names from its headers.
"""

from hardfoc_mkdocs_theme.figkit import Fig


def build(_data):
    f = Fig(
        "driver-layers",
        "Three layers, one of them yours",
        alt="Layer diagram: the application calls the hardware-agnostic driver, which calls the communication "
        "interface, which the platform port implements with the MCU's SDK, which talks to the chip.",
        width=1200,
        kicker="Architecture",
        subtitle="The driver and the interface are the same on every MCU; the port is a small class.",
        profile="overview",
        legend=[("brand", "this library"), ("teal", "you write"), ("slate", "hardware")],
    )
    W = f.body_w
    app = f.card(0, 0, W, "Your application", ["control loop, state machine, CLI"], tone="slate")
    core = f.card(0, app.b + 40, W, "Hardware-agnostic core", ["Driver<Comm>: configure, read, write, errors"],
                  tone="brand", accent=True)
    comm = f.card(0, core.b + 40, W, "Communication interface", ["transfer(), gpioSet(), delayUs()"],
                  tone="brand", mono=True)
    port = f.card(0, comm.b + 40, W, "Platform port (your class)", ["ESP-IDF, STM32 HAL, Zephyr, Linux"],
                  tone="teal", accent=True)
    chip = f.card(0, port.b + 40, W, "The chip", ["SPI / I2C / UART and control pins"], tone="slate")
    for a, b in ((app, core), (core, comm), (comm, port), (port, chip)):
        f.connect(a, b, "bottom", "top", tone="rail")
    return f
