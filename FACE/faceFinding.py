import cv2
import face_recognition
import os

# chargement des visages de référence
"""
Met à jour la liste des prénoms automatiquement au fur et à mesure
que j'ajoute des photos .jpg au dossier faces.
"""

faces_folder = "faces"
reference_images = []

for filename in os.listdir(faces_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        reference_images.append(os.path.join(faces_folder, filename))

known_encodings = []
known_names = []

for img_path in reference_images:

    img = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(img)

    if encodings:
        known_encodings.append(encodings[0])

        # Nom de la personne = nom du fichier
        name = os.path.splitext(os.path.basename(img_path))[0]
        known_names.append(name)
        print(f"Visage chargé : {name}")
    else:
        print(f"Aucun visage trouvé dans : {img_path}")

# vérifier qu'il y a au moins un visage
if not known_encodings:
    print("Aucun visage de référence trouvé.")
    exit()

print("Visages chargés :", known_names)

# ouvrir la webcam et demander du 720p à 30 FPS
cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)

if not cap.isOpened():
    print("Impossible d'ouvrir la webcam UGREEN.")
    exit()

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# réduire le buffer pour éviter l'accumulation d'anciennes images et latence traitement d'images
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("Ouverte :", cap.isOpened())
print("Largeur :", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Hauteur :", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("FPS :", cap.get(cv2.CAP_PROP_FPS))

# reconnaissance en temps réel
while True:

    ret, frame = cap.read()

    if not ret:
        print("Impossible de lire la webcam.")
        break

    # réduire l'image AVANT la reconnaissance
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # BGR -> RGB
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # détection sur la petite image
    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)

        name = "Inconnu"
        color = (0, 0, 255)

        if True in matches:
            match_idx = matches.index(True)
            name = known_names[match_idx]
            color = (0, 255, 0)

        # remettre les coordonnées à l'échelle originale
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Reconnaissance faciale", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
# 7. fermeture
cap.release()
cv2.destroyAllWindows()
