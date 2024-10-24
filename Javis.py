import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import speech_recognition as sr
import pyttsx3
import random
import requests
from datetime import date, timedelta
import webbrowser
import sys
# Khai báo biến toàn cục
current_conversation = None  # Hoặc giá trị mặc định khác nếu cần

# Khởi tạo pyttsx3
robot_mouth = pyttsx3.init()  # Đổi từ engine thành robot_mouth
robot_ear = sr.Recognizer()  # Đổi từ sr.Recognizer thành robot_ear

# Thiết lập thuộc tính giọng nói
voices = robot_mouth.getProperty('voices')
robot_mouth.setProperty('voice', voices[1].id)  # Giọng nữ
robot_mouth.setProperty('rate', 150)  # Tốc độ nói

# Danh sách mẫu câu hỏi và câu trả lời
sample_conversations = {
    "hi": "Welcome back, Peter! It's great to see you again.",
    "how are you": "I'm just a bot, but I'm functioning well! How about you?",
    "feeling good": "That's awesome! Is there anything fun you'd like to share today?",
    "what is your name": "I'm JAVIS, your virtual assistant, always ready to help you!",
    "what can you do for me": "I can assist you with questions about technology, programming, and many other topics. What would you like to learn?",
    "i want to learn how to bake": "Baking is a wonderful art! What kind of cake would you like to try? A chocolate cake or some cookies?",
    "make me laugh": "I've got a joke for you: Why did the scarecrow win an award?",
    "why": "Because he was outstanding in his field!",
    "wow i don't think it that bad": "I'll take that as a compliment, thank you!",
    "thanks": "You're welcome! If you need anything else, just let me know!",

    "what is your favorite hobby": "I don't have hobbies like you do, but I love helping you explore yours! What's your favorite hobby?",
    "i enjoy painting": "That's wonderful! Painting is a great way to express creativity. What do you like to paint?",
    "do you like music": "I think music is fascinating! It can evoke so many emotions. What kind of music do you enjoy?",
    "i love classical music": "Classical music is timeless! Do you have a favorite composer?",
    "can you tell me a fun fact": "Sure! Did you know honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
    "what is your favorite season": "I don't experience seasons, but many people love spring for its blooming flowers. What's your favorite season?",
    "i like summer": "Summer is great for outdoor activities and vacations! Do you have any summer plans?",
    "what is the best way to learn a new skill": "Practice is key! Finding online courses or joining local classes can really help. What skill are you interested in learning?",
    "i want to learn a new language": "That's an exciting goal! Which language are you thinking of learning?",
    "do you have a favorite movie": "I don't watch movies, but I know many people enjoy classic films. What's your favorite movie?",
    "i love sci-fi movies": "Sci-fi movies can take you on amazing adventures! Do you have a favorite sci-fi film?",
    "what is your favorite book": "I don't read books like you do, but I love hearing about what you enjoy! What's a book you recommend?",
    "i recently read a great mystery novel": "Mystery novels can be so gripping! Who's your favorite author?",
    "how can I improve my productivity": "Setting clear goals and breaking tasks into smaller steps can help! Do you have a specific area you want to be more productive in?",
    "i struggle with time management": "Time management can be challenging! Have you tried using a planner or setting timers for tasks?",

    "what is your favorite type of cuisine": "I don't eat, but I know many people enjoy exploring different cuisines! What's your favorite?",
    "i love Italian food": "Italian cuisine is delicious! Do you have a favorite dish, like pasta or pizza?",
    "what are some good ways to relax": "Relaxation is important! Activities like meditation, reading, or taking a walk can help. What do you do to unwind?",
    "i like to listen to music": "Listening to music is a great way to relax! Do you have a go-to playlist or favorite artist?",
    "how do you handle stress": "I don't experience stress, but many people find exercise, talking to friends, or deep breathing helpful. What do you do?",
    "what is your favorite thing about technology": "Technology has transformed our lives! It makes communication faster and easier. What's your favorite tech gadget?",
    "i love my smartphone": "Smartphones are incredibly versatile! What apps do you use the most?",
    "what is the latest tech trend": "Artificial intelligence and machine learning are trending topics right now. Are you interested in any specific tech trends?",
    "how do you stay updated on tech news": "I don't read news, but I know many people follow blogs and podcasts for updates. Do you have any favorite tech sources?",
    "what is your favorite way to stay active": "I don’t exercise, but staying active is great for health! What activities do you enjoy?",
    "i like jogging in the park": "Jogging is a fantastic way to stay fit! Do you have a favorite park you like to run in?",
    "how can I eat healthier": "Incorporating more fruits and vegetables into your diet is a great start! What healthy meals do you enjoy?",
    "i like smoothies": "Smoothies are delicious and nutritious! Do you have a favorite recipe?",
    "what is a good book recommendation": "There are so many great books! What genre do you prefer, and I can suggest something!",
    "i enjoy fantasy novels": "Fantasy novels open up new worlds! Have you read any good ones lately?",
    "what is the best advice you've ever received": "I don't receive advice, but many people value kindness and perseverance. What's the best advice you've gotten?",
    "do you like puzzles": "Puzzles can be a fun challenge! Do you prefer jigsaw puzzles, crosswords, or something else?",
    "i love solving crosswords": "Crosswords are a great way to exercise your brain! How often do you do them?",
    "what is your opinion on social media": "Social media connects people, but it can also be overwhelming. How do you feel about it?",
    "i think it can be both good and bad": "That's a balanced view! It can foster community but also lead to misinformation. What do you use social media for?",

}
def check_internet():
    url = "http://www.google.com"
    timeout = 5
    try:
        # Gửi yêu cầu tới Google với thời gian chờ
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
if not check_internet():
    print("No internet connection. The program cannot start.")
    sys.exit()  # Thoát chương trình nếu không có mạng
