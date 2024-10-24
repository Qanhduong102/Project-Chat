import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import speech_recognition as sr


def activate_mic():
    # Khởi tạo recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)  # Nhận giọng nói từ mic

        try:
            # Nhận diện giọng nói và chuyển đổi thành văn bản
            message = recognizer.recognize_google(audio, language="en-US")
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"You: {message}\n")
            chat_display.config(state=tk.DISABLED)
            chat_input.delete(0, tk.END)  # Xóa ô nhập văn bản
            chat_input.insert(0, message)  # Chèn văn bản nhận diện vào ô nhập
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


# Hàm chuyển đổi giữa các khung (frame)
def show_frame(frame_in):
    frame_in.tkraise()

# Hàm đăng ký người dùng
def register_user():
    full_name = fullname_entry.get()
    email = signup_email_entry.get()
    password = signup_password_entry.get()

    if full_name and email and password:
        user_data = {"name": full_name, "email": email, "password": password}

        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                data = json.load(file)
        else:
            data = []

        for user in data:
            if user['email'] == email:
                messagebox.showerror("Error", "Email already registered.")
                return

        data.append(user_data)
        with open("users.json", "w") as file:
            json.dump(data, file)

        messagebox.showinfo("Success", "Registration successful!")
        show_frame(login_frame)
    else:
        messagebox.showerror("Error", "All fields are required.")

# Hàm đăng nhập
def login_user():
    email = email_entry.get()
    password = password_entry.get()

    if email and password:
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                data = json.load(file)

            for user in data:
                if user['email'] == email and user['password'] == password:
                    global current_user
                    current_user = user  # Lưu thông tin người dùng hiện tại
                    messagebox.showinfo("Success", f"Welcome {user['name']}!")
                    show_frame(home_frame)
                    return
            messagebox.showerror("Error", "Invalid email or password.")
        else:
            messagebox.showerror("Error", "No users found. Please register first.")
    else:
        messagebox.showerror("Error", "Both fields are required.")

# Hàm hiển thị thông tin người dùng
def show_user_info():
    if current_user:
        user_info = f"Name: {current_user['name']}\nEmail: {current_user['email']}"
        messagebox.showinfo("User Info", user_info)

# Hàm đăng xuất
def logout_user():
    global current_user
    current_user = None  # Đặt người dùng hiện tại về None
    show_frame(login_frame)  # Quay lại trang đăng nhập

