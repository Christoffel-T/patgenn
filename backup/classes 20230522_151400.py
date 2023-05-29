from __future__ import print_function
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from datetime import datetime
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import base64
import ctypes
import os
import sys
import time
import tkinter as tk
import pyautogui
import requests

class Variables:
    class CssSelectors:
        evatcoin_leverage = "[id^='el-popover-'] > div.list > div:nth-child(3)"
        evatcoin_open_confim = 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary'
        evatcoin_close_long = 'body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div:nth-child(4) > div.px-2.flex-fill.mb-4 > button'
        evatcoin_close_short = 'body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div:nth-child(4) > div:nth-child(2) > button'
        evatcoin_close_confirm = 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary'
        evatcoin_current_price = 'body > div > main > div > div.page-top.d-flex.pt-2 > div.kline-box.flex-fill.mr-2 > div.coin-change.d-flex.align-items-center.py-2.pl-4.heading.justify-content-between > div.d-flex.align-items-center > div.price.px-3.border-right > span.current'

    class XPaths:
        evatcoin_perpetual = '/html/body/div[1]/header/nav/div/ul[1]/li[4]/a'
        evatcoin_leverage = '/html/body/div[1]/main/div/div[1]/div[3]/div[1]/div[3]/span/span/div'
        evatcoin_leverage_selector = '/html/body/div[2]/div[1]'
        evatcoin_slider = '/html/body/div[1]/main/div/div[1]/div[3]/div[2]/div[3]/div/div/div[3]'
        evatcoin_buy_long = '/html/body/div[1]/main/div/div[1]/div[3]/div[2]/div[5]/div[1]/button'
        evatcoin_sell_short = '/html/body/div[1]/main/div/div[1]/div[3]/div[2]/div[5]/div[2]/button'
        evatcoin_balance = '/html/body/div/main/div/div[2]/div[2]/div/div/div[2]/div[1]/div[2]'
        evatcoin_direction = '/html/body/div[1]/main/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td[4]'
        evatcoin_opening_price = '/html/body/div[1]/main/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td[8]'
        evatcoin_latest_price = '/html/body/div[1]/main/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td[9]'
        evatcoin_forced_closing_price = '/html/body/div[1]/main/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td[10]'
        evatcoin_latest_unrealized_profit_loss = '/html/body/div[1]/main/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td[11]'
        evatcoin_yield = '/html/body/div/main/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td[12]'
        evatcoin_profile = '/html/body/div[1]/header/nav/div/ul[2]/li[4]/a/img'
        tradingview_logout_btn = '/html/body/div[6]/div/span/div[1]/div/div/div[8]/span[2]/span/span'
        evatcoin_open_position = '/html/body/div[1]/main/div/div[1]/div[3]/div[1]/div[1]/a'
        evatcoin_open_quantity = '/html/body/div[1]/main/div/div[1]/div[3]/div[2]/div[2]/input'
        evatcoin_close_position = '/html/body/div[1]/main/div/div[1]/div[3]/div[1]/div[2]/a'
        evatcoin_close_quantity = '/html/body/div/main/div/div[1]/div[3]/div[2]/div[2]/input'
        evatcoin_leaf_bought = '/html/body/div[1]/main/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td[5]'
        tradingview_logs = {}
        for i in range(1, 10):
            tradingview_logs[i] = f'/html/body/div[2]/div[6]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[{i+1}]'
        tradingview_charts = {}
        for i in range(1, 9):
            tradingview_charts[i] = f'/html/body/div[2]/div[5]/div[{i+1}]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[8]/div[2]'

    class Misc:
        state_break = False
        screen_width, screen_height = pyautogui.size()
        url_tradingview = r'https://www.tradingview.com/chart'
        url_evatcoin = r'https://evatcoin.com/#/contract'
        url_github = 'https://api.github.com/repos/Christoffel-T/fiverr-pat-20230331/contents/'
        filename = 'Yields.csv'
        chrome_user_profile = os.environ['USERPROFILE'] + r"\AppData\Local\Google\Chrome\User Data"
        tradingview_charts_data = {}
        for i in range(1, 9):
            tradingview_charts_data[i] = '-'
        leverage = 100

class FloatingText:
    def __init__(self, master):
        self.master = master
        self.text = tk.StringVar()
        self.text.set("Hello World!")
        self.text_box = tk.Text(master, width=85, height=7, wrap="word", font=("Arial", 11))
        self.text_box.insert("1.0", self.text.get())
        self.text_box.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")
        self.ok_button = tk.Button(master, text='OK', command=self.hide_ok_button)
        self.ok_button_pressed = None
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.resizable(False, False)
        self.master.wm_attributes("-topmost", True)
        self.master.geometry(f"+{10}+{int(Variables.Misc.screen_height*0.6)}")

    def update_text(self, new_text, show_ok=False):
        if Variables.Misc.state_break:
            print('Stopped')
            return
        # self.text_box.delete("1.0", "end")
        # self.text_box.insert("1.0", new_text)
        # self.master.update()
        print(new_text)
        if show_ok:
            pass
        #     self.show_ok_button()
        return new_text

    def hide_ok_button(self):
        self.ok_button.grid_forget()
        self.ok_button_pressed = True
        self.master.update()

    def show_ok_button(self):
        self.ok_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="s")
        self.ok_button_pressed = False
        self.master.update()
        self.wait_for_ok_button()

    def wait_for_ok_button(self):
        while not self.ok_button_pressed:
            if Variables.Misc.state_break:
                print('Stopped')
                sys.exit()
            self.master.update()
        self.ok_button_pressed = False

    def hide_floating_text(self):
        self.master.withdraw()

    def show_floating_text(self):
        self.master.update()
        self.master.deiconify()
        self.master.lift()

