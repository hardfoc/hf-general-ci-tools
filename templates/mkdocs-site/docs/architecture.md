# Architecture

How the driver is built: hardware-agnostic core, communication interface, platform port.

<!-- Write this page to docs/DOCS-STYLE-GUIDE.md (page "Architecture"). -->

<!-- figure: driver-layers -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="diagrams/driver-layers.dark.svg">
  <img src="diagrams/driver-layers.svg"
    alt="Layer diagram: the application calls the hardware-agnostic driver, which calls the communication
    interface, which the platform port implements with the MCU's SDK, which talks to the chip.">
</picture>
<!-- /figure -->
