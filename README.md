#🚀 TurboCopy
TurboCopy is a modern, high-performance file transfer utility for Windows. It acts as a powerful GUI wrapper for the native Robocopy engine, combining command-line speed with ease of use.

Designed to replace the standard Windows copy handler, TurboCopy offers multi-threaded transfers, drag-and-drop support, and smart conflict resolution in a sleek dark-mode interface.

#✨ Key Features
⚡ 3 Speed Modes (Gear System):

🐢 Slow (Background): Uses Inter-Packet Gap (/IPG:5) to copy files silently without slowing down your PC. Perfect for background tasks while gaming.

🚗 Medium (Balanced): Uses standard multi-threading (/MT:8). The sweet spot between speed and system responsiveness.

🚀 Turbo (Unleashed): Uses aggressive multi-threading (/MT:32). Maximizes CPU and Disk usage for the fastest possible transfer.

🌍 Multi-Language Support:

Supports 8 Languages: English, Turkish, Arabic, Italian, Japanese, French, Russian, and Chinese.



🖱️ Drag & Drop: Easily drag folders from your desktop directly into the Source and Destination fields.

📂 Context Menu Integration: Adds a "Copy with TurboCopy" option to the Windows Right-Click menu for instant access.

🛡️ Smart Conflict Resolution:

Overwrite: Force copy everything.

Skip: Ignore existing files (Fastest).

Smart Update: Only copy new or updated files.

Smart Memory: Remembers your language preference via config.json.

🛑 Safe & Secure:

Prevents accidental data loss (No "Mirror" mode enabled by default).

Auto-Kill: Instantly terminates background Robocopy processes when the app is closed.

🔌 Auto-Shutdown: Optional feature to shut down the computer automatically after a large transfer is complete.

#📦 Installation
Option 1: Installer (Recommended)
Download the latest TurboCopy_Setup.exe from the Releases page.

Run the installer (requires Administrator privileges to register the Context Menu).

Right-click any folder and select Copy with TurboCopy.

Option 2: Portable
Download turbocopy.exe.

Run it directly. Note: Context menu integration requires the Setup version.