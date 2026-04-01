<div align="center">

# 🚨 AirAlarm

**A desktop application that monitors and notifies about air raid alerts in Ukraine.**

[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart-3.x-0175C2?logo=dart&logoColor=white)](https://dart.dev)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#)
[![Version](https://img.shields.io/badge/Version-3.0.0-blue)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE.txt)

</div>

---

## 📖 Overview

**AirAlarm** is a cross-platform desktop application built with Flutter that connects to the [Ukraine Alarm API](https://api.ukrainealarm.com) and provides real-time audio notifications when an air raid alert is declared in your region of Ukraine.

Designed to run quietly in the system tray, it ensures you never miss a critical alert — even when your screen is off or you're focused on other tasks.

---

## ✨ Features

### 🔔 Alert Notifications
- **Air Raid Siren** — plays a siren sound for **3 minutes** (configurable) when an alert is declared in your region
- **All-clear Announcement** — plays a voice notification when the alert is lifted

### 🎵 Daily Rituals
- **09:00** — A minute of silence (*Хвилина мовчання*)
- **09:01** — The Ukrainian National Anthem (*Гімн України*)

### ⚙️ System Integration
- **Auto-start** on OS boot — runs in the background automatically
- **System tray** icon — stays out of your way until needed
- **Configurable region** — monitor any of Ukraine's administrative regions
- **Customizable siren duration** — adjust how long the alert sound plays

---

## 🖥️ Platform Support

| Platform | Status |
|----------|--------|
| Windows  | ✅ Supported (primary) |
| macOS    | ⚠️ Experimental |
| Linux    | ⚠️ Experimental |

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Flutter SDK** `>=3.x` — [Install Flutter](https://docs.flutter.dev/get-started/install)
- **Dart SDK** `>=3.2.6 <4.0.0` (bundled with Flutter)
- A **Ukraine Alarm API key** — obtain one at [api.ukrainealarm.com](https://api.ukrainealarm.com)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/andriytrotsyuk/AirAlarm.git
cd AirAlarm
```

### 2. Create the `.env` file

Create a `.env` file in the **root of the project** with the following content:

```env
UKRAINE_ALARM_API_KEY=your_api_key_here
```

| Variable | Description | Required |
|----------|-------------|----------|
| `UKRAINE_ALARM_API_KEY` | Your API key from [api.ukrainealarm.com](https://api.ukrainealarm.com) | ✅ Yes |

### 3. Install dependencies

```bash
flutter pub get
```

### 4. Run the application

```bash
flutter run -d windows
```

---

## 📦 Building a Release

### Windows Installer (`.exe`)

This project uses [`inno_bundle`](https://pub.dev/packages/inno_bundle) to generate a Windows installer via [Inno Setup](https://jrsoftware.org/isinfo.php).

**Requirements:**
- [Inno Setup](https://jrsoftware.org/isdl.php) must be installed on your system
- A path to the project must not contain cyrillic symbols

**Build the installer:**

```bash
flutter build windows --release
dart run inno_bundle
```

The generated installer (`.exe`) will be saved to:

```
build\inno_bundle\
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE.txt](LICENSE.txt) for details.

Copyright © 2025–2026 [zd4school](https://github.com/andriytrotsyuk)

---

<div align="center">

**Stay safe. Слава Україні! 🇺🇦**

</div>