else:
    print("Internet connection detected. Starting program...")
    # Khởi động chương trình chatbot của bạn ở đây
# Dự báo thời tiết giả lập
def get_weather():
    weather_conditions = ['sunny', 'cloudy', 'rainy', 'snowy', 'windy']
    temperature = random.randint(15, 35)
    condition = random.choice(weather_conditions)
    return f"The weather is {condition} and {temperature} degrees Celsius."

# Lấy tin tức
def get_news():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=aa322ef7db774b6da2eb37acc2827518'
    try:
        response = requests.get(url, timeout=10)
        news_data = response.json()

        if isinstance(news_data, dict) and news_data.get('status') == 'ok':
            articles = news_data.get('articles', [])
            if not articles:
                return "No articles found."
            news_summary = "Here are the top news headlines: " + ", ".join([article['title'] for article in articles[:5]])
            return news_summary
        else:
            return "I'm unable to fetch the news right now."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def send():
    user_input = chat_input.get()  # Lấy nội dung từ ô nhập văn bản
    if user_input.strip():  # Kiểm tra nếu ô không trống
        chat_display.config(state="normal")  # Cho phép chỉnh sửa Textbox
        chat_display.insert(tk.END, f"You: {user_input}\n")  # Hiển thị tin nhắn của người dùng
        chat_display.config(state="disabled")  # Khóa Textbox để không thể chỉnh sửa

        chat_input.delete(0, tk.END)  # Xóa nội dung ô nhập văn bản

        # Phản hồi tự động (ví dụ: trả lời lại)
        bot_response = generate_response(user_input)  # Gọi hàm để tạo phản hồi
        chat_display.config(state="normal")
        chat_display.insert(tk.END, f"Bot: {bot_response}\n")  # Hiển thị phản hồi của bot
        chat_display.config(state="disabled")
