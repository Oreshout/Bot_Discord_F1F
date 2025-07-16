import polib
import os

# Dossier source = tes .po
input_dir = "pot"
# Dossier destination = les .mo compilés
output_dir = "mo"

# Création du dossier mo/ s’il n’existe pas
os.makedirs(output_dir, exist_ok=True)

# Compilation
for filename in os.listdir(input_dir):
    if filename.endswith(".po"):
        po_path = os.path.join(input_dir, filename)
        mo_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".mo")
        try:
            po = polib.pofile(po_path)
            po.save_as_mofile(mo_path)
            print(f"✅ {filename} compilé en {mo_path}")
        except Exception as e:
            print(f"❌ Erreur dans {filename} : {e}")
