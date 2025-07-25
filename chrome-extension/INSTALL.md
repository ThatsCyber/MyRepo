# 🚀 QuickSight Auto Downloader - Installation Guide

## 📦 What This Extension Does

✅ **Automatically downloads Supply & Demand CSV** from QuickSight  
✅ **Runs every 1.5 hours** from 7 AM to 5 PM (your local time)  
✅ **No manual intervention** needed after setup  
✅ **Beautiful dashboard** to monitor downloads  
✅ **Expandable** for future additional sheets  

## 🔧 Installation Steps

### 1. **Prepare Icons (Optional)**
- Add PNG icon files to the `icons/` folder:
  - `icon16.png`, `icon32.png`, `icon48.png`, `icon128.png`
- Or skip this step (extension will work with warnings)

### 2. **Load Extension in Chrome**

1. **Open Chrome** and go to: `chrome://extensions/`

2. **Enable Developer Mode** (toggle in top-right corner)

3. **Click "Load unpacked"** button

4. **Select the `chrome-extension` folder** from your project:
   ```
   MyRepo-main/chrome-extension/
   ```

5. **Extension should appear** in your extensions list! 🎉

### 3. **Grant Permissions**
- Chrome will ask for permissions to:
  - Access QuickSight websites
  - Show notifications
  - Set alarms
  - Download files
- **Click "Allow"** for all permissions

### 4. **Test Installation**

1. **Open QuickSight** in a new tab
2. **Log in** and navigate to your Supply & Demand dashboard
3. **Click the extension icon** in the toolbar (📥)
4. **Verify the popup shows** your schedule and status

## 🎯 How to Use

### **Automatic Mode (Recommended)**
- Extension runs automatically every 1.5 hours
- Downloads happen at: 7:00 AM, 8:30 AM, 10:00 AM, 11:30 AM, 1:00 PM, 2:30 PM, 4:00 PM
- Just keep QuickSight open in a browser tab!

### **Manual Mode**
- Click the extension icon
- Click "📥 Download Now" button
- Downloads immediately

### **Monitor & Control**
- **View schedule** in the popup
- **See download history** and success/failures
- **Enable/disable** automatic downloads
- **Reset schedule** if needed

## 📊 Daily Schedule

The extension automatically calculates 7 download times:

```
7:00 AM  →  8:30 AM  →  10:00 AM  →  11:30 AM
    ↓
1:00 PM  →  2:30 PM  →  4:00 PM
```

**Stops before 5:00 PM** as requested! ✅

## 🔧 Troubleshooting

### **Extension not appearing?**
- Make sure you selected the correct folder
- Check Chrome console for errors: `chrome://extensions/` → Details → Inspect views

### **Downloads not working?**
- Ensure you're logged into QuickSight
- Check popup for error messages
- Make sure QuickSight tab is not sleeping/inactive

### **Wrong data downloading?**
- Open popup and try "Download Now" manually
- Check if you're on the correct QuickSight dashboard
- The extension looks for "Supply & Demand" chart specifically

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Popup shows "Auto Download: Enabled"
- ✅ Schedule shows all 7 daily times
- ✅ Downloads appear in your Downloads folder
- ✅ Recent Activity shows successful downloads

## 🔮 Future Enhancements

This extension is designed to be easily expandable for:
- Additional sheets (just add to config)
- Different schedules
- Multiple QuickSight dashboards
- Custom notifications

**Enjoy your automated downloads!** 🎊 