def generate_response(user_input):
    # Ở đây bạn có thể thêm logic để tạo phản hồi cho bot
    responses = {
    "Hello, how are you today?": "Hello! I'm glad to see you. How can I help you today?",
    "What can you do for me?": "I can help you answer questions about IT, programming, and technology. What would you like to ask?",
    "I want to learn about IT": "Great! Do you want to start with hardware, software, or programming?",
    "Are there any new updates in the tech industry?": "There are many interesting news! Which specific area are you interested in?",
    "Can you explain artificial intelligence?": "Certainly! Artificial intelligence (AI) is the ability of computers to perform tasks that require human-like intelligence.",
    "Do you know how to learn programming effectively?": "Yes! Learning by practicing, taking online courses, and reading documentation is the best way.",
    "Are there any tech events happening today?": "You can check tech websites for the latest event information!",
    "I need technical support, can you help?": "Certainly! Let me know what problem you're facing.",
    "Can you introduce a programming language?": "Of course! Python is an easy-to-learn and very popular programming language today.",
    "I want to know more about information security": "Information security is crucial in the digital age. Which aspect would you like to learn about?",
    "Can you explain blockchain?": "Blockchain is a distributed ledger technology that records and secures information transparently.",
    "I've heard about 5G, can you explain it?": "5G is the new generation of mobile networks, offering faster internet speeds and lower latency.",
    "I want to know about AI applications in daily life": "AI is used in many areas such as virtual assistants, image recognition, and data analysis.",
    "Do you know any software that helps with time management?": "Yes, software like Trello, Todoist, and Asana are very useful for time and task management.",
    "Can you suggest a programming book?": "The book 'Automate the Boring Stuff with Python' is a great choice for beginners.",
    "How can I improve my programming skills?": "Practice regularly, join open-source projects, and learn from online lessons.",
    "Can you help me learn about the Internet of Things (IoT)?": "IoT is a network of devices connected to the internet to collect and exchange data.",
    "What technology is trending right now?": "AI, Machine Learning, and Blockchain are technologies that are receiving a lot of attention lately.",
    "Can you explain DevOps?": "DevOps is a method that combines software development and operations to improve workflow.",
    "Are there any software tools to help learn programming?": "Platforms like Codecademy, Coursera, and Udacity offer many online programming courses.",
    "What programming languages does Codecademy offer?": "Codecademy offers courses in Python, Java, JavaScript, Ruby, and many other languages.",
    "Does Coursera collaborate with any universities?": "Coursera collaborates with top universities like Stanford, Yale, and the University of Michigan to offer quality courses.",
    "Does Udacity have nanodegree programs?": "Yes, Udacity offers nanodegree programs that allow students to specialize in areas such as AI, Data Science, and web development.",
    "Are there any free software tools?": "Yes! Many platforms like FreeCodeCamp and Khan Academy offer free programming courses for learners.",
    "Can I learn programming on a smartphone?": "Yes, you can use apps like SoloLearn and Mimo to learn programming on a smartphone.",
    "How do I choose a programming language to learn?": "You should determine your goal; if you want to do web development, JavaScript is a good choice. If you're into data science, try Python.",
    "Is learning programming difficult?": "Learning programming can be difficult at first, but with patience and regular practice, you'll improve quickly.",
    "Can you suggest a programming project for a beginner?": "A good project for beginners is to create a personal website to introduce yourself and your interests.",
    "Why is learning programming important?": "Learning programming helps you develop logical thinking, problem-solving skills, and expands career opportunities in today's tech-driven world.",
    "What are good forums for asking about programming?": "Some good forums include Stack Overflow, Reddit, and programming-focused Facebook groups.",
    "When did the IT industry start forming?": "The IT industry began to form in the mid-20th century with the development of the first electronic computers.",
    "Who invented the first computer?": "Charles Babbage is considered the 'father of the computer' with his design of the Analytical Engine in 1837.",
    "What is ARPANET?": "ARPANET was the first computer network, developed in the 1960s, and is the precursor to today's Internet.",
    "When was the Internet born?": "The Internet officially came into existence in 1983 when the TCP/IP protocol was standardized.",
    "What was the first operating system?": "The first operating system was GM-NAA I/O, developed for the IBM 704 computer in 1956.",
    "What was the first programming language?": "The first recognized programming language is Fortran, developed in the 1950s.",
    "What was a major turning point in the development of the IT industry?": "The advent of the PC (Personal Computer) in the 1970s-1980s revolutionized the way people use computers.",
    "Who invented the World Wide Web?": "The World Wide Web was invented by Tim Berners-Lee in 1989.",
    "Why is the development of open-source software important?": "Open-source software encourages innovation and collaboration within the global software development community.",
    "What are the most popular operating systems today?": "Windows, macOS, and Linux are the three most popular operating systems today.",
    "Do you have any hobbies?": "I enjoy helping users learn and solve problems. How about you?",
    "I like drawing": "Drawing is a very creative hobby! What do you usually draw?",
    "I like drawing landscapes": "Landscapes are beautiful! Do you have a painting you're particularly proud of?",
    "Yes, I have a painting of the sea": "That's awesome! Thank you for sharing your hobby with me!",
    "I like fantasy novels": "Fantasy is a captivating genre! Have you read any recently?",
    "I just read 'Harry Potter'": "A great choice! I hope you continue finding many other interesting books!",
    "Do you know about video games?": "Yes, I know a lot about video games. What game do you like the most?",
    "I like role-playing games.": "Role-playing games are usually very exciting! Do you have a favorite character in any game?",
    "I like the main character in 'The Witcher'.": "Geralt of Rivia is indeed very captivating! Thank you for sharing your gaming interest!",
    "I like action movies.": "Action movies are very exciting! Do you have a favorite movie?",
    "I like 'Mad Max'.": "'Mad Max' is a great movie! I hope you find more exciting movies to watch!",
    "Do you listen to music?": "I don't listen to music, but I can suggest some popular songs for you! What genre do you like?",
    "I like pop music.": "Pop music is usually very upbeat! Is there a song you listen to often?",
    "I like the song 'Blinding Lights'.": "That's a very famous song! I hope you enjoy your time with the music!",
    "Do you know how to cook?": "I don't cook, but I can provide recipes and cooking tips for you! What dish are you looking for?",
    "I want to learn how to bake.": "Baking is an art! What kind of cake would you like to try?",
    "I want to try making a sponge cake.": "Sponge cake is delicious! I wish you success with your baking and hope you create many tasty dishes!",
    "Do you have any hobbies besides technology?": "Technology is my main field, but I enjoy exploring new topics with you! Is there a subject you'd like to discuss?",
    "I want to talk about traveling.": "Traveling is an exciting topic! Have you been anywhere recently?",
    "I just returned from Da Nang.": "Da Nang is a wonderful destination! I hope you had memorable experiences!",
    "Do you know about sports?": "Yes, I know about many sports. What sport do you like the most?",
    "I like soccer.": "Soccer is a very popular sport! Do you have a favorite team?",
    "I like Barcelona.": "Barcelona has many talented players! I hope you enjoy following the matches!",
    "I'm planning a beach trip.": "The beach is a great place to relax! I hope you have a fun and enjoyable trip!",
    "Do you know about culture and art?": "Yes, I know a lot about culture and art. What aspect would you like to learn about?",
    "I want to know about modern art.": "Modern art is very diverse! Thank you for sharing your interest in culture and art!",
    "Can you tell me about a famous artist?": "Certainly! Pablo Picasso is a famous artist, the founder of the Cubism movement, and known for works like 'Guernica.'",
    "Why is art important in life?": "Art helps us express emotions, convey messages, and explore ourselves, while also reflecting the culture and history of society.",
    "What are some popular art styles?": "Some popular art styles include Impressionism, Abstract, Realism, and Contemporary Art.",
    "Do you know about traditional art from different countries?": "Yes, every country has unique traditional art. For example, Vietnamese pottery is famous for its intricate designs.",
    "Can you talk about Japanese culture?": "Japanese culture is very diverse, from tea ceremonies and kimonos to manga and anime, reflecting both respect for tradition and modern creativity.",
    "Why does culture influence art?": "Culture shapes how artists perceive the world, influencing their style, themes, and creative methods.",
    "Can you recommend an art film?": "'Amélie' is a famous French art film known for its unique visual style and colorful story.",
    "Are there any prominent art exhibitions recently?": "Contemporary art exhibitions at major museums like MoMA in New York and Tate Modern in London often attract significant public attention.",
    "Do you know about classical music?": "Yes, classical music is often performed by musicians in concerts and includes works by composers like Beethoven, Mozart, and Bach.",
    "Is street art considered art?": "Street art, like graffiti, is a form of modern art that expresses the artist's ideas and social messages.",
    "What can AI do in everyday life?": "AI can assist in many areas, such as customer support, image recognition, and workflow optimization.",
    "What is a database management system?": "A database management system (DBMS) is software that helps create, manage, and retrieve data in a database.",
    "What is caching?": "Caching is the process of temporarily storing data to speed up future retrieval.",
    "Why is it important to protect personal information?": "Protecting personal information helps prevent misuse and safeguards your privacy.",
    "What is Git?": "Git is a version control system that tracks changes in source code and enables team collaboration.",
    "What is software testing?": "Software testing is the process of checking software to ensure it functions according to requirements.",
    "What are the benefits of cloud computing?": "Cloud computing saves costs, increases flexibility, and makes resource scaling easier.",
    "What is an API and why is it important?": "An API (Application Programming Interface) allows applications to communicate with each other, making software development more efficient.",
    "What is DevOps?": "DevOps is a methodology that combines development and operations, helping to speed up software releases and improve quality.",
    "What is an operating system?": "An operating system is software that manages hardware and software on a computer, allowing users to interact with it.",
    "What are the benefits of open-source software?": "Open-source software allows users to freely use, modify, and distribute it, promoting rapid development.",
    "How does blockchain work?": "Blockchain records transactions in a chain of information blocks, ensuring transparency and security.",
    "How does IoT impact everyday life?": "IoT connects devices in everyday life, enabling automation and optimization of processes.",
    "What is cybersecurity?": "Cybersecurity involves measures to protect computer systems and information from threats and attacks.",
    "Why is it important to use strong passwords?": "Strong passwords help protect your accounts from being hacked and misused.",
    "Why is learning to code important?": "Learning to code develops logical thinking, problem-solving skills, and expands career opportunities.",
    "What is Agile in software development?": "Agile is a flexible software development methodology that allows quick adjustments to customer requirements.",
    "Why is it important to back up data?": "Backing up data protects information from loss due to hardware failure or attacks.",
    "What are common types of cyberattacks?": "Common attacks include phishing, malware, DDoS, and man-in-the-middle attacks.",
    "Is creating a personal website easy to do?": "Yes, this project is very suitable for beginners, helping you practice HTML, CSS, and JavaScript.",
    "Is learning programming only useful for IT careers?": "No! Learning programming enhances critical thinking and problem-solving skills, which are useful in many fields.",
    "What special features does Stack Overflow have?": "Stack Overflow allows users to ask questions and receive answers from the community, helping solve problems quickly and efficiently.",
    "How does culture influence art?": "Culture influences art by shaping themes, styles, and how artists express themselves through their works.",
    "Are there any prominent artists in modern art?": "Ai Weiwei is a prominent artist in modern art, known for his works that reflect politics and society.",
    "How can art help us?": "Art can relieve stress, inspire creativity, and connect people through shared experiences.",
    "What art styles are popular right now?": "Contemporary art and digital art are very popular now, with many artists using technology to create their works.",
    "Do you have any hobbies besides programming?": "I enjoy exploring new technology and helping others learn. How about you?",
    "What kind of music do you like?": "I don’t have emotions, but many people like pop, rock, or classical music. What’s your preference?",
    "Do you like reading books?": "Reading is a great way to learn. What genres do you usually read?",
    "Do you like watching movies?": "Many people love movies. What is your favorite movie genre?",
    "Do you like playing video games?": "Video games are very diverse nowadays. What do you usually play?",
    "Do you have any sports-related hobbies?": "Many people love sports like soccer, basketball, or swimming. What’s your favorite?",
    "Do you like cooking?": "Cooking is an interesting art! Do you have a favorite dish?",
    "Do you like traveling?": "Traveling opens up many opportunities to experience new cultures. Where have you been, and where did you like the most?",
    "Do you like participating in art activities?": "Many people enjoy painting, photography, or writing. Do you have any art activities you like?",
    "Do you have any hobbies other than technology?": "Besides technology, many people enjoy nature or gardening. Do you have any hobbies related to nature?",
    "Do you like outdoor activities?": "Outdoor activities are very enjoyable! What do you usually like to do outside?",
    "I like hiking.": "That's great! Hiking not only helps you exercise but also relaxes you.",
    "Do you like participating in clubs or groups?": "Joining clubs can help you connect with people who share the same interests. Are you in any clubs?",
    "I'm in a book club.": "A book club is a great place to explore new works and discuss them with others!",
    "Do you like creating content?": "Creating content like blogging or making videos is very fun! Can you tell me about the content you've created?",
    "I've written a travel blog.": "That's great! Writing a travel blog can inspire many people to explore the world.",
    "Do you have any hobbies related to work?": "Many people find joy in their work. Is there anything you love about your current job?",
    "I like helping others.": "That's a wonderful hobby! Helping others can bring satisfaction and meaning to work.",
    "Do you like participating in cultural events?": "Cultural events are a great opportunity to experience art and traditions. Have you attended any events recently?",
    "I attended a music festival.": "Sounds exciting! Music festivals often provide great experiences and unforgettable memories.",
    "Do you like collecting items?": "Collecting is an interesting hobby! Are you collecting anything special?",
    "I collect stamps.": "Collecting stamps is a fascinating hobby! It not only gives you a chance to learn about history but also creates beautiful memories.",
    "Do you like trying new foods?": "Experimenting with new cuisine can be very exciting. What dish have you tried recently that you liked?",
    "I tried sushi for the first time.": "Sushi is a delicious and exciting dish! Many people love its fresh flavors.",
    "Do you like attending classes or workshops?": "Classes and workshops can provide a lot of useful knowledge. Have you attended any classes recently?",
    "I attended a cooking class.": "Cooking classes are very fun! Did you learn any special dishes?",
    "Do you like watching TV shows?": "There are many interesting TV shows. Do you have any favorites?",
    "I like watching reality shows.": "Reality shows are often very entertaining and bring lots of laughter!",
    "Do you like writing?": "Writing is a wonderful way to express yourself. Have you ever written short stories or poems?",
    "I've written a poem.": "That's wonderful! Poetry is a very creative form of art. Can you share the theme of that poem?"
}
    # Chuyển đổi đầu vào của người dùng thành chữ thường để so sánh dễ dàng hơn
    user_input = user_input.lower().strip()

    # Kiểm tra xem câu hỏi có trong từ điển không
    if user_input in responses:
        return responses[user_input]  # Trả về phản hồi tương ứng
    else:
        return "I'm sorry, I don't understand that. Could you please rephrase?"


