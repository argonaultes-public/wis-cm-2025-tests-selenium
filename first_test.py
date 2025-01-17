import face_recognition
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread

# Liste des objets disponibles
MATERIALS = [
    "Mousqueton",
    "Gants d’intervention",
    "Brassard de sécurité",
    "Porte menottes",
    "Bandeau agent de sécurité cynophile",
    "Talkies walkies",
    "Lampe Torche",
    "Kit oreillette",
    "Tasers",
    "Bombes lacrymogènes"
]

# Liste des visages connus
KNOWN_FACES = [
    {"name": "Bob", "encoding": None}  # Ajouter une photo de Bob nommée "bob.png"
]


# Fonction pour démarrer la caméra et afficher le flux vidéo
def start_camera(feed_label, stop_flag):
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def update_feed():
        while not stop_flag[0]:
            if not feed_label.winfo_exists():  # Vérifie si le widget existe
                break
            ret, frame = video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                try:
                    feed_label.configure(image=imgtk)
                    feed_label.image = imgtk
                except tk.TclError:
                    break
        video_capture.release()

    thread = Thread(target=update_feed, daemon=True)
    thread.start()


# Initialiser les visages connus
def initialize_known_faces():
    for face in KNOWN_FACES:
        try:
            image_path = f"{face['name'].lower()}.png"
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                face["encoding"] = encodings[0]
            else:
                print(f"Aucun visage détecté dans {image_path}")
        except Exception as e:
            print(f"Erreur avec le fichier {image_path}: {e}")


# Identifier directement l'utilisateur depuis le flux vidéo
def verify_access_direct(video_capture, main_frame, root):
    ret, frame = video_capture.read()
    if not ret:
        messagebox.showerror("Erreur", "Impossible de lire le flux vidéo.")
        return

    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        for face in KNOWN_FACES:
            if face.get("encoding") is not None:
                results = face_recognition.compare_faces([face["encoding"]], face_encoding)
                if results[0]:
                    messagebox.showinfo("Accès autorisé", f"Bienvenue {face['name']} !")
                    show_inventory_interface(main_frame, face['name'], root)
                    return

    messagebox.showerror("Accès refusé", "Visage non reconnu. Accès refusé.")


# Afficher l'interface de l'inventaire
def show_inventory_interface(main_frame, name, root):
    for widget in main_frame.winfo_children():
        widget.destroy()

    def identify_again():
        for widget in main_frame.winfo_children():
            widget.destroy()
        start_camera_interface(main_frame, root)

    # Bouton identification
    id_btn = tk.Button(main_frame, text="Identification", command=identify_again, font=("Helvetica", 12), padx=10, pady=5)
    id_btn.pack(side=tk.TOP, anchor="nw", padx=10, pady=10)

    # Afficher l'image de l'utilisateur en haut à droite
    try:
        image_path = f"{name.lower()}.png"  # Image associée au nom
        img = Image.open(image_path)
        img = img.resize((300, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(main_frame, image=photo)
        label.image = photo  # Prévenir le garbage collection
        label.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image pour {name}: {e}")

    # Message de bienvenue
    tk.Label(main_frame, text=f"Bienvenue {name}. Sélectionnez le matériel emprunté:", font=("Helvetica", 12)).pack(pady=10)

    # Checkboxes pour le matériel
    checkbox_vars = []
    for material in MATERIALS:
        var = tk.IntVar()
        checkbox_vars.append(var)
        tk.Checkbutton(main_frame, text=material, variable=var, font=("Helvetica", 10)).pack(anchor='w')

    # Bouton de validation
    def submit():
        selected_items = [MATERIALS[i] for i, var in enumerate(checkbox_vars) if var.get() == 1]

        messagebox.showinfo("Confirmation", f"Matériel emprunté par {name}: {', '.join(selected_items)}")
        root.destroy()

    tk.Button(main_frame, text="Valider", command=submit, font=("Helvetica", 12), padx=10, pady=5).pack(pady=10)


# Interface principale
def start_camera_interface(main_frame, root):
    for widget in main_frame.winfo_children():
        widget.destroy()

    camera_frame = tk.Frame(main_frame)
    camera_frame.pack(side=tk.LEFT, padx=10, pady=10)
    feed_label = tk.Label(camera_frame)
    feed_label.pack()

    stop_flag = [False]
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    start_camera(feed_label, stop_flag)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)
    tk.Button(
        button_frame,
        text="Identifier et accéder à l'inventaire",
        font=("Helvetica", 14),
        padx=20,
        pady=10,
        command=lambda: verify_access_direct(video_capture, main_frame, root)
    ).pack()


# Lancer l'interface
def open_camera_interface():
    initialize_known_faces()

    root = tk.Tk()
    root.title("Interface de reconnaissance faciale")
    root.geometry("1000x600")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    start_camera_interface(main_frame, root)

    root.mainloop()


if __name__ == "__main__":
    open_camera_interface()
