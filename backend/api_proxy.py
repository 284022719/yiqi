#!/usr/bin/env python3
"""
本地开发 API 代理服务器
用于在本地开发环境中模拟 Netlify Functions
"""

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import subprocess

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from src.database.api import handle_api_request
except ImportError as e:
    print(f"导入错误: {e}")
    print(f"当前路径: {current_dir}")
    print(f"Python 路径: {sys.path}")
    sys.exit(1)

class APIProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 解析 URL 和查询参数
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # 提取 action 参数
            action = query_params.get('action', [None])[0]
            
            if not action:
                self.send_error_response('缺少 action 参数')
                return
            
            # 构建参数字典
            params = {}
            for key, value in query_params.items():
                if key != 'action':
                    params[key] = value[0] if value else ''
            
            # 调用数据库 API
            result = handle_api_request(action, params)
            
            # 返回 JSON 响应
            self.send_json_response(result)
            
        except Exception as e:
            print(f"API 代理错误: {str(e)}")
            self.send_error_response(f'服务器内部错误: {str(e)}')
    
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_json_response(self, data):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_body = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response_body.encode('utf-8'))
    
    def send_error_response(self, error_message):
        """发送错误响应"""
        error_data = {
            'success': False,
            'error': error_message
        }
        self.send_json_response(error_data)
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[API代理] {format % args}")

def run_server(port=3001):
    """运行 API 代理服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIProxyHandler)
    print(f"API 代理服务器运行在 http://localhost:{port}")
    print("按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3001
    run_server(port) 