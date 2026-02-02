#!/usr/bin/env python3
"""
微信消息转发器 - Android 版本
简化版，确保构建成功
"""

import socket
import threading
import time
import json
from urllib.parse import urlparse, parse_qs, unquote

# 配置
PORT = 8999
CONFIG_FILE = "webhook.txt"

def log_message(message):
    """记录日志"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def handle_client(client_socket):
    """处理客户端请求"""
    try:
        # 接收请求
        request_data = client_socket.recv(1024).decode('utf-8', errors='ignore')
        
        if not request_data:
            client_socket.close()
            return
        
        # 解析请求
        lines = request_data.split('\r\n')
        if not lines:
            client_socket.close()
            return
            
        request_line = lines[0]
        parts = request_line.split()
        
        if len(parts) < 2:
            client_socket.close()
            return
            
        method, full_path = parts[0], parts[1]
        
        # 解析 URL
        parsed_url = urlparse(full_path)
        path = parsed_url.path
        
        if path == '/wechat':
            # 解析查询参数
            query = parse_qs(parsed_url.query)
            text = query.get('text', [''])[0]
            
            if text:
                try:
                    text = unquote(text)
                except:
                    pass
                
                log_message(f"收到消息: {text}")
                
                # 构建响应
                response_data = {
                    'success': True,
                    'message': '消息已接收',
                    'text': text,
                    'timestamp': time.time()
                }
                
                response_json = json.dumps(response_data, ensure_ascii=False)
                
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json; charset=utf-8\r\n"
                    f"Content-Length: {len(response_json.encode('utf-8'))}\r\n"
                    "\r\n"
                    f"{response_json}"
                )
            else:
                response = (
                    "HTTP/1.1 400 Bad Request\r\n"
                    "Content-Type: application/json\r\n"
                    "\r\n"
                    '{"error": "缺少消息文本"}'
                )
        else:
            # 默认响应
            html = f"""<!DOCTYPE html>
<html>
<head><title>微信转发器</title><meta charset="utf-8"></head>
<body>
    <h1>微信消息转发器</h1>
    <p>服务器运行中</p>
    <p>端口: {PORT}</p>
    <p>接口: <code>/wechat?text=消息内容</code></p>
</body>
</html>"""
            
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                "\r\n"
                f"{html}"
            )
        
        # 发送响应
        client_socket.send(response.encode('utf-8'))
        
    except Exception as e:
        log_message(f"处理请求错误: {e}")
    finally:
        client_socket.close()

def start_server():
    """启动服务器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', PORT))
    server.listen(5)
    
    log_message(f"微信转发器启动成功，端口: {PORT}")
    log_message(f"访问: http://localhost:{PORT}")
    log_message("按 Ctrl+C 停止服务器")
    
    try:
        while True:
            client_socket, client_address = server.accept()
            client_socket.settimeout(5)
            
            # 在新线程中处理请求
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        log_message("服务器停止")
    except Exception as e:
        log_message(f"服务器错误: {e}")
    finally:
        server.close()

if __name__ == '__main__':
    start_server()