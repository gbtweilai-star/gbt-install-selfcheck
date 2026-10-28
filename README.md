# install_selfcheck

**One capability bit from GBT V8, packaged standalone.** No. 217 of 341,
`security` domain (Security).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> **装机自检 · 查病毒木马/后门**（主人 2026-10-17 令「安装上我们的大模型就自动自检一遍排除病毒木马等」）：按 **OS 结构**做只读检查 —— Windows(Run/RunOnce 自启键·计划任务·服务·Winlogon·监听端口·PE 头) · Linux(cron/systemd/rc.local/ld.so.preload·ELF·setuid) · macOS(LaunchAgents/Daemons·Gatekeeper/隔离位·SIP·Mach-O)；跨平台戳危险特征（powershell -enc·mshta 远程·certutil-urlcache·bitsadmin·curl|bash·base64 执行·反连 shell）· 双扩展名/伪装脚本/隐藏可执行；模型文件复核 sha manifest。**只读**：命中≠定罪，不擅自杀/删，给人工复核与建议。op=status/scan/persistence/plan/where

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-install-selfcheck.git
cd gbt-install-selfcheck
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_install_selfcheck info                  # capability card
python -m gbt_install_selfcheck spec --json           # machine-readable contract
python -m gbt_install_selfcheck check --payload '{}'
python -m gbt_install_selfcheck run   --payload '{}'
```

Real `info` output from this machine:

```text
install_selfcheck  (security)  v1.0.0
----------------------------------------
**装机自检 · 查病毒木马/后门**（主人 2026-10-17 令「安装上我们的大模型就自动自检一遍排除病毒木马等」）：按 **OS 结构**做只读检查 —— Windows(Run/RunOnce 自启键·计划任务·服务·Winlogon·监听端口·PE 头) · Linux(cron/systemd/rc.local/ld.so.preload·ELF·setuid) · macOS(LaunchAgents/Daemons·Gatekeeper/隔离位·SIP·Mach-O)；跨平台戳危险特征（powershell -enc·mshta 远程·certutil-urlcache·bitsadmin·curl|bash·base64 执行·反连 shell）· 双扩展名/伪装脚本/隐藏可执行；模型文件复核 sha manifest。**只读**：命中≠定罪，不擅自杀/删，给人工复核与建议。op=status/scan/persistence/plan/where

gated      : False
external   : False
multi-op   : True
params     : (none)
values     : cron, systemd, rc
```

Wire a real implementation:

```python
from gbt_install_selfcheck import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（3 个）**：`cron`、`systemd`、`rc`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Not gated: the registry marks this bit `safe: true`.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `install_selfcheck` |
| domain | `security` |
| handler | `install_selfcheck` |
| safe | `True` (gated = `False`) |
| external | `False` |
| atlas page | [security/install_selfcheck](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/security/install_selfcheck.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
