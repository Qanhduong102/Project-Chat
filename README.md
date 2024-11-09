# Voice Chatbot

## Mô tả dự án 
Dự án Voice Chatbot là một ứng dụng chatbot hỗ trợ giao tiếp với người dùng thông qua giọng nói. Chatbot có khả năng hiểu và phản hồi các yêu cầu bằng cách sử dụng công nghệ xử lý ngôn ngữ tự nhiên (NLP) và chuyển đổi giọng nói thành văn bản (Speech-to-Text) và ngược lại (Text-to-Speech). Dự án này thích hợp để phát triển các kỹ năng về xử lý ngôn ngữ tự nhiên, lập trình, và học máy.

## Mục tiêu 
1. Xây dựng một chatbot có thể hiểu và phản hồi yêu cầu của người dùng qua giọng nói.
2. Tích hợp tính năng chuyển đổi giọng nói thành văn bản và ngược lại.
3. Áp dụng các mô hình học máy cơ bản để cải thiện khả năng hiểu ngữ cảnh của chatbot.
4. Giúp sinh viên làm quen với việc sử dụng các API về NLP và TTS (Text-to-Speech) & STT (Speech-to-Text).

## Yêu cầu hệ thống 
+ Python 3.7 trở lên
+ Các thư viện Python: 
    1. **SpeechRecognition**: hỗ trợ chuyển đổi giọng nói thành văn bản
    2. **gTTS**: để chuyển đổi văn bản thành giọng nói
    3. **transformers**: dùng để tích hợp các mô hình NLP tiên tiến như BERT hoặc GPT
    4. **pyaudio**: hỗ trợ ghi âm giọng nói
+ Microphone và loa hoặc tai nghe

## Cài đặt 
1. Clone kho mã nguồn
```c
git clone https://github.com/Qanhduong102/Project-Chat.git
cd Project-Chat
```
1. Cài đặt các thư viện cần thiết Sử dụng pip để cài đặt các thư viện:
```c 
pip install SpeechRecognition gTTS transformers pyaudio
```
1. Cấu hình API cho NLP (nếu cần) Nếu bạn sử dụng mô hình AI từ bên thứ ba (như OpenAI API hoặc Hugging Face Transformers), hãy đảm bảo rằng bạn đã đăng ký API key và thiết lập các biến môi trường cho khóa API này.

## Hướng dẫn sử dụng 
1. Khởi động chatbot: 
```c
python main.py
```
2. Sử dụng chatbot:
+ **Bước 1**: Nói vào microphone để đặt câu hỏi hoặc yêu cầu.
+ **Bước 2**: Chatbot sẽ chuyển đổi giọng nói của bạn thành văn bản và xử lý câu hỏi.
+ **Bước 3**: Chatbot phản hồi bằng cách đọc to câu trả lời hoặc hiển thị câu trả lời trên màn hình.
3. Dừng chatbot: Nhấn Ctrl + C để thoát chương trình.
## Cấu trúc thư mục 
+ **Javis.py**: Tệp chính để chạy chatbot.
+ **Signln_Login.py**: Giao diện của chatbot

## Tài liệu tham khảo 
+ **https://pypi.org/project/SpeechRecognition/**
+ **https://pypi.org/project/gTTS/**
+ **https://TransformersDocumentation/**

## Ghi chú 
+ Hãy đảm bảo rằng bạn có kết nối internet để sử dụng các API yêu cầu dữ liệu từ xa.
+ Nếu gặp vấn đề về microphone, kiểm tra cài đặt âm thanh của hệ thống hoặc đảm bảo đã cấp quyền truy cập microphone cho chương trình.

## Đóng góp 
Chúng mình luôn chào đón các đóng góp từ cộng đồng. Nếu bạn có ý tưởng hoặc phát hiện lỗi, vui lòng tạo Issue hoặc gửi Pull Request trên GitHub. Xin cảm ơn! 