class MainFunction:
    def __init__(self, floating_text_obj, root):
        self.output = []
        self.floating_text_obj = floating_text_obj
        self.root = root
        self.LocalSheets = None
        self.trigger_open_30 = 0
        self.count_close = 0
        self.cumulative_diff = float(0)
        self.count_open_short = 0
        self.count_open_long = 0
        self.cumulative_percent_str2 = ''
        self.cumulative_value_str2 = ''
        self.cumulative_percent2 = float(0)
        self.cumulative_value2 = float(0)
        self.cumulative_value_str = ''
        self.cumulative_percent_str = ''
        self.subtext1 = ''
        self.cumulative_percent = float(0)
        self.cumulative_value = float(0)
        self.count_consecutive = 0
        self.anchor_price_5_min = float(0)
        self.anchor_price = float(0)
        self.v_previous_price = float(0)
        self.trigger_open = False
        self.trigger_close_count = 0
        self.alerts_csv_file = 'alerts.csv'
        self.trigger_open_count_reset = 3
        self.list_reverses = []
        self.v_yield_temp_str = ''
        self.temp_yields = []
        self.note = ''
        self.v_state_yield_temp = False
        self.v_yield_temp = float(0)
        self.v_aop_temp = float(0)
        self.v_aop = float(0)
        self.v_bal = float(150)
        self.v_bal_leaf = float(40)
        self.v_diff = float(0)
        self.v_latest_price = float(0)
        self.v_esp = float(0)
        self.v_unrealized = float(0)
        self.v_yield = float(0)
        self.v_current_time_str = self.f_current_time()
        self.v_bal_open = self.v_bal
        self.yields = [float(0) for _ in range(60)]

        self.trigger_open_count = 0
        self.wait = None
        self.csv_columns = 30
        self.csv_empty_line = self.format_csv_string('')
        self.textbox_row5 = 'ROW5'
        self.textbox_row4 = 'ROW4'
        self.textbox_row3 = 'ROW3'
        self.textbox_row2 = 'ROW2'
        self.textbox_row1 = 'ROW1'
        self.trigger_close = False
        self.trigger_open_short = False
        self.trigger_open_long = False
        self.v_tp_sl_str = float(0)
        self.v_reason = 'CLOSED'
        self.percent_stop_loss_reset = float(-2000)
        self.percent_stop_loss = self.percent_stop_loss_reset
        self.percent_take_profit_reset = float(3)
        self.percent_take_profit = self.percent_take_profit_reset
        self.last_reset_time = datetime.now().replace(second=0, microsecond=0)
        self.last_reset_time2 = datetime.now().replace(second=0, microsecond=0)
        self.last_reset_time_30 = datetime.now().replace(second=0, microsecond=0)
        self.last_reset_time_googlesheet = datetime.now().replace(second=0, microsecond=0)
        self.alerts_to_trigger_open_long = 2
        self.alerts_to_trigger_open_short = 2
        self.v_stop_loss = False
        self.short_closed = False
        self.long_closed = False
        self.v_failed = False
        self.v_direction = 'NO_POS'
        self.count_short = 0
        self.count_long = 0
        self.rate_limit_github = 0
        self.raw_data_message = '-'
        self.current_time_utc = None
        self.alert_new_time_obj = None
        self.alert_new = 'neutral'
        self.alert_new_time = ''
        self.driver = None
        self.state_break = False
        self.v_reload = False
        self.driver = None
        self.prices_list = []
        self.alerts_dict = {
            'BWMA': ['BWMA', '-', '-'],
        }

    def f_main1(self):
        self.f_open_chrome()
        self.floating_text_obj.update_text('RUNNING')
        self.rate_limit_github = 0
        self.f_update_textbox('SCRIPT_STARTED', True, True)
        self.trigger_open_count = 0
        self.LocalSheets = LocalSheets()
        while True:
            if self.f_main2() == 'break':
                break

    def f_main2(self):
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        print(f'\n=== Loop at: {self.f_current_time()}')
        now = datetime.now()
        if Variables.Misc.state_break:
            print('Stopped')
            return 'break'

        if (now - self.last_reset_time_googlesheet).seconds >= 5:
            self.last_reset_time_googlesheet = now.replace(microsecond=0)
            if self.LocalSheets.append(self.output):
                self.output = []

        self.f_get_data_tradingview()
        self.f_get_data_evatcoin()

        now = datetime.now()
        subtext2 = ''

        if now.minute in [24, 54]:
            self.anchor_price_5_min = self.v_latest_price

        """
        if (now.minute == 29 and now.second >= 30) or (now.minute == 59 and now.second >= 30):
            if self.anchor_price_5_min != float(0):
                diff = self.v_latest_price - self.anchor_price_5_min
                if self.v_latest_price >= self.anchor_price_5_min:
                    subtext2 = f" - last_5_min_increase_by: {'{:.2f}'.format(diff)} ({'{:.4f}'.format(diff / self.anchor_price_5_min)}%)"
                if self.v_latest_price < self.anchor_price_5_min:
                    subtext2 = f" - last_5_min_decrease_by: {'{:.2f}'.format(diff)} ({'{:.4f}'.format(diff / self.anchor_price_5_min)}%)"
        """

        if self.alerts_dict['BWMA'][1] != self.alerts_dict['BWMA'][2] and self.alerts_dict['BWMA'][2] != '-':
            self.f_update_textbox('ALERT_REVERSE', True, True)
            self.cumulative_value2 = float(0)
            self.cumulative_percent2 = float(0)
        else:
            cumulative_value_previous2 = self.cumulative_value2
            if self.v_previous_price != float(0):
                self.cumulative_value2 += self.v_latest_price - self.v_previous_price
            if self.v_latest_price == self.v_previous_price:
                if self.cumulative_value2 > 0:
                    self.cumulative_value_str2 = f"+{'{:.2f}'.format(self.cumulative_value2)}"
                else:
                    self.cumulative_value_str2 = f"{'{:.2f}'.format(self.cumulative_value2)}"

                if self.cumulative_percent > 0:
                    self.cumulative_percent_str2 = f"+{'{:.2f}'.format(self.cumulative_percent2)}"
                else:
                    self.cumulative_percent_str2 = f"{'{:.2f}'.format(self.cumulative_percent2)}"

            elif cumulative_value_previous2 != float(0):
                self.cumulative_percent2 = 100 * (self.cumulative_value2 - cumulative_value_previous2) / abs(
                    cumulative_value_previous2)
                if self.cumulative_percent2 > 0:
                    self.cumulative_percent_str2 = f"+{'{:.2f}'.format(self.cumulative_percent2)}"
                else:
                    self.cumulative_percent_str2 = f"{'{:.2f}'.format(self.cumulative_percent2)}"

            if self.cumulative_value2 > 0:
                self.cumulative_value_str2 = f"+{'{:.2f}'.format(self.cumulative_value2)}"
            else:
                self.cumulative_value_str2 = f"{'{:.2f}'.format(self.cumulative_value2)}"

        if (now - self.last_reset_time2).seconds >= 60 and (now.minute in [00, 30]):
            self.trigger_open_30 = 0
            self.last_reset_time2 = now.replace(second=0, microsecond=0)

        if (now - self.last_reset_time_30).seconds >= 120 and (now.minute in [00, 10, 20, 30, 40, 50]):
            self.cumulative_value = float(0)
            self.cumulative_percent = float(0)
            self.cumulative_value_str = f"{'{:.2f}'.format(self.cumulative_value)}"
            self.cumulative_percent_str = f"{'{:.2f}'.format(self.cumulative_percent)}"
            self.last_reset_time_30 = now.replace(second=0, microsecond=0)
            self.f_update_textbox('10_MIN', True, True)
        else:
            cumulative_value_previous = self.cumulative_value
            if self.v_previous_price != float(0):
                self.cumulative_value += self.v_latest_price - self.v_previous_price

            self.cumulative_diff = self.cumulative_value - cumulative_value_previous

            if self.v_latest_price == self.v_previous_price:
                if self.cumulative_value > 0:
                    self.cumulative_value_str = f"+{'{:.2f}'.format(self.cumulative_value)}"
                else:
                    self.cumulative_value_str = f"{'{:.2f}'.format(self.cumulative_value)}"

                if self.cumulative_percent > 0:
                    self.cumulative_percent_str = f"+{'{:.2f}'.format(self.cumulative_percent)}"
                else:
                    self.cumulative_percent_str = f"{'{:.2f}'.format(self.cumulative_percent)}"
            elif cumulative_value_previous != float(0):
                self.cumulative_percent = 100 * (self.cumulative_value - cumulative_value_previous) / abs(
                    cumulative_value_previous)
                if self.cumulative_percent > 0:
                    self.cumulative_percent_str = f"+{'{:.2f}'.format(self.cumulative_percent)}"
                else:
                    self.cumulative_percent_str = f"{'{:.2f}'.format(self.cumulative_percent)}"

            if self.cumulative_value > 0:
                self.cumulative_value_str = f"+{'{:.2f}'.format(self.cumulative_value)}"
            else:
                self.cumulative_value_str = f"{'{:.2f}'.format(self.cumulative_value)}"

            """
            if cumulative_value_previous < 0 and self.cumulative_value > 0 and self.cumulative_diff >= 2.5:
                self.count_open_long = 1
            elif cumulative_value_previous > 0 and self.cumulative_value < 0 and self.cumulative_diff <= -2.5:
                self.count_open_short = 1
            """

            if self.cumulative_value >= 2.5:
                self.count_open_short = 0
                if self.v_latest_price != self.v_previous_price:
                    self.count_open_long += 1
            elif self.cumulative_value <= -2.5:
                self.count_open_long = 0
                if self.v_latest_price != self.v_previous_price:
                    self.count_open_short += 1
            else:
                self.count_open_long = 0
                self.count_open_short = 0

        if (now - self.last_reset_time).seconds >= 86400:
            self.LocalSheets.backup()
            self.last_reset_time = now.replace(second=0, microsecond=0)

        if self.v_previous_price == 0:
            self.v_previous_price = self.v_latest_price

        if self.v_latest_price > self.v_previous_price:
            if self.count_consecutive < 0:
                self.count_consecutive = 0
            if self.count_consecutive == 0:
                self.anchor_price = self.v_previous_price
            self.count_consecutive += 1
        elif self.v_latest_price < self.v_previous_price:
            if self.count_consecutive > 0:
                self.count_consecutive = 0
            if self.count_consecutive == 0:
                self.anchor_price = self.v_previous_price
            self.count_consecutive -= 1

        self.subtext1 = ''
        percent_diff = 0
        diff = self.v_latest_price - self.anchor_price
        if self.anchor_price != 0:
            percent_diff = (diff / self.anchor_price) * 100
        percent_diff_str = f"{'{:.4f}'.format(percent_diff)}%"

        if self.count_consecutive > 0:
            self.subtext1 = f"con_p_increase={abs(self.count_consecutive)} - by: {'{:.2f}'.format(diff)} ({percent_diff_str})"
        elif self.count_consecutive < 0:
            self.subtext1 = f"con_p_decrease={abs(self.count_consecutive)} - by: {'{:.2f}'.format(diff)} ({percent_diff_str})"

        self.v_previous_price = self.v_latest_price
        text = f'{self.note}{self.subtext1}{subtext2}'
        self.f_update_textbox(f'{text}')

        if self.v_direction == 'NO_POS':
            self.trigger_close = False
            if self.count_short >= 1 and self.trigger_open_30 < 2 and self.cumulative_value < 0 and self.count_consecutive <= -3:
                # self.trigger_open_30 += 1
                self.f_open_position('SHORT')
            if self.count_long >= 1 and self.trigger_open_30 < 2 and self.cumulative_value > 0 and self.count_consecutive >= 3:
                # self.trigger_open_30 += 1
                self.f_open_position('LONG')
            """
            if self.count_open_long >= 2:
                if self.count_long >= 1:
                    self.f_open_position('LONG')
                self.count_open_long = 0
                self.count_open_short = 0
            if self.count_open_short >= 2:
                if self.count_short >= 1:
                    self.f_open_position('SHORT')
                self.count_open_long = 0
                self.count_open_short = 0
            """

            """

            if self.trigger_count_open >= 5 and self.count_long >= 1:
                self.trigger_count_open = 0
                self.f_open_position('LONG')
                self.subtext1 = f"con_p_decrease={abs(self.trigger_count_open)}"

            if self.trigger_count_open <= -5 and self.count_short >= 1:
                self.trigger_count_open = 0
                self.f_open_position('SHORT')
                self.subtext1 = f"con_p_increase={abs(self.trigger_count_open)}"

            if self.count_long >= 6 and not self.trigger_open_long:
                self.trigger_open = True
                self.trigger_open_count = 0
                self.trigger_open_long = True
                self.trigger_open_short = False
                self.v_previous_price = self.v_latest_price
                self.v_aop_temp = float(self.v_latest_price)
                self.f_update_textbox(f"6_LONG_ALERTS", True, True)
            elif self.count_short >= 6 and not self.trigger_open_short:
                self.trigger_open = True
                self.trigger_open_count = 0
                self.trigger_open_long = False
                self.trigger_open_short = True
                self.v_previous_price = self.v_latest_price
                self.v_aop_temp = float(self.v_latest_price)
                self.f_update_textbox(f"6_SHORT_ALERTS", True, True)

            if self.trigger_open:
                if self.trigger_open_long:
                    if self.v_latest_price > self.v_previous_price:
                        self.trigger_open_count += 1
                    elif self.v_latest_price < self.v_previous_price:
                        self.trigger_open_count = 0
                    subtext1 = f'-consec_price_increase={self.trigger_open_count}'
                    if self.trigger_open_count > self.trigger_open_count_reset:
                        self.f_open_position('LONG')
                        self.trigger_open_count = 0
                        self.trigger_open = False
                        self.trigger_open_long = False
                elif self.trigger_open_short:
                    if self.v_latest_price < self.v_previous_price:
                        self.trigger_open_count += 1
                    elif self.v_latest_price > self.v_previous_price:
                        self.trigger_open_count = 0
                    subtext1 = f'-consec_price_decrease={self.trigger_open_count}'
                    if self.trigger_open_count > self.trigger_open_count_reset:
                        self.f_open_position('SHORT')
                        self.trigger_open_count = 0
                        self.trigger_open = False
                        self.trigger_open_short = False
                self.v_previous_price = self.v_latest_price
            """
        else:
            if self.v_direction == 'Empty':
                if self.count_long >= 1:
                    self.v_reason = 'Closed. ALERT different'
                    self.f_close_position()
                """
                if self.cumulative_value > 0:
                    self.v_reason = 'Closed. CROSSOVER'
                    time.sleep(0.1)
                    self.f_close_position()
                if self.cumulative_value > 0 and self.cumulative_diff >= 10:
                    self.v_reason = 'CLOSED +10'
                    self.f_close_position()
                    time.sleep(0.1)
                    self.f_open_position('LONG')
                    self.count_open_long = 0
                    self.count_open_short = 0
                    self.cumulative_value = 0
                    self.cumulative_percent = 0
                if self.cumulative_value > 0 and self.cumulative_diff >= 2.5:
                    self.count_close += 1
                elif self.count_close > 0 and self.cumulative_value > 0:
                    self.count_close = 0
                    self.count_open_long = 0
                    self.count_open_short = 0
                    if self.cumulative_value >= 2.5:
                        self.count_open_long = 1
                    if self.cumulative_value <= -2.5:
                        self.count_open_short = 1
                    self.v_reason = 'Closed 2row'
                    self.f_close_position()
                """
            if self.v_direction == 'Multi':
                if self.count_short >= 1:
                    self.v_reason = 'Closed. ALERT different'
                    self.f_close_position()

                """

                if self.cumulative_value < 0:
                    self.v_reason = 'Closed. CROSSOVER'
                    time.sleep(0.1)
                    self.f_close_position()

                if self.cumulative_value < 0 and self.cumulative_diff <= -10:
                    self.v_reason = 'CLOSED -10'
                    self.f_close_position()
                    time.sleep(0.1)
                    self.f_open_position('SHORT')
                    self.count_open_long = 0
                    self.count_open_short = 0
                    self.cumulative_value = 0
                    self.cumulative_percent = 0
                if self.cumulative_value < 0 and self.cumulative_diff <= -2.5:
                    self.count_close += 1
                elif self.count_close > 0 and self.cumulative_value < 0:
                    self.count_close = 0
                    self.count_open_long = 0
                    self.count_open_short = 0
                    self.f_close_position()
                """

            if self.v_yield >= self.percent_take_profit:
                self.percent_take_profit = self.v_yield
                self.percent_stop_loss = self.percent_take_profit - float(1.5)

            if self.v_yield <= self.percent_stop_loss:
                self.v_reason = f'Closed. Yield < ({self.percent_stop_loss}%)'
                self.percent_take_profit = self.percent_take_profit_reset
                self.percent_stop_loss = self.percent_stop_loss_reset
                self.f_close_position()
                self.count_consecutive = 0
                self.count_open_long = 0
                self.count_open_short = 0
                self.cumulative_value = float(0)
                self.cumulative_percent = float(0)

            """
            if self.v_direction == 'Empty' and self.count_long >= 1:
                self.f_update_textbox(f'LONG Triggered while SHORT', True, True)
            if self.v_direction == 'Multi' and self.count_short >= 1:
                self.f_update_textbox(f'SHORT Triggered while LONG', True, True)

            if self.count_consecutive >= 5 and self.v_direction == 'Empty' and self.count_long >= 1:
                self.count_consecutive = 0
                self.v_reason = 'Closed. 5 con increase'
                self.f_close_position()
                self.f_open_position('LONG')
                self.subtext1 = f"con_p_decrease={abs(self.count_consecutive)}"
            if self.count_consecutive <= -5 and self.v_direction == 'Multi' and self.count_short >= 1:
                self.count_consecutive = 0
                self.v_reason = 'CLOSED. 5 con decrease'
                self.f_close_position()
                self.f_open_position('SHORT')
                self.subtext1 = f"con_p_increase={abs(self.count_consecutive)}"

            if self.trigger_close:
                self.trigger_close_count += 1
                if self.trigger_close_count >= 60:
                    self.f_close_position()
                    self.trigger_close = False
                if self.v_yield > self.v_yield_temp:
                    self.v_yield_temp = self.v_yield
                if self.v_yield - self.v_yield_temp <= float(-1):
                    self.f_close_position()
                    self.trigger_close_count = 0
                    self.trigger_close = False
                subtext1 = f'-yield_drop={"{:.2f}".format(self.v_yield - self.v_yield_temp)}'
            else:
                subtext1 = ''
                if self.v_direction == 'Multi':
                    if self.count_short >= 2:
                        self.trigger_close = True
                        self.trigger_close_count = 0
                        self.v_yield_temp = self.v_yield
                        self.v_reason = f"Closed:_>=2_SHORT_WHILE_LONG"
                        self.f_update_textbox(f'_>=2_SHORT_WHILE_LONG')
                elif self.v_direction == 'Empty':
                    if self.count_long >= 2:
                        self.trigger_close = True
                        self.trigger_close_count = 0
                        self.v_yield_temp = self.v_yield
                        self.v_reason = f"Closed:_>=2_LONG_WHILE_SHORT"
                        self.f_update_textbox(f'_>=2_LONG_WHILE_SHORT')
            """

    def f_update_textbox(self, note='', blank_before=False, blank_after=False):
        self.textbox_row1 = f"{self.f_current_time()},{self.v_direction},{'{:.2f}'.format(self.v_latest_price)},{'{:.2f}'.format(self.v_bal)},\'{Variables.Misc.tradingview_charts_data[1]},\'{Variables.Misc.tradingview_charts_data[2]},\'{Variables.Misc.tradingview_charts_data[3]},\'{Variables.Misc.tradingview_charts_data[4]},\'{Variables.Misc.tradingview_charts_data[5]},\'{Variables.Misc.tradingview_charts_data[6]},\'{Variables.Misc.tradingview_charts_data[7]},\'{Variables.Misc.tradingview_charts_data[8]},\'{self.cumulative_value_str} / {self.cumulative_percent_str}%,\'{self.cumulative_value_str2} / {self.cumulative_percent_str2}%,{'{:.2f}'.format(self.v_unrealized)},{'{:.2f}'.format(self.v_yield)}%,{note},{self.v_tp_sl_str},{'{:.2f}'.format(self.v_aop)},{'{:.2f}'.format(self.v_esp)},{'{:.2f}'.format(self.v_diff)},{self.alerts_dict['BWMA']}"
        self.textbox_row2 = f'Recent Alert: {self.raw_data_message}'
        # self.floating_text_obj.update_text(f"{self.textbox_row1}\n{self.textbox_row2}\n{self.textbox_row3}\n{self.textbox_row4}\n{self.textbox_row5}")
        csv_string = [[self.textbox_row1]]
        if blank_before:
            csv_string = [[]] + csv_string
        if blank_after:
            csv_string = csv_string
        self.output = csv_string + self.output
        for key, value in self.alerts_dict.items():
            value[2] = value[1]
        print(note)
        return

    def f_backup_github(self, file):
        try:
            print('GITHUB: Backing up')
            headers = {'Authorization': 'token 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'}
            url = f'{Variables.Misc.url_github}{self.alerts_csv_file}'
            response = requests.get(url, headers=headers)
            response_json = response.json()
            content = response_json['content']
            current_sha = response_json['sha']
            data = {
                'message': 'Replace file content',
                'content': content,
                'sha': current_sha
            }

            url = f'{Variables.Misc.url_github}{file}'
            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                print('File content replaced successfully.')
            else:
                print('An error occurred while replacing the file content.')
            self.rate_limit_github = 1
            print('GITHUB: Backup Done')
            return True

        except:
            print('failed to backup')
            return False

    def f_update_github(self, new_content, add_header=True):
        try:
            print('GITHUBBING')
            headers = {'Authorization': 'token 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'}
            url = f'{Variables.Misc.url_github}{self.alerts_csv_file}'
            response = requests.get(url, headers=headers)
            response_json = response.json()
            content = response_json['content']
            decoded_content = base64.b64decode(content).decode('utf-8')
            current_sha = response_json['sha']

            if not add_header:
                updated_content = f'{new_content}\n{decoded_content}'
            else:
                lines = decoded_content.split('\n')
                while len(lines) >= 1500:
                    lines.pop()
                decoded_content = "\n".join(lines[1:])
                alert1 = 'alert1, recent, previous'
                string = f'date,time,direction,current_price,balance,10min,last_rev,unr_p/l,yield,note,to_SL/to_TP,aop,esp,aop-esp,{alert1}'
                updated_content = f"{self.format_csv_string(string)}\n{new_content}\n{decoded_content}"

            encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

            data = {
                'message': 'Replace file content',
                'content': encoded_content,
                'sha': current_sha
            }

            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                print('File content replaced successfully.')
            else:
                print('An error occurred while replacing the file content.')
            self.rate_limit_github = 1
            print('GITHUBBING DONE')

            return True
        except:
            print('failed to read/write')
            return False

    def f_process_alert_new(self, fv_message):
        alert = fv_message[0].strip()
        for key, value in self.alerts_dict.items():
            if value[0].lower() in fv_message[2].lower():
                self.alerts_dict[key][1] = alert
                break
        return alert

    def f_get_data_evatcoin(self):
        print('SCRAPING EVATCOIN')
        self.driver.switch_to.window(self.driver.window_handles[0])
        try:
            self.driver.find_element(By.XPATH, Variables.XPaths.evatcoin_perpetual).click()
        except:
            self.driver.get(Variables.Misc.url_evatcoin)
            time.sleep(2)

        try:
            self.v_latest_price = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_current_price))).text
            self.v_latest_price = float(self.v_latest_price[:-1])
        except:
            self.v_latest_price = float(0)

        if len(self.prices_list) >= 120:
            self.prices_list.pop(0)

        self.prices_list.append(float(self.v_latest_price))

        if all(val == self.prices_list[0] for val in self.prices_list):
            self.driver.get(Variables.Misc.url_evatcoin)

        if self.v_direction == 'Multi':
            self.v_tp_sl_str = f"{'{:.2f}'.format(float(self.v_latest_price) - ((float(self.v_aop)) - ((float(self.v_aop) * float(self.percent_stop_loss)) / (100 * Variables.Misc.leverage))))}/{'{:.2f}'.format(-float(self.v_latest_price) + ((float(self.v_aop)) + ((float(self.v_aop) * float(self.percent_take_profit)) / (100 * Variables.Misc.leverage))))}"
            self.v_yield = Variables.Misc.leverage * 100 * ((float(self.v_latest_price) - float(self.v_aop)) / float(self.v_aop))
        elif self.v_direction == 'Empty':
            self.v_tp_sl_str = f"{'{:.2f}'.format(-float(self.v_latest_price) + ((float(self.v_aop)) + ((float(self.v_aop) * float(self.percent_stop_loss)) / (100 * Variables.Misc.leverage))))}/{'{:.2f}'.format(float(self.v_latest_price) - ((float(self.v_aop)) - ((float(self.v_aop) * float(self.percent_take_profit)) / (100 * Variables.Misc.leverage))))}"
            self.v_yield = Variables.Misc.leverage * 100 * ((-float(self.v_latest_price) + float(self.v_aop)) / float(self.v_aop))
        else:
            self.v_yield = float(0)
            self.v_tp_sl_str = '-/-'

        try:
            self.v_esp = '{:.2f}'.format(
                float(self.driver.find_element(By.XPATH, Variables.XPaths.evatcoin_forced_closing_price).text))
        except:
            self.v_esp = float(0)

        try:
            self.v_unrealized = float(self.driver.find_element(By.XPATH, Variables.XPaths.evatcoin_latest_unrealized_profit_loss).text)
        except:
            self.v_unrealized = float(0)

        try:
            self.v_diff = float(self.v_aop) - float(self.v_esp)
        except:
            self.v_diff = float(0)

        self.v_unrealized = (float(self.v_bal_leaf * (self.v_yield / 100)))
        self.v_bal = self.v_bal_open + self.v_bal_leaf * (self.v_yield / 100)
        print('SCRAPING EVATCOIN DONE')

    def f_get_data_tradingview(self):
        while True:
            if Variables.Misc.state_break:
                break
            try:
                self.driver.switch_to.window(self.driver.window_handles[1])
                print('SCRAPING TRADINGVIEW')
                try:
                    raw_data = self.wait.until(EC.presence_of_element_located((By.XPATH, Variables.XPaths.tradingview_logs[1]))).text
                    self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_logs[1]).click()
                    raw_data = raw_data.split('\n')
                except:
                    self.driver.get(Variables.Misc.url_tradingview)
                    time.sleep(3)
                    continue

                for i in range(1, 9):
                    Variables.Misc.tradingview_charts_data[i] = self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_charts[i]).text

                self.raw_data_message = f'{raw_data[1]}'
                try:
                    if not (any(s.lower() in self.raw_data_message.lower() for s in [self.alerts_dict[key][0].lower() for key in self.alerts_dict])):
                        raise ValueError('WrongFormat')
                    if not (any(s.lower() in self.raw_data_message.lower() for s in ['long', 'short'])):
                        raise ValueError('WrongFormat')
                    self.raw_data_message = raw_data[1]
                    raw_data_message_splitted = self.raw_data_message.split(',')
                    self.alert_new = self.f_process_alert_new(raw_data_message_splitted)
                    self.alert_new_time = raw_data_message_splitted[3].strip()
                    self.alert_new_time_obj = datetime.strptime(self.alert_new_time, "%Y-%m-%dT%H:%M:%SZ")
                    self.current_time_utc = datetime.utcnow()
                    time_diff = self.current_time_utc - self.alert_new_time_obj
                    for key, value in sorted(Variables.XPaths.tradingview_logs.items(), reverse=True):
                        try:
                            raw_data_message_splitted = self.driver.find_element(By.XPATH, value).text
                            raw_data_message_splitted = raw_data_message_splitted.split('\n')
                            raw_data_message_splitted = raw_data_message_splitted[1]
                            raw_data_message_splitted = raw_data_message_splitted.split(',')
                            self.f_process_alert_new(raw_data_message_splitted)
                        except:
                            pass
                    self.count_short = 0
                    self.count_long = 0
                    for value in self.alerts_dict.values():
                        if value[1].lower() == 'short':
                            self.count_short += 1
                        elif value[1].lower() == 'long':
                            self.count_long += 1
                    if time_diff.total_seconds() > 120:
                        self.textbox_row3 = f'Current time: {self.current_time_utc} has passed more than 2 minutes than alert time: {self.alert_new_time_obj}\nR'
                        self.note = ''
                        self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_logs[1]).click()
                    else:
                        self.textbox_row3 = 'ROW3'
                        self.note = ''
                    print('SCRAPING TRADINGVIEW DONE')
                    return
                except:
                    self.textbox_row3 = 'Wrong alert message format. Please make sure you use this format in the alert message:\nLONG/SHORT, 30 Min, MESSAGE, {{timenow}}, '
                    self.f_update_textbox('ALERT_FORMAT_WRONG')
                    time.sleep(1)
            except ValueError:
                self.textbox_row3 = f'Failed to get the data. Please check if you are logged in on tradingview.'
                self.textbox_row4 = '(If you are trying to login with Google and it blocks you, please close this script instead, then reopen chrome, login to tradingview with google, close browser, then start again.)'
                self.f_update_textbox('TRADINGVIEW_NOT_LOGGED')
                time.sleep(1)
                continue

    def f_open_chrome(self):
        try:
            print(f'\nOpening Chrome. \nPlease restart this script if it takes too long.\n')
            # subprocess.Popen(chrome_cmd)
            options = Options()
            # options.add_experimental_option("debuggerAddress", debugger_address)
            options.add_argument(f'--user-data-dir={Variables.Misc.chrome_user_profile}')
            options.add_argument("--disable-infobars")
            options.set_capability("detach", True)
            options.service_args = ['--keep-alive']
            print('Installing driver. restart if this this takes too long')
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            print('Driver installed')
            self.wait = WebDriverWait(self.driver, 10)

            self.driver.get(Variables.Misc.url_evatcoin)
            self.driver.execute_script('window.open("");')
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(0.2)
            self.driver.get(Variables.Misc.url_tradingview)
            time.sleep(0.2)
            return self.driver
        except:
            messagebox.showinfo("ALERT", 'Make sure you have an internet connection before starting the script.\nExiting...')
            self.driver.quit()
            self.root.destroy()
            sys.exit()

    def f_current_time(self):
        self.v_current_time_str = datetime.now().strftime("%Y-%m-%d,%H:%M:%S.%f")[:-3]
        return self.v_current_time_str

    def format_csv_string(self, csv_string):
        items = csv_string.split(',')
        if len(items) < self.csv_columns:
            items += [''] * (self.csv_columns - len(items))
        elif len(items) > self.csv_columns:
            raise ValueError(f'CSV string has more than {self.csv_columns} columns')
        return ','.join(items)

    def f_open_position(self, direction):
        self.v_aop = float(self.v_latest_price)
        self.v_bal = self.v_bal - 0.2 - 0.02 * self.v_bal_leaf
        self.v_bal_open = self.v_bal
        if direction.upper() == 'LONG':
            self.v_direction = 'Multi'
        else:
            self.v_direction = 'Empty'
        print(f'{self.v_bal} - {direction}')
        self.f_update_textbox(f"POSITION_OPENED:{direction.upper()}", True, True)
        return

    def f_close_position(self):
        self.v_aop = 0
        self.v_bal = self.v_bal - 0.2 - 0.02 * self.v_bal_leaf
        self.v_bal_open = self.v_bal
        self.v_direction = 'NO_POS'
        self.f_update_textbox(f"{self.v_reason}", True, True)
        return

