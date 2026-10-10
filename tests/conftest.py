"""Keep tests away from an operator's real registry, key, and head record.

Identity (ADR-0011) and integrity (ADR-0012) read config/agents.json,
config/integrity.key, and env vars. A developer's checkout may have all of
them. Point every test at paths that do not exist unless a test creates them.
"""

import os
import tempfile

_SANDBOX = tempfile.mkdtemp(prefix="ag-tests-")
os.environ["AG_AGENT_REGISTRY"] = os.path.join(_SANDBOX, "agents.json")
os.environ["AG_INTEGRITY_KEY_FILE"] = os.path.join(_SANDBOX, "integrity.key")
for _k in ("AG_INTEGRITY_KEY", "AG_AGENT_TOKEN", "AG_INTEGRITY_HEAD", "AG_APPROVAL", "AG_APPROVAL_TOKEN"):
    os.environ.pop(_k, None)