# Tạo danh sách để ghi lại các cuộc hội thoại
conversation_log = []

def activate_mic():
    stop_listening = False  # Cờ để kiểm tra khi cần dừng

    # Chỉ nói "I'm listening" khi khởi động
    robot_mouth.say("I'm listening")
    robot_mouth.runAndWait()
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "I'm listening...\n")
    chat_display.config(state=tk.DISABLED)
    window.update()  # Cập nhật giao diện để hiển thị thông báo ngay lập tức

    while not stop_listening:
        with sr.Microphone() as source:
            audio = robot_ear.listen(source)  # Đổi từ recognizer.listen thành robot_ear.listen

            try:
                message = robot_ear.recognize_google(audio, language="en-US")  # Đổi từ recognizer.recognize_google thành robot_ear.recognize_google
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"You: {message}\n")
                chat_display.config(state=tk.DISABLED)
                chat_input.delete(0, tk.END)
                chat_input.insert(0, message)

                # Ghi lại lời nói ngay sau khi nhận diện
                conversation_log.append({"user": message})  # Ghi lại lời nói của người dùng

                # Kiểm tra nếu người dùng nói "stop" để dừng chương trình
                translated_input = message.lower()
                if translated_input == "today":
                    today = date.today()
                    response_message = f"Today is {today.strftime('%B %d, %Y')}."
                elif translated_input == "yesterday":
                    yesterday = date.today() - timedelta(days=1)  # Tính ngày hôm qua
                    response_message = f"Yesterday was {yesterday.strftime('%B %d, %Y')}."
                elif "in" in translated_input and "days" in translated_input:
                    # Tách số ngày từ câu
                    words = translated_input.split()
                    try:
                        index_of_in = words.index("in")
                        days = int(words[index_of_in + 1])  # Lấy số ngày
                        future_date = date.today() + timedelta(days=days)  # Tính ngày trong tương lai
                        response_message = f"The date in {days} days will be {future_date.strftime('%B %d, %Y')}."
                    except (ValueError, IndexError):
                        response_message = "I'm sorry, I didn't understand the number of days."
                elif "stop" in message.lower():
                    stop_listening = True
                    response_message = "Goodbye!"
                elif "weather" in message.lower():  # Kiểm tra câu hỏi về thời tiết
                    response_message = get_weather()
                elif "news" in message.lower():
                    response_message = get_news()
                    # Kiểm tra yêu cầu phát nhạc
                elif "play music" in message.lower():
                        # Lấy yêu cầu nhạc từ người dùng
                        user_request = message.lower().replace("play music", "").strip()
                        webbrowser.open(
                            "https://www.youtube.com/results?search_query=" + "+".join(user_request.split()))
                        response_message = f"Playing {user_request} for you on YouTube!"
                elif "turn on youtube" in message.lower():
                    webbrowser.open("https://www.youtube.com")
                    response_message = "Opening YouTube for you!"
                elif "turn on facebook" in message.lower():
                    webbrowser.open("https://www.facebook.com")
                    response_message = "Opening Facebook for you!"

                elif "turn on google" in message.lower():
                    webbrowser.open("https://www.google.com")
                    response_message = "Opening Google for you!"

                elif "turn on twitter" in message.lower():
                    webbrowser.open("https://www.twitter.com")
                    response_message = "Opening Twitter for you!"

                else:
                    # Kiểm tra trong mẫu cuộc trò chuyện
                    response_message = sample_conversations.get(message.lower(), "I'm not sure how to respond to that.")

                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Bot: {response_message}\n")
                chat_display.config(state=tk.DISABLED)

                # Chuyển phản hồi thành giọng nói
                robot_mouth.say(response_message)
                robot_mouth.runAndWait()

                # Ghi lại phản hồi của bot vào cuộc hội thoại
                conversation_log.append({"bot": response_message})  # Ghi lại phản hồi của bot

            except sr.UnknownValueError:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, "Could not understand audio.\n")
                chat_display.config(state=tk.DISABLED)

                robot_mouth.say("I could not understand the audio.")
                robot_mouth.runAndWait()

            except sr.RequestError as e:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Request error: {e}\n")
                chat_display.config(state=tk.DISABLED)

                robot_mouth.say(f"There was a request error: {e}")
                robot_mouth.runAndWait()
