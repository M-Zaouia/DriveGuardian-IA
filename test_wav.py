import winsound

# CHEMIN ABSOLU (copié tel quel)
path = r"C:\Users\marou\Desktop\DriveGuardianIA\data\audio\warning.wav"

print("Chemin testé :", path)
print("Lecture…")
winsound.PlaySound(path, winsound.SND_FILENAME)
print("Fin de lecture.")
