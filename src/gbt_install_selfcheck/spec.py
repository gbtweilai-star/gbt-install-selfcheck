"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "install_selfcheck",
 "domain": "security",
 "desc": "**装机自检 · 查病毒木马/后门**（主人 2026-10-17 令「安装上我们的大模型就自动自检一遍排除病毒木马等」）：按 **OS 结构**做只读检查 —— Windows(Run/RunOnce 自启键·计划任务·服务·Winlogon·监听端口·PE 头) · Linux(cron/systemd/rc.local/ld.so.preload·ELF·setuid) · macOS(LaunchAgents/Daemons·Gatekeeper/隔离位·SIP·Mach-O)；跨平台戳危险特征（powershell -enc·mshta 远程·certutil-urlcache·bitsadmin·curl|bash·base64 执行·反连 shell）· 双扩展名/伪装脚本/隐藏可执行；模型文件复核 sha manifest。**只读**：命中≠定罪，不擅自杀/删，给人工复核与建议。op=status/scan/persistence/plan/where",
 "handler": "install_selfcheck",
 "safe": true,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": true,
 "ops": [
  "cron",
  "systemd",
  "rc"
 ],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
