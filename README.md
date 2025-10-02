# Calendar & Clock Application

## English

### Overview
The **Calendar & Clock** application is a versatile desktop tool built using Python and PyQt6, designed to display time and calendars in multiple formats. It supports Gregorian, Jalali (Persian), and Hijri (Islamic) calendars, displayed simultaneously side-by-side for easy comparison. Users can view digital and analog clocks for multiple time zones, customize the interface with different themes and languages, and track time-related actions in a history log.

### Features
- **Multi-Calendar Display**: View Gregorian, Jalali, and Hijri calendars concurrently for a selected year and month.
- **Time Zone Support**: Add and remove multiple time zones, with real-time digital and analog clock displays.
- **Customizable Interface**: Choose from multiple themes (Windows11, Dark, Light, Red, Blue) and languages (English, Persian, Chinese, Russian).
- **Time Format Options**: Toggle between 12-hour and 24-hour time formats.
- **History Tracking**: Log time zone additions and removals with timestamps, savable to a JSON file.
- **Holiday Highlights**: Mark significant holidays in each calendar system with customizable colors.

### Requirements
- Python 3.9 or higher
- PyQt6
- pytz

### Installation
1. Ensure Python 3.9+ is installed on your system.
2. Install the required packages:
   ```bash
   pip install PyQt6 pytz
   ```
3. Download the application source code from the repository.
4. Run the application:
   ```bash
   python calendar_clock_app.py
   ```

### Usage
- **Calendar Tab**: Select a year and month to view Gregorian, Jalali, and Hijri calendars side-by-side. Holidays are highlighted based on the selected theme.
- **Clock Tab**: Add or remove time zones, choose a time format, and view digital and analog clocks.
- **History Tab**: Review logged actions (e.g., time zone changes) and save them to a JSON file.
- **Settings Tab**: Customize the language and theme to suit your preferences.

### Contributing
Contributions are welcome! Feel free to submit issues or pull requests to enhance the application.

### License
This project is licensed under the MIT License.

---

## فارسی

### بررسی اجمالی
برنامه **تقویم و ساعت** یک ابزار دسکتاپ چندمنظوره است که با استفاده از پایتون و PyQt6 توسعه یافته و برای نمایش زمان و تقویم‌ها در قالب‌های مختلف طراحی شده است. این برنامه از تقویم‌های میلادی، جلالی (شمسی) و هجری (قمری) پشتیبانی می‌کند که به‌صورت همزمان در کنار یکدیگر نمایش داده می‌شوند تا مقایسه آسان‌تر شود. کاربران می‌توانند ساعت‌های دیجیتال و عقربه‌ای را برای چندین منطقه زمانی مشاهده کنند، رابط کاربری را با تم‌ها و زبان‌های مختلف شخصی‌سازی کنند و اقدامات مرتبط با زمان را در یک لاگ تاریخچه ثبت کنند.

### ویژگی‌ها
- **نمایش چند تقویمی**: مشاهده همزمان تقویم‌های میلادی، جلالی و هجری برای سال و ماه انتخاب‌شده.
- **پشتیبانی از مناطق زمانی**: افزودن و حذف مناطق زمانی متعدد با نمایش ساعت‌های دیجیتال و عقربه‌ای به‌صورت real-time.
- **رابط کاربری قابل‌تنظیم**: انتخاب از میان تم‌های مختلف (ویندوز ۱۱، تیره، روشن، قرمز، آبی) و زبان‌ها (انگلیسی، فارسی، چینی، روسی).
- **گزینه‌های فرمت زمان**: جابجایی بین فرمت‌های ۱۲ ساعته و ۲۴ ساعته.
- **پیگیری تاریخچه**: ثبت افزودن و حذف مناطق زمانی با زمان‌بندی، قابل ذخیره در فایل JSON.
- **برجسته‌سازی تعطیلات**: علامت‌گذاری تعطیلات مهم در هر سیستم تقویمی با رنگ‌های قابل‌تنظیم.

### پیش‌نیازها
- پایتون ۳.۹ یا بالاتر
- PyQt6
- pytz

### نصب
۱. اطمینان حاصل کنید که پایتون ۳.۹ یا بالاتر روی سیستم شما نصب است.
۲. بسته‌های موردنیاز را نصب کنید:
   ```bash
   pip install PyQt6 pytz
   ```
۳. کد منبع برنامه را از مخزن دانلود کنید.
۴. برنامه را اجرا کنید:
   ```bash
   python calendar_clock_app.py
   ```

### استفاده
- **تب تقویم**: سال و ماه را انتخاب کنید تا تقویم‌های میلادی، جلالی و هجری را در کنار هم مشاهده کنید. تعطیلات بر اساس تم انتخاب‌شده برجسته می‌شوند.
- **تب ساعت**: مناطق زمانی را اضافه یا حذف کنید، فرمت زمان را انتخاب کنید و ساعت‌های دیجیتال و عقربه‌ای را مشاهده کنید.
- **تب تاریخچه**: اقدامات ثبت‌شده (مانند تغییرات منطقه زمانی) را بررسی کنید و آن‌ها را در فایل JSON ذخیره کنید.
- **تب تنظیمات**: زبان و تم را مطابق با ترجیحات خود شخصی‌سازی کنید.

### مشارکت
از مشارکت استقبال می‌شود! لطفاً برای بهبود برنامه، مشکلات را گزارش دهید یا درخواست‌های pull ارسال کنید.

### مجوز
این پروژه تحت مجوز MIT منتشر شده است.

---

## 中文

### 概述
**日历与时钟**应用程序是一款使用Python和PyQt6构建的多功能桌面工具，旨在以多种格式显示时间和日历。它支持公历、波斯历（Jalali）和伊斯兰历（Hijri），并可同时并排显示以便于比较。用户可以查看多个时区的数字和模拟时钟，定制不同主题和语言的界面，并记录与时间相关的操作历史。

### 功能
- **多日历显示**：同时查看选定年份和月份的公历、波斯历和伊斯兰历。
- **时区支持**：添加和删除多个时区，实时显示数字和模拟时钟。
- **可定制界面**：从多个主题（Windows11、暗色、亮色、红色、蓝色）和语言（英语、波斯语、汉语、俄语）中选择。
- **时间格式选项**：在12小时制和24小时制之间切换。
- **历史记录**：记录时区添加和删除操作及时间戳，可保存为JSON文件。
- **节日高亮**：在每个日历系统中标记重要节日，支持自定义颜色。

### 要求
- Python 3.9 或更高版本
- PyQt6
- pytz

### 安装
1. 确保系统中已安装Python 3.9或更高版本。
2. 安装所需包：
   ```bash
   pip install PyQt6 pytz
   ```
3. 从仓库下载应用程序源代码。
4. 运行应用程序：
   ```bash
   python calendar_clock_app.py
   ```

### 使用方法
- **日历选项卡**：选择年份和月份，同时查看公历、波斯历和伊斯兰历。节日将根据所选主题高亮显示。
- **时钟选项卡**：添加或删除时区，选择时间格式，查看数字和模拟时钟。
- **历史记录选项卡**：查看记录的操作（例如时区更改）并将其保存为JSON文件。
- **设置选项卡**：根据偏好自定义语言和主题。

### 贡献
欢迎贡献！请提交问题或拉取请求以改进应用程序。

### 许可证
本项目采用MIT许可证。