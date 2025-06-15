# 使用 Windows Server Core 作為基礎映像
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# 設置工作目錄
WORKDIR /app

# 安裝 Python 3.8
RUN powershell -Command \
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe -OutFile python.exe ; \
    Start-Process -FilePath python.exe -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1' -Wait ; \
    Remove-Item python.exe

# 複製專案文件
COPY . .

# 安裝依賴
RUN pip install -r requirements.txt

# 設置環境變數
ENV PYTHONPATH=/app

# 運行測試
CMD ["python", "main.py"] 