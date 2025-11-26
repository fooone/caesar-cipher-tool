import tkinter as tk
from tkinter import messagebox

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("凯撒密码加密/解密工具")
        self.root.geometry("500x450")
        
        # 创建界面组件
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="凯撒密码加密/解密工具", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 明文输入区域
        plaintext_label = tk.Label(self.root, text="明文/密文:", font=("Arial", 12))
        plaintext_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.plaintext_text = tk.Text(self.root, height=5, width=50, font=("Arial", 11))
        self.plaintext_text.pack(padx=20, pady=5, fill="x")
        
        # 密钥输入区域
        key_label = tk.Label(self.root, text="密钥 (1-25):", font=("Arial", 12))
        key_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        key_frame = tk.Frame(self.root)
        key_frame.pack(padx=20, pady=5, fill="x")
        
        self.key_entry = tk.Entry(key_frame, width=10, font=("Arial", 12))
        self.key_entry.pack(side="left")
        self.key_entry.insert(0, "3")  # 默认密钥
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        encrypt_btn = tk.Button(button_frame, text="加密", command=self.encrypt,
                               font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
        encrypt_btn.pack(side="left", padx=10)
        
        decrypt_btn = tk.Button(button_frame, text="解密", command=self.decrypt,
                               font=("Arial", 12), bg="#2196F3", fg="white", width=10)
        decrypt_btn.pack(side="left", padx=10)
        
        clear_btn = tk.Button(button_frame, text="清空", command=self.clear,
                             font=("Arial", 12), bg="#f44336", fg="white", width=10)
        clear_btn.pack(side="left", padx=10)
        
        # 结果输出区域
        result_label = tk.Label(self.root, text="结果:", font=("Arial", 12))
        result_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.result_text = tk.Text(self.root, height=5, width=50, font=("Arial", 11))
        self.result_text.pack(padx=20, pady=5, fill="x")
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief="sunken", anchor="w", font=("Arial", 10))
        status_bar.pack(fill="x", padx=20, pady=10)
    
    def get_text_from_widget(self, widget):
        """安全地从文本组件获取内容"""
        try:
            content = widget.get("1.0", "end-1c")  # 获取除最后一个换行符外的所有内容
            return content.strip()
        except Exception as e:
            messagebox.showerror("错误", f"读取文本时出错: {str(e)}")
            return ""
    
    def set_text_to_widget(self, widget, text):
        """安全地设置文本组件内容"""
        try:
            widget.delete("1.0", "end")
            widget.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("错误", f"写入文本时出错: {str(e)}")
    
    def encrypt(self):
        """加密函数"""
        plaintext = self.get_text_from_widget(self.plaintext_text)
        if not plaintext:
            messagebox.showwarning("输入错误", "请输入要加密的文本！")
            return
        
        key_str = self.key_entry.get().strip()
        if not key_str:
            messagebox.showwarning("输入错误", "请输入密钥！")
            return
        
        try:
            key = int(key_str)
            if not 1 <= key <= 25:
                messagebox.showwarning("输入错误", "密钥必须在1-25之间！")
                return
        except ValueError:
            messagebox.showwarning("输入错误", "密钥必须是整数！")
            return
        
        # 执行加密
        ciphertext = self.caesar_cipher(plaintext, key)
        self.set_text_to_widget(self.result_text, ciphertext)
        self.status_var.set("加密完成")
    
    def decrypt(self):
        """解密函数"""
        ciphertext = self.get_text_from_widget(self.plaintext_text)
        if not ciphertext:
            messagebox.showwarning("输入错误", "请输入要解密的文本！")
            return
        
        key_str = self.key_entry.get().strip()
        if not key_str:
            messagebox.showwarning("输入错误", "请输入密钥！")
            return
        
        try:
            key = int(key_str)
            if not 1 <= key <= 25:
                messagebox.showwarning("输入错误", "密钥必须在1-25之间！")
                return
        except ValueError:
            messagebox.showwarning("输入错误", "密钥必须是整数！")
            return
        
        # 执行解密（使用负密钥）
        plaintext = self.caesar_cipher(ciphertext, -key)
        self.set_text_to_widget(self.result_text, plaintext)
        self.status_var.set("解密完成")
    
    def caesar_cipher(self, text, shift):
        """凯撒密码算法 - 符号跳过字母范围"""
        result = ""
        
        for char in text:
            if char.isupper():
                # 大写字母处理 - 在26个字母范围内循环
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            elif char.islower():
                # 小写字母处理 - 在26个字母范围内循环
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                # 其他ASCII字符处理 - 跳过字母范围
                ascii_val = ord(char)
                if 32 <= ascii_val <= 126:  # 可打印ASCII字符范围
                    new_ascii = ascii_val + shift
                    
                    # 调整结果，跳过字母范围
                    while (65 <= new_ascii <= 90) or (97 <= new_ascii <= 122):
                        if shift > 0:
                            new_ascii += 26  # 加密时跳过字母区域
                        else:
                            new_ascii -= 26  # 解密时跳过字母区域
                    
                    # 确保在可打印范围内循环
                    while new_ascii > 126:
                        new_ascii = 32 + (new_ascii - 127)
                    while new_ascii < 32:
                        new_ascii = 126 - (31 - new_ascii)
                    
                    result += chr(new_ascii)
                else:
                    # 非可打印ASCII字符保持不变
                    result += char
        
        return result    
    
    def clear(self):
        """清空所有输入和输出"""
        self.plaintext_text.delete("1.0", "end")
        self.result_text.delete("1.0", "end")
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, "3")
        self.status_var.set("已清空")

def main():
    # 创建主窗口
    root = tk.Tk()
    app = CaesarCipherApp(root)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()