import shutil
import sys
from pathlib import Path

loader, bundle = map(Path, sys.argv[1:3])
base = 'https://github.com/Wolfkid200444/revenge-manager/releases/download/runtime-latest'
p = loader / 'app/src/main/kotlin/io/github/revenge/xposed/tweaks/RevengeUpdater.kt'
s = p.read_text()
old = 'val customLoadUrl: CustomLoadUrl = CustomLoadUrl(),'
assert s.count(old) == 1, 'Loader configuration changed upstream'
s = s.replace(old, f'val customLoadUrl: CustomLoadUrl = CustomLoadUrl(enabled = true, url = "{base}/revenge.bundle", manifestUrl = "{base}/manifest.json"),')
p.write_text(s)
p = loader / 'app/src/main/kotlin/io/github/revenge/xposed/tweaks/RevengeScriptLoader.kt'
s = p.read_text()
assert s.count('if (mainScript.exists())') == 1
p.write_text(s.replace('if (mainScript.exists())', 'if (mainScript.exists() && mainScript.length() > 0)'))
assets = loader / 'app/src/main/assets'
for name in ['revenge.bundle', 'manifest.json']:
    source = bundle / name
    assert source.stat().st_size > 0, f'Empty bundle asset: {name}'
    shutil.copyfile(source, assets / name)
print('Configured hosted updates and embedded fallback bundle')