def save_conversations():
    with open("conversations.json", "w") as file:
        json.dump(conversations, file)

def load_conversations():
    if os.path.exists("conversations.json"):
        with open("conversations.json", "r") as file:
            return json.load(file)
    return {}

conversations = load_conversations()  # Tải các cuộc hội thoại khi khởi động

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

# Hàm xử lý hiệu ứng hover cho nút
def on_enter(event, button):
    button.config(bg="#004d40", fg="white")

def on_leave(event, button):
    button.config(bg="#00796b", fg="white")

# Hàm đăng nhập
def login_user():
    email = email_entry.get()
    password = password_entry.get()

    if email and password:
        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            for user in data:
                if user['email'] == email and user['password'] == password:
                    global current_user
                    current_user = user  # Lưu thông tin người dùng hiện tại
                    messagebox.showinfo("Success", f"Welcome {user['name']}!")
                    show_frame(home_frame)
                    # Lưu phiên đăng nhập nếu "Remember Me" được chọn
                    if remember_me_var.get() == 1:
                        with open("session.json", "w", encoding="utf-8") as session_file:  # Cũng chỉ định mã hóa ở đây
                            json.dump(user, session_file)
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

# Biến lưu trạng thái của checkbox "Lưu đăng nhập"
remember_me_var = tk.IntVar()

