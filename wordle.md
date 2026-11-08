# Wordle FastAPI Server & Pygame Client (極速實作版)

這是一個基於 Python 實作的 Wordle 遊戲專案，包含後端 FastAPI 伺服器與前端 Pygame 桌面客戶端。
本指南專為**快速測試與學校電腦環境**設計，不使用虛擬環境與 Git 指令，採用最簡單的圖形化介面與直接安裝法。

## 階段一：準備工作與安裝套件

1. **建立專案資料夾：** 在桌面上新增一個資料夾，命名為 `wordle-api`。
2. **使用 VS Code 開啟：** 打開 VS Code，點擊左上角「檔案」>「開啟資料夾」，選擇剛剛建立的 `wordle-api`。
3. **開啟終端機並安裝套件：** 
   點擊上方選單「終端機」>「新增終端機」。在下方出現的終端機輸入以下指令並按 Enter（直接安裝到系統環境）：
   ```bash
   pip install fastapi uvicorn[standard] requests pygame
   ```

## 階段二：建立伺服器 (Server) 與本機測試

1. **新增 main.py：** 在 VS Code 建立新檔案 `main.py`，貼上老師提供的 FastAPI 伺服器程式碼並存檔。
2. **新增 requirements.txt：** 建立新檔案 `requirements.txt`，貼上以下內容並存檔：
   ```text
   fastapi
   uvicorn[standard]
   ```
3. **啟動本機伺服器：** 在終端機輸入以下指令啟動：
   ```bash
   python -m uvicorn main:app --reload
   ```
4. **驗證：** 打開瀏覽器前往 `http://127.0.0.1:8000/docs`。若看見 API 測試文件畫面即代表成功。（請保持終端機開啟）

## 階段三：建立遊戲畫面 (Client) 與連線測試

1. **新增 client.py：** 在 VS Code 建立新檔案 `client.py`，貼上老師提供的 Pygame 客戶端程式碼並存檔。
2. **確認網址設定：** 確認 `client.py` 內的網址為本機地址：
   ```python
   API_BASE_URL = "http://127.0.0.1:8000"
   ```
3. **開啟第二個終端機：** 點擊 VS Code 終端機面板右側的 **「+」號圖示**，開啟新的終端機分頁。
4. **啟動遊戲：** 在新終端機輸入以下指令啟動遊戲：
   ```bash
   python client.py
   ```
5. **測試遊玩：** 在彈出的視窗中猜測英文單字。測試無誤後，關閉遊戲視窗，並在兩個終端機皆按下 `Ctrl + C` 終止程式。

## 階段四：上傳 GitHub (網頁拖曳法)

1. 登入 GitHub，點擊右上角「+」>「New repository」。
2. 名稱填寫 `wordle-api`，直接滑到最下方點擊「Create repository」。
3. 在下一個畫面，點擊藍色文字 **「uploading an existing file」**。
4. 將電腦裡的 `main.py` 和 `requirements.txt` 拖曳進網頁的虛線框內。
5. 檔案讀取完畢後，點擊下方綠色的「Commit changes」按鈕完成上傳。

## 階段五：部署至 Render 與最終連線

1. 登入 [Render](https://render.com/)，點選右上角 **New** > **Web Service**。
2. 選擇「Build and deploy from a Git repository」，連結並選擇你剛建立的 `wordle-api` 儲存庫。
3. 填寫部署設定：
   * **Name:** 隨意命名 (例如 `my-wordle-api`)
   * **Runtime / Language:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. 選擇 Free 方案，點擊最底下的 **Deploy Web Service**。等待部署日誌跑完並顯示綠色的 **Live**。
5. **更新 Client 網址：** 複製 Render 分配給你的專屬網址，回到 VS Code 修改 `client.py`：
   ```python
   # 將原本的本機網址替換為雲端網址
   API_BASE_URL = "https://你的專屬網址.onrender.com"
   ```
6. 存檔後再次執行 `python client.py`，你的桌面遊戲現在已成功連線到雲端伺服器！