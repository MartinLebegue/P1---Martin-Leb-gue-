try:
    with open("test_simple.txt", "w") as fichier_test:
        fichier_test.write("Ceci est un test.\n")
    print("Fichier écrit avec succès.")
except Exception as e:
    print(f"Erreur lors de l'écriture du fichier test : {e}")