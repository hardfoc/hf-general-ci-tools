# Examples

The example applications, what each one shows and how to build it.

<!-- Write this page to docs/DOCS-STYLE-GUIDE.md (page "Examples"). -->

## The apps

<!-- generated: examples -->
| App | What it shows | Source | CI |
| --- | --- | --- | --- |
| `basic` :material-star:{ title="featured" } | Smallest example: initialise, read, print | [`basic.cpp`](../examples/esp32/main/basic.cpp) | yes |

Build and flash one (from `examples/esp32`, ESP-IDF environment loaded):

```bash
./scripts/build_app.sh basic Release
./scripts/flash_app.sh flash_monitor basic Release
```

Source of this table: [`examples/esp32/app_config.yml`](../examples/esp32/app_config.yml).
<!-- /generated -->
