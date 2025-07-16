import polib
import os

po_files = [
    'locales/pot/get_started.po',
    'locales/pot/index.po',
    'locales/pot/terms_of_service.po',
    'locales/pot/privacy_policy.po'
]

for po_file in po_files:
    mo_file = os.path.splitext(po_file)[0] + '.mo'
    po = polib.pofile(po_file)
    po.save_as_mofile(mo_file)
    print(f"✅ Compiled {po_file} -> {mo_file}")
