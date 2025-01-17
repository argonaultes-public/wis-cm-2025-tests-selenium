import cv2
import face_recognition
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread

MATERIALS = [
    "Mousqueton", "Gants d’intervention", "Brassard de sécurité", "Porte menottes",
    "Bandeau agent de sécurité cynophile", "Talkies walkies", "Lampe Torche",
    "Kit oreillette", "Tasers", "Bombes lacrymogènes"
]

KNOWN_FACES = [
    {"name": "Bob", "encoding": None}  # Fichier image attendu : "bob.png"
]

def initialize_known_faces():
    for face in KNOWN_FACES:
        try:
            img = face_recognition.load_image_file(face["name"].lower() + ".png")
            enc = face_recognition.face_encodings(img)
            face["encoding"] = enc[0] if enc else None
        except:
            face["encoding"] = None

def update_feed(video_capture, feed_label, stop_flag):
    while not stop_flag[0]:
        if not feed_label.winfo_exists():
            break
        ret, frame = video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
            try:
                feed_label.configure(image=imgtk)
                feed_label.image = imgtk
            except tk.TclError:
                break
    video_capture.release()

def start_camera(feed_label, stop_flag):
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    Thread(target=update_feed, args=(video_capture, feed_label, stop_flag), daemon=True).start()
    return video_capture

def verify_access_direct(video_capture, main_frame, root):
    ret, frame = video_capture.read()
    if not ret:
        messagebox.showerror("Erreur", "Impossible de lire le flux vidéo.")
        return

    rgb_frame = frame[:, :, ::-1]
    locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, locations)

    for encoding in encodings:
        for face in KNOWN_FACES:
            if face["encoding"] is not None:
                if face_recognition.compare_faces([face["encoding"]], encoding)[0]:
                    messagebox.showinfo("Accès autorisé", f"Bienvenue {face['name']} !")
                    show_inventory_interface(main_frame, face['name'], root)
                    return
    messagebox.showerror("Accès refusé", "Visage non reconnu. Accès refusé.")

def show_inventory_interface(main_frame, name, root):
    for widget in main_frame.winfo_children():
        widget.destroy()

    def identify_again():
        for w in main_frame.winfo_children():
            w.destroy()
        start_camera_interface(main_frame, root)

    tk.Button(main_frame, text="Identification", command=identify_again,
              font=("Helvetica", 12), padx=10, pady=5).pack(side=tk.TOP, anchor="nw", padx=10, pady=10)

    try:
        img = Image.open(name.lower() + ".png").resize((300, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(main_frame, image=photo)
        label.image = photo
        label.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)
    except:
        pass

    tk.Label(main_frame, text=f"Bienvenue {name}. Sélectionnez le matériel emprunté:",
             font=("Helvetica", 12)).pack(pady=10)

    vars_ = [tk.IntVar() for _ in MATERIALS]
    for mat, var in zip(MATERIALS, vars_):
        tk.Checkbutton(main_frame, text=mat, variable=var, font=("Helvetica", 10)).pack(anchor='w')

    def submit():
        sel = [m for m, v in zip(MATERIALS, vars_) if v.get() == 1]
        messagebox.showinfo("Confirmation", f"Matériel emprunté par {name}: {', '.join(sel)}")
        root.destroy()

    tk.Button(main_frame, text="Valider", command=submit, font=("Helvetica", 12), padx=10, pady=5).pack(pady=10)

def start_camera_interface(main_frame, root):
    for w in main_frame.winfo_children():
        w.destroy()

    camera_frame = tk.Frame(main_frame)
    camera_frame.pack(side=tk.LEFT, padx=10, pady=10)
    feed_label = tk.Label(camera_frame)
    feed_label.pack()

    stop_flag = [False]
    video_capture = start_camera(feed_label, stop_flag)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)
    tk.Button(button_frame, text="Identifier et accéder à l'inventaire",
              font=("Helvetica", 14), padx=20, pady=10,
              command=lambda: verify_access_direct(video_capture, main_frame, root)).pack()

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
