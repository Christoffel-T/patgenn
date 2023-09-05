from __future__ import print_function

import base64
import ctypes
import math
import os
import re
import sys
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import gspread
import pyautogui
import requests
# from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# UPDATE
class Variables:
    class CssSelectors:
        def __init__(self):
            pass

        evatcoin_leverage = [
            "body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.nav.nav-pills > div.flex-fill.px-3.justify-content-end.d-flex.align-items-center > span > span > div",
            "[id^='el-popover-'] > div.list > div:nth-child(1)",
            "[id^='el-popover-'] > div.list > div:nth-child(2)",
            "[id^='el-popover-'] > div.list > div:nth-child(3)"]
        evatcoin_open_long = 'body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div:nth-child(5) > div.px-2.flex-fill.mb-4 > button'
        evatcoin_open_short = 'body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div:nth-child(5) > div:nth-child(2) > button'
        evatcoin_open_confirm = 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary'
        evatcoin_close_long = 'body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div:nth-child(4) > div.px-2.flex-fill.mb-4 > button'
        evatcoin_close_short = 'body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div:nth-child(4) > div:nth-child(2) > button'
        evatcoin_close_confirm = '#exampleModal > div > div > div.modal-footer > button.btn.btn-primary'
        evatcoin_current_price = 'body > div > main > div > div.page-top.d-flex.pt-2 > div.kline-box.flex-fill.mr-2 > div.coin-change.d-flex.align-items-center.py-2.pl-4.heading.justify-content-between > div.d-flex.align-items-center > div.price.px-3.border-right.increace > span.current'
        evatcoin_25 = "body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div.px-2 > div > div > div:nth-child(3)"
        evatcoin_50 = "body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div.px-2 > div > div > div:nth-child(4)"
        evatcoin_hirakura = "body > div:nth-child(1) > main > div > div.d-flex.pb-2.mt-2 > div.markets-pair-list.page-bottom.bg-plain.flex-fill > div.body > div > table > tbody > tr > td:nth-child(14) > button.btn.btn-sm.btn-danger.mb-1"
        evatcoin_marketprice = "#exampleModal > div > div > div.modal-body > form > div:nth-child(1) > div > div > button"
        evatcoin_qty = "#message-text"
        evatcoin_buy_qty = "body > div:nth-child(1) > main > div > div.page-top.d-flex.pt-2 > div.markets-pair-list.exchange-store.bg-plain > div.content-box.px-3 > div.input-group.mb-4.input-group-sm > input"
        evatcoin_direction = "body > div:nth-child(1) > main > div > div.d-flex.pb-2.mt-2 > div.markets-pair-list.page-bottom.bg-plain.flex-fill > div.body > div > table > tbody > tr > td:nth-child(4)"
        evatcoin_balance = "body > div > main > div > div.d-flex.pb-2.mt-2 > div.ml-2 > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
        evatcoin_esp = "body > div:nth-child(1) > main > div > div.d-flex.pb-2.mt-2 > div.markets-pair-list.page-bottom.bg-plain.flex-fill > div.body > div > table > tbody > tr > td:nth-child(10)"
        elw_chart_5m = "body > div.js-rootresizer__contents > div.layout__area--top.header-chart-panel > div > div > div.left > div:nth-child(8) > div"
        elw_chart_ohlc = {
            'O': [
                'body > div.js-rootresizer__contents > div.layout__area--center > div > div.chart-widget > table > tbody > tr:nth-child(1) > td.chart-markup-table.pane > div > div.pane-legend > div.pane-legend-line.pane-legend-wrap.main > div > span:nth-child(1)',
                float(0)],
            'H': [
                'body > div.js-rootresizer__contents > div.layout__area--center > div > div.chart-widget > table > tbody > tr:nth-child(1) > td.chart-markup-table.pane > div > div.pane-legend > div.pane-legend-line.pane-legend-wrap.main > div > span:nth-child(2)',
                float(0)],
            'L': [
                'body > div.js-rootresizer__contents > div.layout__area--center > div > div.chart-widget > table > tbody > tr:nth-child(1) > td.chart-markup-table.pane > div > div.pane-legend > div.pane-legend-line.pane-legend-wrap.main > div > span:nth-child(3)',
                float(0)],
            'C': [
                'body > div.js-rootresizer__contents > div.layout__area--center > div > div.chart-widget > table > tbody > tr:nth-child(1) > td.chart-markup-table.pane > div > div.pane-legend > div.pane-legend-line.pane-legend-wrap.main > div > span:nth-child(4)',
                float(0)],
        }
        elw_chart_close_price = elw_chart_ohlc['C'][0]

    class XPaths:
        evatcoin_current_price = "/html/body/div[1]/main/div/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]"
        tradingview_ohlc_prev = {
            'C': ['', float(0)]
        }
        evatcoin_perpetual = '/html/body/div[1]/header/nav/div/ul[1]/li[4]/a'
        evatcoin_leverage = '/html/body/div[1]/main/div/div[1]/div[3]/div[1]/div[3]/span/span/div'
        evatcoin_leverage_selector = '/html/body/div[2]/div[1]'
        evatcoin_slider = '/html/body/div[1]/main/div/div[1]/div[3]/div[2]/div[3]/div/div/div[3]'
        evatcoin_buy_long = '/html/body/div[1]/main/div/div[1]/div[3]/div[2]/div[5]/div[1]/button'
        evatcoin_sell_short = '/html/body/div[1]/main/div/div[1]/div[3]/div[2]/div[5]/div[2]/button'
        evatcoin_balance = '/html/body/div/main/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[2]'
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
        # tradingview_volume = '/html/body/div[2]/div[5]/div[9]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[9]/div[2]'
        tradingview_volume = '/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[3]/td[2]/div/div[3]/div/div/span[1]'
        elw_chart_5m = '/html/body/div[1]/div[2]/div/div/div[2]/div[8]/div'
        tradingview_logs = {}
        for i in range(1, 10):
            tradingview_logs[
                i] = f'/html/body/div[2]/div[6]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[{i + 1}]'
        tradingview_charts = {}
        for i in range(1, 9):
            tradingview_charts[
                i] = f'/html/body/div[2]/div[5]/div[{i + 1}]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[8]/div[2]'
        # tradingview_ohlc = {
        #     'O': ['/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]',float(0)],
        #     'H': ['/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[3]/div[2]',float(0)],
        #     'L': ['/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[4]/div[2]',float(0)],
        #     'C': ['/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[5]/div[2]',float(0)],
        # }
        tradingview_ohlc = {
            'O': ['/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/div[3]/div/div/span[1]/span[2]',
                  float(0)],
            'H': ['/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/div[3]/div/div/span[2]/span[2]',
                  float(0)],
            'L': ['/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/div[3]/div/div/span[3]/span[2]',
                  float(0)],
            'C': ['/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/div[3]/div/div/span[4]/span[2]',
                  float(0)],
        }

    class Misc:
        def __init__(self):
            pass

        state_break = False
        screen_width, screen_height = pyautogui.size()
        url_tradingview = r'https://www.tradingview.com/chart/cS9mKSgi/'
        # url_tradingview = r'https://www.tradingview.com/chart/eYD79MKQ/'
        # url_tradingview = r'https://m.elwallets.com/#/pages/exchange/index?code=BTC%252FUSDT'
        url_evatcoin = r'https://elwallets.com/#/contract'
        url_github = 'https://api.github.com/repos/Christoffel-T/fiverr-pat-20230331/contents/'
        filename = 'Yields.csv'
        chrome_user_profile = os.environ['USERPROFILE'] + r"\AppData\Local\Google\Chrome\User Data"
        tv_vol = ''
        tradingview_charts_data = {}
        for i in range(1, 9):
            tradingview_charts_data[i] = '-'
        tradingview_charts_data2 = {}
        for i in range(1, 9):
            tradingview_charts_data2[i] = ['', '']
        tradingview_charts_data1 = {}
        for i in range(1, 9):
            tradingview_charts_data1[i] = '-'
        tv_HA = {
            1: [
                '/html/body/div[2]/div[5]/div[9]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[6]/div',
                float(0)],
            2: [
                '/html/body/div[2]/div[5]/div[9]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[16]/div',
                float(0)],
            3: [
                '/html/body/div[2]/div[5]/div[9]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[17]/div',
                float(0)],
            4: [
                '/html/body/div[2]/div[5]/div[9]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[18]/div',
                float(0)],
            5: [
                '/html/body/div[2]/div[5]/div[9]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[19]/div',
                float(0)],
        }

        leverages = {50: [50, 0.01, 20], 100: [100, 0.02, 10], 200: [200, 0.04, 5]}
        leverage = leverages[100]
        count_consec_1 = 0
        count_consec_2 = 0
        count_consec_3 = 0


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
        self.master.geometry(f"+{10}+{int(Variables.Misc.screen_height * 0.6)}")

    def update_text(self, new_text, show_ok=False):
        if Variables.Misc.state_break:
            print('Stopped')
            return
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", new_text)
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
        self.last_minute = -1
        self.prclprs = [float(0)]
        self.count_qualifier_SUM1 = 0
        self.count_qualifier_SUM2 = 0
        self.count_qualifier_SUM = float(0)
        self.count_qualifier_NOTES = 0
        self.disable_sum = False
        self.count_qualifier_OHCPRC = 0
        self.sum_net2 = [float(0), float(0), float(0), float(0)]
        self.count_qualifier_COP = 0
        self.count_qualifier_OLHO = 0
        self.count_stoploss = 0
        self.qualifier_stoploss = ''
        self.count_sudden = 0
        self.diff = [float(0), float(0)]
        self.diff_anchor = [float(0), float(0)]
        self.no_repeat_time = None
        self.state_prclpr = ''
        self.prclpr = round(float(0),2)
        self.count_consecutive_sum = 0
        self.opened_by = ''
        self.v_direction_evat = ''
        self.v_bal_elw = float(0)
        self.override = False
        self.note3 = ''
        self.sum_net = [float(0), float(0), float(0), float(0)]
        self.resetted = ''
        self.price_close = 0
        self.price_low = 0
        self.price_high = 0
        self.price_open = 0
        self.str_profit_loss = ''
        self.prices = [float(0),float(0)]
        self.count_tfsc_long2 = 0
        self.count_tfsc_short2 = 0
        self.count_rows_2 = 0
        self.count_rows_3 = 0
        self.v_reason_open = ''
        self.state_logic4 = ''
        self.state_logic3 = ''
        self.state_logic2 = ''
        self.v_evat_latest_price = float(0)
        self.take_profit = 0
        self.stop_loss = 0
        self.count_sc5m_short2 = 0
        self.count_sc5m_long2 = 0
        self.count_sc5m_long = 0
        self.count_sc5m_short = 0
        self.count_tfsc_long = 0
        self.count_tfsc_short = 0
        self.trigger_close_long = False
        self.trigger_close_short = False
        self.output = []
        self.floating_text_obj = floating_text_obj
        self.root = root
        self.LocalSheets = None
        self.trigger_open_30 = 0
        self.count_close = 0
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
        self.anchor_price_2 = float(0)
        self.anchor_price = float(0)
        self.trigger_open = ''
        self.trigger_close_count = 0
        self.alerts_csv_file = 'alerts.csv'
        self.trigger_open_count_reset = 3
        self.list_reverses = []
        self.v_yield_temp_str = ''
        self.temp_yields = []
        self.note = ''
        self.note2 = ''
        self.v_state_yield_temp = False
        self.v_yield_temp = float(0)
        self.v_aop_temp = float(0)
        self.v_aop = float(0)
        self.v_bal = float(72)
        self.v_percentage = 1
        self.leaf_size = Variables.Misc.leverage[2]
        self.v_buy_qty = math.floor((self.v_bal * self.v_percentage) / self.leaf_size)
        self.v_bal_leaf = self.v_buy_qty * self.leaf_size
        self.v_diff = float(0)
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
        self.trigger_close = ''
        self.trigger_open_short = False
        self.trigger_open_long = False
        self.v_tp_sl_str = ''
        self.v_reason_close = 'C'
        self.percent_stop_loss_reset = float(-2000)
        self.percent_stop_loss = self.percent_stop_loss_reset
        self.percent_take_profit_reset = float(3)
        self.percent_take_profit = self.percent_take_profit_reset
        self.script_timeframe = {
            5: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            10: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            15: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            30: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            60: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            120: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            180: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            240: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            300: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            304: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
            306: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], '', float(0), float(0), ''],
        }
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
        self.count_tf_short = 0
        self.count_tf_long = 0
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
        self.checker_prices = []
        self.alerts_dict = {
            'ALERT1': ['Heiken Ashi', '-', '-'],
        }

    def f_close_evat(self):
        try:
            # self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_hirakura).click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_marketprice).click()
            time.sleep(1)
            input_elem = self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_qty)
            input_elem.clear()
            input_elem.send_keys("999")
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_close_confirm).click()

        except:
            self.f_update_textbox('evat_close_error', True, True)
            print('evat_close_error')
            raise ValueError

    def f_open_evat(self):
        try:
            if self.v_bal_elw < 55555.5:
                print('NOT ENOUGH BALANCE')
                return
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_leverage[0]).click()
            time.sleep(0.7)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_leverage[3]).click()
            time.sleep(1)
            input_elem = self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_buy_qty)
            input_elem.clear()
            self.v_buy_qty = math.floor((self.v_bal * self.v_percentage) / self.leaf_size)
            self.v_bal_leaf = self.v_buy_qty * self.leaf_size

            input_elem.send_keys(self.v_buy_qty)
            time.sleep(1)
            if self.v_direction == 'Multi':
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_open_long).click()
                print('opened long')
            elif self.v_direction == 'Empty':
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_open_short).click()
                print('opened short')
            else:
                print('nodirection')
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_open_confirm).click()
            time.sleep(1)

        except:
            self.f_update_textbox('evat_open_error', True, True)
            print('evat_open_error')
            raise ValueError

    def f_main1(self):
        self.f_open_chrome()
        self.floating_text_obj.update_text('RUNNING')
        self.rate_limit_github = 0
        self.f_update_textbox('SCRIPT_STARTED', True, True)
        self.trigger_open_count = 0
        self.LocalSheets = LocalSheets()
        self.no_repeat_time = datetime.now()
        loop = True
        while loop:
            try:
                return_val = self.f_main2()
                if return_val == 'break':
                    loop = False
            except Exception as e:
                loop = True
                print(e)
                time.sleep(2)

    def f_main2(self):

        # region GET-DATA: Misc
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

        for key in self.script_timeframe:
            self.script_timeframe[key][3] = self.script_timeframe[key][1][0]

        self.f_get_data_tradingview()
        self.f_get_data_evatcoin()

        subtext2 = ''

        if self.alerts_dict['ALERT1'][1] != self.alerts_dict['ALERT1'][2] and self.alerts_dict['ALERT1'][2] != '-':
            # self.f_update_textbox('ALERT_REVERSE', True, True)
            self.cumulative_value2 = float(0)
            self.cumulative_percent2 = float(0)
        else:
            cumulative_value_previous2 = self.cumulative_value2
            if self.prices[1] != float(0):
                self.cumulative_value2 += self.prices[0] - self.prices[1]
            if self.prices[0] == self.prices[1]:
                if self.cumulative_value2 > 0:
                    self.cumulative_value_str2 = f"+{'{:.2f}'.format(self.cumulative_value2)}"
                else:
                    self.cumulative_value_str2 = f"{'{:.2f}'.format(self.cumulative_value2)}"
                # ?
                if self.cumulative_percent2 > 0:
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

        self.count_tf_short = 0
        self.count_tf_long = 0
        self.count_tfsc_short = 0
        self.count_tfsc_long = 0
        self.count_tfsc_short2 = 0
        self.count_tfsc_long2 = 0
        self.trigger_close_short = False
        self.trigger_close_long = False

        if now.minute in [x for x in range(14, 60, 15)] and 54 <= now.second <= 59:
            self.prclpr = self.prices[0]
        if now.minute in [x for x in range(0, 60, 15)] and now.minute not in [self.last_minute]:
            self.prclprs.insert(0,self.prclpr)
            self.last_minute = now.minute

        if now.minute in [x for x in range(4, 60, 5)] and 55 <= now.second <= 59:
            self.sum_net.insert(0, float(0))
            self.sum_net2.insert(0, float(0))
        if now.minute in [x for x in range(2, 60, 5)] and 26 <= now.second <= 30:
            self.sum_net.insert(0, float(0))
            self.sum_net2.insert(0, float(0))
        for key in self.script_timeframe:
            # if key == 304:
            #     self.f_last_reset_time(now, key, offset=-1)
            if key == 306:
                self.f_last_reset_time(now, key, offset=1)
            else:
                self.f_last_reset_time(now, key)
            if self.script_timeframe[key][1][0] > 0:
                self.count_tfsc_long += 1
            elif self.script_timeframe[key][1][0] < 0:
                self.count_tfsc_short += 1

        if self.script_timeframe[300][1][0] > self.script_timeframe[300][3]:
            self.count_sc5m_long += 1
            self.count_sc5m_short = 0
        elif self.script_timeframe[300][1][0] < self.script_timeframe[300][3]:
            self.count_sc5m_long = 0
            self.count_sc5m_short += 1

        if not self.script_timeframe[300][1][0] == self.script_timeframe[300][3]:
            if self.script_timeframe[300][1][0] > 0:
                self.count_sc5m_long2 += 1
                self.count_sc5m_short2 = 0
            elif self.script_timeframe[300][1][0] < 0:
                self.count_sc5m_long2 = 0
                self.count_sc5m_short2 += 1

        if self.script_timeframe[300][1][0] >= 40 and self.script_timeframe[300][1][0] > self.take_profit:
            self.take_profit = self.script_timeframe[300][1][0]
            self.stop_loss = self.take_profit - 10
        if self.script_timeframe[300][1][0] <= -40 and self.script_timeframe[300][1][0] < self.take_profit:
            self.take_profit = self.script_timeframe[300][1][0]
            self.stop_loss = self.take_profit + 10

        for key in self.script_timeframe:
            if key == 300:
                self.script_timeframe[key][4] += self.script_timeframe[key][1][0] - self.script_timeframe[key][3]
                if self.script_timeframe[key][4] > 0:
                    self.script_timeframe[key][5] = f"+{'{:.2f}'.format(self.script_timeframe[key][4])}"
                else:
                    self.script_timeframe[key][5] = f"{'{:.2f}'.format(self.script_timeframe[key][4])}"

        # for i in Variables.Misc.tradingview_charts_data2:
        #     print(f'num:{Variables.Misc.tradingview_charts_data2[i][0]}')
        #     if float(Variables.Misc.tradingview_charts_data2[i][0]) > 0 or Variables.Misc.tradingview_charts_data2[i][0] == '+0.00':
        #         self.count_tf_long += 1
        #         print(f'POSITIVE {self.count_tf_long}')
        #     if float(Variables.Misc.tradingview_charts_data2[i][0]) < 0 or Variables.Misc.tradingview_charts_data2[i][0] == '−0.00':
        #         self.count_tf_short += 1
        #         print(f'NEGATIVE {self.count_tf_short}')
        #     if i == 7 and self.count_tf_long == 7 and self.script_timeframe[300][1][0] >= 0:
        #         self.trigger_close_short = True
        #         self.trigger_close_long = False
        #     elif i == 7 and self.count_tf_short == 7 and self.script_timeframe[300][1][0] <= 0:
        #         self.trigger_close_long = True
        #         self.trigger_close_short = False

        # endregion1

        # region GET-DATA: Misc
        if self.prices[0] > self.prices[1] > 0:
            if self.count_consecutive < 0:
                self.count_consecutive = 0
            if self.count_consecutive == 0:
                self.anchor_price = self.prices[1]
            self.count_consecutive += 1
            self.count_stoploss += 1
        elif self.prices[0] < self.prices[1] > 0:
            if self.count_consecutive > 0:
                self.count_consecutive = 0
            if self.count_consecutive == 0:
                self.anchor_price = self.prices[1]
            self.count_consecutive -= 1
            self.count_stoploss -= 1

        if self.anchor_price == 0:
            self.anchor_price = self.prices[0]

        self.subtext1 = ''
        if self.prices[1] != 0:
            self.diff.insert(0, self.prices[0] - self.prices[1])
        self.diff_anchor.insert(0, self.prices[0] - self.anchor_price)
        while len(self.diff) > 10:
            self.diff.pop()
        while len(self.diff_anchor) > 10:
            self.diff_anchor.pop()
        diff = self.diff_anchor[0]
        self.sum_net.insert(0, self.sum_net[0] + self.diff[0])
        self.sum_net2.insert(0, self.sum_net2[0] + self.diff[0])
        while len(self.sum_net) > 5:
            self.sum_net.pop()
        while len(self.sum_net2) > 5:
            self.sum_net2.pop()
        percent_diff = 0
        if self.anchor_price != 0:
            percent_diff = (diff / self.anchor_price) * 100
        percent_diff_str = f"{'{:.4f}'.format(percent_diff)}%"

        if self.count_consecutive > 0:
            self.subtext1 = f"inc={abs(self.count_consecutive)} - by: {'{:.2f}'.format(self.diff_anchor[0])} ({percent_diff_str})"
        elif self.count_consecutive < 0:
            self.subtext1 = f"dec={abs(self.count_consecutive)} - by: {'{:.2f}'.format(self.diff_anchor[0])} ({percent_diff_str})"

        text = f'{self.note}{self.subtext1}{subtext2}'
        self.f_update_textbox(f'{text}')

        # endregion

        self.f_LOGICS()
        return

    def f_LOGICS(self):
        # region LOGIC: stoploss
        var1 = 20

        if self.v_esp != 0:
            if self.prices[0] <= (self.v_esp + var1) and self.v_direction == 'Multi':
                if self.count_stoploss < 0:
                    self.count_stoploss = 0
                self.qualifier_stoploss = 'LONG'
            elif self.prices[0] >= (self.v_esp - var1) and self.v_direction == 'Empty':
                if self.count_stoploss > 0:
                    self.count_stoploss = 0
                self.qualifier_stoploss = 'SHORT'

            if self.qualifier_stoploss == 'LONG' and self.count_stoploss >= 1:
                self.qualifier_stoploss = ''
                self.count_stoploss = 0
                resetted = f'STOPLOSS: <esp+{var1}'
                self.opened_by = ''
                self.v_reason_close = resetted
                self.trigger_close = 'LONG'
                self.f_main3()
            if self.qualifier_stoploss == 'SHORT' and self.count_stoploss >= 1:
                self.qualifier_stoploss = ''
                self.count_stoploss = 0
                resetted = f'STOPLOSS: <esp+{var1}'
                self.opened_by = ''
                self.v_reason_close = resetted
                self.trigger_close = 'LONG'
                self.f_main3()

        # endregion

        # region LOGIC: SUDDEN
        sudden = 50
        if self.diff[0] >= sudden and self.diff[1] >= sudden and self.v_direction == 'Empty':
            self.trigger_close = 'SHORT'
            self.v_reason_close = f'SUDDEN_inc{sudden}'
            self.f_main3()
            self.count_sudden = 0
            return
        if self.diff[0] <= -sudden and self.diff[1] <= -sudden and self.v_direction == 'Multi':
            self.trigger_close = 'LONG'
            self.v_reason_close = f'SUDDEN_dec{sudden}'
            self.f_main3()
            self.count_sudden = 0
            return
        # endregion

        # region LOGIC 4 SCENARIOS

        if self.count_consecutive >= 2 and self.diff_anchor[0] > 8 and self.v_direction != 'Multi' and \
                (self.prices[0] > self.prclprs[0] > 0 and self.prices[0] > self.prclprs[1] > 0):
            self.resetted = f'Scenario1 inc C {self.prices[0]} > PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}>=2 by:{self.diff_anchor[0]}>=8'
            self.v_reason_close = self.resetted
            self.trigger_close = 'SHORT'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'LONG'
            self.f_main3()
            self.resetted = ''
            return
        if self.count_consecutive <= -2 and self.diff_anchor[0] < -8 and self.v_direction != 'Empty' and \
                (self.prices[0] < self.prclprs[0] > 0 and self.prices[0] < self.prclprs[1] > 0):
            self.resetted = f'Scenario1 dec C {self.prices[0]} < PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}<=-2 by:{self.diff_anchor[0]}<=-8'
            self.v_reason_close = self.resetted
            self.trigger_close = 'LONG'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'SHORT'
            self.f_main3()
            self.resetted = ''
            return

        if self.count_consecutive > 1 and self.diff_anchor[1] >= 10 and \
                (self.prices[0] > self.prclprs[0] > 0 and self.prices[0] > self.prclprs[1] > 0):
            self.resetted = f'Scenario2 inc C {self.prices[0]} > PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}>1 prev_diff:{self.diff_anchor[1]}>=10'
            self.v_reason_close = self.resetted
            self.trigger_close = 'SHORT'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'LONG'
            self.f_main3()
            self.resetted = ''
            return
        if self.count_consecutive < -1 and self.diff_anchor[1] <= -10 and \
                (self.prices[0] < self.prclprs[0] > 0 and self.prices[0] < self.prclprs[1] > 0):
            self.resetted = f'Scenario2 dec C {self.prices[0]} < PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}<-1 prev_diff:{self.diff_anchor[1]}<=-10'
            self.v_reason_close = self.resetted
            self.trigger_close = 'LONG'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'SHORT'
            self.f_main3()
            self.resetted = ''
            return

        if self.count_consecutive >= 3 and self.diff_anchor[0] > 3.7 and self.v_direction != 'Multi' and \
                (self.prices[0] > self.prclprs[0] > 0 and self.prices[0] > self.prclprs[1] > 0):
            self.resetted = f'Scenario3 inc C {self.prices[0]} > PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}>=3 diff:{self.diff_anchor[0]}>=3.7'
            self.v_reason_close = self.resetted
            self.trigger_close = 'SHORT'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'LONG'
            self.f_main3()
            self.resetted = ''
            return
        if self.count_consecutive <= -3 and self.diff_anchor[0] < -3.7 and self.v_direction != 'Empty' and \
                (self.prices[0] < self.prclprs[0] > 0 and self.prices[0] < self.prclprs[1] > 0):
            self.resetted = f'Scenario3 dec C {self.prices[0]} < PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}<=-3 diff:{self.diff_anchor[0]}<=-3.7'
            self.v_reason_close = self.resetted
            self.trigger_close = 'LONG'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'SHORT'
            self.f_main3()
            self.resetted = ''
            return

        if self.count_consecutive >= 2 and \
                (self.diff_anchor[0] > self.diff_anchor[1] >= 3.7) and \
                (self.prices[0] > self.prclprs[0] > 0 and self.prices[0] > self.prclprs[1] > 0):
            self.resetted = f'Scenario4 inc C {self.prices[0]} > PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}>=2 diff>prev_diff:{self.diff_anchor[0]}>=3.7'
            self.v_reason_close = self.resetted
            self.trigger_close = 'SHORT'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'LONG'
            self.f_main3()
            self.resetted = ''
            return
        if self.count_consecutive <= -2 and \
                (self.diff_anchor[0] < self.diff_anchor[1] <= -3.7) and \
                (self.prices[0] < self.prclprs[0] > 0 and self.prices[0] < self.prclprs[1] > 0):
            self.resetted = f'Scenario4 dec C {self.prices[0]} < PRC1 {self.prclprs[0]} & PRC2 {self.prclprs[1]} ||| notes:{self.count_consecutive}<=-2 diff<prev_diff:{self.diff_anchor[0]}<=-3.7'
            self.v_reason_close = self.resetted
            self.trigger_close = 'LONG'
            self.f_main3()
            self.v_reason_open = self.resetted
            self.trigger_open = 'SHORT'
            self.f_main3()
            self.resetted = ''
            return

        # if self.prices[0] == self.prclpr and self.v_direction not in ['NO_POS']:
        #     self.resetted = f'C=PRCLPR {self.prices[0]}={self.prclpr}'
        #     self.v_reason_close = self.resetted
        #     if self.v_direction in ['Multi']:
        #         self.trigger_close = 'LONG'
        #     if self.v_direction in ['Empty']:
        #         self.trigger_close = 'SHORT'
        #     self.f_main3()
        #     self.resetted = ''
        #     return

        # endregion

        # region LOGIC: O=L O=H DISABLED
        # if self.resetted == 'O=L & C>PRC' and (+ self.count_consecutive - self.count_qualifier_OHCPRC) >= 1:
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'LONG'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        # if self.resetted == 'O=H & C<PRC' and (- self.count_consecutive + self.count_qualifier_OHCPRC) >= 1:
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'SHORT'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        #
        # if open1 == low1 and \
        #         self.v_direction != 'Multi' and \
        #         self.prclpr > 0 and \
        #         (+ Variables.XPaths.tradingview_ohlc['C'][1] - self.prclpr) > 0:
        #     self.disable_sum = True
        #     resetted = 'O=L & C>PRC'
        #     self.resetted = resetted
        #     self.count_qualifier_OHCPRC = self.count_consecutive
        # elif open1 == high1 and \
        #         self.v_direction != 'Empty' and \
        #         self.prclpr > 0 and \
        #         (- Variables.XPaths.tradingview_ohlc['C'][1] + self.prclpr) > 0:
        #     self.disable_sum = True
        #     resetted = 'O=H & C<PRC'
        #     self.resetted = resetted
        #     self.count_qualifier_OHCPRC = self.count_consecutive
        # else:
        #     self.disable_sum = False
        # endregion

        # region LOGIC: (O<>L) (H<>O) DISABLED
        # if self.resetted == 'O<>L' and (- self.count_consecutive + self.count_qualifier_OLHO) >= 1 and \
        #         (self.opened_by == f'C>O>PRCLPR' or self.opened_by == f'C<O<PRCLPR'):
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        # if self.resetted == 'O<>H' and (+ self.count_consecutive - self.count_qualifier_OLHO) >= 1 and \
        #         (self.opened_by == f'C>O>PRCLPR' or self.opened_by == f'C<O<PRCLPR'):
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #
        # if self.v_direction != 'NO_POS' and (open1 > low1 or open1 < low1):
        #     self.disable_sum = True
        #     resetted = 'O<>L'
        #     self.count_qualifier_OLHO = self.count_consecutive
        #     self.opened_by = resetted
        #     self.resetted = resetted
        #     self.anchor_price_2 = round(self.prices[0],2)
        #     self.no_repeat_time = now
        # elif self.v_direction != 'NO_POS' and (open1 < high1 or open1 > high1):
        #     self.disable_sum = True
        #     resetted = 'O<>H'
        #     self.count_qualifier_OLHO = self.count_consecutive
        #     self.opened_by = resetted
        #     self.resetted = resetted
        #     self.anchor_price_2 = round(self.prices[0],2)
        #     self.no_repeat_time = now
        # else:
        #     self.disable_sum = False
        # endregion

        # region C<>PRCLPR DISABLED
        # if self.v_direction in ['NO_POS', 'Empty'] and \
        #         self.prices[0] > self.prclpr > 0:
        #     self.resetted = f'C>PRCLPR'
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'LONG'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        # if self.v_direction in ['NO_POS', 'Multi'] and \
        #         self.prices[0] < self.prclpr < 0:
        #     self.resetted = f'C<PRCLPR'
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'SHORT'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        #
        # if self.v_direction in ['Multi'] and \
        #         self.diff_anchor[0] <= -15:
        #     self.resetted = f'Notes <= -15'
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        # if self.v_direction in ['Empty'] and \
        #         self.diff_anchor[0] >= +15:
        #     self.resetted = f'Notes >= +15'
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #
        # endregion

        # region C<>O<>PRCLPR DISABLED
        # if self.resetted == f'C>O>PRCLPR' and (+ self.count_consecutive - self.count_qualifier_COP) >= 1:
        #     self.opened_by = self.resetted
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'LONG'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        # if self.resetted == f'C<O<PRCLPR' and (- self.count_consecutive + self.count_qualifier_COP) >= 1:
        #     self.opened_by = self.resetted
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'SHORT'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        #
        # if 0 < self.prclpr < Variables.XPaths.tradingview_ohlc['O'][1] < Variables.XPaths.tradingview_ohlc['C'][1] and self.v_direction != 'Multi':
        #     self.disable_sum = True
        #     resetted = f'C>O>PRCLPR'
        #     self.resetted = resetted
        #     self.count_qualifier_COP = self.count_consecutive
        #     self.no_repeat_time = now
        # elif 0 < self.prclpr and self.prclpr > Variables.XPaths.tradingview_ohlc['O'][1] > Variables.XPaths.tradingview_ohlc['C'][1] and self.v_direction != 'Multi':
        #     self.disable_sum = True
        #     resetted = f'C<O<PRCLPR'
        #     self.resetted = resetted
        #     self.count_qualifier_COP = self.count_consecutive
        #     self.no_repeat_time = now
        # else:
        #     self.disable_sum = False
        # endregion

        # region column O & P DISABLED
        # print(f'{self.script_timeframe[306][1]}')
        #
        # if self.v_direction in ['Empty'] and \
        #         (self.sum_net2[0] >= 16):
        #     self.resetted = 'sum_net2 > +15.99'
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        # if self.v_direction in ['Multi'] and \
        #         (self.sum_net2[0] <= -16):
        #     self.resetted = 'sum_net2 < -15.99'
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        #
        # if self.v_direction in ['Empty'] and \
        #         (self.sum_net[0] > self.sum_net[1] >= +3) and \
        #         (self.prices[0] > self.prclpr or self.prclpr == 0):
        #     self.resetted = 'sum_net go GREEN'
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        # if self.v_direction in ['Multi'] and \
        #         (self.sum_net[0] < self.sum_net[1] <= -3) and \
        #         (self.prices[0] < self.prclpr or self.prclpr == 0):
        #     self.resetted = 'sum_net go RED'
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        #
        # if self.v_direction in ['Empty'] and \
        #         (self.script_timeframe[306][1][0] >= +3 > self.script_timeframe[306][1][1]) and \
        #         (self.prices[0] > self.prclpr or self.prclpr == 0):
        #     self.resetted = 'sc_5m_6 go GREEN'
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        # if self.v_direction in ['Multi'] and \
        #         (self.script_timeframe[306][1][0] <= -3 < self.script_timeframe[306][1][1]) and \
        #         (self.prices[0] < self.prclpr or self.prclpr == 0):
        #     self.resetted = 'sc_5m_6 go RED'
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        #
        # if self.v_direction in ['NO_POS','Multi'] and \
        #         self.script_timeframe[306][1][0] < self.script_timeframe[306][1][1] <= -3 and \
        #         self.sum_net[0] <= -3 and \
        #         (self.prices[0] < self.prclpr or self.prclpr == 0):
        #     self.resetted = 'sc_5m_6 and sum_net match <-3'
        #     self.trigger_close = 'LONG'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'SHORT'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        # if self.v_direction in ['NO_POS','Empty'] and \
        #         self.script_timeframe[306][1][0] > self.script_timeframe[306][1][1] >= +3 and \
        #         self.sum_net[0] >= +3 and \
        #         (self.prices[0] > self.prclpr or self.prclpr == 0):
        #     self.resetted = 'sc_5m_6 and sum_net match >+3'
        #     self.trigger_close = 'SHORT'
        #     self.v_reason_close = self.resetted
        #     self.f_main3()
        #     self.trigger_open = 'LONG'
        #     self.v_reason_open = self.resetted
        #     self.f_main3()
        #     self.resetted = ''
        # endregion

    def f_main3(self):
        if self.v_direction == 'NO_POS':
            if not self.trigger_open == '':
                self.f_open_position(self.trigger_open)
                return
        elif self.v_direction == 'Empty':
            if self.trigger_close == 'SHORT':
                self.f_close_position()
                return
        elif self.v_direction == 'Multi':
            if self.trigger_close == 'LONG':
                self.f_close_position()
                return

    def f_last_reset_time(self, now, key, offset=0):
        if key >= 60:
            if key == 304:
                # condition = 30 <= (now - self.script_timeframe[key][0]).seconds <= 32
                condition = 29 <= now.second <= 31 or 59 <= now.second or 0 <= now.second <= 1
                # offset2 = -2
                # condition = (now - self.script_timeframe[key][0]).seconds >= 60 and (now.minute - offset2) % int(key / 60) == 0
                # if not condition:
                #     offset2 = -4
                #     condition = (now - self.script_timeframe[key][0]).seconds >= 30 and (now.minute - offset2) % int(key / 60) == 0
                # if not condition:
                #     offset2 = -1
                #     condition = (now - self.script_timeframe[key][0]).seconds >= 30 and (now.minute - offset2) % int(key / 60) == 0
            else:
                condition = (now - self.script_timeframe[key][0]).seconds >= 60 and (now.minute - offset) % int(
                    key / 60) == 0
            if key == 306:
                condition = condition and now.second >= 7
        else:
            condition = (now - self.script_timeframe[key][0]).seconds >= 1 and now.second % key == 0
        if condition:
            self.script_timeframe[key][0] = now.replace(second=0, microsecond=0)
            self.script_timeframe[key][1][0] = float(0)
            self.script_timeframe[key][2] = f"{'{:.2f}'.format(self.cumulative_value)}"
            return True
        else:
            if self.prices[1] != float(0):
                self.script_timeframe[key][1].insert(0, self.script_timeframe[key][1][0] + round(self.prices[0],2) - round(self.prices[1],2))
                if len(self.script_timeframe[key][1]) > 5:
                    self.script_timeframe[key][1].pop()
                if self.script_timeframe[key][1][0] > 0:
                    self.script_timeframe[key][2] = f"+{'{:.2f}'.format(self.script_timeframe[key][1][0])}"
                else:
                    self.script_timeframe[key][2] = f"{'{:.2f}'.format(self.script_timeframe[key][1][0])}"
            return False

    def f_update_textbox(self, note='', blank_before=False, blank_after=False, header_only=False, note2=False):
        list_output = [
            ['unr_p/l', '{:.2f}'.format(self.v_unrealized) if not note2 else ''],
            ['yld', '{:.2f}'.format(self.v_yield) if not note2 else ''],
            ['note2', self.note2],
            ['date', self.f_current_time(out='date') if not note2 else ''],
            ['time', self.f_current_time(out='time') if not note2 else ''],
            ['evat_dir', self.v_direction_evat if not note2 else ''],
            ['direction', self.v_direction if not note2 else ''],
            ['C_price', '{:.2f}'.format(self.prices[0]) if not note2 else ''],
            ['elw_price', '{:.2f}'.format(round(self.v_evat_latest_price, 2)) if not note2 else ''],
        ['esp', '{:.2f}'.format(self.v_esp) if not note2 else ''],
        ['vol', Variables.Misc.tv_vol if not note2 else ''],
        ['evat_balance', '{:.2f}'.format(self.v_bal_elw) if not note2 else ''],
        ['sim_balance', '{:.2f}'.format(self.v_bal) if not note2 else ''],
        # ['tv_5s', f'\'{Variables.Misc.tradingview_charts_data[1]}' if not note2 else ''],
        # ['tv_10s', f'\'{Variables.Misc.tradingview_charts_data[2]}' if not note2 else ''],
        # ['tv_15s', f'\'{Variables.Misc.tradingview_charts_data[3]}' if not note2 else ''],
        # ['tv_30s', f'\'{Variables.Misc.tradingview_charts_data[4]}' if not note2 else ''],
        # ['tv_1m', f'\'{Variables.Misc.tradingview_charts_data[5]}' if not note2 else ''],
        # ['tv_2m', f'\'{Variables.Misc.tradingview_charts_data[6]}' if not note2 else ''],
        # ['tv_3m', f'\'{Variables.Misc.tradingview_charts_data[7]}' if not note2 else ''[],

        # ['tv_5m', f'\'{Variables.Misc.tradingview_charts_data[8]}' if not note2 else ''],
        ['sc_5m_3', f'\'{self.script_timeframe[304][2]}' if not note2 else ''],
        ['sc_5m_6', f'\'{self.script_timeframe[306][2]}' if not note2 else ''],
        # ['script', f"\'{self.note3}" if not note2 else ''],
        ['sum_net', f"{'{:.2f}'.format(self.sum_net[0])}" if not note2 else ''],
        ['sum_net2', f"{'{:.2f}'.format(self.sum_net2[0])}" if not note2 else ''],
        ['note', note if not note2 else ''],
        ['PRCLPR', f"\'{'{:.2f}'.format(self.prclpr)}" if not note2 else ''],
        ['O', f"\'{'{:.2f}'.format(Variables.XPaths.tradingview_ohlc['O'][1])}" if not note2 else ''],
        ['H', f"\'{'{:.2f}'.format(Variables.XPaths.tradingview_ohlc['H'][1])}" if not note2 else ''],
        ['L', f"\'{'{:.2f}'.format(Variables.XPaths.tradingview_ohlc['L'][1])}" if not note2 else ''],
        ['C', f"\'{'{:.2f}'.format(Variables.XPaths.tradingview_ohlc['C'][1])}" if not note2 else ''],
        ['sc_5s', f'\'{self.script_timeframe[5][2]}' if not note2 else ''],
        ['sc_10s', f'\'{self.script_timeframe[10][2]}' if not note2 else ''],
        ['sc_15s', f'\'{self.script_timeframe[15][2]}' if not note2 else ''],
        ['sc_30s', f'\'{self.script_timeframe[30][2]}' if not note2 else ''],
        ['sc_1m', f'\'{self.script_timeframe[60][2]}' if not note2 else ''],
        ['sc_2m', f'\'{self.script_timeframe[120][2]}' if not note2 else ''],
        ['sc_3m', f'\'{self.script_timeframe[180][2]}' if not note2 else ''],
        ['sc_4m', f'\'{self.script_timeframe[240][2]}' if not note2 else ''],
        ['sc_5m', f'\'{self.script_timeframe[300][2]}' if not note2 else ''],
        # ['HA1', f'\'{Variables.Misc.tv_HA[1][1]}' if not note2 else ''],
        # ['HA2', f'\'{Variables.Misc.tv_HA[2][1]}' if not note2 else ''],
        # ['HA3', f'\'{Variables.Misc.tv_HA[3][1]}' if not note2 else ''],
        # ['HA4', f'\'{Variables.Misc.tv_HA[4][1]}' if not note2 else ''],
        # ['HA5', f'\'{Variables.Misc.tv_HA[5][1]}' if not note2 else ''],
        # ['sc_5m_2', f'\'{self.script_timeframe[300][5]}' if not note2 else ''],
        # ['last_rev', self.cumulative_value_str2 if not note2 else ''],
        # ['to_SL/to_TP', self.v_tp_sl_str if not note2 else ''],
        # ['aop', '{:.2f}'.format(self.v_aop) if not note2 else ''],
        # ['aop-esp', '{:.2f}'.format(self.v_diff) if not note2 else ''],
        # ['alert1', f"{self.alerts_dict['ALERT1'][0]}" if not note2 else ''],
        # ['recent', f"{self.alerts_dict['ALERT1'][1]}" if not note2 else ''],
        # ['previous', f"{self.alerts_dict['ALERT1'][2]}" if not note2 else ''],
        ]
        if header_only:
            return [[f"{','.join([sublist[0] for sublist in list_output])}"]]

        self.textbox_row1 = ','.join([sublist[1] for sublist in list_output])
        self.textbox_row2 = f'Recent Alert: {self.raw_data_message}'
        # self.floating_text_obj.update_text(f"{self.textbox_row1}\n{self.textbox_row2}\n{self.textbox_row3}\n{self.textbox_row4}\n{self.textbox_row5}")
        csv_string = [[self.textbox_row1]]
        if blank_before:
            csv_string = [[]] + csv_string
        if blank_after:
            csv_string = csv_string + [[]]
        self.output = csv_string + self.output
        for key, value in self.alerts_dict.items():
            value[2] = value[1]
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

        # self.driver.get(Variables.Misc.url_evatcoin)
        time.sleep(0.1)

        try:
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_current_price).click
        except:
            time.sleep(1)

        try:
            self.v_bal_elw = extract_float_numbers(
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_balance).text)
        except:
            self.v_bal_elw = float(0)

        try:
            self.v_direction_evat = self.driver.find_element(By.XPATH, Variables.XPaths.evatcoin_direction).text
        except:
            self.v_direction_evat = 'NO_POS'

        try:
            self.v_esp = extract_float_numbers(
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_esp).text)
        except:
            self.v_esp = float(0)

        while len(self.checker_prices) >= 200:
            self.checker_prices.pop()

        self.checker_prices.insert(0, float(self.prices[0]))

        if all(val == self.checker_prices[0] for val in self.checker_prices) and len(self.checker_prices) > 150:
            self.driver.get(Variables.Misc.url_evatcoin)
            self.checker_prices.pop()
            self.checker_prices.pop()
            self.checker_prices.insert(0, float(123))
            self.checker_prices.insert(0, float(self.prices[0]))

        if self.v_direction == 'Multi':
            self.v_tp_sl_str = f"{'{:.2f}'.format(float(self.prices[0]) - ((float(self.v_aop)) - ((float(self.v_aop) * float(self.percent_stop_loss)) / (100 * Variables.Misc.leverage[0]))))}/{'{:.2f}'.format(-float(self.prices[0]) + ((float(self.v_aop)) + ((float(self.v_aop) * float(self.percent_take_profit)) / (100 * Variables.Misc.leverage[0]))))}"
            self.v_yield = Variables.Misc.leverage[0] * 100 * (
                        (float(self.prices[0]) - float(self.v_aop)) / float(self.v_aop))
        elif self.v_direction == 'Empty':
            self.v_tp_sl_str = f"{'{:.2f}'.format(-float(self.prices[0]) + ((float(self.v_aop)) + ((float(self.v_aop) * float(self.percent_stop_loss)) / (100 * Variables.Misc.leverage[0]))))}/{'{:.2f}'.format(float(self.prices[0]) - ((float(self.v_aop)) - ((float(self.v_aop) * float(self.percent_take_profit)) / (100 * Variables.Misc.leverage[0]))))}"
            self.v_yield = Variables.Misc.leverage[0] * 100 * (
                        (-float(self.prices[0]) + float(self.v_aop)) / float(self.v_aop))
        else:
            self.v_yield = float(0)
            self.v_tp_sl_str = '-/-'

        self.v_unrealized = (float(self.v_bal_leaf * (self.v_yield / 100)))
        self.v_bal = self.v_bal_open + self.v_bal_leaf * (self.v_yield / 100)

        test = True
        while test:
            print(round(self.v_evat_latest_price, 2))
            try:
                self.v_evat_latest_price = extract_float_numbers(
                    self.driver.find_element(By.XPATH, Variables.XPaths.evatcoin_current_price).text)
                test = False
            except:
                self.driver.get(Variables.Misc.url_evatcoin)
                time.sleep(5)

        print('SCRAPING EVATCOIN DONE')

    def f_get_data_tradingview(self):
        while True:
            if Variables.Misc.state_break:
                break
            try:
                # self.driver.switch_to.window(self.driver.window_handles[1])
                print('SCRAPING TRADINGVIEW')
                self.driver.find_element(By.XPATH, '/html/body/div/main/div/div[1]/div[1]/div[1]/div[1]/div[2]').click()
                WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))
                # inner_iframe = self.driver.find_element(By.TAG_NAME, 'iframe')
                # self.driver.switch_to.frame(inner_iframe)
                legend = self.driver.find_element(By.CLASS_NAME, 'pane-legend')
                pass_1 = False
                while not pass_1:
                    try:
                        pane_legend_item_value_title = legend.find_elements(By.CLASS_NAME,
                                                                            'pane-legend-item-value-title')
                        pane_legend_item_value = legend.find_elements(By.CLASS_NAME, 'pane-legend-item-value')
                        # pane_legend_item_value[0].click()
                        index = 0
                        for _ in pane_legend_item_value_title:
                            if index == 0:
                                Variables.XPaths.tradingview_ohlc['O'][1] = float(
                                    pane_legend_item_value[index].text.replace("'", "."))
                            if index == 1:
                                Variables.XPaths.tradingview_ohlc['H'][1] = float(
                                    pane_legend_item_value[index].text.replace("'", "."))
                            if index == 2:
                                Variables.XPaths.tradingview_ohlc['L'][1] = float(
                                    pane_legend_item_value[index].text.replace("'", "."))
                            if index == 3:
                                Variables.XPaths.tradingview_ohlc['C'][1] = float(
                                    pane_legend_item_value[index].text.replace("'", "."))
                            # line_text += title.text + ': ' + pane_legend_item_value[index].text + ' '
                            index += 1
                            pass_1 = True
                    except Exception as e:
                        print(e)
                        self.driver.get(Variables.Misc.url_evatcoin)
                        time.sleep(5)
                        self.driver.find_element(By.XPATH,
                                                 '/html/body/div/main/div/div[1]/div[1]/div[1]/div[1]/div[2]').click()
                        WebDriverWait(self.driver, 20).until(
                            EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))
                        # inner_iframe = self.driver.find_element(By.TAG_NAME, 'iframe')
                        # self.driver.switch_to.frame(inner_iframe)
                        legend = self.driver.find_element(By.CLASS_NAME, 'pane-legend')
                        pass_1 = False

                # error = True
                # latest_price = 0
                # while error:
                #     try:
                #         latest_price = round(float(self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_ohlc['C'][0]).text),2)
                #         error = False
                #         if latest_price == 0:
                #             error = True
                #     except:
                #         error = True

                self.prices.insert(0, round(Variables.XPaths.tradingview_ohlc['C'][1],2))
                while len(self.prices) > 10:
                    self.prices.pop()

                if self.anchor_price_2 == 0:
                    self.anchor_price_2 = self.prices[0]

                # try:
                #     raw_data = self.wait.until(ec.presence_of_element_located((By.XPATH, Variables.XPaths.tradingview_logs[1]))).text
                #     self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_charts[1]).click()
                #     raw_data = raw_data.split('\n')
                # except:
                #     self.driver.get(Variables.Misc.url_tradingview)
                #     time.sleep(3)
                #     continue
                try:
                    Variables.Misc.tv_vol = self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_volume).text
                    # Variables.Misc.tv_vol = float(Variables.Misc.tv_vol)
                except:
                    Variables.Misc.tv_vol = ''
                    # Variables.Misc.tv_vol = float(0)
                # for key in Variables.Misc.tv_HA:
                #     Variables.Misc.tv_HA[key][1] = self.driver.find_element(By.XPATH, Variables.Misc.tv_HA[key][0]).text

                # error = True
                # while error:
                #     try:
                #         Variables.XPaths.tradingview_ohlc['O'][1] = round(float(self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_ohlc['O'][0]).text),2)
                #         Variables.XPaths.tradingview_ohlc['H'][1] = round(float(self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_ohlc['H'][0]).text),2)
                #         Variables.XPaths.tradingview_ohlc['L'][1] = round(float(self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_ohlc['L'][0]).text),2)
                #         Variables.XPaths.tradingview_ohlc['C'][1] = self.prices[0]
                #         error = False
                #     except:
                #         error = True

                # for i in range(1, 9):
                #     Variables.Misc.tradingview_charts_data[i] = self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_charts[i]).text
                #     text = Variables.Misc.tradingview_charts_data[i]
                #     text = text.replace('(', '').replace(')', '').replace('%', '').replace('−', '-')
                #     print(f'text{i}:{text}')
                #     try:
                #         matches = text.split()
                #         Variables.Misc.tradingview_charts_data1[i] = matches[0]
                #         Variables.Misc.tradingview_charts_data2[i][0] = matches[1]
                #     except Exception as e:
                #         print(f'error:{e}')

                # self.raw_data_message = f'{raw_data[1]}'
                # try:
                #     # if not (any(s.lower() in self.raw_data_message.lower() for s in [self.alerts_dict[key][0].lower() for key in self.alerts_dict])):
                #     #     raise ValueError('WrongFormat')
                #     # if not (any(s.lower() in self.raw_data_message.lower() for s in ['long', 'short'])):
                #     #     raise ValueError('WrongFormat')
                #     self.raw_data_message = raw_data[1]
                #     raw_data_message_splitted = self.raw_data_message.split(',')
                #     self.alert_new = self.f_process_alert_new(raw_data_message_splitted)
                #     self.alert_new_time = raw_data_message_splitted[3].strip()
                #     self.alert_new_time_obj = datetime.strptime(self.alert_new_time, "%Y-%m-%dT%H:%M:%SZ")
                #     self.current_time_utc = datetime.utcnow()
                #     time_diff = self.current_time_utc - self.alert_new_time_obj
                #     for key, value in sorted(Variables.XPaths.tradingview_logs.items(), reverse=True):
                #         try:
                #             raw_data_message_splitted = self.driver.find_element(By.XPATH, value).text
                #             raw_data_message_splitted = raw_data_message_splitted.split('\n')
                #             raw_data_message_splitted = raw_data_message_splitted[1]
                #             raw_data_message_splitted = raw_data_message_splitted.split(',')
                #             self.f_process_alert_new(raw_data_message_splitted)
                #         except:
                #             pass
                #     self.count_short = 0
                #     self.count_long = 0
                #     for value in self.alerts_dict.values():
                #         if value[1].lower() == 'short':
                #             self.count_short += 1
                #         elif value[1].lower() == 'long':
                #             self.count_long += 1
                #     if time_diff.total_seconds() > 120:
                #         self.textbox_row3 = f'Current time: {self.current_time_utc} has passed more than 2 minutes than alert time: {self.alert_new_time_obj}\nR'
                #         self.note = ''
                #         self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_charts[1]).click()
                #     else:
                #         self.textbox_row3 = 'ROW3'
                #         self.note = ''
                print('SCRAPING TRADINGVIEW DONE')
                return
                # except:
                #     self.textbox_row3 = 'Wrong alert message format. Please make sure you use this format in the alert message:\nLONG/SHORT, 30 Min, MESSAGE, {{timenow}}, '
                #     self.f_update_textbox('ALERT_FORMAT_WRONG')
                #     time.sleep(1)
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
            # options.set_capability("detach", True)
            options.add_experimental_option("detach", True)
            options.service_args = ['--keep-alive']
            print('Installing driver. restart if this this takes too long')
            # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver = webdriver.Chrome(options=options)
            print('Driver installed')
            self.wait = WebDriverWait(self.driver, 10)

            self.driver.get(Variables.Misc.url_evatcoin)
            self.driver.execute_script('window.open("");')
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(0.2)
            # self.driver.get(Variables.Misc.url_tradingview)
            return self.driver
        except Exception as e:
            print(e)
            messagebox.showinfo("ALERT",
                                'Make sure you have an internet connection before starting the script.\nExiting...')
            self.driver.quit()
            self.root.destroy()
            sys.exit()

    def f_current_time(self, out='all'):
        self.v_current_time_str = datetime.now().strftime("%Y-%m-%d,%H:%M:%S.%f")[:-3]
        if out == 'date':
            return datetime.now().strftime("%Y-%m-%d")
        elif out == 'time':
            return datetime.now().strftime("%H:%M:%S.%f")[:-3]
        else:
            return self.v_current_time_str

    def format_csv_string(self, csv_string):
        items = csv_string.split(',')
        if len(items) < self.csv_columns:
            items += [''] * (self.csv_columns - len(items))
        elif len(items) > self.csv_columns:
            raise ValueError(f'CSV string has more than {self.csv_columns} columns')
        return ','.join(items)

    def f_open_position(self, direction, full=True):
        if self.v_bal >= self.leaf_size:
            if direction.upper() == 'LONG':
                self.v_direction = 'Multi'
            else:
                self.v_direction = 'Empty'
            if full:
                self.v_aop = float(self.prices[0])
                self.v_bal = self.v_bal - Variables.Misc.leverage[1] * self.v_bal_leaf
                self.v_bal_open = self.v_bal
                self.str_profit_loss = "{:.2f}".format(- Variables.Misc.leverage[1] * self.v_bal_leaf)
                self.v_reason_open = self.v_reason_open + f' p/l: {self.str_profit_loss}'

                print(f'{self.v_bal} - {direction}')
                self.note2 = f"O {direction.upper()}: {self.v_reason_open}"
                self.f_update_textbox(blank_after=True, blank_before=True, note2=True)
                self.note2 = ''
        else:
            self.note2 = f"O {direction.upper()}: {self.v_reason_open} -- FAILED! NOT ENOUGH BALANCE"
            self.f_update_textbox(blank_after=True, blank_before=True, note2=True)
            self.note2 = ''

        self.f_get_data_evatcoin()
        if self.v_direction_evat == 'NO_POS':
            self.f_open_evat()
            print('open evat')

        self.sum_net2.insert(0, float(0))
        self.v_reason_open = ''
        self.trigger_open = ''
        self.v_reason_close = ''
        self.trigger_close = ''
        self.count_consecutive = 0
        self.diff.insert(0, round(float(0), 2))

        return

    def f_close_position(self, full=True):
        if full:
            self.v_aop = 0
            self.v_bal = self.v_bal - Variables.Misc.leverage[1] * self.v_bal_leaf
            self.str_profit_loss = "{:.2f}".format(
                self.v_bal - self.v_bal_open - Variables.Misc.leverage[1] * self.v_bal_leaf)
            self.v_bal_open = self.v_bal
            self.v_reason_close = self.v_reason_close + f' p/l: {self.str_profit_loss}'
            self.note2 = f"C: {self.v_reason_close}"
            self.f_update_textbox(blank_after=True, blank_before=True, note2=True)
            self.note2 = ''
        if self.v_direction_evat != 'NO_POS':
            self.f_close_evat()
            time.sleep(7)
            print('close evat')
        self.v_direction = 'NO_POS'
        self.sum_net2.insert(0, float(0))
        self.v_reason_open = ''
        self.trigger_open = ''
        self.v_reason_close = ''
        self.trigger_close = ''
        self.count_consecutive = 0
        self.diff.insert(0, round(float(0), 2))
        return


