

# Hardware Monitoring System (HMS)

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production--ready-success)

A professional, cross-platform system monitoring tool that provides real-time tracking of CPU, Memory, GPU, Disk, and Network resources. Built with Python for reliability, extensibility, and ease of use. Perfect for system administrators, developers, and power users who need comprehensive hardware insights.

---

## Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Command-Line Arguments](#command-line-arguments)
- [Monitoring Components](#monitoring-components)
- [Configuration Examples](#configuration-examples)
- [Data Logging](#data-logging)
- [Output Format](#output-format)
- [Platform-Specific Notes](#platform-specific-notes)
- [Troubleshooting](#troubleshooting)
- [Performance Considerations](#performance-considerations)
- [Comparison with Original](#comparison-with-original)
- [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## Features

### Core Monitoring Capabilities
- **CPU Monitoring**: Real-time usage, frequency, core count, and temperature (where supported)
- **Memory Tracking**: RAM usage, available memory, swap usage, and statistics
- **GPU Support**: Multi-GPU monitoring for NVIDIA and AMD cards with memory and temperature
- **Disk Analysis**: All mounted partitions with usage, capacity, and filesystem information
- **Network Statistics**: Data transfer (sent/received) and packet counts
- **Process Tracking**: Top N processes by CPU and memory consumption

### Cross-Platform Compatibility
- **Windows**: Full support with WMIC-based CPU detection
- **Linux**: Complete feature set including temperature monitoring
- **macOS**: Standard monitoring with platform-specific optimizations

### Advanced Features
- **Rolling Statistics**: Track min/max/average for CPU, Memory, and GPU over 60-second window
- **Alert System**: Configurable warning and critical thresholds with visual indicators
- **CSV Logging**: Optional data logging for historical analysis and reporting
- **Process Monitoring**: Identify resource-intensive applications in real-time
- **System Information**: Uptime, hostname, OS details, and session duration
- **Multiple GPU Support**: Monitor all available GPUs simultaneously

### Quality of Life Improvements
- **Configurable Refresh Rate**: Adjust update frequency from 0.1 to 10+ seconds
- **Customizable Thresholds**: Set warning and critical levels per component
- **Flexible Display**: Choose number of processes to display
- **Non-Intrusive**: Minimal system overhead during monitoring
- **Graceful Degradation**: Works even when optional features are unavailable

---

## System Requirements

### Required
- **Python**: 3.6 or higher
- **Operating System**: Windows 7+, Linux (any modern distribution), macOS 10.12+
- **Terminal**: Any terminal emulator with Python support
- **Memory**: Minimal (typically <50 MB)
- **CPU**: Any modern processor

### Python Dependencies

#### Core Dependency (Required)
```bash
psutil>=5.9.0
```

#### Optional Dependencies (Enhanced Features)
```bash
py-cpuinfo>=9.0.0      # Better CPU identification
nvidia-ml-py3>=7.352.0  # NVIDIA GPU support
gputil>=1.4.0          # AMD GPU support
```

**Note**: The system works with just `psutil` installed. Optional packages enhance functionality but are not required.

---

## Installation

### Method 1: Quick Install (Recommended)

```bash
# Step 1: Install core dependency
pip install psutil

# Step 2: Download the script
wget https://raw.githubusercontent.com/yourusername/hms/main/hms_improved.py
# or use curl
curl -O https://raw.githubusercontent.com/yourusername/hms/main/hms_improved.py

# Step 3: Run the monitor
python hms_improved.py
```

### Method 2: Full Installation with All Features

```bash
# Step 1: Clone the repository
git clone https://github.com/yourusername/hms.git
cd hms

# Step 2: Install all dependencies
pip install -r requirements.txt

# Step 3: Run the monitor
python hms_improved.py
```

### Method 3: Virtual Environment (Best Practice)

```bash
# Step 1: Create virtual environment
python -m venv hms_env

# Step 2: Activate environment
# On Windows:
hms_env\Scripts\activate
# On Linux/macOS:
source hms_env/bin/activate

# Step 3: Install dependencies
pip install psutil py-cpuinfo

# Step 4: Run the monitor
python hms_improved.py
```

### Verify Installation

```bash
# Check Python version
python --version

# Verify psutil installation
python -c "import psutil; print('psutil version:', psutil.__version__)"

# Test the script
python hms_improved.py --help
```

---

## Quick Start

### Basic Usage (No Configuration)

```bash
python hms_improved.py
```

This launches HMS with default settings:
- 1-second refresh rate
- 80% warning threshold, 90% critical threshold
- 5 top processes displayed
- No logging enabled

### Exit the Program

Press `Ctrl+C` to stop monitoring and view session summary.

---

## Usage Guide

### Starting the Monitor

1. **Open your terminal**
2. **Navigate to HMS directory**:
   ```bash
   cd path/to/hms
   ```
3. **Run the program**:
   ```bash
   python hms_improved.py
   ```

### Understanding the Display

The monitor displays five main sections:

1. **Header**: System information, uptime, session start time
2. **CPU Information**: Model, cores, usage, temperature, statistics
3. **Memory Information**: Total, used, available, swap, statistics
4. **GPU Information**: Model(s), usage, memory, temperature (if available)
5. **Disk Information**: All partitions with usage and capacity
6. **Network Information**: Data transfer and packet counts
7. **Top Processes**: Resource-intensive applications

### Reading Alert Indicators

```
[WARNING] CPU at 85.0%     # Yellow alert: Approaching limits
[CRITICAL] Memory at 95.0%  # Red alert: Urgent attention needed
```

### Session Information

When you exit (Ctrl+C), HMS displays:
- Total session duration
- Log file location (if logging was enabled)

---

## Command-Line Arguments

### General Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--refresh` | float | 1.0 | Update interval in seconds (0.1-10.0) |
| `--processes` | int | 5 | Number of top processes to display (1-20) |
| `--log` | flag | False | Enable CSV logging |
| `--log-file` | string | hms_log.csv | Path to log file |

### CPU Thresholds

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--cpu-warn` | int | 80 | CPU warning threshold (%) |
| `--cpu-crit` | int | 90 | CPU critical threshold (%) |

### Memory Thresholds

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--mem-warn` | int | 80 | Memory warning threshold (%) |
| `--mem-crit` | int | 90 | Memory critical threshold (%) |

### GPU Thresholds

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--gpu-warn` | int | 80 | GPU warning threshold (%) |
| `--gpu-crit` | int | 90 | GPU critical threshold (%) |

### Disk Thresholds

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--disk-warn` | int | 80 | Disk warning threshold (%) |
| `--disk-crit` | int | 90 | Disk critical threshold (%) |

### Help

```bash
python hms_improved.py --help
```

---

## Monitoring Components

### CPU Information

**What is Monitored:**
- CPU model and manufacturer
- Physical and logical core count
- Current frequency (MHz)
- Real-time usage percentage
- Per-core utilization (tracked internally)
- CPU temperature (Linux systems with sensors)
- Rolling statistics (min/max/average)

**Detection Methods:**
1. py-cpuinfo library (most accurate)
2. platform.processor()
3. /proc/cpuinfo parsing (Linux)
4. WMIC query (Windows)
5. Fallback to architecture name

**Example Output:**
```
[CPU INFORMATION]
--------------------------------------------------------------------------------
 Model: AMD Ryzen 9 5950X 16-Core Processor
 Cores: 16 Physical, 32 Logical
 Frequency: 3400 MHz
 Temperature: 45.0C
 Usage: 35.2%
 Statistics: Min=12.5% | Avg=32.8% | Max=85.3%
```

### Memory Information

**What is Monitored:**
- Total installed RAM
- Used memory
- Available memory
- Memory usage percentage
- Swap space (total/used/percentage)
- Rolling statistics

**Example Output:**
```
[MEMORY INFORMATION]
--------------------------------------------------------------------------------
 Total: 64.00 GB
 Used: 28.50 GB
 Available: 35.50 GB
 Usage: 44.5%
 Swap: 0.00 GB / 8.00 GB (0.0%)
 Statistics: Min=35.2% | Avg=42.1% | Max=68.9%
```

### GPU Information

**Supported Vendors:**
- NVIDIA (via nvidia-ml-py3)
- AMD (via gputil)

**What is Monitored:**
- GPU model and vendor
- GPU utilization percentage
- Video memory (used/total)
- GPU temperature
- Multiple GPUs supported

**Requirements:**
- Appropriate GPU drivers installed
- Python GPU library installed

**Example Output:**
```
[GPU INFORMATION]
--------------------------------------------------------------------------------
 GPU 0: NVIDIA GeForce RTX 3080 (NVIDIA)
 Usage: 25.0%
 Memory: 3.20 GB / 10.00 GB (32.0%)
 Temperature: 55.0C
 Statistics (GPU 0): Min=8.0% | Avg=22.5% | Max=95.0%
```

**No GPU Detected:**
```
[GPU INFORMATION]
--------------------------------------------------------------------------------
 No GPU detected or drivers not installed
```

### Disk Information

**What is Monitored:**
- All mounted partitions
- Device name and mount point
- Filesystem type
- Total capacity
- Used space
- Free space
- Usage percentage

**Filtered Out:**
- Loop devices
- Snap mounts
- Special filesystems

**Example Output:**
```
[DISK INFORMATION]
--------------------------------------------------------------------------------
 / (dev/nvme0n1p2, ext4)
 Total: 512.00 GB | Used: 256.00 GB | Free: 256.00 GB
 Usage: 50.0%
 --------------------------------------------------------------------------------
 /home (dev/nvme0n1p3, ext4)
 Total: 1024.00 GB | Used: 512.00 GB | Free: 512.00 GB
 Usage: 50.0%
 >> [WARNING] Disk /home at 82.5%
```

### Network Information

**What is Monitored:**
- Cumulative data sent (MB)
- Cumulative data received (MB)
- Packets sent (count)
- Packets received (count)

**Note**: Values are cumulative since system boot, not per-second rates.

**Example Output:**
```
[NETWORK INFORMATION]
--------------------------------------------------------------------------------
 Data Sent: 1024.50 MB (524,288 packets)
 Data Received: 2048.75 MB (1,048,576 packets)
```

### Top Processes

**What is Monitored:**
- Process name
- Process ID (PID)
- CPU usage percentage
- Memory usage percentage

**Sorted By:**
- CPU usage (descending)
- Memory usage (descending)

**Example Output:**
```
[TOP PROCESSES]
--------------------------------------------------------------------------------
 By CPU Usage:
  1. chrome                        PID: 12345    CPU:  15.5%
  2. python                        PID: 23456    CPU:   8.2%
  3. code                          PID: 34567    CPU:   5.1%
  4. firefox                       PID: 45678    CPU:   3.8%
  5. gnome-shell                   PID: 56789    CPU:   2.4%

 By Memory Usage:
  1. chrome                        PID: 12345    MEM:  12.5%
  2. code                          PID: 34567    MEM:   8.3%
  3. firefox                       PID: 45678    MEM:   6.1%
  4. python                        PID: 23456    MEM:   4.2%
  5. gnome-shell                   PID: 56789    MEM:   3.8%
```

---

## Configuration Examples

### Example 1: Basic Monitoring
```bash
python hms_improved.py
```
**Use Case**: Quick system check with default settings

### Example 2: Fast Refresh for Performance Testing
```bash
python hms_improved.py --refresh 0.5
```
**Use Case**: Testing performance under load, need rapid updates

### Example 3: Long-Term Server Monitoring
```bash
python hms_improved.py --refresh 5 --log --log-file /var/log/hms.csv
```
**Use Case**: Production server monitoring with logging for analysis

### Example 4: Development Workstation
```bash
python hms_improved.py --refresh 2 --processes 10
```
**Use Case**: Track resource usage during development with more process details

### Example 5: High-Resource Environment
```bash
python hms_improved.py --cpu-warn 60 --cpu-crit 75 --mem-warn 70 --mem-crit 85
```
**Use Case**: Lower thresholds for early warnings in resource-constrained systems

### Example 6: Gaming PC Monitoring
```bash
python hms_improved.py --refresh 1 --gpu-warn 75 --gpu-crit 85
```
**Use Case**: Monitor GPU performance during gaming sessions

### Example 7: Minimal Overhead Monitoring
```bash
python hms_improved.py --refresh 10 --processes 3
```
**Use Case**: Monitor with minimal impact on system performance

### Example 8: Comprehensive Logging
```bash
python hms_improved.py --refresh 1 --log --processes 10 --cpu-warn 70 --mem-warn 70 --gpu-warn 70
```
**Use Case**: Detailed monitoring with logging and sensitive thresholds

---

## Data Logging

### Enabling Logging

```bash
python hms_improved.py --log
```

Default log file: `hms_log.csv` in current directory

### Custom Log Location

```bash
python hms_improved.py --log --log-file /path/to/custom_log.csv
```

### CSV Format

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | Date and time | 2026-05-07 14:35:22 |
| CPU_Usage_% | CPU utilization | 45.2 |
| Memory_Usage_% | Memory utilization | 62.8 |
| GPU_Usage_% | GPU utilization | 32.5 |
| Disk_Usage_% | Average disk utilization | 55.0 |
| CPU_Temp_C | CPU temperature | 52.0 |
| GPU_Temp_C | GPU temperature | 65.0 |
| Network_Sent_MB | Cumulative MB sent | 1024.50 |
| Network_Recv_MB | Cumulative MB received | 2048.75 |

### Log File Example

```csv
Timestamp,CPU_Usage_%,Memory_Usage_%,GPU_Usage_%,Disk_Usage_%,CPU_Temp_C,GPU_Temp_C,Network_Sent_MB,Network_Recv_MB
2026-05-07 14:35:22,45.2,62.8,32.5,55.0,52.0,65.0,1024.50,2048.75
2026-05-07 14:35:23,46.1,63.0,33.2,55.0,52.5,65.5,1024.55,2048.82
2026-05-07 14:35:24,44.8,62.5,31.8,55.0,51.8,65.2,1024.60,2048.90
```

### Analyzing Log Data

**Using Python:**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Read log file
df = pd.read_csv('hms_log.csv', parse_dates=['Timestamp'])

# Plot CPU usage over time
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['CPU_Usage_%'])
plt.title('CPU Usage Over Time')
plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.grid(True)
plt.show()
```

**Using Excel:**
1. Open log file in Excel
2. Select data range
3. Insert → Chart → Line Chart
4. Analyze trends and patterns

---

## Output Format

### Complete Display Example

```
================================================================================
                         HARDWARE MONITORING SYSTEM
================================================================================
 System: Linux 5.15.0-91-generic
 Hostname: workstation-dev
 Uptime: 2 days, 5:30:15
 Monitoring started: 2026-05-07 14:30:00
================================================================================

[CPU INFORMATION]
--------------------------------------------------------------------------------
 Model: AMD Ryzen 9 5950X 16-Core Processor
 Cores: 16 Physical, 32 Logical
 Frequency: 3400 MHz
 Temperature: 45.0C
 Usage: 35.2%
 Statistics: Min=12.5% | Avg=32.8% | Max=85.3%

[MEMORY INFORMATION]
--------------------------------------------------------------------------------
 Total: 64.00 GB
 Used: 28.50 GB
 Available: 35.50 GB
 Usage: 44.5%
 Swap: 0.00 GB / 8.00 GB (0.0%)
 Statistics: Min=35.2% | Avg=42.1% | Max=68.9%

[GPU INFORMATION]
--------------------------------------------------------------------------------
 GPU 0: NVIDIA GeForce RTX 3080 (NVIDIA)
 Usage: 25.0%
 Memory: 3.20 GB / 10.00 GB (32.0%)
 Temperature: 55.0C
 Statistics (GPU 0): Min=8.0% | Avg=22.5% | Max=95.0%

[DISK INFORMATION]
--------------------------------------------------------------------------------
 / (dev/nvme0n1p2, ext4)
 Total: 512.00 GB | Used: 256.00 GB | Free: 256.00 GB
 Usage: 50.0%

[NETWORK INFORMATION]
--------------------------------------------------------------------------------
 Data Sent: 1024.50 MB (524,288 packets)
 Data Received: 2048.75 MB (1,048,576 packets)

[TOP PROCESSES]
--------------------------------------------------------------------------------
 By CPU Usage:
  1. chrome                        PID: 12345    CPU:  15.5%
  2. python                        PID: 23456    CPU:   8.2%
  3. code                          PID: 34567    CPU:   5.1%
  4. firefox                       PID: 45678    CPU:   3.8%
  5. gnome-shell                   PID: 56789    CPU:   2.4%

 By Memory Usage:
  1. chrome                        PID: 12345    MEM:  12.5%
  2. code                          PID: 34567    MEM:   8.3%
  3. firefox                       PID: 45678    MEM:   6.1%
  4. python                        PID: 23456    MEM:   4.2%
  5. gnome-shell                   PID: 56789    MEM:   3.8%

================================================================================
 Last Updated: 2026-05-07 14:35:22
 Logging to: hms_log.csv
 Press Ctrl+C to exit
================================================================================
```

### Alert Display Examples

**Warning Alert:**
```
[CPU INFORMATION]
--------------------------------------------------------------------------------
 Model: Intel Core i7-9700K
 Cores: 8 Physical, 8 Logical
 Usage: 85.0%
 >> [WARNING] CPU at 85.0%
```

**Critical Alert:**
```
[MEMORY INFORMATION]
--------------------------------------------------------------------------------
 Total: 16.00 GB
 Used: 15.20 GB
 Available: 0.80 GB
 Usage: 95.0%
 >> [CRITICAL] Memory at 95.0%
```

---

## Platform-Specific Notes

### Linux

**Advantages:**
- Full temperature monitoring support
- Most reliable CPU detection
- Best overall feature support
- Access to /proc/cpuinfo

**Setup Temperature Monitoring:**
```bash
# Install lm-sensors
sudo apt-get install lm-sensors  # Debian/Ubuntu
sudo yum install lm_sensors      # RedHat/CentOS

# Detect sensors
sudo sensors-detect

# Test
sensors
```

**Permissions:**
- Most features work without root
- Temperature monitoring may need lm-sensors
- Some disk operations may need elevated privileges

### Windows

**Advantages:**
- Full GPU support with proper drivers
- Native WMIC support for CPU detection

**Limitations:**
- Limited temperature monitoring
- No native sensors support

**Setup:**
```bash
# Install Python
# Download from python.org

# Install psutil
pip install psutil

# Optional: Install GPU libraries
pip install nvidia-ml-py3  # For NVIDIA GPUs
pip install gputil         # For AMD GPUs
```

**Run as Administrator (if needed):**
- Right-click Command Prompt
- Select "Run as Administrator"
- Navigate to HMS directory
- Run the script

### macOS

**Advantages:**
- Reliable CPU and memory monitoring
- Clean terminal output

**Limitations:**
- Limited temperature monitoring
- GPU detection varies by hardware

**Setup:**
```bash
# Install Python (if not present)
brew install python3

# Install dependencies
pip3 install psutil py-cpuinfo

# Run the monitor
python3 hms_improved.py
```

---

## Troubleshooting

### Problem: "No GPU detected"

**Possible Causes:**
1. GPU drivers not installed
2. GPU library not installed
3. Unsupported GPU vendor

**Solutions:**
```bash
# For NVIDIA GPUs
pip install nvidia-ml-py3

# For AMD GPUs
pip install gputil

# Verify drivers
# Linux:
nvidia-smi  # For NVIDIA
# Windows:
# Check Device Manager
```

### Problem: "Unknown CPU"

**Cause**: Limited CPU identification methods available

**Solutions:**
```bash
# Install py-cpuinfo
pip install py-cpuinfo

# Verify installation
python -c "import cpuinfo; print(cpuinfo.get_cpu_info()['brand_raw'])"
```

### Problem: Temperature shows "N/A"

**Platform-Specific Solutions:**

**Linux:**
```bash
# Install sensors
sudo apt-get install lm-sensors
sudo sensors-detect
sensors
```

**Windows:**
- Limited native support
- Temperature monitoring often unavailable

**macOS:**
- Limited native support
- Consider third-party tools for temperature

### Problem: Permission Errors

**Linux:**
```bash
# Run without sudo first
python hms_improved.py

# If needed, run with sudo
sudo python hms_improved.py

# Or fix permissions for specific files
sudo chown $USER:$USER /path/to/hms_improved.py
```

**Windows:**
- Run Command Prompt as Administrator

### Problem: High CPU Usage from HMS

**Solutions:**
```bash
# Increase refresh rate
python hms_improved.py --refresh 5

# Reduce process count
python hms_improved.py --processes 3

# Both
python hms_improved.py --refresh 5 --processes 3
```

### Problem: Log File Not Created

**Checks:**
```bash
# Verify write permissions
touch hms_log.csv

# Use absolute path
python hms_improved.py --log --log-file /home/user/hms_log.csv

# Check if logging is enabled
python hms_improved.py --log  # Don't forget the --log flag!
```

### Problem: Script Crashes on Start

**Debug:**
```bash
# Run with Python directly
python -u hms_improved.py

# Check for missing dependencies
pip list | grep psutil

# Reinstall psutil
pip uninstall psutil
pip install psutil
```

---

## Performance Considerations

### System Overhead

**Typical Resource Usage:**
- CPU: <1% on modern systems
- Memory: 20-50 MB
- Disk I/O: Minimal (logging only)
- Network: None

### Optimization Tips

**Reduce Overhead:**
```bash
# Slower refresh rate
python hms_improved.py --refresh 5

# Fewer processes tracked
python hms_improved.py --processes 3

# Disable logging (if enabled)
# Don't use --log flag
```

**Balance Performance vs Detail:**
```bash
# Balanced configuration
python hms_improved.py --refresh 2 --processes 5
```

### Refresh Rate Guidelines

| Refresh Rate | Use Case | CPU Impact |
|--------------|----------|------------|
| 0.1 - 0.5s | Performance testing, debugging | Higher |
| 1.0 - 2.0s | General monitoring, development | Low |
| 3.0 - 5.0s | Server monitoring, dashboards | Minimal |
| 10.0s+ | Long-term logging, low priority | Negligible |

---

## Comparison with Original

### Feature Comparison Table

| Feature | Original HMS | Improved HMS |
|---------|-------------|--------------|
| **Platform Support** | Windows only (`cls`) | Cross-platform (Windows, Linux, macOS) |
| **CPU Detection** | Single method | 4 fallback methods |
| **GPU Support** | Single GPU only | Multi-GPU support |
| **GPU Vendors** | NVIDIA, AMD | NVIDIA, AMD (better detection) |
| **Disk Monitoring** | Not available | All partitions monitored |
| **Network Statistics** | Not available | Full network I/O tracking |
| **Temperature** | Not available | CPU & GPU (where supported) |
| **Statistics** | Not available | Min/Max/Avg tracking (60s window) |
| **Process Monitoring** | Not available | Top N by CPU/Memory |
| **Data Logging** | Not available | Optional CSV logging |
| **Configuration** | Hard-coded values | 12+ command-line arguments |
| **Thresholds** | Fixed at 80/90% | Fully configurable per component |
| **Uptime Display** | Not available | System uptime shown |
| **Session Tracking** | Not available | Session duration tracked |
| **Error Handling** | Basic try-catch | Comprehensive with graceful degradation |
| **Code Structure** | Procedural | Object-oriented (SystemMonitor class) |
| **Documentation** | Minimal | Comprehensive with examples |
| **Lines of Code** | ~180 | ~650 (with extensive features) |

### Migration from Original

**Original Command:**
```bash
python hms.py
```

**Equivalent New Command:**
```bash
python hms_improved.py
```

**Migrating Custom Thresholds:**

If you modified the original script's constants:
```python
# Original (in code)
CPU_WARNING = 75
CPU_CRITICAL = 85
```

New approach (command-line):
```bash
python hms_improved.py --cpu-warn 75 --cpu-crit 85
```

---

## Advanced Usage

### Continuous Monitoring with Auto-Restart

**Linux/macOS (systemd service):**
```bash
# Create service file
sudo nano /etc/systemd/system/hms.service
```

```ini
[Unit]
Description=Hardware Monitoring System
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/hms
ExecStart=/usr/bin/python3 /path/to/hms/hms_improved.py --refresh 5 --log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable hms
sudo systemctl start hms
sudo systemctl status hms
```

### Monitoring Remote Systems via SSH

```bash
ssh user@remote-server 'python3 /path/to/hms_improved.py'
```

### Integration with Monitoring Systems

**Export to Prometheus:**
- Parse CSV logs
- Use node_exporter for system metrics
- Create custom exporter for HMS data

**Send to InfluxDB:**
```python
# Modify log_data() method to send to InfluxDB
from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
# Write metrics to InfluxDB
```

### Scripted Alerting

```bash
# Monitor and alert on high CPU
python hms_improved.py --cpu-crit 70 > /tmp/hms_output.txt &
PID=$!

# Check for CRITICAL in output
while kill -0 $PID 2>/dev/null; do
    if grep -q "CRITICAL" /tmp/hms_output.txt; then
        echo "Alert: Critical threshold exceeded!" | mail -s "HMS Alert" admin@example.com
    fi
    sleep 60
done
```

### Custom Thresholds by Use Case

**Gaming PC:**
```bash
# GPU-focused monitoring
python hms_improved.py --gpu-warn 70 --gpu-crit 80 --refresh 1
```

**Web Server:**
```bash
# Memory and disk focused
python hms_improved.py --mem-warn 70 --disk-warn 75 --refresh 5 --log
```

**Development Workstation:**
```bash
# Balanced with process details
python hms_improved.py --processes 15 --refresh 2
```

**Render Farm Node:**
```bash
# All resources monitored closely
python hms_improved.py --cpu-warn 60 --gpu-warn 60 --refresh 1 --log
```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and small
- Handle errors gracefully

---

## License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Support

### For Academic Inquiries
- **Institution**: Batangas State University - JPLPC Malvar Campus
- **Course**: BSIT

### For Technical Support
- Open an issue on GitHub
- Contact: markdroeidmendoza@gmail.com

---

## Acknowledgments

- **psutil** developers for the excellent cross-platform system monitoring library
- **py-cpuinfo** contributors for reliable CPU identification
- **NVIDIA** and **AMD** for GPU monitoring APIs
- All contributors and users who provide feedback and improvements

---

## Quick Reference Card

```
================================================================================
                   HARDWARE MONITORING SYSTEM - QUICK REFERENCE
================================================================================

BASIC USAGE:
    python hms_improved.py                    # Default monitoring

COMMON OPTIONS:
    --refresh <seconds>      # Update interval (default: 1.0)
    --processes <count>      # Number of processes to show (default: 5)
    --log                    # Enable CSV logging
    --log-file <path>        # Specify log file location

THRESHOLD CONFIGURATION:
    --cpu-warn <percent>     # CPU warning level (default: 80)
    --cpu-crit <percent>     # CPU critical level (default: 90)
    --mem-warn <percent>     # Memory warning level (default: 80)
    --mem-crit <percent>     # Memory critical level (default: 90)
    --gpu-warn <percent>     # GPU warning level (default: 80)
    --gpu-crit <percent>     # GPU critical level (default: 90)
    --disk-warn <percent>    # Disk warning level (default: 80)
    --disk-crit <percent>    # Disk critical level (default: 90)

EXAMPLES:
    python hms_improved.py --refresh 2 --processes 10
    python hms_improved.py --log --log-file /var/log/hms.csv
    python hms_improved.py --cpu-warn 70 --mem-warn 75 --refresh 5

EXIT:
    Press Ctrl+C to stop monitoring

MONITORED COMPONENTS:
    • CPU: Usage, frequency, cores, temperature
    • Memory: Total, used, available, swap
    • GPU: Usage, memory, temperature (NVIDIA/AMD)
    • Disk: All partitions with usage
    • Network: Data sent/received, packets
    • Processes: Top N by CPU and memory

ALERT LEVELS:
    [WARNING]  - Component at warning threshold
    [CRITICAL] - Component at critical threshold

================================================================================
```

<div align="center">

**Built with Python and psutil**

*Professional system monitoring made simple*

[Report Bug](https://github.com/yourusername/hms/issues) • [Request Feature](https://github.com/yourusername/hms/issues) • [Documentation](https://github.com/yourusername/hms/wiki)

</div>

---

## Star This Repository

If HMS has been useful for your system monitoring needs, please consider giving it a star on GitHub. It helps others discover the project and motivates continued development.

**Happy Monitoring!**

---

*Last Updated: May 2026*
*Version: 2.0.0*
