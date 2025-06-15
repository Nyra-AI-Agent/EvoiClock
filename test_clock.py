#!/usr/bin/env python3
"""
EVOI Trading Clock 測試腳本
用於驗證核心功能是否正常運作
"""

import unittest
from datetime import datetime, time
from time_logic import TimeLogic
from price_tracker import PriceTracker
import tkinter as tk
from clock_widget import ClockWidget

class TestEVOIClock(unittest.TestCase):
    def setUp(self):
        """測試前的準備工作"""
        self.time_logic = TimeLogic()
        self.price_tracker = PriceTracker()
        
    def test_nyam_session(self):
        """測試 NYAM 交易時段判斷"""
        # 測試 NYAM 時段內
        test_time = time(22, 0)  # 22:00
        self.assertTrue(self.time_logic.is_nyam_session())
        
        # 測試非 NYAM 時段
        test_time = time(15, 0)  # 15:00
        self.assertFalse(self.time_logic.is_nyam_session())
        
    def test_kill_zone(self):
        """測試 Kill Zone 判斷"""
        # 測試第一個 Kill Zone
        test_time = time(21, 45)  # 21:45
        self.assertTrue(self.time_logic.is_kill_zone())
        
        # 測試第二個 Kill Zone
        test_time = time(22, 45)  # 22:45
        self.assertTrue(self.time_logic.is_kill_zone())
        
        # 測試非 Kill Zone
        test_time = time(22, 15)  # 22:15
        self.assertFalse(self.time_logic.is_kill_zone())
        
    def test_price_levels(self):
        """測試關鍵價位功能"""
        # 設置測試價格
        test_levels = {
            'K1': 18000.0,
            'K2': 17950.0,
            'K3': 17900.0,
            'K4': 17925.0
        }
        
        self.price_tracker.update_key_levels(test_levels)
        current_levels = self.price_tracker.get_key_levels()
        
        # 驗證價格設置
        for level, value in test_levels.items():
            self.assertEqual(current_levels[level], value)
            
    def test_role_analysis(self):
        """測試 1K 角色分析"""
        # 設置測試角色
        test_role = "Bullish"
        self.price_tracker.update_role_analysis(test_role)
        
        # 驗證角色設置
        current_role = self.price_tracker.get_current_role()
        self.assertEqual(current_role, test_role)
        
    def test_clock_widget(self):
        """測試時鐘元件"""
        root = tk.Tk()
        clock = ClockWidget()
        
        # 測試基本屬性
        self.assertEqual(clock.title(), "EVOI Trading Clock")
        self.assertTrue(clock.attributes('-topmost'))
        
        # 測試模式切換
        clock.set_mode("NYAM")
        self.assertEqual(clock.time_logic.current_mode, "NYAM")
        
        clock.set_mode("QUOTE")
        self.assertEqual(clock.time_logic.current_mode, "QUOTE")
        
        root.destroy()

def run_tests():
    """執行所有測試"""
    print("🧪 開始執行 EVOI Trading Clock 測試")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 創建測試套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEVOIClock)
    
    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 輸出測試結果摘要
    print("\n📊 測試結果摘要")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"執行測試: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失敗: {len(result.failures)}")
    print(f"錯誤: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_tests() 