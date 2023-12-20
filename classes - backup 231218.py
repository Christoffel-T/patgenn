from __future__ import print_function

import base64
import ctypes
import math
import os
import re
import sys
import time
import tkinter as tk
from datetime import datetime, timedelta
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
from selenium.common.exceptions import NoSuchElementException

# UPDATE1
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
        evatcoin_current_price = "/html/body/div/main/div/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]"
        tradingview_ohlc_prev = {
            'C': ['', float(0)]
        }
        evatcoin_perpetual = '//*[@id="headerMenu"]/ul[1]/li[4]/a'
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
                  [float(0)]],
            'H': ['/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/div[3]/div/div/span[2]/span[2]',
                  [float(0)]],
            'L': ['/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/div[3]/div/div/span[3]/span[2]',
                  [float(0)]],
            'C': ['/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/div[3]/div/div/span[4]/span[2]',
                  [float(0)]],
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
        tv_vol = 0
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

    # def update_text(self, new_text, show_ok=False):
    #     if Variables.Misc.state_break:
    #         print('Stopped')
    #         return
    #     self.text_box.delete("1.0", "end")
    #     self.text_box.insert("1.0", new_text)
    #     # self.master.update()
    #     print(new_text)
    #     if show_ok:
    #         pass
    #     #     self.show_ok_button()
    #     return new_text

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
    def __init__(self, root):
        self.list_group_multi = []
        self.list_group_empty = []
        self.state_resetted_NOTES2group_empty = False
        self.state_resetted_NOTES2group_multi = False
        self.state_resetted_NOTES2group = False
        self.count_logic_group_multi = 0
        self.count_logic_group_empty = 0
        self.count_logic_group = 0
        self.tradingview_scraped = False
        self.current_time = datetime.now().replace(second=0, microsecond=0)
        self.sum_3_cumulative_c = [float(0) for _ in range(10)]
        self.state_logic_NOTES2_reverse = ''
        self.sum_3_cumulative_b = [float(0) for _ in range(10)]
        self.count_entries_11b = 0
        self.sum_3_cumulative_a = [float(0) for _ in range(10)]
        self.count_entries_11 = 0
        self.diff_5s = [float(0) for _ in range(10)]
        self.anchor_price_5s = [float(0) for _ in range(10)]
        self.total_pos3new = [float(0) for _ in range(10)]
        self.total_neg3new = [float(0) for _ in range(10)]
        self.total_sum3new = [float(0) for _ in range(10)]
        self.sum_H_expand = float(0)
        self.sum_L_expand = float(0)
        self.closed_NOTES2c = [float(0) for _ in range(10)]
        self.marked_sum_NOTES2 = float(0)
        self.marked_sum_NOTES2_multi = float(0)
        self.marked_sum_NOTES2_empty = float(0)
        self.state_sumAFsame2 = ''
        self.suspender2 = ''
        self.suspender = ''
        self.count_changes_after_suspender = 0
        self.state_sumAFsame = ''
        self.count_changes_after_sumAFsame = 0
        self.state_logic_marked_price = ''
        self.marked_price = float(0)
        self.state_logic_saf3 = ''
        self.state_logic_Cp = ''
        self.state_logic_HpLp = ''
        self.v_bal_reset = float(75)
        self.count_changes_after_HL = 0
        self.count_changes_after_HL2 = 0
        self.state_logic_HL2 = ''
        self.state_logic_HL = ''
        self.closed_O = [float(0) for _ in range(10)]
        self.closed_H = [float(0) for _ in range(10)]
        self.closed_L = [float(0) for _ in range(10)]
        self.closed_C = [float(0) for _ in range(10)]
        self.sum_af_OPENED = float(0)
        self.count_crossed_cprc = 0
        self.count_changes_after_3consec = 0
        self.sum_AF_marked = float(0)
        self.count_balance_add = 0
        self.count_changes_after_trigger_AF = 0
        self.state_logic_AF = ''
        self.state_C_PRC = ''
        self.count_changes_after_trigger_NOTES2 = 0
        self.state_logic_NOTES2 = ''
        self.trigger_AF = ''
        self.trigger_AF_count = 0
        self.last_AF_val = float(0)
        self.sum_AF = [float(0) for _ in range(10)]
        self.sum_AF2 = [float(0) for _ in range(10)]
        self.sum_AF3 = [float(0) for _ in range(10)]
        self.sum_from_AF4 = [float(0) for _ in range(10)]
        self.count_changes_after_trade = 0
        self.profit_taken = float(0)
        self.last_pos = ''
        self.count_closed_15m_multi = 0
        self.count_closed_15m_empty = 0
        self.count_trades_profit = 0
        self.count_trades = 0
        self.price_changes = [float(0) for _ in range(10)]
        self.count_opened_15m = 0
        self.last_reason = ''
        self.O_prices = [float(0)]
        self.H_prices = [float(0)]
        self.L_prices = [float(0)]
        self.C_price = [float(0)]
        self.hl = float(0)
        self.multiavg = [float(0) for _ in range(10)]
        self.emptyavg = [float(0) for _ in range(10)]
        self.total_sum4 = [float(0) for _ in range(10)]
        self.total_sum5 = [float(0) for _ in range(10)]
        self.total_pos4 = [float(0) for _ in range(10)]
        self.total_pos5 = [float(0) for _ in range(10)]
        self.total_neg4 = [float(0) for _ in range(10)]
        self.total_neg5 = [float(0) for _ in range(10)]
        self.total_sum3 = [float(0) for _ in range(10)]
        self.total_pos3 = [float(0) for _ in range(10)]
        self.total_neg3 = [float(0) for _ in range(10)]
        self.total_sum2 = [float(0) for _ in range(10)]
        self.total_pos2 = [float(0) for _ in range(10)]
        self.total_neg2 = [float(0) for _ in range(10)]
        self.total_sum2_new = [float(0) for _ in range(10)]
        self.total_pos2_new = [float(0) for _ in range(10)]
        self.total_neg2_new = [float(0) for _ in range(10)]
        self.qualifier_W_A_total_multi = False
        self.qualifier_W_A_total_empty = False
        self.sum_4_state = ''
        self.sum_4 = [float(0)]
        self.prices_5sec = []
        self.sec5_note = ''
        self.W_A_total = [float(0), float(0), float(0), float(0)]
        self.W_A = [float(0), float(0), float(0), float(0)]
        self.average_diff_sum = [float(0), float(0), float(0), float(0)]
        self.average_diff = [float(0), float(0), float(0), float(0)]
        self.average_prc = [float(0), float(0), float(0), float(0)]
        self.qualifier_comb5 = ['NONE', 0]
        self.average_HL = [float(0)]
        self.custom1 = True
        self.peak_price = float(0)
        self.text = ''
        self.qualifier_comb2_multi = False
        self.qualifier_comb2_empty = False
        self.qualifier_SUM3 = float(0)
        self.sum_net3 = [float(0), float(0), float(0), float(0)]
        self.qualifier_sc6_empty = None
        self.qualifier_sc6_multi = None
        self.qualifier_sum1_empty = None
        self.qualifier_sum1_multi = None
        self.qualifier_vol = None
        self.qualifier_tv_vol = 0
        self.last_minute = -1
        self.prclprs = [float(0), float(0), float(0), float(0)]
        self.count_qualifier_SUM1 = 0
        self.count_qualifier_SUM2 = 0
        self.count_qualifier_SUM = float(0)
        self.count_qualifier_NOTES = 0
        self.disable_sum = False
        self.count_qualifier_OHCPRC = 0
        self.sum_NOTES2 = [float(0), float(0), float(0), float(0)]
        self.count_qualifier_COP = 0
        self.count_qualifier_OLHO = 0
        self.count_stoploss = 0
        self.qualifier_stoploss = ''
        self.count_sudden = 0
        self.diff = [float(0), float(0)]
        self.diff_anchor = [float(0), float(0)]
        self.no_repeat_time = None
        self.state_prclpr = ''
        self.prclpr = float(0)
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
        self.prices = [float(0), float(0)]
        self.count_tfsc_long2 = 0
        self.count_tfsc_short2 = 0
        self.count_rows_2 = 0
        self.count_rows_3 = 0
        self.v_reason_open = ''
        self.state_logic4 = ''
        self.state_logic3 = ''
        self.state_logic2 = ''
        self.take_profit = float(0)
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
        # self.floating_text_obj = floating_text_obj
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
        self.v_bal_now = self.v_bal_reset
        self.v_percentage = 1
        self.leaf_size = Variables.Misc.leverage[2]
        self.v_buy_qty = math.ceil((self.v_bal_now * self.v_percentage) / self.leaf_size)
        self.v_bal_leaf = self.v_buy_qty * self.leaf_size
        self.v_diff = float(0)
        self.v_esp = float(0)
        self.v_unrealized = float(0)
        self.v_yield = float(0)
        self.v_current_time_str = self.f_current_time()
        self.v_bal_open = self.v_bal_now
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
            5: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            10: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            15: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            30: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            60: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            120: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            180: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            240: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            300: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            304: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
            306: [datetime.now().replace(second=0, microsecond=0), [float(0), float(0)], 0, float(0), float(0), ''],
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
        self.checker_prices = [float(0)]
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
            if self.v_bal_elw < 1000000:
                print('NOT ENOUGH BALANCE')
                return
            # self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_leverage[0]).click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_leverage[3]).click()
            time.sleep(0.5)
            input_elem = self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_buy_qty)
            input_elem.clear()
            v_buy_qty = math.ceil((self.v_bal_elw * self.v_percentage) / self.leaf_size)
            input_elem.send_keys(v_buy_qty)
            time.sleep(0.5)
            if self.v_direction == 'Multi':
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_open_long).click()
                print('opened long')
            elif self.v_direction == 'Empty':
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_open_short).click()
                print('opened short')
            else:
                print('nodirection')
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_open_confirm).click()
            time.sleep(0.5)

        except:
            self.f_update_textbox('evat_open_error', True, True)
            print('evat_open_error')
            raise ValueError

    def f_main1(self):
        self.f_open_chrome()
        # self.floating_text_obj.update_text('RUNNING')
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
            except NoSuchElementException:
                error = True
                while error:
                    try:
                        self.driver.get(Variables.Misc.url_evatcoin)
                        self.driver.refresh()
                        print(f"refresh 513")
                        time.sleep(5)
                        error = False
                    except:
                        error = True
                time.sleep(5)

    def f_main2(self):

        # region GET-DATA: Misc
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        now = datetime.now()
        if now < self.current_time + timedelta(seconds=1):
            time.sleep(0.1)
            return
        now = now.replace(microsecond=0)
        self.current_time = now
        print(f'\n=== Loop at: {self.f_current_time(now)}')
        if Variables.Misc.state_break:
            print('Stopped')
            return 'break'
        if (now - self.last_reset_time_googlesheet).seconds >= 10:
            self.last_reset_time_googlesheet = now.replace(microsecond=0)
            if self.LocalSheets.append(self.output):
                self.output = []
        if not self.tradingview_scraped:
            self.f_get_data_tradingview()
            self.tradingview_scraped = True
        self.f_get_data_evatcoin()
        subtext2 = ''

        # endregion1

        # region GET-DATA: Misc
        if self.prices[0] > self.prices[1] > 0:
            if self.count_consecutive < 0:
                self.count_consecutive = 0
                self.qualifier_comb5[1] = 0
            if self.count_consecutive == 0:
                self.anchor_price = self.prices[1]
            self.count_consecutive += 1
            self.qualifier_comb5[1] += 1
            self.count_stoploss += 1
        elif self.prices[0] < self.prices[1] > 0:
            if self.count_consecutive > 0:
                self.count_consecutive = 0
                self.qualifier_comb5[1] = 0
            if self.count_consecutive == 0:
                self.anchor_price = self.prices[1]
            self.count_consecutive -= 1
            self.qualifier_comb5[1] -= 1
            self.count_stoploss -= 1

        if self.anchor_price == 0:
            self.anchor_price = self.prices[0]

        self.subtext1 = ''
        if self.prices[1] != 0 and self.prices[0] != self.prices[1]:
            self.diff = [round(self.prices[0] - self.prices[1], 2)] + self.diff[:9]
        self.diff_anchor = [round(self.prices[0] - self.anchor_price, 2)] + self.diff_anchor[:9]
        diff = self.diff_anchor[0]

        #endregion

        #region PRICE CHANGE
        if self.prices[0] != self.prices[1]:
            if self.diff[0] <= -10:
                self.total_neg5.insert(0, self.diff[0])

            if self.H_prices[0] > self.O_prices[0] or self.L_prices[0] < self.O_prices[0]:
                self.total_pos4.insert(0, 0)
                self.total_neg4.insert(0, 0)

            if self.prices[0] > self.prclprs[0] or self.prices[0] < self.prclprs[0]:
                self.total_pos3.insert(0, 0)
                self.total_neg3.insert(0, 0)

            self.average_diff = [round((self.diff[0] - self.average_diff[0]) / 2, 2)] + self.average_diff[:9]
            self.count_changes_after_suspender += 1
            self.count_changes_after_sumAFsame += 1
            self.count_changes_after_HL2 += 1
            self.count_changes_after_HL += 1
            self.count_changes_after_trade += 1
            self.count_changes_after_trigger_NOTES2 += 1
            self.count_changes_after_trigger_AF += 1
            self.count_changes_after_3consec += 1
            # average_diff = self.average_diff[0] - self.average_diff[1]
            self.average_diff_sum = [round(self.average_diff[0] + self.average_diff[1], 2)] + self.average_diff_sum[:9]
            self.sum_net = [round(self.sum_net[0] + self.diff[0], 2)] + self.sum_net[:9]
            self.sum_NOTES2 = [round(self.sum_NOTES2[0] + self.diff[0], 2)] + self.sum_NOTES2[:9]
            self.closed_NOTES2c[0] = self.sum_NOTES2[0]
            self.sum_net3 = [round(self.sum_net3[0] + self.diff[0], 2)] + self.sum_net3[:9]
            if self.diff[0] > 0:
                self.total_pos2 = [round(self.total_pos2[0] + self.diff[0], 2)] + self.total_pos2[:9]
                self.total_pos2_new = [round(self.total_pos2_new[0] + self.diff[0], 2)] + self.total_pos2_new[:9]
                self.total_pos3 = [round(self.total_pos3[0] + self.diff[0], 2)] + self.total_pos3[:9]
                self.total_pos3new = [round(self.total_pos3new[0] + self.diff[0], 2)] + self.total_pos3new[:9]
                self.total_pos4 = [round(self.total_pos4[0] + self.diff[0], 2)] + self.total_pos4[:9]
                self.total_pos5 = [round(self.total_pos5[0] + self.diff[0], 2)] + self.total_pos5[:9]
            if self.diff[0] < 0:
                self.total_neg2 = [round(self.total_neg2[0] + self.diff[0], 2)] + self.total_neg2[:9]
                self.total_neg2_new = [round(self.total_neg2_new[0] + self.diff[0], 2)] + self.total_neg2_new[:9]
                self.total_neg3 = [round(self.total_neg3[0] + self.diff[0], 2)] + self.total_neg3[:9]
                self.total_neg3new = [round(self.total_neg3new[0] + self.diff[0], 2)] + self.total_neg3new[:9]
                self.total_neg4 = [round(self.total_neg4[0] + self.diff[0], 2)] + self.total_neg4[:9]
                self.total_neg5 = [round(self.total_neg5[0] + self.diff[0], 2)] + self.total_neg5[:9]

            # if self.count_consecutive >= 3 and self.v_direction != 'Multi':
            #     self.total_pos2_new.insert(0, self.diff_anchor[0])
            #     self.total_neg2_new.insert(0, 0)
            #
            # if self.count_consecutive <= -3 and self.v_direction != 'Empty':
            #     self.total_pos2_new.insert(0, 0)
            #     self.total_neg2_new.insert(0, self.diff_anchor[0])

            self.total_sum2 = [round(self.total_pos2[0] + self.total_neg2[0], 2)] + self.total_sum2[:9]
            self.total_sum2_new = [round(self.total_pos2_new[0] + self.total_neg2_new[0], 2)] + self.total_sum2_new[:9]
            self.total_sum3 = [round(self.total_pos3[0] + self.total_neg3[0], 2)] + self.total_sum3[:9]
            self.total_sum3new = [round(self.total_pos3new[0] + self.total_neg3new[0], 2)] + self.total_sum3new[:9]

            self.sum_AF = [round(self.sum_AF[0] + self.total_sum3[0], 2)] + self.sum_AF[:9]
            self.sum_AF2 = [round(self.sum_AF2[0] + self.total_sum3[0], 2)] + self.sum_AF2[:9]
            self.sum_AF3 = [round(self.sum_AF3[0] + self.total_sum3[0], 2)] + self.sum_AF3[:9]
            self.sum_from_AF4 = [round(self.sum_from_AF4[0] + self.total_sum3[0], 2)] + self.sum_from_AF4[:9]

            self.total_sum4 = [round(self.total_pos4[0] + self.total_neg4[0], 2)] + self.total_sum4[:9]
            self.total_sum5 = [round(self.total_pos5[0] + self.total_neg5[0], 2)] + self.total_sum5[:9]

            self.sum_4 = [round(self.sum_4[0] + self.diff[0], 2)] + self.sum_4[:9]

            self.script_timeframe[304][1].insert(0, round(self.script_timeframe[304][1][0] + self.diff[0], 2))
            self.script_timeframe[306][1].insert(0, round(self.script_timeframe[306][1][0] + self.diff[0], 2))
            self.script_timeframe[304][2] = f"{str(self.script_timeframe[304][1][0])}"
            self.script_timeframe[306][2] = f"{str(self.script_timeframe[306][1][0])}"
            if self.script_timeframe[304][1][0] > 0:
                self.script_timeframe[304][2] = f"+{str(self.script_timeframe[304][1][0])}"
            if self.script_timeframe[306][1][0] > 0:
                self.script_timeframe[306][2] = f"+{str(self.script_timeframe[306][1][0])}"

        #endregion

        #region PROCESS DATA 1

        if self.anchor_price_5s[0] > 0:
            self.diff_5s[0] = round(self.prices[0] - self.anchor_price_5s[0],2)
            if self.prices[0] != self.prices[1]:
                self.sum_3_cumulative_a = [round(self.sum_3_cumulative_a[0] + self.diff[0], 2)] + self.sum_3_cumulative_a[:9]
                self.sum_3_cumulative_b = [round(self.sum_3_cumulative_b[0] + self.diff[0], 2)] + self.sum_3_cumulative_b[:9]
        self.count_entries_11 += 1
        if self.current_time.second in [x for x in range(4, 60, 5)]:
            self.anchor_price_5s[0] = self.prices[0]
            self.count_entries_11 = 0
            self.count_entries_11b += 1
            if self.total_sum3new[0] > 0:
                self.total_pos3new = [self.total_sum3new[0]] + self.total_pos3new[:9]
                self.total_neg3new = [float(0)] + self.total_neg3new[:9]
                self.total_sum3new = [round(self.total_pos3new[0] + self.total_neg3new[0], 2)] + self.total_sum3new[:9]
            if self.total_sum3new[0] < 0:
                self.total_pos3new = [float(0)] + self.total_pos3new[:9]
                self.total_neg3new = [self.total_sum3new[0]] + self.total_neg3new[:9]
                self.total_sum3new = [round(self.total_pos3new[0] + self.total_neg3new[0], 2)] + self.total_sum3new[:9]

        percent_diff = 0
        if self.anchor_price != 0:
            percent_diff = (diff / self.anchor_price) * 100
        percent_diff_str = f"{'{:.4f}'.format(percent_diff)}%"

        if self.count_consecutive > 0:
            self.subtext1 = f"inc={abs(self.count_consecutive)} - by: {str(self.diff_anchor[0])} ({percent_diff_str})"
        elif self.count_consecutive < 0:
            self.subtext1 = f"dec={abs(self.count_consecutive)} - by: {str(self.diff_anchor[0])} ({percent_diff_str})"

        self.W_A[0] = round(self.H_prices[0] - self.L_prices[0], 2)
        self.sum_H_expand = round(self.H_prices[0] - self.O_prices[0], 2)
        self.sum_L_expand = round(-self.L_prices[0] + self.O_prices[0], 2)

        if self.prices[0] != self.prices[1]:
            w_a_total = 0.60 * self.W_A[0] + 0.20 * self.W_A[1] + 0.1 * self.W_A[2] + 0.1 * self.W_A[3]
            self.W_A_total.insert(0, w_a_total)

        if (now - self.last_reset_time2).seconds >= 60 and (now.minute in [00, 30]):
            self.trigger_open_30 = 0
            self.last_reset_time2 = now.replace(second=0, microsecond=0)

        if now.second in [x for x in range(0, 60, 5)]:
            repeats = len(self.prices_5sec) - len(set(self.prices_5sec))
            changes = len(set(self.prices_5sec))
            if len(self.prices_5sec) > 4:
                net_inc_dec = round(self.prices_5sec[0] - self.prices_5sec[4], 2)
            else:
                net_inc_dec = 0
            Hdiff = 0
            Ldiff = 0
            if len(self.H_prices) > 6:
                if self.H_prices[0] == 0 or self.H_prices[1] == 0:
                    Hdiff = self.H_prices[0] - self.H_prices[5]
                if self.L_prices[0] == 0 or self.L_prices[1] == 0:
                    Ldiff = self.L_prices[0] - self.L_prices[5]
            self.sec5_note = f"rep: {repeats} --- changes: {changes} --- Hdiff: {Hdiff} Ldiff: {Ldiff} --- net inc/dec: {net_inc_dec}"
            self.prices_5sec = []
        #endregion

        #region PROCESS DATA (time resets)
        if now.minute in [x for x in range(14, 60, 15)] and 54 <= now.second <= 59:
            self.prclpr = self.prices[0]

        if now.minute in [x for x in range(0, 60, 1)] and now.minute not in [self.last_minute]:
            self.count_entries_11b = 0
            self.sum_3_cumulative_a[0] = 0
            pass

        if now.minute in [x for x in range(0, 60, 5)] and now.minute not in [self.last_minute]:
            pass

        if now.minute in [x for x in range(0, 60, 15)] and now.minute not in [self.last_minute]:
            self.total_pos2.insert(0, 0)
            self.total_neg2.insert(0, 0)
            self.total_sum2.insert(0, round(self.total_pos2[0] + self.total_neg2[0], 2))
            self.sum_3_cumulative_c = [self.sum_3_cumulative_b[0]] + self.sum_3_cumulative_c[:9]
            self.sum_3_cumulative_b[0] = 0
            self.count_crossed_cprc = 0
            self.prclprs = [self.prclpr] + self.prclprs[:9]
            self.average_diff = [float(0)] + self.average_diff[:9]
            self.average_diff_sum = [float(0)] + self.average_diff_sum[:9]
            self.closed_NOTES2c = [self.sum_NOTES2[0]] + [self.closed_NOTES2c[0]] + self.closed_NOTES2c[:9]
            self.count_closed_15m_multi = 0
            self.count_closed_15m_empty = 0
            self.count_opened_15m = 0
            self.note2 = f"MARK15-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            self.f_update_textbox(note2=True)
            self.note2 = f""

            w_a = round(self.H_prices[0] - self.L_prices[0], 2)
            self.W_A.insert(1, w_a)
            self.sum_H_expand = 0
            self.sum_L_expand = 0
            self.O_prices = [self.prices[0]] + self.O_prices[:9]
            self.H_prices = [self.prices[0]] + self.H_prices[:9]
            self.L_prices = [self.prices[0]] + self.L_prices[:9]
            self.closed_O = [self.prices[0]] + self.closed_O[:9]
            self.closed_H = [self.prices[0]] + self.closed_H[:9]
            self.closed_L = [self.prices[0]] + self.closed_L[:9]
            self.closed_C = [self.prices[0]] + self.closed_C[:9]
            self.hl = round(self.H_prices[0] - self.L_prices[0], 2)

            if self.prclprs[1] > 0:
                self.average_prc = [round(((self.prclprs[0] - self.prclprs[1]) - self.average_prc[0]) / 2, 2)] + self.average_prc[:9]

        if now.minute in [x for x in range(1, 60, 1)] and 0 <= now.second <= 5:
            if self.sum_net[0] != 0:
                self.sum_net.insert(0, float(0))
        if now.minute in [x for x in range(4, 60, 5)] and 0 <= now.second <= 5:
            if self.script_timeframe[304][1][0] != 0 and self.script_timeframe[304][1][1] != 0:
                self.script_timeframe[304][1].insert(0, round(float(0), 2))
                self.script_timeframe[304][2] = f"{str(self.script_timeframe[304][1][0])}"
        if now.minute in [x for x in range(1, 60, 1)] and 0 <= now.second <= 5:
            if self.script_timeframe[306][1][0] != 0 and self.script_timeframe[306][1][1] != 0:
                self.script_timeframe[306][1].insert(0, round(float(0), 2))
                self.script_timeframe[306][2] = f"{str(self.script_timeframe[306][1][0])}"

        self.last_minute = now.minute
        #endregion

        #region PROCESS DATA 2

        if self.H_prices[0] == self.prices[0] or self.L_prices[0] == self.prices[0]:
            self.total_pos2.insert(0, 0)
            self.total_neg2.insert(0, 0)
            self.total_sum2.insert(0, round(self.total_pos2[0] + self.total_neg2[0], 2))

        while len(self.script_timeframe[304][1]) > 10:
            self.script_timeframe[304][1].pop()
        while len(self.script_timeframe[306][1]) > 10:
            self.script_timeframe[306][1].pop()

        if self.total_sum2[0] > 0 > self.total_sum2[1] or self.total_sum2[0] < 0 < self.total_sum2[1]:
            self.total_pos2.insert(0, 0)
            self.total_neg2.insert(0, 0)
            self.total_sum2.insert(0, round(self.total_pos2[0] + self.total_neg2[0], 2))
        # endregion

        # region PROCESS DATA 3

        direction = 'Multi'
        priors_exist = self.closed_L[1] > 0
        if self.state_logic_HpLp != direction and self.closed_H[0] > self.closed_H[1] and self.closed_L[0] > self.closed_L[1] and priors_exist:
            self.sum_AF.insert(0, 0)
            self.state_logic_HpLp = direction
        if self.state_logic_HpLp == direction and (self.closed_H[0] < self.closed_H[1] or self.closed_L[0] < self.closed_L[1]) and priors_exist:
            self.state_logic_HpLp = ''
        direction = 'Empty'
        if self.state_logic_HpLp != direction and self.closed_H[0] < self.closed_H[1] and self.closed_L[0] < self.closed_L[1] and priors_exist:
            self.sum_AF.insert(0, 0)
            self.state_logic_HpLp = direction
        if self.state_logic_HpLp == direction and (self.closed_H[0] > self.closed_H[1] or self.closed_L[0] > self.closed_L[1]) and priors_exist:
            self.state_logic_HpLp = ''

        direction = 'Multi'
        if self.state_logic_Cp != direction and self.prices[0] > self.closed_C[0] and priors_exist:
            self.sum_AF2.insert(0, 0)
            self.state_logic_Cp = direction
        direction = 'Empty'
        if self.state_logic_Cp != direction and self.prices[0] < self.closed_C[0] and priors_exist:
            self.sum_AF2.insert(0, 0)
            self.state_logic_Cp = direction

        direction = 'True'
        if self.state_logic_saf3 != direction and self.state_logic_Cp != direction \
        and (self.closed_H[0] > self.closed_H[1] and self.closed_L[0] < self.closed_L[1] or self.closed_H[0] < self.closed_H[1] and self.closed_L[0] > self.closed_L[1]) and priors_exist:
            self.sum_AF3.insert(0, 0)
            self.state_logic_Cp = direction
        if self.state_logic_Cp == direction \
        and (self.closed_H[0] > self.closed_H[1] and self.closed_L[0] > self.closed_L[1] or self.closed_H[0] < self.closed_H[1] and self.closed_L[0] < self.closed_L[1]) and priors_exist:
            self.state_logic_Cp = ''


        self.qualifier_sum1_multi = ((self.sum_NOTES2[0] >= +6 and self.sum_NOTES2[0] > self.sum_NOTES2[1] > self.sum_NOTES2[
            2]) or (self.sum_NOTES2[0] >= +5 and self.sum_NOTES2[0] > self.sum_NOTES2[1] > self.sum_NOTES2[2] > self.sum_NOTES2[
            3])) and (self.sum_NOTES2[1] < 0 or self.sum_NOTES2[2] < 0 or self.sum_NOTES2[3] < 0 or self.sum_NOTES2[4] < 0 or
                      self.sum_NOTES2[5] < 0)
        self.qualifier_sum1_empty = ((self.sum_NOTES2[0] <= -6 and self.sum_NOTES2[0] < self.sum_NOTES2[1] < self.sum_NOTES2[
            2]) or (self.sum_NOTES2[0] <= -5 and self.sum_NOTES2[0] < self.sum_NOTES2[1] < self.sum_NOTES2[2] < self.sum_NOTES2[
            3])) and (self.sum_NOTES2[1] > 0 or self.sum_NOTES2[2] > 0 or self.sum_NOTES2[3] > 0 or self.sum_NOTES2[4] > 0 or
                      self.sum_NOTES2[5] > 0)
        self.qualifier_sc6_multi = (self.diff_anchor[0] >= +8 and self.count_consecutive >= +2)
        self.qualifier_sc6_empty = (self.diff_anchor[0] <= -8 and self.count_consecutive <= -2)

        if ((self.qualifier_SUM3 > 0 and self.count_consecutive == -1) or (
                self.qualifier_SUM3 < 0 and self.count_consecutive == 1)) and self.custom1:
            self.custom1 = False
            self.sum_net3.insert(0, float(0))

        self.hl = round(self.H_prices[0] - self.L_prices[0], 2)
        self.qualifier_vol = self.hl >= 30 and self.W_A_total[0] >= 30

        self.qualifier_W_A_total_multi = (30 <= self.W_A_total[0] <= 60 and (
            round(+ self.prices[0] - self.average_HL[0], 2)) >= 0) or (self.W_A_total[0] > 60)
        self.qualifier_W_A_total_empty = (30 <= self.W_A_total[0] <= 60 and (
            round(- self.prices[0] + self.average_HL[0], 2)) >= 0) or (self.W_A_total[0] > 60)

        if self.v_direction != 'Multi' \
                and self.count_consecutive >= +2 \
                and True:
            if not self.sum_4_state == 'Multi':
                self.sum_4.insert(0, 0)
                self.sum_4_state = 'Multi'
        if self.v_direction != 'Empty' \
                and self.count_consecutive <= -2 \
                and True:
            if not self.sum_4_state == 'Empty':
                self.sum_4.insert(0, 0)
                self.sum_4_state = 'Empty'
        #endregion

        Empty = 'Empty'
        Multi = 'Multi'
        Nopos = 'NO_POS'

        direction = Multi
        if self.v_direction not in []:
            if self.count_consecutive == 1 and (self.sum_NOTES2[0] < self.marked_sum_NOTES2_multi != 0 or self.marked_sum_NOTES2_multi == 0):
                self.count_logic_group_multi = 1
                self.marked_sum_NOTES2_multi = self.sum_NOTES2[0]
                self.state_resetted_NOTES2group_multi = True
            if self.count_consecutive == 1 and self.sum_NOTES2[0] > self.marked_sum_NOTES2_multi != 0 and self.prices[0] != self.prices[1] and self.diff[1] < 0:
                self.count_logic_group_multi += 1
                self.marked_sum_NOTES2_multi = self.sum_NOTES2[0]
            if self.count_consecutive >= 2:
                self.marked_sum_NOTES2_multi = self.sum_NOTES2[0]

        direction = Empty
        if self.v_direction not in []:
            if -self.count_consecutive == 1 and (self.sum_NOTES2[0] > self.marked_sum_NOTES2_empty != 0 or self.marked_sum_NOTES2_empty == 0):
                self.count_logic_group_empty = 1
                self.marked_sum_NOTES2_empty = self.sum_NOTES2[0]
                self.state_resetted_NOTES2group_empty = True
            if -self.count_consecutive == 1 and self.sum_NOTES2[0] < self.marked_sum_NOTES2_empty != 0 and self.prices[0] != self.prices[1] and self.diff[1] > 0:
                self.count_logic_group_empty += 1
                self.marked_sum_NOTES2_empty = self.sum_NOTES2[0]
            if -self.count_consecutive >= 2 and self.marked_sum_NOTES2_empty != 0:
                self.marked_sum_NOTES2_empty = self.sum_NOTES2[0]

        direction = Multi
        if self.v_direction not in [direction, Nopos]:
            if self.count_consecutive == 1 and (self.sum_NOTES2[0] < self.marked_sum_NOTES2 != 0 or self.marked_sum_NOTES2 == 0):
                self.count_logic_group = 1
                self.marked_sum_NOTES2 = self.sum_NOTES2[0]
                self.state_resetted_NOTES2group = True
            if self.count_consecutive == 1 and self.sum_NOTES2[0] > self.marked_sum_NOTES2 != 0 and self.prices[0] != self.prices[1] and self.diff[1] < 0:
                self.count_logic_group += 1
                self.marked_sum_NOTES2 = self.sum_NOTES2[0]
            if self.count_consecutive >= 2:
                self.marked_sum_NOTES2 = self.sum_NOTES2[0]
            if self.count_logic_group_multi == 2:
                self.list_group_multi.insert(0, self.sum_NOTES2[0])
            else:
                self.list_group_multi = []
        direction = Empty
        if self.v_direction not in [direction, Nopos]:
            if -self.count_consecutive == 1 and (self.sum_NOTES2[0] > self.marked_sum_NOTES2 != 0 or self.marked_sum_NOTES2 == 0):
                self.count_logic_group = 1
                self.marked_sum_NOTES2 = self.sum_NOTES2[0]
                self.state_resetted_NOTES2group = True
            if -self.count_consecutive == 1 and self.sum_NOTES2[0] < self.marked_sum_NOTES2 != 0 and self.prices[0] != self.prices[1] and self.diff[1] > 0:
                self.count_logic_group += 1
                self.marked_sum_NOTES2 = self.sum_NOTES2[0]
            if -self.count_consecutive >= 2 and self.marked_sum_NOTES2 != 0:
                self.marked_sum_NOTES2 = self.sum_NOTES2[0]
            if self.count_logic_group_multi == 2:
                self.list_group_empty.insert(0, self.sum_NOTES2[0])
            else:
                self.list_group_empty = []


        self.text = f'{self.note}{self.subtext1}{subtext2}'
        self.f_update_textbox(f'{self.text}')

        self.f_LOGICS()
        return

    def f_LOGICS(self):
        Empty = 'Empty'
        Multi = 'Multi'
        Nopos = 'NO_POS'
        # pass

        #region profit stop loss
        # profit_stop_loss = 4
        #
        # if self.v_yield >= 5 and self.v_yield > self.take_profit + profit_stop_loss:
        #     self.take_profit = self.v_yield - profit_stop_loss
        #
        # if self.v_direction != 'NO_POS' and self.v_yield <= self.take_profit > 0:
        #     reason = f"{round(self.take_profit,2)} profit taken"
        #     self.f_close_position(reason)
        #     return
        #endregion

        direction = Multi
        if self.v_direction in [Nopos] and self.count_logic_group_multi >= 3:
            reason = f'3 grouping increases'
            self.f_close_position(reason)
            self.f_open_position(reason, direction)
            return
        direction = Empty
        if self.v_direction in [Nopos] and self.count_logic_group_empty >= 3:
            reason = f'3 grouping decreases'
            self.f_close_position(reason)
            self.f_open_position(reason, direction)
            return

        direction = Multi
        if self.v_direction not in [direction, Nopos] and self.prices[0] > self.average_HL[0] \
        and self.closed_H[0] > self.closed_H[1] > 0:
            reason = f'H color reverse'
            self.f_close_position(reason)
            # self.f_open_position(reason, direction)
            return
        direction = Empty
        if self.v_direction not in [direction, Nopos] and self.prices[0] < self.average_HL[0] \
        and self.closed_L[0] < self.closed_L[1] > 0:
            reason = f'L color reverse'
            self.f_close_position(reason)
            # self.f_open_position(reason, direction)
            return

        direction = Multi
        if self.v_direction not in [direction, Nopos] and len(self.list_group_multi) > 1 and self.list_group_multi[0] >= self.list_group_multi[-1] + 20:
            reason = f'u2 status improve by 20'
            self.f_close_position(reason)
            # self.f_open_position(reason, direction)
            return
        direction = Empty
        if self.v_direction not in [direction, Nopos] and len(self.list_group_multi) > 1 and self.list_group_multi[0] <= self.list_group_multi[-1] - 20:
            reason = f'd2 status improve by 20'
            self.f_close_position(reason)
            # self.f_open_position(reason, direction)
            return

        direction = Multi
        if self.v_direction not in [direction, Nopos] and self.count_logic_group >= 3:
            reason = f'3 grouping increases'
            self.f_close_position(reason)
            self.f_open_position(reason, direction)
            return

        direction = Empty
        if self.v_direction not in [direction, Nopos] and self.count_logic_group >= 3:
            reason = f'3 grouping decreases'
            self.f_close_position(reason)
            self.f_open_position(reason, direction)
            return


    def f_update_textbox(self, note='', blank_before=False, blank_after=False, header_only=False, note2=False):
        # count_trades = f"{self.count_trades_profit} of {self.count_trades}"
        avg_hl = f'{self.average_HL[0]}'
        if self.average_HL[0] > 0:
            avg_hl = f"({round(+self.H_prices[0] - self.average_HL[0],2)}) {self.average_HL[0]} ({round(-self.L_prices[0] + self.average_HL[0],2)})"
            if self.prices[0] > self.average_HL[0]:
                avg_hl += ' u'
            if self.prices[0] < self.average_HL[0]:
                avg_hl += ' d'

        price_diff_aop = round(self.prices[0] - self.v_aop,2)
        buy_price = f"{self.v_aop}"

        if price_diff_aop > 0 and self.v_aop > 0:
            buy_price = f"{self.v_aop} (+{price_diff_aop})"
        if price_diff_aop < 0:
            buy_price = f"{self.v_aop} ({price_diff_aop})"

        groupings_m = ''
        groupings_e = ''
        if self.count_logic_group_multi > 0:
            groupings_m = f" u{self.count_logic_group_multi}{'reset' if self.state_resetted_NOTES2group_multi else ''} ({self.marked_sum_NOTES2_multi})"
        self.state_resetted_NOTES2group_multi = False
        if self.count_logic_group_empty > 0:
            groupings_e = f" d{self.count_logic_group_empty}{'reset' if self.state_resetted_NOTES2group_empty else ''} ({self.marked_sum_NOTES2_empty})"
        self.state_resetted_NOTES2group_empty = False

        sim_balance = f"({self.count_balance_add}) {round(self.v_bal_now, 2)} / {round(self.v_unrealized, 2)} / {buy_price}"
        if self.v_direction == 'Multi':
            sim_balance = f"{sim_balance} M"
            c_elw_price = f"{self.prices[0]} M"
            if self.count_logic_group > 0:
                sim_balance += f" d{self.count_logic_group}{'reset' if self.state_resetted_NOTES2group else ''} ({self.marked_sum_NOTES2})"
            self.state_resetted_NOTES2group = False
        elif self.v_direction == 'Empty':
            sim_balance = f"{sim_balance} E"
            c_elw_price = f"{self.prices[0]} E"
            if self.count_logic_group > 0:
                sim_balance += f" u{self.count_logic_group}{'reset' if self.state_resetted_NOTES2group else ''} ({self.marked_sum_NOTES2})"
            self.state_resetted_NOTES2group = False
        else:
            sim_balance = f"{sim_balance} N"
            c_elw_price = f"{self.prices[0]} N"


        sum_note2 = f"+{str(self.total_pos2[0])} {str(self.total_neg2[0])} = {str(self.total_sum2[0])}"
        if self.H_prices[0] == self.prices[0] and self.hl > 1:
            c_elw_price = f"H=C {c_elw_price}"
            sum_note2 = f'H=C {sum_note2}'
        if self.L_prices[0] == self.prices[0] and self.hl > 1:
            c_elw_price = f"L=C {c_elw_price}"
            sum_note2 = f'L=C {sum_note2}'
        sum_note2 = fr"'{sum_note2}"

        wa = [''] + [f"{self.W_A[i]} ({self.closed_NOTES2c[i]})" for i in range(4)]

        PRCLPR = f"{self.prclprs[0]} ({self.prclprs[1]}) ({self.prclprs[2]}) ({self.prclprs[3]})"
        Oprice = f"{self.O_prices[0]} ({self.closed_O[1]}) ({self.closed_O[2]}) ({self.closed_O[3]})"
        Hprice = f"({self.sum_H_expand}) {self.H_prices[0]} ({self.closed_H[1]}) ({self.closed_H[2]}) ({self.closed_H[3]})"
        Lprice = f"({self.sum_L_expand}) {self.L_prices[0]} ({self.closed_L[1]}) ({self.closed_L[2]}) ({self.closed_L[3]})"

        if self.closed_O[0] > 0:
            for i in range(4):
                if self.closed_H[i] > self.closed_H[i+1] and self.L_prices[i] > self.closed_L[i+1] and self.closed_NOTES2c[i] > 0:
                    wa[i+1] += ' u'
                if self.closed_H[i] < self.closed_H[i+1] and self.L_prices[i] < self.closed_L[i+1] and self.closed_NOTES2c[i] < 0:
                    wa[i+1] += ' u'
                if (self.closed_H[i] > self.closed_H[i+1] and self.L_prices[i] > self.closed_L[i+1] and self.closed_NOTES2c[i] < 0)\
                or (self.closed_H[i] < self.closed_H[i+1] and self.L_prices[i] < self.closed_L[i+1] and self.closed_NOTES2c[i] > 0):
                    wa[i+1] += ' n'

            if self.closed_O[0] > self.closed_O[1] > 0:
                Oprice += ' u'
            if self.closed_O[0] < self.closed_O[1] > 0:
                Oprice += ' d'
            if self.closed_H[0] > self.closed_H[1] > 0:
                Hprice += ' u'
            if self.closed_H[0] < self.closed_H[1] > 0:
                Hprice += ' d'
            if self.closed_L[0] > self.closed_L[1] > 0:
                Lprice += ' u'
            if self.closed_L[0] < self.closed_L[1] > 0:
                Lprice += ' d'
            if self.prices[0] - 15 > self.closed_C[1] > 0:
                c_elw_price += ' u'
            if self.prices[0] + 15 < self.closed_C[1] > 0:
                c_elw_price += ' d'
        Cprice = f"{c_elw_price} ({self.closed_C[1]}) ({self.closed_C[2]}) ({self.closed_C[3]}) ({self.closed_C[4]})"

        progression = f""
        direction = 'Multi'
        if self.state_logic_NOTES2_reverse == direction:
            if self.v_direction not in [direction,'NO_POS']:
                progression = f"waiting MULTI (NOTES2 reverse). waiting 3inc"
        direction = 'Empty'
        if self.state_logic_NOTES2_reverse == direction:
            if self.v_direction not in [direction,'NO_POS']:
                progression = f"waiting EMPTY (NOTES2 reverse). waiting 3dec"
        # direction = 'Multi'
        # if self.state_logic_HL == direction:
        #     if self.v_direction != direction:
        #         progression = f"waiting MULTI. Qualified: {self.last_reason}. waiting 3 inc"
        # direction = 'Empty'
        # if self.state_logic_HL == direction:
        #     if self.v_direction != direction:
        #         progression = f"waiting EMPTY. Qualified: {self.last_reason}. waiting 3 dec"

        if self.count_consecutive > 0:
            NOTES2 = f"inc={abs(self.count_consecutive)} ({str(self.diff[0])}) / ({str(self.diff_anchor[0])}) / ({self.sum_NOTES2[0]})"
        elif self.count_consecutive < 0:
            NOTES2 = f"dec={abs(self.count_consecutive)} ({str(self.diff[0])}) / ({str(self.diff_anchor[0])}) / ({self.sum_NOTES2[0]})"
        else:
            NOTES2 = f""
        if self.sum_NOTES2[0] > 0:
            NOTES2 += ' u'
        if self.sum_NOTES2[0] < 0:
            NOTES2 += ' d'
        multiavg = ''
        emptyavg = ''
        if round(+ self.prices[0] - self.average_HL[0], 2) >= 0 \
                and self.hl >= 30 \
                and self.prices[0] > self.multiavg[0]:
            multiavg = str(self.multiavg[0])
        elif round(- self.prices[0] + self.average_HL[0], 2) >= 0 \
                and self.hl >= 30 \
                and self.prices[0] < self.emptyavg[0]:
            emptyavg = str(self.emptyavg[0])
        sum_3 = f"\'+{str(self.total_pos3new[0])} {str(self.total_neg3new[0])} = {str(self.total_sum3new[0])} ({self.diff_5s[0]}) ({self.sum_3_cumulative_a[0]}) ({self.sum_3_cumulative_b[0]}) ({self.sum_3_cumulative_c[0]})"
        if self.count_entries_11 == 0:
            if self.diff_5s[0] > 0:
                sum_3 += ' u'
            elif self.diff_5s[0] < 0:
                sum_3 += ' d'
            else:
                sum_3 += ' n'
        if self.current_time.second == 59:
            sum_3 += ' x12'
        sum_note2_new = f"\'+{str(self.total_pos2_new[0])} {str(self.total_neg2_new[0])} = {str(self.total_sum2_new[0])}"
        sum_note3 = f"\'+{str(self.total_pos3[0])} {str(self.total_neg3[0])} = {str(self.total_sum3[0])}"
        sum_note4 = f"\'+{str(self.total_pos4[0])} {str(self.total_neg4[0])} = {str(self.total_sum4[0])}"

        sum_AF = f"{self.sum_AF[0]}"
        sum_AF2 = f"{self.sum_AF2[0]} ({self.count_crossed_cprc})"
        sum_AF3 = f"{self.sum_AF3[0]}"

        if not (self.H_prices[0] < self.closed_H[0] and self.L_prices[0] < self.closed_L[0] and self.prices[0] + 15 < self.closed_C[0] > 0) \
        and not (self.H_prices[0] > self.closed_H[0] and self.L_prices[0] > self.closed_L[0] and self.prices[0] - 15 > self.closed_C[0] > 0):
            if self.suspender == '':
                val = 0
            else:
                val = 40
            if self.sum_AF[0] > val:
                sum_AF = sum_AF + ' u'
            if self.sum_AF[0] < -val:
                sum_AF = sum_AF + ' d'

        if self.sum_AF2[0] > 0:
            sum_AF2 = sum_AF2 + ' u'
        if self.sum_AF2[0] < 0:
            sum_AF2 = sum_AF2 + ' d'

        if self.sum_AF3[0] > 0:
            sum_AF3 = sum_AF3 + ' u'
        if self.sum_AF3[0] < 0:
            sum_AF3 = sum_AF3 + ' d'

        list_output = [
            # ['unr_p/l', str(self.v_unrealized) if not note2 else ''],
            ['yld', str(self.v_yield) if not note2 else ''],
            ['note2', f"\'{self.note2}"],
            ['date', self.f_current_time(self.current_time, out='date') if not note2 else ''],
            ['time', self.f_current_time(self.current_time, out='time') if not note2 else ''],
            ['evat_dir', self.v_direction_evat if not note2 else ''],
            ['direction', self.v_direction if not note2 else ''],
            ['esp', str(self.v_esp) if not note2 else ''],
            ['vol', '{:f}'.format(Variables.Misc.tv_vol) if not note2 else ''],
            ['qsum',
             {self.qualifier_sum1_multi: 'u', self.qualifier_sum1_empty: 'd'}.get(True, '') if not note2 else ''],
            ['qsc', {self.qualifier_sc6_multi: 'u', self.qualifier_sc6_empty: 'd'}.get(True, '') if not note2 else ''],
            # ['tv_5s', f'\'{Variables.Misc.tradingview_charts_data[1]}' if not note2 else ''],
            # ['tv_10s', f'\'{Variables.Misc.tradingview_charts_data[2]}' if not note2 else ''],
            # ['tv_15s', f'\'{Variables.Misc.tradingview_charts_data[3]}' if not note2 else ''],
            # ['tv_30s', f'\'{Variables.Misc.tradingview_charts_data[4]}' if not note2 else ''],
            # ['tv_1m', f'\'{Variables.Misc.tradingview_charts_data[5]}' if not note2 else ''],
            # ['tv_2m', f'\'{Variables.Misc.tradingview_charts_data[6]}' if not note2 else ''],
            # ['tv_3m', f'\'{Variables.Misc.tradingview_charts_data[7]}' if not note2 else ''[],

            # ['tv_5m', f'\'{Variables.Misc.tradingview_charts_data[8]}' if not note2 else ''],
            # ['script', f"\'{self.note3}" if not note2 else ''],
            ['NOTE', note if not note2 else ''],
            # ['profit_counter', f"{round(self.profit_taken)}" if not note2 else ''],
            # ['counter', count_trades if not note2 else ''],
            ['qvol', f'{f"Yes {self.hl}" if self.qualifier_vol else f"No {self.hl}"}' if not note2 else ''],
            ['WA_total', f"{str(self.W_A_total[0])}" if not note2 else ''],
            ['elw_bal', str(self.v_bal_elw) if not note2 else ''],
            # ['buy_price', buy_price if not note2 else ''],
            ['PRCLPR', PRCLPR if not note2 else ''],
            ['O', Oprice if not note2 else ''],
            ['H', Hprice if not note2 else ''],
            ['sim_balance/buy_price', sim_balance if not note2 else ''],
            ['group_M', groupings_m if not note2 else ''],
            ['group_E', groupings_e if not note2 else ''],
            ['sum_note2', sum_note2 if not note2 else ''],
            ['AVG(HL)', avg_hl if not note2 else ''],
            ['NOTES2', NOTES2 if not note2 else ''],
            ['sum_3/PrDif/12x11', sum_3 if not note2 else ''],
            ['L', Lprice if not note2 else ''],
            ['C(elw_price)', Cprice if not note2 else ''],
            ['sum_H=L', sum_AF if not note2 else ''],
            ['sum_C<>Cp', sum_AF2 if not note2 else ''],
            ['sum_H<>L', sum_AF3 if not note2 else ''],
            ['MultiAVG', f"{multiavg}" if not note2 else ''],
            ['EmptyAVG', f"{emptyavg}" if not note2 else ''],
            ['qNET', f"{str(self.sum_net3[0])}" if not note2 else ''],
            ['qnet', {self.qualifier_comb2_multi: 'u', self.qualifier_comb2_empty: 'd'}.get(True, '') if not note2 else ''],
            ['sim_balance2', sim_balance if not note2 else ''],
            ['new_sum_note2', sum_note2_new if not note2 else ''],
            ['progression', progression if not note2 else ''],
            ['sum_note3', sum_note3 if not note2 else ''],
            ['sum_note4', sum_note4 if not note2 else ''],
            # ['C(elw_price)', str(self.prices[0]) if not note2 else ''],
            # ['C(iframe)', f"{str(self.C_price[0])}" if not note2 else ''],
            ['sum_15m', f"{str(self.sum_NOTES2[0])}" if not note2 else ''],
            # ['sum_net', f"{str(self.sum_net[0])}" if not note2 else ''],
            ['sc_5m_6', f'{self.script_timeframe[306][1][0]}' if not note2 else ''],
            ['sc_5m_3', f'{self.script_timeframe[304][1][0]}' if not note2 else ''],
            ['avg_diff', f"{str(self.average_diff[0])}" if not note2 else ''],
            ['SUM_avg_diff', f"{str(self.average_diff_sum[0])}" if not note2 else ''],
            # ['avg(prc)', f"{str(self.average_prc[0])}" if not note2 else ''],
            # ['avg(prc2)', f"{str(self.average_prc[1])}" if not note2 else ''],
            # ['avg(prc3)', f"{str(self.average_prc[2])}" if not note2 else ''],
            # ['avg(prc4)', f"{str(self.average_prc[3])}" if not note2 else ''],
            ['WA_total', f"{str(self.W_A_total[0])}" if not note2 else ''],
            ['WA1', wa[1] if not note2 else ''],
            ['WA2', wa[2] if not note2 else ''],
            ['WA3', wa[3] if not note2 else ''],
            ['WA4', wa[4] if not note2 else ''],
            ['5sec_report', f"{str(self.sec5_note)}" if not note2 else ''],
            # ['sc_5s', f'{self.script_timeframe[5][1][0]}' if not note2 else ''],
            # ['sc_10s', f'{self.script_timeframe[10][1][0]}' if not note2 else ''],
            # ['sc_15s', f'{self.script_timeframe[15][1][0]}' if not note2 else ''],
            # ['sc_30s', f'{self.script_timeframe[30][1][0]}' if not note2 else ''],
            # ['sc_1m', f'{self.script_timeframe[60][1][0]}' if not note2 else ''],
            # ['sc_2m', f'{self.script_timeframe[120][1][0]}' if not note2 else ''],
            # ['sc_3m', f'{self.script_timeframe[180][1][0]}' if not note2 else ''],
            # ['sc_4m', f'{self.script_timeframe[240][1][0]}' if not note2 else ''],
            # ['sc_5m', f'{self.script_timeframe[300][1][0]}' if not note2 else ''],
            # ['HA1', f'\'{Variables.Misc.tv_HA[1][1]}' if not note2 else ''],
            # ['HA2', f'\'{Variables.Misc.tv_HA[2][1]}' if not note2 else ''],
            # ['HA3', f'\'{Variables.Misc.tv_HA[3][1]}' if not note2 else ''],
            # ['HA4', f'\'{Variables.Misc.tv_HA[4][1]}' if not note2 else ''],
            # ['HA5', f'\'{Variables.Misc.tv_HA[5][1]}' if not note2 else ''],
            # ['sc_5m_2', f'\'{self.script_timeframe[300][5]}' if not note2 else ''],
            # ['last_rev', self.cumulative_value_str2 if not note2 else ''],
            # ['to_SL/to_TP', self.v_tp_sl_str if not note2 else ''],
            # ['aop', str(self.v_aop) if not note2 else ''],
            # ['aop-esp', str(self.v_diff) if not note2 else ''],
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
        print(f"\nnew row:\n{self.output}\n")
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
        # try:
        #     self.driver.find_element(By.CSS_SELECTOR, Variables.XPaths.evatcoin_perpetual).click()
        # except:
        #     self.driver.get(Variables.Misc.url_evatcoin)
        #     self.driver.refresh()
        #     print(f"refresh 1285")
        #     time.sleep(2)

        average_HL = round(self.L_prices[0] + self.hl / 2, 2)
        hl_4 = self.hl / 4 + average_HL
        if self.prices[0] != self.prices[1]:
            self.average_HL.insert(0, average_HL)
            self.emptyavg.insert(0, hl_4)
            self.multiavg.insert(0, hl_4)

        if self.anchor_price_2 == 0:
            self.anchor_price_2 = self.prices[0]

        # self.driver.get(Variables.Misc.url_evatcoin)
        time.sleep(0.1)

        try:
            self.v_bal_elw = extract_float_numbers(
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_balance).text)
        except:
            self.v_bal_elw = float(0)

        test = True
        while test:
            try:
                self.prices.insert(0, extract_float_numbers(self.driver.find_element(By.XPATH, Variables.XPaths.evatcoin_current_price).text))
                self.closed_C[0] = self.prices[0]
                test = False
            except:
                self.driver.get(Variables.Misc.url_evatcoin)
                self.driver.refresh()
                print(f"refresh 1311")
                time.sleep(5)
        if self.prices[0] > self.H_prices[0] or self.H_prices[0] == 0:
            self.H_prices = [self.prices[0]] + self.H_prices[:9]
            self.closed_H[0] = self.prices[0]
        if self.prices[0] < self.L_prices[0] or self.L_prices[0] == 0:
            self.L_prices = [self.prices[0]] + self.L_prices[:9]
            self.closed_L[0] = self.prices[0]

        if self.prices[0] != self.prices[1]:
            self.price_changes.insert(0, self.prices[0])
        self.prices_5sec.insert(0, self.prices[0])
        while len(self.prices) > 20:
            self.prices.pop()
        while len(self.price_changes) > 20:
            self.price_changes.pop()

        try:
            self.v_direction_evat = self.driver.find_element(By.XPATH, Variables.XPaths.evatcoin_direction).text
        except:
            self.v_direction_evat = 'NO_POS'

        try:
            self.v_esp = extract_float_numbers(
                self.driver.find_element(By.CSS_SELECTOR, Variables.CssSelectors.evatcoin_esp).text)
        except:
            self.v_esp = float(0)

        while len(self.checker_prices) >= 150:
            self.checker_prices.pop()

        self.checker_prices.insert(0, self.prices[0])

        if all(val == self.checker_prices[0] for val in self.checker_prices) and len(self.checker_prices) > 100:
            self.driver.get(Variables.Misc.url_evatcoin)
            self.driver.refresh()
            print(f"refresh 1348")
            time.sleep(5)
            self.checker_prices.insert(0, float(123))
            self.checker_prices.insert(0, float(self.prices[0]))

        if self.v_direction == 'Multi':
            self.v_tp_sl_str = f"{str(float(self.prices[0]) - ((float(self.v_aop)) - ((float(self.v_aop) * float(self.percent_stop_loss)) / (100 * Variables.Misc.leverage[0]))))}/{str(-float(self.prices[0]) + ((float(self.v_aop)) + ((float(self.v_aop) * float(self.percent_take_profit)) / (100 * Variables.Misc.leverage[0]))))}"
            self.v_yield = Variables.Misc.leverage[0] * 100 * (
                    (float(self.prices[0]) - float(self.v_aop)) / float(self.v_aop))
        elif self.v_direction == 'Empty':
            self.v_tp_sl_str = f"{str(-float(self.prices[0]) + ((float(self.v_aop)) + ((float(self.v_aop) * float(self.percent_stop_loss)) / (100 * Variables.Misc.leverage[0]))))}/{str(float(self.prices[0]) - ((float(self.v_aop)) - ((float(self.v_aop) * float(self.percent_take_profit)) / (100 * Variables.Misc.leverage[0]))))}"
            self.v_yield = Variables.Misc.leverage[0] * 100 * (
                    (-float(self.prices[0]) + float(self.v_aop)) / float(self.v_aop))
        else:
            self.v_yield = float(0)
            self.v_tp_sl_str = '-/-'

        self.v_unrealized = (float(self.v_bal_leaf * (self.v_yield / 100)))
        self.v_bal_now = self.v_bal_open + self.v_bal_leaf * (self.v_yield / 100)

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
                            val = float(pane_legend_item_value[index].text.replace("'", "."))
                            val = round(val, 2)
                            if index == 0 and self.O_prices[0] == 0:
                                self.O_prices = [val for _ in range(10)]
                                self.closed_O[0] = val
                                self.prclpr = self.prclprs[0] = val
                            if index == 1 and self.H_prices[0] == 0:
                                self.H_prices = [val for _ in range(10)]
                                self.closed_H[0] = val
                            if index == 2 and self.L_prices[0] == 0:
                                self.L_prices = [val for _ in range(10)]
                                self.closed_L[0] = val
                            if index == 3:
                                self.C_price[0] = val
                                self.closed_C[0] = val
                            index += 1
                            pass_1 = True
                    except Exception as e:
                        print(f"LINE 1395\n{e}")
                        self.driver.get(Variables.Misc.url_evatcoin)
                        self.driver.refresh()
                        print(f"refresh 1408")
                        time.sleep(5)
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
                try:
                    Variables.Misc.tv_vol = self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_volume).text
                except:
                    Variables.Misc.tv_vol = ''

                if 'K' in Variables.Misc.tv_vol:
                    Variables.Misc.tv_vol = int(float(Variables.Misc.tv_vol.replace('K', '')) * 1000)
                else:
                    Variables.Misc.tv_vol = int(Variables.Misc.tv_vol.replace('K', ''))

                # try:
                #     raw_data = self.wait.until(ec.presence_of_element_located((By.XPATH, Variables.XPaths.tradingview_logs[1]))).text
                #     self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_charts[1]).click()
                #     raw_data = raw_data.split('\n')
                # except:
                #     self.driver.get(Variables.Misc.url_tradingview)
                #     time.sleep(3)
                #     continue

                # for key in Variables.Misc.tv_HA:
                #     Variables.Misc.tv_HA[key][1] = self.driver.find_element(By.XPATH, Variables.Misc.tv_HA[key][0]).text

                # error = True
                # while error:
                #     try:
                #         self.O_price = round(float(self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_ohlc['O'][0]).text),2)
                #         self.H_price = round(float(self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_ohlc['H'][0]).text),2)
                #         self.L_price = round(float(self.driver.find_element(By.XPATH, Variables.XPaths.tradingview_ohlc['L'][0]).text),2)
                #         self.C_price = self.prices[0]
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
                #     # if not (any(s.lower() in self.raw_data_message.lower() for s in ['Multi', 'Empty'])):
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
                #         if value[1].lower() == 'Empty':
                #             self.count_short += 1
                #         elif value[1].lower() == 'Multi':
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
                continue
            except:
                self.driver.get(Variables.Misc.url_evatcoin)
                self.driver.refresh()
                print(f"refresh 1631")
                time.sleep(5)
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
            # self.driver.execute_script('window.open("");')
            # self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(0.2)
            # self.driver.get(Variables.Misc.url_tradingview)
            return self.driver
        except Exception as e:
            print(f"LINE 1543\n{e}")
            messagebox.showinfo("ALERT",
                                'Make sure you have an internet connection before starting the script.\nExiting...')
            self.driver.quit()
            self.root.destroy()
            sys.exit()

    def f_current_time(self, date_time=datetime.now(), out='all'):
        self.v_current_time_str = date_time.strftime("%Y-%m-%d,%H:%M:%S.%f")[:-3]
        if out == 'date':
            return date_time.strftime("%Y-%m-%d")
        elif out == 'time':
            return date_time.strftime("%H:%M:%S.%f")[:-3]
        else:
            return self.v_current_time_str

    def format_csv_string(self, csv_string):
        items = csv_string.split(',')
        if len(items) < self.csv_columns:
            items += [''] * (self.csv_columns - len(items))
        elif len(items) > self.csv_columns:
            raise ValueError(f'CSV string has more than {self.csv_columns} columns')
        return ','.join(items)

    def f_open_position(self, reason, direction, full=True):
        if self.v_direction != 'NO_POS' or direction == '':
            return
        self.note2 = ''
        self.f_update_textbox()

        self.count_logic_group_multi = 0
        self.count_logic_group_empty = 0
        self.marked_sum_NOTES2 = 0
        self.marked_sum_NOTES2_multi = 0
        self.marked_sum_NOTES2_empty = 0
        self.sum_NOTES2 = [float(0)] + self.sum_NOTES2[:9]
        self.state_logic_marked_price = ''
        self.count_opened_15m += 1
        self.state_logic_AF = ''
        self.count_changes_after_trigger_AF = 0
        self.count_changes_after_3consec = 0
        self.trigger_AF = ''
        self.trigger_AF_count = 0
        self.count_changes_after_trade = 0
        self.last_AF_val = 0
        self.sum_AF.insert(0, 0)
        self.v_reason_open = reason
        self.trigger_open = direction
        self.resetted = ''
        self.v_buy_qty = math.floor((self.v_bal_now * self.v_percentage) / self.leaf_size)
        self.v_bal_leaf = self.v_buy_qty * self.leaf_size
        self.v_direction = direction
        if full:
            self.v_aop = float(self.prices[0])
            self.peak_price = self.prices[0]
            self.v_bal_now = self.v_bal_now - Variables.Misc.leverage[1] * self.v_bal_leaf
            self.v_bal_open = self.v_bal_now
            self.str_profit_loss = "{:.2f}".format(- Variables.Misc.leverage[1] * self.v_bal_leaf)
            self.v_reason_open = self.v_reason_open + f' p/l: {self.str_profit_loss}'

            print(f'{self.v_bal_now} - {direction}')
            self.note2 = f"========================================================================================================================================================================================================================================================================================================================================================================== O {direction.upper()}: {self.v_reason_open}"
            self.f_update_textbox(blank_after=True, blank_before=True, note2=True)

        self.f_get_data_evatcoin()
        if self.v_direction_evat == 'NO_POS':
            self.f_open_evat()
            print('open evat')

        # self.sum_net2.insert(0, float(0))
        self.v_reason_open = ''
        self.trigger_open = ''
        self.v_reason_close = ''
        self.trigger_close = ''
        self.count_consecutive = 0
        self.qualifier_comb5[1] = 0
        self.diff.insert(0, float(0))
        self.sum_4_state = ''

        return

    def f_close_position(self, reason, full=True):
        if self.v_direction == 'NO_POS':
            return
        self.note2 = ''
        self.f_update_textbox()

        self.count_logic_group_multi = 0
        self.count_logic_group_empty = 0
        self.marked_sum_NOTES2 = 0
        self.marked_sum_NOTES2_multi = 0
        self.marked_sum_NOTES2_empty = 0
        self.sum_NOTES2 = [float(0)] + self.sum_NOTES2[:9]
        self.count_logic_group = 0
        self.state_logic_marked_price = ''
        self.state_logic_AF = ''
        self.take_profit = 0
        self.trigger_AF = ''
        self.trigger_AF_count = 0
        self.count_changes_after_trade = 0
        self.count_changes_after_3consec = 0
        self.last_AF_val = 0
        self.sum_AF.insert(0, 0)
        self.count_changes_after_trigger_AF = 0
        self.count_trades += 1
        if self.v_unrealized > 0:
            self.count_trades_profit += 1

        self.trigger_close = self.v_direction
        if full:
            self.v_aop = 0
            self.v_unrealized = float(0)
            self.v_yield = float(0)
            self.v_bal_now = self.v_bal_now - Variables.Misc.leverage[1] * self.v_bal_leaf
            self.str_profit_loss = "{:.2f}".format(
                self.v_bal_now - self.v_bal_open - Variables.Misc.leverage[1] * self.v_bal_leaf)
            self.v_bal_open = self.v_bal_now
            self.v_reason_close = reason + f' p/l: {self.str_profit_loss}'
            self.note2 = f"========================================================================================================================================================================================================================================================================================================================================================================== C: {self.v_reason_close}"
            self.f_update_textbox(blank_after=True, blank_before=True, note2=True)
        if self.v_direction_evat != 'NO_POS':
            self.f_close_evat()
            time.sleep(7)
            print('close evat')
        self.v_direction = 'NO_POS'
        if self.v_bal_now < self.leaf_size:
            amount = round(self.v_bal_reset - self.v_bal_now,2)
            self.v_bal_now += amount
            self.v_bal_open = self.v_bal_now
            self.note2 = f"BALANCE<{self.leaf_size}. Adding ${amount} To Balance"
            self.f_update_textbox(blank_after=True, blank_before=True, note2=True)
            self.note2 = ''
            self.f_update_textbox()
            self.count_balance_add += 1
        # self.sum_net2.insert(0, float(0))
        self.v_reason_open = ''
        self.trigger_open = ''
        self.v_reason_close = ''
        self.trigger_close = ''
        self.count_consecutive = 0
        self.qualifier_comb5[1] = 0
        self.diff.insert(0, float(0))
        self.sum_4_state = ''
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
        self.SPREADSHEET_ID = '11oiQsgrqOmYjq6OjO_4Xf2q2eQa_wCIY50mLLaBOYRw'
        # self.SPREADSHEET_ID = '1liNHmgvzUeCjYVIPTywnQEeavIgaB2e0BeJFmrqR5l8'
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.localspreadsheet = LocalSheets().file

    def append(self, data):
        print('UPDATING TO GOOGLE SHEETS')
        self.backup()
        instance1 = MainFunction('')
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

    def backup(self, row_limit=10000, clear=False):
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
            worksheet.delete_rows(row_limit-1000 if row_limit > 1000 else row_limit, row_count - 3)  # Assuming headers are in row 1

            print("rows deleted successfully!")
        else:
            print("No need")

        return