# Checkbox "Remember Me"
remember_me_checkbox = tk.Checkbutton(login_frame, text="Remember Me", variable=remember_me_var, font=("Arial", 12), bg="white", fg="#00796b")
remember_me_checkbox.pack(pady=5)

# Nút đăng nhập
login_button = tk.Button(login_frame, text="Sign In", font=("Arial", 14, "bold"), bg="#00796b", fg="white", width=20,
                         command=login_user)

# Thêm hiệu ứng hover cho nút
login_button.bind("<Enter>", lambda e: on_enter(login_button))
login_button.bind("<Leave>", lambda e: on_leave(login_button))

login_button.pack(pady=10)

# Nút chuyển sang trang đăng ký
signup_switch_button = tk.Button(login_frame, text="Don't have an account? Sign Up", font=("Arial", 12), bg="white",
                                 fg="#00796b", borderwidth=0, command=lambda: show_frame(signup_frame))
signup_switch_button.pack(pady=5)

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

                    # Lưu phiên đăng nhập nếu "Remember Me" được chọn
                    if remember_me_var.get() == 1:
                        with open("session.json", "w") as session_file:
                            # Lưu thông tin người dùng dưới dạng chuỗi JSON
                            json.dump(user, session_file)
                    return
            messagebox.showerror("Error", "Invalid email or password.")
        else:
            messagebox.showerror("Error", "No users found. Please register first.")
    else:
        messagebox.showerror("Error", "Both fields are required.")