class LocalSheets:
    def __init__(self):
        self.file = 'data.txt'
        self.SERVICE_ACCOUNT_FILE = 'keys.json'
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.SPREADSHEET_ID = '14H-OyOk_rdHtuTCj6lRj5C1__BJksgskzBg9G5NOCpo'
        self.service = build('sheets', 'v4', credentials=self.creds)

    def append(self, data):
        if not os.path.exists(self.file):
            print('UPDATING TO LOCAL SHEETS')
            with open(self.file, 'w', encoding='utf-8') as f:
                f.write(repr(data))
            print('UPDATING TO LOCAL SHEETS DONE')
            return True
        else:
            print('FILE STILL EXIST')
            return False

    def backup(self):
        return

class GoogleSheets:
    def __init__(self):
        self.SERVICE_ACCOUNT_FILE = 'keys.json'
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.SPREADSHEET_ID = '14H-OyOk_rdHtuTCj6lRj5C1__BJksgskzBg9G5NOCpo'
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.header = [[f'date,time,direction,current_price,balance,5s,10s,15s,30s,1m,2m,3m,5m,5min,last_rev,unr_p/l,yield,note,to_SL/to_TP,aop,esp,aop-esp,alert1,recent,previous']]
        self.localspreadsheet = LocalSheets().file

    def append(self, data):
        print('UPDATING TO GOOGLE SHEETS')
        body = {
            'requests': [
                {
                    'insertDimension': {
                        'range': {
                            'sheetId': 0,
                            'dimension': 'ROWS',
                            'startIndex': 0,
                            'endIndex': len(data)  # Set endIndex based on length of values
                        },
                        'inheritFromBefore': False
                    }
                },
                {
                    'pasteData': {
                        'data': '\n'.join([','.join(map(str, row)) for row in self.header + data]),
                        'type': 'PASTE_NORMAL',
                        'delimiter': ',',
                        'coordinate': {
                            'sheetId': 0,
                            'rowIndex': 0,
                            'columnIndex': 0
                        }
                    }
                }
            ]
        }
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body)
        try:
            request.execute()
            print('UPDATING TO GOOGLE SHEETS DONE')
            return True
        except:
            return False

    def backup(self):
        return
