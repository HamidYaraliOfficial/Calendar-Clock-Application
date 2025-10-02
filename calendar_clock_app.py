import sys
import math
from datetime import datetime, date, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QTextEdit, QLabel, QStyleFactory, QTabWidget, QGridLayout,
    QScrollArea, QMenuBar, QMenu, QFileDialog, QMessageBox, QLineEdit, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont, QPainter, QPen, QBrush
import json
from pathlib import Path
import pytz
import calendar

class ClockWidget(QWidget):
    def __init__(self, timezone, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.timezone = pytz.timezone(timezone)

    def set_timezone(self, timezone):
        self.timezone = pytz.timezone(timezone)
        self.update()

    def update_time(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        size = min(self.width(), self.height())
        center = self.rect().center()
        radius = size // 2 - 15

        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(center, radius, radius)

        painter.setFont(QFont("Segoe UI", 12))
        for i in range(12):
            angle = (i * 30 - 90) * math.pi / 180
            x = center.x() + (radius - 25) * math.cos(angle)
            y = center.y() + (radius - 25) * math.sin(angle)
            painter.drawText(QRectF(x - 15, y - 15, 30, 30), Qt.AlignmentFlag.AlignCenter, str(12 if i == 0 else i))

        for i in range(60):
            if i % 5 != 0:
                angle = (i * 6 - 90) * math.pi / 180
                x1 = center.x() + (radius - 4) * math.cos(angle)
                y1 = center.y() + (radius - 4) * math.sin(angle)
                x2 = center.x() + radius * math.cos(angle)
                y2 = center.y() + radius * math.sin(angle)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        current_time = datetime.now(self.timezone)
        hour = current_time.hour % 12 + current_time.minute / 60.0
        minute = current_time.minute + current_time.second / 60.0
        second = current_time.second

        hour_angle = (hour * 30 - 90) * math.pi / 180
        hour_x = center.x() + (radius - 40) * math.cos(hour_angle)
        hour_y = center.y() + (radius - 40) * math.sin(hour_angle)
        painter.setPen(QPen(QColor(0, 0, 255), 5))
        painter.drawLine(center.x(), center.y(), int(hour_x), int(hour_y))

        minute_angle = (minute * 6 - 90) * math.pi / 180
        minute_x = center.x() + (radius - 25) * math.cos(minute_angle)
        minute_y = center.y() + (radius - 25) * math.sin(minute_angle)
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.drawLine(center.x(), center.y(), int(minute_x), int(minute_y))

        second_angle = (second * 6 - 90) * math.pi / 180
        second_x = center.x() + (radius - 15) * math.cos(second_angle)
        second_y = center.y() + (radius - 15) * math.sin(second_angle)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawLine(center.x(), center.y(), int(second_x), int(second_y))

class CalendarClockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendar & Clock")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('icon.ico'))

        self.current_lang = 'en'
        self.current_theme = 'Windows11'
        self.time_format = '24'
        self.timezones = [self.get_system_timezone()]
        self.clocks = []
        self.history = []
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.holidays = self.load_holidays()
        self.load_history()

        self.texts = {
            'en': {
                'title': 'Calendar & Clock',
                'country_label': 'Select Country:',
                'timezone_label': 'Select Timezone:',
                'add_timezone_btn': 'Add Timezone',
                'remove_timezone_btn': 'Remove Selected',
                'format_label': 'Time Format:',
                'digital_label': 'Digital Clocks:',
                'analog_label': 'Analog Clocks:',
                'calendar_label': 'Calendar:',
                'month_label': 'Month:',
                'year_label': 'Year:',
                'history_tab': 'History',
                'calendar_tab': 'Calendar',
                'settings_tab': 'Settings',
                'language_label': 'Language:',
                'theme_label': 'Theme:',
                'clear_history': 'Clear History',
                'status_idle': 'Displaying current time and calendar...',
                'status_updated': 'Updated: {time}',
                'status_added': 'Timezone {tz} added',
                'status_removed': 'Timezone {tz} removed',
                'history_time': 'Time',
                'history_timezone': 'Timezone',
                'history_date': 'Date',
                'history_action': 'Action',
                'save_history': 'Save History to File',
                'apply': 'Apply',
                'file_menu': 'File',
                'exit_action': 'Exit',
                'about': 'About',
                'about_text': 'Calendar & Clock\nVersion 1.0\nDeveloped by Hamid Yarali\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'copy_btn': 'Copy Time',
                'format_12': '12-Hour',
                'format_24': '24-Hour',
                'gregorian': 'Gregorian',
                'jalali': 'Jalali (Persian)',
                'hijri': 'Hijri (Islamic)',
                'calendar_format_label': 'Calendar Format:'
            },
            'fa': {
                'title': 'تقویم و ساعت',
                'country_label': 'انتخاب کشور:',
                'timezone_label': 'انتخاب منطقه زمانی:',
                'add_timezone_btn': 'افزودن منطقه زمانی',
                'remove_timezone_btn': 'حذف انتخاب‌شده',
                'format_label': 'فرمت زمان:',
                'digital_label': 'ساعت‌های دیجیتال:',
                'analog_label': 'ساعت‌های عقربه‌ای:',
                'calendar_label': 'تقویم:',
                'month_label': 'ماه:',
                'year_label': 'سال:',
                'history_tab': 'تاریخچه',
                'calendar_tab': 'تقویم',
                'settings_tab': 'تنظیمات',
                'language_label': 'زبان:',
                'theme_label': 'تم:',
                'clear_history': 'پاک کردن تاریخچه',
                'status_idle': 'نمایش زمان و تقویم کنونی...',
                'status_updated': 'به‌روزرسانی شد: {time}',
                'status_added': 'منطقه زمانی {tz} اضافه شد',
                'status_removed': 'منطقه زمانی {tz} حذف شد',
                'history_time': 'زمان',
                'history_timezone': 'منطقه زمانی',
                'history_date': 'تاریخ',
                'history_action': 'عملیات',
                'save_history': 'ذخیره تاریخچه در فایل',
                'apply': 'اعمال',
                'file_menu': 'فایل',
                'exit_action': 'خروج',
                'about': 'درباره',
                'about_text': 'تقویم و ساعت\nنسخه ۱.۰\nتوسعه‌یافته توسط حمید یارعلی\nگیت‌هاب: https://github.com/HamidYaraliOfficial\nاینستاگرام: https://www.instagram.com/hamidyaraliofficial\nتلگرام: @Hamid_Yarali',
                'copy_btn': 'کپی زمان',
                'format_12': '۱۲ ساعته',
                'format_24': '۲۴ ساعته',
                'gregorian': 'میلادی',
                'jalali': 'جلالی (شمسی)',
                'hijri': 'هجری (قمری)',
                'calendar_format_label': 'فرمت تقویم:'
            },
            'zh': {
                'title': '日历与时钟',
                'country_label': '选择国家：',
                'timezone_label': '选择时区：',
                'add_timezone_btn': '添加时区',
                'remove_timezone_btn': '移除选定',
                'format_label': '时间格式：',
                'digital_label': '数字时钟：',
                'analog_label': '模拟时钟：',
                'calendar_label': '日历：',
                'month_label': '月份：',
                'year_label': '年份：',
                'history_tab': '历史记录',
                'calendar_tab': '日历',
                'settings_tab': '设置',
                'language_label': '语言：',
                'theme_label': '主题：',
                'clear_history': '清除历史记录',
                'status_idle': '显示当前时间和日历...',
                'status_updated': '已更新：{time}',
                'status_added': '已添加时区 {tz}',
                'status_removed': '已移除时区 {tz}',
                'history_time': '时间',
                'history_timezone': '时区',
                'history_date': '日期',
                'history_action': '操作',
                'save_history': '将历史记录保存到文件',
                'apply': '应用',
                'file_menu': '文件',
                'exit_action': '退出',
                'about': '关于',
                'about_text': '日历与时钟\n版本 1.0\n由 Hamid Yarali 开发\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'copy_btn': '复制时间',
                'format_12': '12小时制',
                'format_24': '24小时制',
                'gregorian': '公历',
                'jalali': '波斯历',
                'hijri': '伊斯兰历',
                'calendar_format_label': '日历格式：'
            },
            'ru': {
                'title': 'Календарь и часы',
                'country_label': 'Выберите страну:',
                'timezone_label': 'Выберите часовой пояс:',
                'add_timezone_btn': 'Добавить часовой пояс',
                'remove_timezone_btn': 'Удалить выбранный',
                'format_label': 'Формат времени:',
                'digital_label': 'Цифровые часы:',
                'analog_label': 'Аналоговые часы:',
                'calendar_label': 'Календарь:',
                'month_label': 'Месяц:',
                'year_label': 'Год:',
                'history_tab': 'История',
                'calendar_tab': 'Календарь',
                'settings_tab': 'Настройки',
                'language_label': 'Язык:',
                'theme_label': 'Тема:',
                'clear_history': 'Очистить историю',
                'status_idle': 'Отображение текущего времени и календаря...',
                'status_updated': 'Обновлено: {time}',
                'status_added': 'Часовой пояс {tz} добавлен',
                'status_removed': 'Часовой пояс {tz} удален',
                'history_time': 'Время',
                'history_timezone': 'Часовой пояс',
                'history_date': 'Дата',
                'history_action': 'Действие',
                'save_history': 'Сохранить историю в файл',
                'apply': 'Применить',
                'file_menu': 'Файл',
                'exit_action': 'Выход',
                'about': 'О программе',
                'about_text': 'Календарь и часы\nВерсия 1.0\nРазработано Hamid Yarali\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'copy_btn': 'Копировать время',
                'format_12': '12-часовой',
                'format_24': '24-часовой',
                'gregorian': 'Григорианский',
                'jalali': 'Джалали (Персидский)',
                'hijri': 'Хиджри (Исламский)',
                'calendar_format_label': 'Формат календаря:'
            }
        }

        self.themes = {
            'Windows11': {
                'background': QColor(243, 243, 243),
                'text': QColor(0, 0, 0),
                'button': QColor(225, 225, 225),
                'button_text': QColor(0, 0, 0),
                'button_hover': QColor(200, 200, 200),
                'accent': QColor(0, 90, 158),
                'border': QColor(180, 180, 180),
                'header': QColor(230, 230, 230),
                'calendar_holiday': QColor(255, 204, 204)
            },
            'Dark': {
                'background': QColor(32, 32, 32),
                'text': QColor(230, 230, 230),
                'button': QColor(50, 50, 50),
                'button_text': QColor(230, 230, 230),
                'button_hover': QColor(70, 70, 70),
                'accent': QColor(0, 120, 212),
                'border': QColor(80, 80, 80),
                'header': QColor(40, 40, 40),
                'calendar_holiday': QColor(100, 50, 50)
            },
            'Light': {
                'background': QColor(255, 255, 255),
                'text': QColor(0, 0, 0),
                'button': QColor(240, 240, 240),
                'button_text': QColor(0, 0, 0),
                'button_hover': QColor(220, 220, 220),
                'accent': QColor(0, 120, 212),
                'border': QColor(200, 200, 200),
                'header': QColor(245, 245, 245),
                'calendar_holiday': QColor(255, 204, 204)
            },
            'Red': {
                'background': QColor(255, 235, 235),
                'text': QColor(80, 0, 0),
                'button': QColor(255, 200, 200),
                'button_text': QColor(80, 0, 0),
                'button_hover': QColor(255, 180, 180),
                'accent': QColor(200, 0, 0),
                'border': QColor(220, 150, 150),
                'header': QColor(255, 220, 220),
                'calendar_holiday': QColor(255, 150, 150)
            },
            'Blue': {
                'background': QColor(235, 245, 255),
                'text': QColor(0, 0, 80),
                'button': QColor(200, 220, 255),
                'button_text': QColor(0, 0, 80),
                'button_hover': QColor(180, 200, 255),
                'accent': QColor(0, 0, 200),
                'border': QColor(150, 180, 220),
                'header': QColor(220, 235, 255),
                'calendar_holiday': QColor(150, 200, 255)
            }
        }

        self.init_ui()
        self.apply_theme(self.current_theme)
        self.update_texts()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clocks)
        self.timer.start(1000)

    def get_system_timezone(self):
        try:
            return str(pytz.timezone(datetime.now().astimezone().tzinfo.name))
        except:
            return 'Asia/Tehran'

    def load_holidays(self):
        return {
            'gregorian': {
                (1, 1): 'New Year',
                (12, 25): 'Christmas'
            },
            'jalali': {
                (1, 1): 'نوروز',
                (1, 2): 'نوروز'
            },
            'hijri': {
                (1, 10): 'عاشورا',
                (12, 17): 'عید قربان'
            }
        }

    def gregorian_to_jalali(self, gy, gm, gd):
        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        if gy > 1600:
            jy = 979
            gy -= 1600
        else:
            jy = 0
            gy -= 621
        if gm > 2:
            gy2 = gy + 1
        else:
            gy2 = gy
        days = (365 * gy) + (int((gy2 + 3) / 4)) - (int((gy2 + 99) / 100)) + (int((gy2 + 399) / 400)) - 80 + gd + g_d_m[gm - 1]
        jy += 33 * (int(days / 12053))
        days %= 12053
        jy += 4 * (int(days / 1461))
        days %= 1461
        if days > 365:
            jy += int((days - 1) / 365)
            days = (days - 1) % 365
        if days < 186:
            jm = 1 + int(days / 31)
            jd = 1 + (days % 31)
        else:
            jm = 7 + int((days - 186) / 30)
            jd = 1 + ((days - 186) % 30)
        return [jy, jm, jd]

    def gregorian_to_hijri(self, gy, gm, gd):
        d = date(gy, gm, gd)
        jd = int((d - date(1, 1, 1)).days + 2)
        z = jd + 1721424
        l = z - 1948440
        n = int((l - 1) / 10631)
        l = l - 10631 * n + 354
        j = (int((10985 - l) / 5316)) * (int((50 * l) / 17719)) + (int(l / 5670)) * (int((43 * l) / 15238))
        l = l - (int((30 - j) / 15)) * (int((17719 * j) / 50)) - (int(j / 16)) * (int((15238 * j) / 43)) + 29
        hy = 30 * n + j - 30
        hm = l
        hd = z - (355 * n + 355 * j + (int((l + 1) / 30)) * 30 + l) + 1948440 - 1
        return [hy, hm, hd]

    def days_in_jalali_month(self, jy, jm):
        if jm <= 6:
            return 31
        elif jm <= 11:
            return 30
        else:
            return 29 if (jy % 33) % 4 == 1 else 30

    def days_in_hijri_month(self, hy, hm):
        if hm in [1, 3, 5, 7, 8, 10, 12]:
            return 30
        elif hm == 2:
            return 29 if (hy % 30) % 2 == 1 else 28
        else:
            return 29

    def jalali_weekday(self, jy, jm, jd):
        g_date = self.jalali_to_gregorian(jy, jm, jd)
        return date(g_date[0], g_date[1], g_date[2]).weekday()

    def hijri_weekday(self, hy, hm, hd):
        g_date = self.hijri_to_gregorian(hy, hm, hd)
        return date(g_date[0], g_date[1], g_date[2]).weekday()

    def jalali_to_gregorian(self, jy, jm, jd):
        if jy > 979:
            gy = 1600
            jy -= 979
        else:
            gy = 621
        if jm < 7:
            days = (jm - 1) * 31
        else:
            days = ((jm - 7) * 30) + 186
        days += 365 * jy + (int(jy / 33)) * 8 + (int(((jy % 33) + 3) / 4)) + 78 + jd
        gy += 400 * (int(days / 146097))
        days %= 146097
        if days > 36524:
            gy += 100 * (int(days / 36524))
            days %= 36524
            if days >= 365:
                days += 1
        gy += 4 * (int(days / 1461))
        days %= 1461
        if days > 365:
            gy += int((days - 1) / 365)
            days = (days - 1) % 365
        gd = days + 1
        if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
            g_d_m = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            g_d_m = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0
        while gm < 13 and gd > g_d_m[gm]:
            gd -= g_d_m[gm]
            gm += 1
        return [gy, gm, gd]

    def hijri_to_gregorian(self, hy, hm, hd):
        jd = hd + (int((29 * (hm - 1) + 13) / 30)) + 355 * (hy % 30) + 10631 * (int(hy / 30)) + 1948439
        z = jd - 1721424
        w = int((z - 0.5) / 146097)
        z = z - w * 146097
        x = int((z - 0.5) / 36524)
        if x == 4:
            x = 3
        z = z - x * 36524
        y = int((z - 0.5) / 1461)
        z = z - y * 1461
        n = int((z - 0.5) / 365)
        z = z - n * 365
        gy = 400 * w + 100 * x + 4 * y + n
        gd = z
        if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
            g_d_m = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            g_d_m = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0
        while gm < 13 and gd > g_d_m[gm]:
            gd -= g_d_m[gm]
            gm += 1
        return [gy, gm, gd]

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.menu_bar = QMenuBar()
        self.file_menu = QMenu(self.texts['en']['file_menu'])
        self.exit_action = self.file_menu.addAction(self.texts['en']['exit_action'])
        self.exit_action.triggered.connect(self.close)
        self.about_action = self.file_menu.addAction(self.texts['en']['about'])
        self.about_action.triggered.connect(self.show_about)
        self.menu_bar.addMenu(self.file_menu)
        self.main_layout.addWidget(self.menu_bar)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.95);
            }
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                background: rgba(0, 0, 0, 0.05);
                color: black;
            }
            QTabBar::tab:selected {
                background: rgba(0, 90, 158, 0.3);
                font-weight: bold;
                color: black;
            }
        """)
        self.main_layout.addWidget(self.tabs)

        self.calendar_tab = QWidget()
        self.calendar_layout = QVBoxLayout(self.calendar_tab)
        self.calendar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.calendar_layout.setSpacing(10)

        self.month_label = QLabel()
        self.month_label.setFont(QFont("Segoe UI", 12))
        self.month_combo = QComboBox()
        self.month_combo.addItems([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])
        self.month_combo.setCurrentIndex(self.current_month - 1)
        self.month_combo.setFixedHeight(40)
        self.month_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.month_combo.currentIndexChanged.connect(self.update_calendar)

        self.year_label = QLabel()
        self.year_label.setFont(QFont("Segoe UI", 12))
        self.year_input = QLineEdit(str(self.current_year))
        self.year_input.setFixedHeight(40)
        self.year_input.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)
        self.year_input.textChanged.connect(self.update_calendar)

        self.calendar_label = QLabel()
        self.calendar_label.setFont(QFont("Segoe UI", 12))
        self.calendar_container = QWidget()
        self.calendar_layout_inner = QHBoxLayout(self.calendar_container)
        
        self.gregorian_container = QWidget()
        self.gregorian_grid = QGridLayout(self.gregorian_container)
        self.gregorian_grid.setSpacing(5)
        
        self.jalali_container = QWidget()
        self.jalali_grid = QGridLayout(self.jalali_container)
        self.jalali_grid.setSpacing(5)
        
        self.hijri_container = QWidget()
        self.hijri_grid = QGridLayout(self.hijri_container)
        self.hijri_grid.setSpacing(5)

        self.calendar_layout_inner.addWidget(self.gregorian_container)
        self.calendar_layout_inner.addWidget(self.jalali_container)
        self.calendar_layout_inner.addWidget(self.hijri_container)

        self.clock_tab = QWidget()
        self.clock_layout = QVBoxLayout(self.clock_tab)
        self.clock_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.clock_layout.setSpacing(10)

        self.country_label = QLabel()
        self.country_label.setFont(QFont("Segoe UI", 12))
        self.country_combo = QComboBox()
        self.countries = {
            'Iran': 'Asia/Tehran',
            'United States': 'America/New_York',
            'United Kingdom': 'Europe/London',
            'China': 'Asia/Shanghai',
            'Russia': 'Europe/Moscow',
            'Japan': 'Asia/Tokyo',
            'Germany': 'Europe/Berlin'
        }
        self.country_combo.addItems(self.countries.keys())
        self.country_combo.setCurrentText('Iran')
        self.country_combo.setFixedHeight(40)
        self.country_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.country_combo.currentTextChanged.connect(self.update_timezone_combo)

        self.timezone_label = QLabel()
        self.timezone_label.setFont(QFont("Segoe UI", 12))
        self.timezone_combo = QComboBox()
        self.timezone_combo.addItems(pytz.common_timezones)
        self.timezone_combo.setCurrentText(self.timezones[0])
        self.timezone_combo.setFixedHeight(40)
        self.timezone_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        self.add_timezone_btn = QPushButton()
        self.add_timezone_btn.setFixedHeight(40)
        self.add_timezone_btn.setFont(QFont("Segoe UI", 12))
        self.add_timezone_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.add_timezone_btn.clicked.connect(self.add_timezone)

        self.remove_timezone_btn = QPushButton()
        self.remove_timezone_btn.setFixedHeight(40)
        self.remove_timezone_btn.setFont(QFont("Segoe UI", 12))
        self.remove_timezone_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(200, 0, 0, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(200, 0, 0, 1.0);
            }
        """)
        self.remove_timezone_btn.clicked.connect(self.remove_timezone)

        self.format_label = QLabel()
        self.format_label.setFont(QFont("Segoe UI", 12))
        self.format_combo = QComboBox()
        self.format_combo.addItems([self.texts['en']['format_12'], self.texts['en']['format_24']])
        self.format_combo.setFixedHeight(40)
        self.format_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.format_combo.currentIndexChanged.connect(self.change_format)

        self.timezone_list = QListWidget()
        self.timezone_list.setFixedHeight(100)
        self.timezone_list.setStyleSheet("""
            QListWidget {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)
        for tz in self.timezones:
            self.timezone_list.addItem(tz)

        self.digital_label = QLabel()
        self.digital_label.setFont(QFont("Segoe UI", 12))
        self.digital_container = QWidget()
        self.digital_layout = QGridLayout(self.digital_container)
        self.digital_layout.setSpacing(10)

        self.analog_label = QLabel()
        self.analog_label.setFont(QFont("Segoe UI", 12))
        self.analog_container = QWidget()
        self.analog_layout = QGridLayout(self.analog_container)
        self.analog_layout.setSpacing(10)

        self.copy_btn = QPushButton()
        self.copy_btn.setFixedHeight(40)
        self.copy_btn.setFont(QFont("Segoe UI", 12))
        self.copy_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setFixedHeight(100)
        self.status_text.setStyleSheet("""
            QTextEdit {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)

        calendar_selection_layout = QHBoxLayout()
        calendar_selection_layout.addWidget(self.month_label)
        calendar_selection_layout.addWidget(self.month_combo)
        calendar_selection_layout.addWidget(self.year_label)
        calendar_selection_layout.addWidget(self.year_input)

        self.calendar_layout.addWidget(self.calendar_label)
        self.calendar_layout.addLayout(calendar_selection_layout)
        self.calendar_layout.addWidget(self.calendar_container)

        timezone_layout = QHBoxLayout()
        timezone_layout.addWidget(self.country_label)
        timezone_layout.addWidget(self.country_combo)
        timezone_layout.addWidget(self.timezone_label)
        timezone_layout.addWidget(self.timezone_combo)
        timezone_layout.addWidget(self.add_timezone_btn)
        timezone_layout.addWidget(self.remove_timezone_btn)

        self.clock_layout.addLayout(timezone_layout)
        self.clock_layout.addWidget(self.timezone_list)
        self.clock_layout.addWidget(self.format_label)
        self.clock_layout.addWidget(self.format_combo)
        self.clock_layout.addWidget(self.digital_label)
        self.clock_layout.addWidget(self.digital_container)
        self.clock_layout.addWidget(self.analog_label)
        self.clock_layout.addWidget(self.analog_container)
        self.clock_layout.addWidget(self.copy_btn)
        self.clock_layout.addWidget(self.status_text)

        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout(self.history_tab)
        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_content = QWidget()
        self.history_grid = QGridLayout(self.history_content)
        self.history_grid.setSpacing(10)
        self.history_scroll.setWidget(self.history_content)
        self.history_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.95);
            }
        """)
        self.clear_history_btn = QPushButton()
        self.clear_history_btn.setFixedHeight(40)
        self.clear_history_btn.setFont(QFont("Segoe UI", 12))
        self.clear_history_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(200, 0, 0, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(200, 0, 0, 1.0);
            }
        """)
        self.clear_history_btn.clicked.connect(self.clear_history)
        self.save_history_btn = QPushButton()
        self.save_history_btn.setFixedHeight(40)
        self.save_history_btn.setFont(QFont("Segoe UI", 12))
        self.save_history_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.save_history_btn.clicked.connect(self.save_history_to_file)
        self.history_layout.addWidget(self.history_scroll)
        self.history_layout.addWidget(self.clear_history_btn)
        self.history_layout.addWidget(self.save_history_btn)

        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.settings_layout.setSpacing(10)

        self.language_label = QLabel()
        self.language_label.setFont(QFont("Segoe UI", 12))
        self.language_combo = QComboBox()
        self.language_combo.addItems(['English', 'فارسی', '中文', 'Русский'])
        self.language_combo.setFixedHeight(40)
        self.language_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.theme_label = QLabel()
        self.theme_label.setFont(QFont("Segoe UI", 12))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Windows11', 'Dark', 'Light', 'Red', 'Blue'])
        self.theme_combo.setFixedHeight(40)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        self.apply_btn = QPushButton()
        self.apply_btn.setFixedHeight(40)
        self.apply_btn.setFont(QFont("Segoe UI", 12))
        self.apply_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.apply_btn.clicked.connect(self.apply_settings)

        self.settings_layout.addWidget(self.language_label)
        self.settings_layout.addWidget(self.language_combo)
        self.settings_layout.addWidget(self.theme_label)
        self.settings_layout.addWidget(self.theme_combo)
        self.settings_layout.addWidget(self.apply_btn)
        self.settings_layout.addStretch()

        self.tabs.addTab(self.calendar_tab, self.texts['en']['calendar_tab'])
        self.tabs.addTab(self.clock_tab, self.texts['en']['history_tab'])
        self.tabs.addTab(self.history_tab, self.texts['en']['history_tab'])
        self.tabs.addTab(self.settings_tab, self.texts['en']['settings_tab'])

        self.update_clocks_ui()
        self.update_clocks()
        self.update_calendar()

    def apply_theme(self, theme_name):
        palette = QPalette()
        theme = self.themes.get(theme_name, self.themes['Windows11'])
        palette.setColor(QPalette.ColorRole.Window, theme['background'])
        palette.setColor(QPalette.ColorRole.WindowText, theme['text'])
        palette.setColor(QPalette.ColorRole.Button, theme['button'])
        palette.setColor(QPalette.ColorRole.ButtonText, theme['button_text'])
        palette.setColor(QPalette.ColorRole.Highlight, theme['accent'])
        palette.setColor(QPalette.ColorRole.Base, theme['background'])
        palette.setColor(QPalette.ColorRole.AlternateBase, theme['header'])
        palette.setColor(QPalette.ColorRole.Text, theme['text'])
        self.setPalette(palette)
        self.setStyle(QStyleFactory.create('WindowsVista' if theme_name == 'Windows11' else 'Fusion'))
        self.update_calendar()

    def update_texts(self):
        lang = self.current_lang
        self.setWindowTitle(self.texts[lang]['title'])
        self.country_label.setText(self.texts[lang]['country_label'])
        self.timezone_label.setText(self.texts[lang]['timezone_label'])
        self.add_timezone_btn.setText(self.texts[lang]['add_timezone_btn'])
        self.remove_timezone_btn.setText(self.texts[lang]['remove_timezone_btn'])
        self.format_label.setText(self.texts[lang]['format_label'])
        self.digital_label.setText(self.texts[lang]['digital_label'])
        self.analog_label.setText(self.texts[lang]['analog_label'])
        self.calendar_label.setText(self.texts[lang]['calendar_label'])
        self.month_label.setText(self.texts[lang]['month_label'])
        self.year_label.setText(self.texts[lang]['year_label'])
        self.copy_btn.setText(self.texts[lang]['copy_btn'])
        self.status_text.setText(self.texts[lang]['status_idle'])
        self.clear_history_btn.setText(self.texts[lang]['clear_history'])
        self.save_history_btn.setText(self.texts[lang]['save_history'])
        self.language_label.setText(self.texts[lang]['language_label'])
        self.theme_label.setText(self.texts[lang]['theme_label'])
        self.apply_btn.setText(self.texts[lang]['apply'])
        self.file_menu.setTitle(self.texts[lang]['file_menu'])
        self.exit_action.setText(self.texts[lang]['exit_action'])
        self.about_action.setText(self.texts[lang]['about'])

        self.tabs.setTabText(0, self.texts[lang]['calendar_tab'])
        self.tabs.setTabText(1, self.texts[lang]['history_tab'])
        self.tabs.setTabText(2, self.texts[lang]['history_tab'])
        self.tabs.setTabText(3, self.texts[lang]['settings_tab'])

        current_format = self.format_combo.currentText()
        self.format_combo.clear()
        self.format_combo.addItems([self.texts[lang]['format_12'], self.texts[lang]['format_24']])
        if current_format:
            index = 0 if current_format == self.texts['en']['format_12'] else 1
            self.format_combo.setCurrentIndex(index)

        if lang == 'fa':
            self.month_combo.clear()
            self.month_combo.addItems([
                'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
            ])
            self.month_combo.setCurrentIndex(self.current_month - 1)
        else:
            self.month_combo.clear()
            self.month_combo.addItems([
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ])
            self.month_combo.setCurrentIndex(self.current_month - 1)

        alignment = Qt.AlignmentFlag.AlignRight if lang == 'fa' else Qt.AlignmentFlag.AlignLeft
        self.country_label.setAlignment(alignment)
        self.timezone_label.setAlignment(alignment)
        self.format_label.setAlignment(alignment)
        self.digital_label.setAlignment(alignment)
        self.analog_label.setAlignment(alignment)
        self.calendar_label.setAlignment(alignment)
        self.month_label.setAlignment(alignment)
        self.year_label.setAlignment(alignment)
        self.language_label.setAlignment(alignment)
        self.theme_label.setAlignment(alignment)

    def change_language(self, index):
        langs = ['en', 'fa', 'zh', 'ru']
        self.current_lang = langs[index]
        self.update_texts()
        self.update_history_ui()
        self.update_clocks()
        self.update_calendar()

    def change_theme(self, index):
        themes = ['Windows11', 'Dark', 'Light', 'Red', 'Blue']
        self.current_theme = themes[index]
        self.apply_theme(self.current_theme)

    def change_format(self, index):
        self.time_format = '12' if index == 0 else '24'
        self.update_clocks()

    def apply_settings(self):
        self.update_texts()
        self.apply_theme(self.current_theme)
        self.update_clocks()
        self.update_calendar()

    def show_about(self):
        QMessageBox.information(self, self.texts[self.current_lang]['about'], 
                               self.texts[self.current_lang]['about_text'])

    def update_timezone_combo(self, country):
        timezone = self.countries.get(country, 'Asia/Tehran')
        self.timezone_combo.setCurrentText(timezone)

    def add_timezone(self):
        timezone = self.timezone_combo.currentText()
        if timezone not in self.timezones:
            self.timezones.append(timezone)
            self.timezone_list.addItem(timezone)
            self.update_clocks_ui()
            self.status_text.setText(self.texts[self.current_lang]['status_added'].format(tz=timezone))
            self.add_to_history(timezone)

    def remove_timezone(self):
        selected = self.timezone_list.currentItem()
        if selected and len(self.timezones) > 1:
            timezone = selected.text()
            self.timezones.remove(timezone)
            self.timezone_list.takeItem(self.timezone_list.row(selected))
            self.update_clocks_ui()
            self.status_text.setText(self.texts[self.current_lang]['status_removed'].format(tz=timezone))
            self.add_to_history(timezone, removed=True)

    def update_clocks_ui(self):
        for i in reversed(range(self.digital_layout.count())):
            self.digital_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.analog_layout.count())):
            self.analog_layout.itemAt(i).widget().setParent(None)
        self.clocks = []

        for i, tz in enumerate(self.timezones):
            digital_display = QLineEdit()
            digital_display.setReadOnly(True)
            digital_display.setFixedHeight(40)
            digital_display.setStyleSheet("""
                QLineEdit {
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.95);
                    color: #0000FF;
                }
            """)
            digital_label = QLabel(tz)
            digital_label.setFont(QFont("Segoe UI", 10))
            digital_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            digital_label.setStyleSheet("color: black;")
            self.digital_layout.addWidget(digital_label, i * 2, 0)
            self.digital_layout.addWidget(digital_display, i * 2 + 1, 0)

            analog_clock = ClockWidget(tz)
            self.analog_layout.addWidget(analog_clock, i // 2, i % 2)
            analog_label = QLabel(tz)
            analog_label.setFont(QFont("Segoe UI", 10))
            analog_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            analog_label.setStyleSheet("color: black;")
            self.analog_layout.addWidget(analog_label, (i // 2) + 1, i % 2)

            self.clocks.append((digital_display, analog_clock))

        self.update_clocks()

    def update_clocks(self):
        for i, (digital_display, analog_clock) in enumerate(self.clocks):
            timezone = pytz.timezone(self.timezones[i])
            current_time = datetime.now(timezone)
            format_str = "%I:%M:%S %p" if self.time_format == '12' else "%H:%M:%S"
            time_str = current_time.strftime(format_str)
            digital_display.setText(time_str)
            analog_clock.update_time()
        self.status_text.setText(self.texts[self.current_lang]['status_updated'].format(time=datetime.now(pytz.timezone(self.timezones[0])).strftime(format_str)))

    def copy_to_clipboard(self):
        times = [digital.text() + f" ({tz})" for digital, _ in self.clocks for tz in self.timezones]
        if times:
            QApplication.clipboard().setText("\n".join(times))
            self.status_text.setText(self.texts[self.current_lang]['status_updated'].format(time="Times copied to clipboard"))

    def update_calendar(self):
        for i in reversed(range(self.gregorian_grid.count())):
            self.gregorian_grid.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.jalali_grid.count())):
            self.jalali_grid.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.hijri_grid.count())):
            self.hijri_grid.itemAt(i).widget().setParent(None)

        try:
            self.current_year = int(self.year_input.text())
        except ValueError:
            self.current_year = datetime.now().year
            self.year_input.setText(str(self.current_year))

        self.current_month = max(1, min(12, self.month_combo.currentIndex() + 1))

        headers = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        if self.current_lang == 'fa':
            headers = ['یک‌شنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه']
        elif self.current_lang == 'zh':
            headers = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
        elif self.current_lang == 'ru':
            headers = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']

        for col, header in enumerate(headers):
            for grid, title in [
                (self.gregorian_grid, self.texts[self.current_lang]['gregorian']),
                (self.jalali_grid, self.texts[self.current_lang]['jalali']),
                (self.hijri_grid, self.texts[self.current_lang]['hijri'])
            ]:
                if col == 0:
                    title_label = QLabel(title)
                    title_label.setStyleSheet("font-weight: bold; font-size: 16px; padding: 5px; color: black;")
                    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    grid.addWidget(title_label, 0, 0, 1, 7)
                label = QLabel(header)
                label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; color: black;")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid.addWidget(label, 1, col)

        try:
            # Gregorian Calendar
            cal = calendar.monthcalendar(self.current_year, self.current_month)
            for week, days in enumerate(cal):
                for day, day_num in enumerate(days):
                    label = QLabel(str(day_num) if day_num != 0 else "")
                    label.setFixedSize(50, 50)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if day_num != 0:
                        if (self.current_month, day_num) in self.holidays['gregorian']:
                            label.setStyleSheet(f"""
                                QLabel {{
                                    border-radius: 8px;
                                    font-size: 14px;
                                    background: {self.themes[self.current_theme]['calendar_holiday'].name()};
                                    color: black;
                                }}
                            """)
                        else:
                            label.setStyleSheet("""
                                QLabel {
                                    border-radius: 8px;
                                    font-size: 14px;
                                    background: rgba(255, 255, 255, 0.95);
                                    color: black;
                                }
                            """)
                    self.gregorian_grid.addWidget(label, week + 2, day)
        except ValueError:
            self.status_text.setText("Invalid date for Gregorian calendar")

        try:
            # Jalali Calendar
            j_date = self.gregorian_to_jalali(self.current_year, self.current_month, 1)
            j_year, j_month, j_day = j_date
            days_in_month = self.days_in_jalali_month(j_year, j_month)
            first_day = self.jalali_weekday(j_year, j_month, 1)
            weeks = []
            current_week = [0] * first_day
            for day in range(1, days_in_month + 1):
                if len(current_week) == 7:
                    weeks.append(current_week)
                    current_week = []
                current_week.append(day)
            if current_week:
                current_week.extend([0] * (7 - len(current_week)))
                weeks.append(current_week)
            for week, days in enumerate(weeks):
                for day, day_num in enumerate(days):
                    label = QLabel(str(day_num) if day_num != 0 else "")
                    label.setFixedSize(50, 50)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if day_num != 0:
                        if (j_month, day_num) in self.holidays['jalali']:
                            label.setStyleSheet(f"""
                                QLabel {{
                                    border-radius: 8px;
                                    font-size: 14px;
                                    background: {self.themes[self.current_theme]['calendar_holiday'].name()};
                                    color: black;
                                }}
                            """)
                        else:
                            label.setStyleSheet("""
                                QLabel {
                                    border-radius: 8px;
                                    font-size: 14px;
                                    background: rgba(255, 255, 255, 0.95);
                                    color: black;
                                }
                            """)
                    self.jalali_grid.addWidget(label, week + 2, day)
        except ValueError:
            self.status_text.setText("Invalid date for Jalali calendar")

        try:
            # Hijri Calendar
            h_date = self.gregorian_to_hijri(self.current_year, self.current_month, 1)
            h_year, h_month, h_day = h_date
            days_in_month = self.days_in_hijri_month(h_year, h_month)
            first_day = self.hijri_weekday(h_year, h_month, 1)
            weeks = []
            current_week = [0] * first_day
            for day in range(1, days_in_month + 1):
                if len(current_week) == 7:
                    weeks.append(current_week)
                    current_week = []
                current_week.append(day)
            if current_week:
                current_week.extend([0] * (7 - len(current_week)))
                weeks.append(current_week)
            for week, days in enumerate(weeks):
                for day, day_num in enumerate(days):
                    label = QLabel(str(day_num) if day_num != 0 else "")
                    label.setFixedSize(50, 50)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if day_num != 0:
                        if (h_month, day_num) in self.holidays['hijri']:
                            label.setStyleSheet(f"""
                                QLabel {{
                                    border-radius: 8px;
                                    font-size: 14px;
                                    background: {self.themes[self.current_theme]['calendar_holiday'].name()};
                                    color: black;
                                }}
                            """)
                        else:
                            label.setStyleSheet("""
                                QLabel {
                                    border-radius: 8px;
                                    font-size: 14px;
                                    background: rgba(255, 255, 255, 0.95);
                                    color: black;
                                }
                            """)
                    self.hijri_grid.addWidget(label, week + 2, day)
        except ValueError:
            self.status_text.setText("Invalid date for Hijri calendar")

    def add_to_history(self, timezone, removed=False):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for i, tz in enumerate(self.timezones):
            current_time = datetime.now(pytz.timezone(tz))
            format_str = "%I:%M:%S %p" if self.time_format == '12' else "%H:%M:%S"
            time_str = current_time.strftime(format_str)
            self.history.append({
                'time': time_str,
                'timezone': tz,
                'date': timestamp,
                'action': 'Removed' if removed and tz == timezone else 'Added' if tz == timezone else 'Updated'
            })
        self.save_history()
        self.update_history_ui()

    def save_history(self):
        with open('calendar_clock_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        try:
            with open('calendar_clock_history.json', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save_history_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, self.texts[self.current_lang]['save_history'], "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
            self.status_text.setText(self.texts[self.current_lang]['status_updated'].format(time="History saved to file"))

    def update_history_ui(self):
        for i in reversed(range(self.history_grid.count())):
            self.history_grid.itemAt(i).widget().setParent(None)

        headers = [
            self.texts[self.current_lang]['history_time'],
            self.texts[self.current_lang]['history_timezone'],
            self.texts[self.current_lang]['history_date'],
            self.texts[self.current_lang]['history_action']
        ]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; color: black;")
            label.setAlignment(Qt.AlignmentFlag.AlignRight if self.current_lang == 'fa' else Qt.AlignmentFlag.AlignLeft)
            self.history_grid.addWidget(label, 0, col)

        for row, item in enumerate(self.history, 1):
            time_label = QLabel(item['time'])
            timezone_label = QLabel(item['timezone'])
            date_label = QLabel(item['date'])
            action_label = QLabel(item['action'])
            
            for label in [time_label, timezone_label, date_label, action_label]:
                label.setStyleSheet("font-size: 12px; padding: 5px; border-bottom: 1px solid rgba(0, 0, 0, 0.1); color: black;")
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignRight if self.current_lang == 'fa' else Qt.AlignmentFlag.AlignLeft)
            
            self.history_grid.addWidget(time_label, row, 0)
            self.history_grid.addWidget(timezone_label, row, 1)
            self.history_grid.addWidget(date_label, row, 2)
            self.history_grid.addWidget(action_label, row, 3)

    def clear_history(self):
        self.history = []
        self.save_history()
        self.update_history_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    window = CalendarClockApp()
    window.show()
    sys.exit(app.exec())