# Hàm thêm cuộc hội thoại mới
def add_new_conversation():
    global current_conversation  # Đánh dấu rằng biến này là toàn cục
    conversation_name = f"Conversation 1"  # Tạo cuộc hội thoại mặc định
    conversations[conversation_name] = []  # Tạo cuộc hội thoại mới
    conversation_listbox.insert(tk.END, conversation_name)
    clear_chat_display()  # Xóa nội dung hiển thị chat khi tạo cuộc hội thoại mới
    current_conversation = conversation_name  # Cập nhật cuộc hội thoại hiện tại


# ---------- Giao diện đăng ký ----------

# Tiêu đề "Sign Up"
tk.Label(signup_frame, text="Sign Up", font=("Arial", 30, "bold"), fg="#00796b", bg="white").pack(pady=20)

# Ô nhập Họ tên
fullname_label = tk.Label(signup_frame, text="Full Name", font=("Arial", 14), bg="white")
fullname_label.pack(anchor=tk.W, padx=20, pady=5)
fullname_entry = tk.Entry(signup_frame, font=("Arial", 14), bg="#e0f2f1", width=40, relief="flat")
fullname_entry.pack(padx=20, pady=5)

# Ô nhập Email
email_label = tk.Label(signup_frame, text="Email", font=("Arial", 14), bg="white")
email_label.pack(anchor=tk.W, padx=20, pady=5)
signup_email_entry = tk.Entry(signup_frame, font=("Arial", 14), bg="#e0f2f1", width=40, relief="flat")
signup_email_entry.pack(padx=20, pady=5)

# Ô nhập Password
password_label = tk.Label(signup_frame, text="Password", font=("Arial", 14), bg="white")
password_label.pack(anchor=tk.W, padx=20, pady=5)
signup_password_entry = tk.Entry(signup_frame, font=("Arial", 14), bg="#e0f2f1", width=40, show="*", relief="flat")
signup_password_entry.pack(padx=20, pady=5)

# Thêm khoảng cách giữa các phần cho dễ nhìn
separator = tk.Frame(signup_frame, height=2, bd=1, relief="sunken", bg="#00796b")
separator.pack(fill=tk.X, padx=20, pady=20)

# Nút đăng ký
signup_button = tk.Button(signup_frame, text="Sign Up", font=("Arial", 14, "bold"), bg="#00796b", fg="white", width=20,
                          activebackground="#004d40", activeforeground="white", relief="flat", command=register_user)
signup_button.pack(pady=10)

# Nút quay lại trang đăng nhập
back_to_login_button = tk.Button(signup_frame, text="Back to Sign In", font=("Arial", 12), bg="white", fg="black",
                                 activebackground="#b2dfdb", borderwidth=1, command=lambda: show_frame(login_frame))
back_to_login_button.pack(pady=5)

# Tạo hover effect cho các nút
def on_enter( button):
    button.config(bg="#004d40", fg="white")

def on_leave(button):
    button.config(bg="#00796b", fg="white")

signup_button.bind("<Enter>", lambda e: on_enter(e, signup_button))
signup_button.bind("<Leave>", lambda e: on_leave(e, signup_button))

# ---------- Giao diện trang chủ ----------
tk.Label(home_frame, text=" Home Page", font=("Arial", 30, "bold"), fg="#00796b", bg="white").pack(pady=20, padx=50)
tk.Label(home_frame, text="This is the main application area.", font=("Arial", 14), bg="white").pack(pady=10)

# Thêm ảnh đại diện
avatar_image = Image.open("C:/Users/Acer/PycharmProjects/GUI SignIn_Login/avatar.png")  # Đường dẫn đến hình ảnh avatar
avatar_image = avatar_image.resize((80, 80), Image.LANCZOS)  # Thay đổi kích thước ảnh đại diện
avatar_photo = ImageTk.PhotoImage(avatar_image)

# Khung chứa avatar và các nút thông tin
header_frame = tk.Frame(home_frame, bg="white")
header_frame.place(x=10, y=10, width=400, height=100)
avatar_label = tk.Label(header_frame, image=avatar_photo, bg="white", bd=5, relief="groove")
avatar_label.place(x=0, y=0)