# Hàm đổi avatar
def change_avatar():
    file_path = filedialog.askopenfilename(title="Select an Avatar",
                                           filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        # Cập nhật ảnh đại diện
        global avatar_photo
        avatar_image_outer = Image.open(file_path)
        avatar_image_outer = avatar_image_outer.resize((50, 50), Image.ANTIALIAS)
        avatar_photo = ImageTk.PhotoImage(avatar_image_outer)

        avatar_label.config(image=avatar_photo)  # Cập nhật ảnh đại diện

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Sign In / Sign Up")
window.geometry("1366x768")  # Đặt kích thước cửa sổ
window.configure(bg="#e0f7fa")  # Màu nền nhẹ

# Tạo ba khung cho đăng nhập, đăng ký và trang chủ
login_frame = tk.Frame(window, bg="white", bd=10, relief="ridge")
signup_frame = tk.Frame(window, bg="white", bd=10, relief="ridge")
home_frame = tk.Frame(window, bg="white", bd=10, relief="ridge")

# Tính toán kích thước mới cho các khung
frame_width = 1100
frame_height = 650
x = (1366 - frame_width) // 2
y = (768 - frame_height) // 2

for frame in (login_frame, signup_frame, home_frame):
    frame.place(x=x, y=y, width=frame_width, height=frame_height)

# ---------- Giao diện đăng nhập ----------
tk.Label(login_frame, text="Sign In", font=("Arial", 30, "bold"), fg="#00796b", bg="white").pack(pady=20)

# Ô nhập Email
tk.Label(login_frame, text="Email", font=("Arial", 14), bg="white").pack(pady=5)
email_entry = tk.Entry(login_frame, font=("Arial", 14), bg="#e0f2f1", width=40)
email_entry.pack(pady=5)

# Ô nhập Password
tk.Label(login_frame, text="Password", font=("Arial", 14), bg="white").pack(pady=5)
password_entry = tk.Entry(login_frame, font=("Arial", 14), bg="#e0f2f1", width=40, show="*")
password_entry.pack(pady=5)

# Nút đăng nhập
login_button = tk.Button(login_frame, text="Sign In", font=("Arial", 14), bg="#00796b", fg="white", width=20,
                         command=login_user)
login_button.pack(pady=10)

# Nút chuyển sang trang đăng ký
signup_switch_button = tk.Button(login_frame, text="Don't have an account? Sign Up", font=("Arial", 12), bg="white",
                                 fg="#00796b", borderwidth=0, command=lambda: show_frame(signup_frame))
signup_switch_button.pack(pady=5)

# Hàm đăng nhập
def login_user():
    email = email_entry.get()
    password = password_entry.get()

    if email and password:
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                data = json.load(file)

            for user in data:
                if user['email'] == email and user['password'] == password:
                    global current_user
                    current_user = user  # Lưu thông tin người dùng hiện tại
                    messagebox.showinfo("Success", f"Welcome {user['name']}!")
                    show_frame(home_frame)

                    # Tạo sẵn cuộc hội thoại 1
                    add_new_conversation_ing()  # Thêm cuộc hội thoại mới
                    return
            messagebox.showerror("Error", "Invalid email or password.")
        else:
            messagebox.showerror("Error", "No users found. Please register first.")
    else:
        messagebox.showerror("Error", "Both fields are required.")

# Hàm thêm cuộc hội thoại mới
def add_new_conversation():
    global current_conversation
    conversation_name = f"Conversation 1"  # Tạo cuộc hội thoại mặc định
    conversations[conversation_name] = []  # Tạo cuộc hội thoại mới
    conversation_listbox.insert(tk.END, conversation_name)
    clear_chat_display()  # Xóa nội dung hiển thị chat khi tạo cuộc hội thoại mới
    current_conversation = conversation_name  # Cập nhật cuộc hội thoại hiện tại


# ---------- Giao diện đăng ký ----------
tk.Label(signup_frame, text="Sign Up", font=("Arial", 30, "bold"), fg="#00796b", bg="white").pack(pady=20)

# Ô nhập Họ tên
tk.Label(signup_frame, text="Full Name", font=("Arial", 14), bg="white").pack(pady=5)
fullname_entry = tk.Entry(signup_frame, font=("Arial", 14), bg="#e0f2f1", width=40)
fullname_entry.pack(pady=5)

# Ô nhập Email
tk.Label(signup_frame, text="Email", font=("Arial", 14), bg="white").pack(pady=5)
signup_email_entry = tk.Entry(signup_frame, font=("Arial", 14), bg="#e0f2f1", width=40)
signup_email_entry.pack(pady=5)

# Ô nhập Password
tk.Label(signup_frame, text="Password", font=("Arial", 14), bg="white").pack(pady=5)
signup_password_entry = tk.Entry(signup_frame, font=("Arial", 14), bg="#e0f2f1", width=40, show="*")
signup_password_entry.pack(pady=5)

# Nút đăng ký
signup_button = tk.Button(signup_frame, text="Sign Up", font=("Arial", 14), bg="#00796b", fg="white", width=20,
                          command=register_user)
signup_button.pack(pady=10)

# Nút quay lại trang đăng nhập
back_to_login_button = tk.Button(signup_frame, text="Back to Sign In", font=("Arial", 12), bg="white", fg="black",
                                 borderwidth=1, command=lambda: show_frame(login_frame))
back_to_login_button.pack(pady=5)

# ---------- Giao diện trang chủ ----------
tk.Label(home_frame, text="Welcome to the Home Page", font=("Arial", 30, "bold"), fg="#00796b", bg="white").pack(pady=20)
tk.Label(home_frame, text="This is the main application area.", font=("Arial", 14), bg="white").pack(pady=10)

# Thêm ảnh đại diện
avatar_image = Image.open("C:/Users/Acer/PycharmProjects/GUI SignIn_Login/avatar.png")  # Đường dẫn đến hình ảnh avatar
avatar_image = avatar_image.resize((50, 50), Image.LANCZOS)  # Thay đổi kích thước ảnh đại diện
avatar_photo = ImageTk.PhotoImage(avatar_image)

avatar_label = tk.Label(home_frame, image=avatar_photo, bg="white")
avatar_label.place(x=10, y=10)  # Đặt vị trí ở góc trên bên trái

# Nút hiển thị thông tin người dùng
user_info_button = tk.Button(home_frame, text="User Info", font=("Arial", 12), command=show_user_info)
user_info_button.place(x=70, y=20)  # Đặt vị trí bên cạnh avatar

# Nút đăng xuất
logout_button = tk.Button(home_frame, text="Logout", font=("Arial", 12), command=logout_user)
logout_button.place(x=160, y=20)  # Đặt vị trí bên cạnh nút User Info

# Thêm ảnh nền
background_image = Image.open("img_1.png")  # Đường dẫn đến ảnh nền
background_image = background_image.resize((1920, 1280), Image.LANCZOS)  # Thay đổi kích thước ảnh nền
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Đặt ảnh nền chiếm toàn bộ cửa sổ

# Bắt đầu bằng khung đăng nhập
current_user = None  # Khởi tạo biến người dùng hiện tại
show_frame(login_frame)

# ---------- Giao diện trang chủ (chia thành 2 phần) ----------
home_left_frame = tk.Frame(home_frame, bg="white", width=300, bd=10, relief="ridge")
home_right_frame = tk.Frame(home_frame, bg="white", bd=10, relief="ridge")

home_left_frame.place(x=10, y=100, width=300, height=520)
home_right_frame.place(x=320, y=100, width=700, height=500)  # Phần bên phải (Hội thoại)

# ---------- Phần bên trái: ListView cho các cuộc hội thoại ----------
# Tiêu đề ListView
tk.Label(home_left_frame, text="Conversations", font=("Arial", 16, "bold"), fg="#00796b", bg="white").pack(pady=10)

# Listbox để hiển thị danh sách các cuộc hội thoại
conversation_listbox = tk.Listbox(home_left_frame, font=("Arial", 14), bg="#e0f7fa", fg="black", width=25, height=18)
conversation_listbox.place(x=10, y=10, width=280, height=400)


# Nút để thêm một cuộc hội thoại mới
new_conversation_button = tk.Button(home_left_frame, text="New Conversation", font=("Arial", 12), bg="#00796b", fg="white",
                                    command=lambda: add_new_conversation_ing())
new_conversation_button.pack(side=tk.BOTTOM, pady=10)



# ---------- Phần bên phải: Hiển thị và thao tác hội thoại ----------
# Tiêu đề
tk.Label(home_right_frame, text="Chat Interface", font=("Arial", 16, "bold"), fg="#00796b", bg="white").pack(pady=10)

# Textbox để hiển thị nội dung hội thoại
chat_display = tk.Text(home_right_frame, font=("Arial", 12), bg="#e0f7fa", fg="black", width=70, height=20, state="disabled")
chat_display.pack(pady=10)

# Ô nhập văn bản
chat_input = tk.Entry(home_right_frame, font=("Arial", 14), bg="#e0f2f1", fg="black", width=50)
chat_input.pack(pady=10, side=tk.LEFT)

# Nút gửi tin nhắn
send_button = tk.Button(home_right_frame, text="Send", font=("Arial", 12), bg="#00796b", fg="white", command=lambda: send())
send_button.pack(pady=10, side=tk.RIGHT)
# Nút bật mic
mic_button = tk.Button(home_right_frame, text="🎤 Mic", font=("Arial", 12), bg="#00796b", fg="white", command=activate_mic)
mic_button.pack(pady=10, side=tk.RIGHT)  # Đặt nút bên cạnh nút Send


# --------- Các hàm hỗ trợ ----------
# Hàm thêm cuộc hội thoại mới
def add_conversation():
    conversation_listbox.insert(tk.END, f"Conversation {conversation_listbox.size() + 1}")

# Chức năng xoá cuộc hội thoại
def delete_conversation():
    selected_conversation = conversation_listbox.get(tk.ACTIVE)
    if selected_conversation in conversations:
        del conversations[selected_conversation]
        conversation_listbox.delete(tk.ACTIVE)
        clear_chat_display()

# Hàm gửi tin nhắn
def send_message():
    message = chat_input.get()
    if message:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.config(state=tk.DISABLED)
        chat_input.delete(0, tk.END)

# Khởi tạo danh sách để lưu trữ các cuộc hội thoại
conversations = {}
current_conversation = None  # Khởi tạo cuộc hội thoại hiện tại

# Hàm thêm cuộc hội thoại mới
def add_new_conversation_ing():
    global current_conversation
    conversation_name = f"Conversation {len(conversations) + 1}"
    conversations[conversation_name] = []  # Tạo cuộc hội thoại mới
    conversation_listbox.insert(tk.END, conversation_name)
    clear_chat_display()  # Xóa nội dung hiển thị chat khi tạo cuộc hội thoại mới
    current_conversation = conversation_name  # Cập nhật cuộc hội thoại hiện tại

# Hàm xóa nội dung hiển thị chat
def clear_chat_display():
    chat_display.config(state=tk.NORMAL)
    chat_display.delete(1.0, tk.END)  # Xóa tất cả nội dung
    chat_display.config(state=tk.DISABLED)

# Hàm gửi tin nhắn
def send():
    message = chat_input.get()
    if message:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.config(state=tk.DISABLED)
        chat_input.delete(0, tk.END)

        # Lưu tin nhắn vào cuộc hội thoại hiện tại
        if current_conversation:
            conversations[current_conversation].append(f"You: {message}")

# Hàm hiển thị nội dung cuộc hội thoại
def display_conversation():
    selected_conversation = conversation_listbox.get(conversation_listbox.curselection())
    if selected_conversation in conversations:
        chat_display.config(state=tk.NORMAL)
        chat_display.delete(1.0, tk.END)  # Xóa nội dung hiện tại
        for message in conversations[selected_conversation]:
            chat_display.insert(tk.END, f"{message}\n")  # Hiển thị lại tin nhắn
        chat_display.config(state=tk.DISABLED)

# Gán sự kiện cho Listbox
conversation_listbox.bind('<<ListboxSelect>>', display_conversation)


# Chạy vòng lặp chính của giao diện
window.mainloop()