def extract_float_numbers(string):
    pattern = r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
    float_numbers = re.findall(pattern, string)

    # Convert the matched float numbers to actual floats
    float_numbers = float(float_numbers[0])

    return float_numbers


class LocalSheets:
    def __init__(self):
        self.file = 'data.txt'
        self.SERVICE_ACCOUNT_FILE = 'keys.json'
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE,
                                                                           scopes=self.SCOPES)
        self.SPREADSHEET_ID = '14H-OyOk_rdHtuTCj6lRj5C1__BJksgskzBg9G5NOCpo'
        # self.SPREADSHEET_ID = '1liNHmgvzUeCjYVIPTywnQEeavIgaB2e0BeJFmrqR5l8'
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
        self.count1 = 0
        self.SERVICE_ACCOUNT_FILE = 'keys.json'
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE,
                                                                           scopes=self.SCOPES)
        self.SPREADSHEET_ID = '14H-OyOk_rdHtuTCj6lRj5C1__BJksgskzBg9G5NOCpo'
        # self.SPREADSHEET_ID = '1liNHmgvzUeCjYVIPTywnQEeavIgaB2e0BeJFmrqR5l8'
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.localspreadsheet = LocalSheets().file

    def append(self, data):
        print('UPDATING TO GOOGLE SHEETS')
        self.backup()
        instance1 = MainFunction('', '')
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
                        'data': '\n'.join(
                            [','.join(map(str, row)) for row in instance1.f_update_textbox(header_only=True) + data]),
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

    def backup(self, row_limit=5000, clear=False):
        # Authenticate with Google Sheets API
        credentials = self.creds
        client = gspread.authorize(credentials)

        # Open the spreadsheet
        spreadsheet_id = self.SPREADSHEET_ID
        sheet_name = 'Sheet1'
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        if clear:
            worksheet.clear()
        # Get the row count
        row_count = worksheet.row_count

        # Check if row count exceeds 5000
        if row_count > row_limit:
            # Duplicate the sheet
            # self.count1 += 1
            # duplicated_sheet = spreadsheet.duplicate_sheet(worksheet.id, new_sheet_name=f'BU{i}')

            # Clear rows 5 to the end of the sheet
            # duplicated_worksheet = spreadsheet.worksheet(duplicated_sheet['properties']['title'])
            worksheet.delete_rows(row_limit, row_count - 1)  # Assuming headers are in row 1

            print("rows deleted successfully!")
        else:
            print("No need")

        return