# Nút hiển thị thông tin người dùng
user_info_button = tk.Button(header_frame, text="User Info", font=("Arial", 12, "bold"), bg="#00796b", fg="white", command=show_user_info)
user_info_button.place(x=100, y=20)

# Nút đăng xuất
logout_button = tk.Button(header_frame, text="Logout", font=("Arial", 12, "bold"), bg="#d32f2f", fg="white", command=logout_user)
logout_button.place(x=200, y=20)

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

# Frame để chứa hai nút "New Conversation" và "Delete Conversation"
button_frame = tk.Frame(home_left_frame, bg="white")
button_frame.pack(side=tk.BOTTOM, pady=5)

# Nút để thêm một cuộc hội thoại mới (đặt trên nút xóa)
new_conversation_button = tk.Button(button_frame, text="New Conversation", font=("Arial", 12), bg="#00796b", fg="white",
                                    command=lambda: add_new_conversation_ing())
new_conversation_button.pack(side=tk.TOP, pady=5)  # Sử dụng side=tk.TOP để đặt nút theo chiều dọc

# Nút để xóa cuộc hội thoại (đặt dưới nút thêm)
delete_conversation_button = tk.Button(button_frame, text="Delete Conversation", font=("Arial", 12), bg="#d32f2f", fg="white",
                                       command=lambda: delete_selected_conversation())
delete_conversation_button.pack(side=tk.TOP, pady=5)

# ---------- Phần bên phải: Hiển thị và thao tác hội thoại ----------
# Tiêu đề
tk.Label(home_right_frame, text="Chat Interface", font=("Arial", 16, "bold"), fg="#00796b", bg="white").pack(pady=10)

# Tạo một frame để chứa Textbox và Scrollbar
chat_frame = tk.Frame(home_right_frame, bg="white")
chat_frame.pack(pady=10)

# Textbox để hiển thị nội dung hội thoại
chat_display = tk.Text(chat_frame, font=("Arial", 12), bg="#e0f7fa", fg="black", width=70, height=20, state="disabled")
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Thanh cuộn
scrollbar = tk.Scrollbar(chat_frame, command=chat_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Liên kết Scrollbar với Textbox
chat_display.config(yscrollcommand=scrollbar.set)

# Ô nhập văn bản
chat_input = tk.Entry(home_right_frame, font=("Arial", 14), bg="#e0f2f1", fg="black", width=50)
chat_input.pack(pady=10, side=tk.LEFT)

# Nút gửi tin nhắn
send_button = tk.Button(home_right_frame, text="Send", font=("Arial", 12), bg="#00796b", fg="white", command=send)
send_button.pack(pady=10, side=tk.RIGHT)

# Nút bật mic
mic_button = tk.Button(home_right_frame, text="🎤 Mic", font=("Arial", 12), bg="#00796b", fg="white", command=activate_mic)
mic_button.pack(pady=10, side=tk.RIGHT)  # Đặt nút bên cạnh nút Send

# --------- Các hàm hỗ trợ ----------
# Hàm thêm cuộc hội thoại mới
def add_conversation():
    conversation_listbox.insert(tk.END, f"Conversation {conversation_listbox.size() + 1}")

# Hàm để xóa cuộc hội thoại được chọn
def delete_selected_conversation():
    try:
        # Lấy chỉ mục của mục được chọn trong Listbox
        selected_index = conversation_listbox.curselection()

        if selected_index:
            # Xóa mục được chọn
            conversation_listbox.delete(selected_index)
            messagebox.showinfo("Deleted", "The selected conversation has been deleted.")
        else:
            messagebox.showwarning("No selection", "Please select a conversation to delete.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Hàm gửi tin nhắn
def send_message():
    message = chat_input.get()
    if message:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.config(state=tk.DISABLED)
        chat_input.delete(0, tk.END)

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
def display_conversation(event):  # Thay đổi ở đây để nhận đối số event
    # Lấy chỉ số mục được chọn
    selected_index = conversation_listbox.curselection()
    if selected_index:  # Kiểm tra nếu có mục được chọn
        conversation_name = conversation_listbox.get(selected_index)  # Lấy tên cuộc hội thoại
        # Tiếp tục với logic hiển thị nội dung cuộc hội thoại
        # Ví dụ: hiển thị tin nhắn trong chat_display
        chat_display.config(state="normal")  # Bật chế độ chỉnh sửa
        chat_display.delete(1.0, tk.END)  # Xóa nội dung hiện tại
        for message in conversations.get(conversation_name, []):
            chat_display.insert(tk.END, f"{message}\n")  # Hiển thị tin nhắn
        chat_display.config(state="disabled")  # Bỏ chế độ chỉnh sửa
# Gán sự kiện cho Listbox
conversation_listbox.bind('<<ListboxSelect>>', display_conversation)

# Chạy vòng lặp chính của giao diện
window.mainloop()