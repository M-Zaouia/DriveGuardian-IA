import os
try:
    from playsound import playsound
except ImportError:
    print("❌ playsound n'est pas installé dans ce venv.")
    print("Installe-le avec : pip install playsound==1.2.2")
    raise

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(BASE_DIR, "data", "audio", "warning.wav")

print("Dossier courant  :", BASE_DIR)
print("Chemin testé     :", audio_path)
print("Fichier existe ? :", os.path.exists(audio_path))

if os.path.exists(audio_path):
    print("Lecture du fichier audio...")
    try:
        playsound(audio_path)
        print("✅ Lecture terminée.")
    except Exception as e:
        print("❌ Erreur playsound :", repr(e))
else:
    print("⚠️ Le fichier warning.wav est introuvable à cet endroit.")
