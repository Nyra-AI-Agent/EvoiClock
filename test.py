#!/usr/bin/env python3
"""
EVOI Trading Clock - 測試腳本
驗證所有功能是否正常運行
"""

import tkinter as tk
import datetime
import sys
import os

def test_environment():
    """測試環境配置"""
    print("🧪 EVOI Trading Clock 環境測試")
    print("=" * 40)
    
    # 測試Python版本
    print(f"Python版本: {sys.version}")
    
    # 測試Tkinter
    try:
        root = tk.Tk()
        print(f"✅ Tkinter版本: {tk.TkVersion}")
        root.destroy()
    except Exception as e:
        print(f"❌ Tkinter錯誤: {e}")
        return False
    
    # 測試模組導入
    modules = ['datetime', 'threading', 'json', 'os']
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} 模組正常")
        except ImportError as e:
            print(f"❌ {module} 模組錯誤: {e}")
            return False
    
    print("✅ 環境測試通過")
    return True

def test_simple_gui():
    """測試簡單GUI顯示"""
    print("\n🎨 測試GUI顯示...")
    
    try:
        root = tk.Tk()
        root.title("EVOI測試視窗")
        root.geometry("400x300")
        root.configure(bg='#1a1a1a')
        
        # 測試標籤
        title = tk.Label(root, text="EVOI Trading Clock", 
                        font=('Arial', 16, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(pady=20)
        
        # 測試時間顯示
        time_var = tk.StringVar()
        time_label = tk.Label(root, textvariable=time_var,
                             font=('Courier New', 14),
                             bg='#1a1a1a', fg='#ffffff')
        time_label.pack(pady=10)
        
        # 測試按鈕
        def on_test():
            print("✅ 按鈕測試成功")
            time_var.set(f"測試時間: {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        test_btn = tk.Button(root, text="測試按鈕", command=on_test,
                            bg='#4CAF50', fg='white', font=('Arial', 12))
        test_btn.pack(pady=10)
        
        # 測試框架
        frame = tk.LabelFrame(root, text="測試框架", 
                             bg='#2d2d2d', fg='#ffffff')
        frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(frame, text="如果您能看到這些文字，GUI功能正常",
                bg='#2d2d2d', fg='#ffff00').pack(pady=10)
        
        # 關閉按鈕
        close_btn = tk.Button(root, text="關閉測試", command=root.quit,
                             bg='#f44336', fg='white', font=('Arial', 12))
        close_btn.pack(pady=10)
        
        print("✅ GUI測試視窗已創建")
        print("   如果能看到視窗和文字，請點擊'測試按鈕'")
        print("   測試完成後請關閉視窗")
        
        # 初始更新時間
        time_var.set(f"當前時間: {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        root.mainloop()
        print("✅ GUI測試完成")
        return True
        
    except Exception as e:
        print(f"❌ GUI測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_time_functions():
    """測試時間相關功能"""
    print("\n⏰ 測試時間功能...")
    
    try:
        now = datetime.datetime.now()
        print(f"當前時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 測試NYAM時段計算
        nyam_start = now.replace(hour=21, minute=30, second=0, microsecond=0)
        nyam_end = now.replace(hour=23, minute=0, second=0, microsecond=0)
        
        if now.hour < 12:  # 深夜情況
            nyam_start = nyam_start - datetime.timedelta(days=1)
            nyam_end = nyam_end - datetime.timedelta(days=1)
        
        print(f"NYAM開始: {nyam_start.strftime('%H:%M:%S')}")
        print(f"NYAM結束: {nyam_end.strftime('%H:%M:%S')}")
        
        if nyam_start <= now <= nyam_end:
            print("✅ 當前在NYAM時段內")
        else:
            print("⏰ 當前不在NYAM時段")
        
        # 測試Kill Zone
        kill_zones = {
            'Asian': ('07:00', '11:00'),
            'London': ('15:00', '18:00'),
            'NYAM': ('21:30', '23:00'),
        }
        
        current_time = now.strftime("%H:%M")
        print(f"當前時間: {current_time}")
        
        for zone, (start, end) in kill_zones.items():
            start_time = datetime.datetime.strptime(start, "%H:%M").time()
            end_time = datetime.datetime.strptime(end, "%H:%M").time()
            
            if start_time <= now.time() <= end_time:
                print(f"🔥 當前在 {zone} Kill Zone")
            else:
                print(f"   {zone}: {start}-{end}")
        
        print("✅ 時間功能測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 時間功能測試失敗: {e}")
        return False

def test_file_operations():
    """測試文件操作"""
    print("\n💾 測試文件操作...")
    
    try:
        # 測試JSON讀寫
        import json
        
        test_data = {
            'key_levels': {'K1': 20000.0, 'K2': 19950.0},
            'current_price': 19975.0,
            'test_time': datetime.datetime.now().isoformat()
        }
        
        # 寫入測試
        with open('evoi_test.json', 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print("✅ JSON寫入測試成功")
        
        # 讀取測試
        with open('evoi_test.json', 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        print("✅ JSON讀取測試成功")
        
        # 清理測試文件
        os.remove('evoi_test.json')
        print("✅ 文件清理完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 文件操作測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 EVOI Trading Clock 完整測試")
    print("=" * 50)
    print("這個測試將驗證所有核心功能")
    print()
    
    tests = [
        ("環境配置", test_environment),
        ("時間功能", test_time_functions), 
        ("文件操作", test_file_operations),
        ("GUI顯示", test_simple_gui),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 測試通過")
            else:
                print(f"❌ {test_name} 測試失敗")
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")
    
    print(f"\n{'='*50}")
    print(f"測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！EVOI Trading Clock 可以正常運行")
        print("\n下一步：運行主程式")
        print("指令: python main.py")
    else:
        print("⚠️  部分測試失敗，請檢查環境配置")
    
    print("\n按任意鍵結束...")
    input()

if __name__ == "__main__":
    main()