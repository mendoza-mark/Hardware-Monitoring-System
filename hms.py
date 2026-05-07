#!/usr/bin/env python3
"""
Hardware Monitoring System (HMS)
Advanced system monitoring tool for CPU, Memory, GPU, Disk, and Network
"""

import psutil
import time
import os
import platform
import argparse
import sys
from datetime import datetime, timedelta
from collections import deque
import csv

# Optional imports with graceful fallbacks
try:
    import cpuinfo
    CPUINFO_AVAILABLE = True
except ImportError:
    CPUINFO_AVAILABLE = False

try:
    from pynvml import *
    nvmlInit()
    NVIDIA_AVAILABLE = True
except:
    NVIDIA_AVAILABLE = False

try:
    import GPUtil
    AMD_AVAILABLE = True
except ImportError:
    AMD_AVAILABLE = False

# Default configuration
DEFAULT_CONFIG = {
    'cpu_warning': 80,
    'cpu_critical': 90,
    'memory_warning': 80,
    'memory_critical': 90,
    'gpu_warning': 80,
    'gpu_critical': 90,
    'disk_warning': 80,
    'disk_critical': 90,
    'refresh_rate': 1.0,
    'show_processes': 5,
    'enable_logging': False,
    'log_file': 'hms_log.csv'
}


class SystemMonitor:
    """Main system monitoring class with cross-platform support"""
    
    def __init__(self, config=None):
        self.config = config or DEFAULT_CONFIG.copy()
        self.stats_history = {
            'cpu': deque(maxlen=60),
            'memory': deque(maxlen=60),
            'gpu': deque(maxlen=60)
        }
        self.start_time = time.time()
        self.log_enabled = self.config.get('enable_logging', False)
        self.log_file = self.config.get('log_file', 'hms_log.csv')
        
        if self.log_enabled:
            self._initialize_log()
    
    def _initialize_log(self):
        """Initialize CSV log file with headers"""
        try:
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp', 'CPU_Usage_%', 'Memory_Usage_%', 
                    'GPU_Usage_%', 'Disk_Usage_%', 'CPU_Temp_C', 
                    'GPU_Temp_C', 'Network_Sent_MB', 'Network_Recv_MB'
                ])
        except Exception as e:
            print(f"Warning: Could not initialize log file: {e}")
            self.log_enabled = False
    
    def clear_screen(self):
        """Cross-platform screen clearing"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_cpu_info(self):
        """Get CPU information with multiple fallback methods"""
        cpu_name = None
        
        # Method 1: cpuinfo library (most reliable)
        if CPUINFO_AVAILABLE:
            try:
                info = cpuinfo.get_cpu_info()
                cpu_name = info.get('brand_raw') or info.get('brand')
            except Exception:
                pass
        
        # Method 2: platform.processor()
        if not cpu_name:
            try:
                cpu_name = platform.processor()
            except Exception:
                pass
        
        # Method 3: /proc/cpuinfo on Linux
        if not cpu_name and platform.system() == 'Linux':
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            cpu_name = line.split(':')[1].strip()
                            break
            except Exception:
                pass
        
        # Method 4: wmic on Windows
        if not cpu_name and platform.system() == 'Windows':
            try:
                import subprocess
                result = subprocess.check_output(
                    ['wmic', 'cpu', 'get', 'name'], 
                    encoding='utf-8'
                )
                lines = result.strip().split('\n')
                if len(lines) > 1:
                    cpu_name = lines[1].strip()
            except Exception:
                pass
        
        # Fallback
        if not cpu_name or cpu_name.strip() == '':
            cpu_name = f"{platform.machine()} Processor"
        
        # Get core count
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
        
        return cpu_name, physical_cores, logical_cores
    
    def get_cpu_usage(self):
        """Get detailed CPU usage information"""
        cpu_percent = psutil.cpu_percent(interval=0.5)
        per_cpu = psutil.cpu_percent(interval=0, percpu=True)
        cpu_freq = psutil.cpu_freq()
        
        return {
            'percent': cpu_percent,
            'per_cpu': per_cpu,
            'frequency': cpu_freq.current if cpu_freq else None,
            'max_frequency': cpu_freq.max if cpu_freq else None
        }
    
    def get_cpu_temperature(self):
        """Get CPU temperature (Linux only, requires sensors)"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Try common sensor names
                for name in ['coretemp', 'k10temp', 'cpu_thermal', 'cpu-thermal']:
                    if name in temps:
                        entries = temps[name]
                        if entries:
                            return entries[0].current
                
                # Return first available temperature
                for sensor_list in temps.values():
                    if sensor_list:
                        return sensor_list[0].current
        except (AttributeError, Exception):
            pass
        return None
    
    def get_memory_info(self):
        """Get memory usage information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_gb': mem.total / (1024 ** 3),
            'used_gb': mem.used / (1024 ** 3),
            'available_gb': mem.available / (1024 ** 3),
            'percent': mem.percent,
            'swap_total_gb': swap.total / (1024 ** 3),
            'swap_used_gb': swap.used / (1024 ** 3),
            'swap_percent': swap.percent
        }
    
    def get_gpu_info(self):
        """Get GPU information with support for multiple vendors"""
        gpus = []
        
        # NVIDIA GPUs
        if NVIDIA_AVAILABLE:
            try:
                device_count = nvmlDeviceGetCount()
                for i in range(device_count):
                    handle = nvmlDeviceGetHandleByIndex(i)
                    name = nvmlDeviceGetName(handle)
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    
                    utilization = nvmlDeviceGetUtilizationRates(handle)
                    memory_info = nvmlDeviceGetMemoryInfo(handle)
                    
                    # Try to get temperature
                    try:
                        temperature = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
                    except:
                        temperature = None
                    
                    gpus.append({
                        'index': i,
                        'name': name,
                        'vendor': 'NVIDIA',
                        'usage_percent': utilization.gpu,
                        'memory_used_gb': memory_info.used / (1024 ** 3),
                        'memory_total_gb': memory_info.total / (1024 ** 3),
                        'memory_percent': (memory_info.used / memory_info.total) * 100,
                        'temperature': temperature
                    })
            except Exception as e:
                pass
        
        # AMD GPUs
        if AMD_AVAILABLE and len(gpus) == 0:
            try:
                amd_gpus = GPUtil.getGPUs()
                for i, gpu in enumerate(amd_gpus):
                    gpus.append({
                        'index': i,
                        'name': gpu.name,
                        'vendor': 'AMD',
                        'usage_percent': gpu.load * 100,
                        'memory_used_gb': gpu.memoryUsed / 1024,
                        'memory_total_gb': gpu.memoryTotal / 1024,
                        'memory_percent': gpu.memoryUtil * 100,
                        'temperature': gpu.temperature if hasattr(gpu, 'temperature') else None
                    })
            except Exception:
                pass
        
        return gpus if gpus else None
    
    def get_disk_info(self):
        """Get disk usage information for all partitions"""
        disks = []
        
        for partition in psutil.disk_partitions():
            # Skip special filesystems
            if 'loop' in partition.device or 'snap' in partition.mountpoint:
                continue
            
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total_gb': usage.total / (1024 ** 3),
                    'used_gb': usage.used / (1024 ** 3),
                    'free_gb': usage.free / (1024 ** 3),
                    'percent': usage.percent
                })
            except (PermissionError, OSError):
                continue
        
        return disks
    
    def get_network_info(self):
        """Get network I/O statistics"""
        net_io = psutil.net_io_counters()
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'mb_sent': net_io.bytes_sent / (1024 ** 2),
            'mb_recv': net_io.bytes_recv / (1024 ** 2),
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    
    def get_top_processes(self, count=5, sort_by='cpu'):
        """Get top processes by CPU or memory usage"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'cpu_percent': info['cpu_percent'] or 0,
                    'memory_percent': info['memory_percent'] or 0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by specified metric
        if sort_by == 'cpu':
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        else:
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        
        return processes[:count]
    
    def get_uptime(self):
        """Get system uptime"""
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        return timedelta(seconds=int(uptime_seconds))
    
    def get_warning_status(self, value, component, warning_threshold, critical_threshold):
        """Generate warning status for a component"""
        if value is None:
            return None
        
        if value >= critical_threshold:
            return f"[CRITICAL] {component} at {value:.1f}%"
        elif value >= warning_threshold:
            return f"[WARNING] {component} at {value:.1f}%"
        return None
    
    def update_statistics(self, cpu, memory, gpu):
        """Update rolling statistics"""
        self.stats_history['cpu'].append(cpu)
        self.stats_history['memory'].append(memory)
        if gpu is not None:
            self.stats_history['gpu'].append(gpu)
    
    def get_statistics(self, metric):
        """Get min/max/avg statistics for a metric"""
        data = list(self.stats_history[metric])
        if not data:
            return None, None, None
        
        return min(data), max(data), sum(data) / len(data)
    
    def log_data(self, cpu_usage, mem_usage, gpu_usage, disk_usage, cpu_temp, gpu_temp, net_info):
        """Log data to CSV file"""
        if not self.log_enabled:
            return
        
        try:
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    f"{cpu_usage:.1f}",
                    f"{mem_usage:.1f}",
                    f"{gpu_usage:.1f}" if gpu_usage else "N/A",
                    f"{disk_usage:.1f}" if disk_usage else "N/A",
                    f"{cpu_temp:.1f}" if cpu_temp else "N/A",
                    f"{gpu_temp:.1f}" if gpu_temp else "N/A",
                    f"{net_info['mb_sent']:.2f}",
                    f"{net_info['mb_recv']:.2f}"
                ])
        except Exception:
            pass
    
    def format_header(self):
        """Format the header section"""
        uptime = self.get_uptime()
        lines = []
        lines.append("=" * 80)
        lines.append(" " * 25 + "HARDWARE MONITORING SYSTEM")
        lines.append("=" * 80)
        lines.append(f" System: {platform.system()} {platform.release()}")
        lines.append(f" Hostname: {platform.node()}")
        lines.append(f" Uptime: {uptime}")
        lines.append(f" Monitoring started: {datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        return "\n".join(lines)
    
    def format_cpu_section(self, cpu_info_name, physical_cores, logical_cores, cpu_usage_data, cpu_temp):
        """Format CPU section"""
        lines = []
        lines.append("\n[CPU INFORMATION]")
        lines.append("-" * 80)
        lines.append(f" Model: {cpu_info_name}")
        lines.append(f" Cores: {physical_cores} Physical, {logical_cores} Logical")
        
        if cpu_usage_data['frequency']:
            lines.append(f" Frequency: {cpu_usage_data['frequency']:.0f} MHz")
        
        if cpu_temp:
            lines.append(f" Temperature: {cpu_temp:.1f}C")
        
        lines.append(f" Usage: {cpu_usage_data['percent']:.1f}%")
        
        # Get statistics
        cpu_min, cpu_max, cpu_avg = self.get_statistics('cpu')
        if cpu_min is not None:
            lines.append(f" Statistics: Min={cpu_min:.1f}% | Avg={cpu_avg:.1f}% | Max={cpu_max:.1f}%")
        
        # Warning status
        warning = self.get_warning_status(
            cpu_usage_data['percent'], 
            "CPU", 
            self.config['cpu_warning'],
            self.config['cpu_critical']
        )
        if warning:
            lines.append(f" >> {warning}")
        
        return "\n".join(lines)
    
    def format_memory_section(self, mem_info):
        """Format memory section"""
        lines = []
        lines.append("\n[MEMORY INFORMATION]")
        lines.append("-" * 80)
        lines.append(f" Total: {mem_info['total_gb']:.2f} GB")
        lines.append(f" Used: {mem_info['used_gb']:.2f} GB")
        lines.append(f" Available: {mem_info['available_gb']:.2f} GB")
        lines.append(f" Usage: {mem_info['percent']:.1f}%")
        
        if mem_info['swap_total_gb'] > 0:
            lines.append(f" Swap: {mem_info['swap_used_gb']:.2f} GB / {mem_info['swap_total_gb']:.2f} GB ({mem_info['swap_percent']:.1f}%)")
        
        # Get statistics
        mem_min, mem_max, mem_avg = self.get_statistics('memory')
        if mem_min is not None:
            lines.append(f" Statistics: Min={mem_min:.1f}% | Avg={mem_avg:.1f}% | Max={mem_max:.1f}%")
        
        # Warning status
        warning = self.get_warning_status(
            mem_info['percent'], 
            "Memory", 
            self.config['memory_warning'],
            self.config['memory_critical']
        )
        if warning:
            lines.append(f" >> {warning}")
        
        return "\n".join(lines)
    
    def format_gpu_section(self, gpus):
        """Format GPU section"""
        lines = []
        lines.append("\n[GPU INFORMATION]")
        lines.append("-" * 80)
        
        if not gpus:
            lines.append(" No GPU detected or drivers not installed")
            return "\n".join(lines)
        
        for gpu in gpus:
            lines.append(f" GPU {gpu['index']}: {gpu['name']} ({gpu['vendor']})")
            lines.append(f" Usage: {gpu['usage_percent']:.1f}%")
            lines.append(f" Memory: {gpu['memory_used_gb']:.2f} GB / {gpu['memory_total_gb']:.2f} GB ({gpu['memory_percent']:.1f}%)")
            
            if gpu['temperature']:
                lines.append(f" Temperature: {gpu['temperature']:.1f}C")
            
            # Warning status
            warning = self.get_warning_status(
                gpu['usage_percent'], 
                f"GPU {gpu['index']}", 
                self.config['gpu_warning'],
                self.config['gpu_critical']
            )
            if warning:
                lines.append(f" >> {warning}")
            
            if len(gpus) > 1 and gpu != gpus[-1]:
                lines.append(" " + "-" * 78)
        
        # Get statistics for first GPU
        if gpus:
            gpu_min, gpu_max, gpu_avg = self.get_statistics('gpu')
            if gpu_min is not None:
                lines.append(f" Statistics (GPU 0): Min={gpu_min:.1f}% | Avg={gpu_avg:.1f}% | Max={gpu_max:.1f}%")
        
        return "\n".join(lines)
    
    def format_disk_section(self, disks):
        """Format disk section"""
        lines = []
        lines.append("\n[DISK INFORMATION]")
        lines.append("-" * 80)
        
        for disk in disks:
            lines.append(f" {disk['mountpoint']} ({disk['device']}, {disk['fstype']})")
            lines.append(f" Total: {disk['total_gb']:.2f} GB | Used: {disk['used_gb']:.2f} GB | Free: {disk['free_gb']:.2f} GB")
            lines.append(f" Usage: {disk['percent']:.1f}%")
            
            # Warning status
            warning = self.get_warning_status(
                disk['percent'], 
                f"Disk {disk['mountpoint']}", 
                self.config['disk_warning'],
                self.config['disk_critical']
            )
            if warning:
                lines.append(f" >> {warning}")
            
            if disk != disks[-1]:
                lines.append(" " + "-" * 78)
        
        return "\n".join(lines)
    
    def format_network_section(self, net_info):
        """Format network section"""
        lines = []
        lines.append("\n[NETWORK INFORMATION]")
        lines.append("-" * 80)
        lines.append(f" Data Sent: {net_info['mb_sent']:.2f} MB ({net_info['packets_sent']:,} packets)")
        lines.append(f" Data Received: {net_info['mb_recv']:.2f} MB ({net_info['packets_recv']:,} packets)")
        return "\n".join(lines)
    
    def format_processes_section(self, top_cpu_procs, top_mem_procs):
        """Format top processes section"""
        lines = []
        lines.append("\n[TOP PROCESSES]")
        lines.append("-" * 80)
        
        lines.append(" By CPU Usage:")
        for i, proc in enumerate(top_cpu_procs, 1):
            lines.append(f"  {i}. {proc['name']:<30} PID: {proc['pid']:<8} CPU: {proc['cpu_percent']:>5.1f}%")
        
        lines.append("\n By Memory Usage:")
        for i, proc in enumerate(top_mem_procs, 1):
            lines.append(f"  {i}. {proc['name']:<30} PID: {proc['pid']:<8} MEM: {proc['memory_percent']:>5.1f}%")
        
        return "\n".join(lines)
    
    def format_footer(self):
        """Format footer"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append(f" Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.log_enabled:
            lines.append(f" Logging to: {self.log_file}")
        lines.append(" Press Ctrl+C to exit")
        lines.append("=" * 80)
        return "\n".join(lines)
    
    def display(self):
        """Main display method"""
        # Gather all information
        cpu_name, physical_cores, logical_cores = self.get_cpu_info()
        cpu_usage_data = self.get_cpu_usage()
        cpu_temp = self.get_cpu_temperature()
        mem_info = self.get_memory_info()
        gpus = self.get_gpu_info()
        disks = self.get_disk_info()
        net_info = self.get_network_info()
        top_cpu_procs = self.get_top_processes(self.config['show_processes'], 'cpu')
        top_mem_procs = self.get_top_processes(self.config['show_processes'], 'memory')
        
        # Update statistics
        gpu_usage_for_stats = gpus[0]['usage_percent'] if gpus else None
        self.update_statistics(cpu_usage_data['percent'], mem_info['percent'], gpu_usage_for_stats)
        
        # Log data if enabled
        disk_avg = sum(d['percent'] for d in disks) / len(disks) if disks else None
        gpu_temp = gpus[0]['temperature'] if gpus and gpus[0]['temperature'] else None
        self.log_data(
            cpu_usage_data['percent'], 
            mem_info['percent'], 
            gpu_usage_for_stats,
            disk_avg,
            cpu_temp,
            gpu_temp,
            net_info
        )
        
        # Clear screen and display
        self.clear_screen()
        
        print(self.format_header())
        print(self.format_cpu_section(cpu_name, physical_cores, logical_cores, cpu_usage_data, cpu_temp))
        print(self.format_memory_section(mem_info))
        print(self.format_gpu_section(gpus))
        print(self.format_disk_section(disks))
        print(self.format_network_section(net_info))
        print(self.format_processes_section(top_cpu_procs, top_mem_procs))
        print(self.format_footer())
    
    def run(self):
        """Main monitoring loop"""
        try:
            while True:
                self.display()
                time.sleep(self.config['refresh_rate'])
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user.")
            print(f"Session duration: {timedelta(seconds=int(time.time() - self.start_time))}")
            if self.log_enabled:
                print(f"Data logged to: {self.log_file}")
            sys.exit(0)


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Hardware Monitoring System - Monitor CPU, Memory, GPU, Disk, and Network',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hms_improved.py                    # Run with default settings
  python hms_improved.py --refresh 2        # Update every 2 seconds
  python hms_improved.py --log              # Enable logging to CSV
  python hms_improved.py --processes 10     # Show top 10 processes
  python hms_improved.py --cpu-warn 70      # Set CPU warning threshold to 70%
        """
    )
    
    parser.add_argument(
        '--refresh', 
        type=float, 
        default=1.0,
        help='Refresh rate in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--processes', 
        type=int, 
        default=5,
        help='Number of top processes to show (default: 5)'
    )
    
    parser.add_argument(
        '--cpu-warn', 
        type=int, 
        default=80,
        help='CPU warning threshold percentage (default: 80)'
    )
    
    parser.add_argument(
        '--cpu-crit', 
        type=int, 
        default=90,
        help='CPU critical threshold percentage (default: 90)'
    )
    
    parser.add_argument(
        '--mem-warn', 
        type=int, 
        default=80,
        help='Memory warning threshold percentage (default: 80)'
    )
    
    parser.add_argument(
        '--mem-crit', 
        type=int, 
        default=90,
        help='Memory critical threshold percentage (default: 90)'
    )
    
    parser.add_argument(
        '--gpu-warn', 
        type=int, 
        default=80,
        help='GPU warning threshold percentage (default: 80)'
    )
    
    parser.add_argument(
        '--gpu-crit', 
        type=int, 
        default=90,
        help='GPU critical threshold percentage (default: 90)'
    )
    
    parser.add_argument(
        '--disk-warn', 
        type=int, 
        default=80,
        help='Disk warning threshold percentage (default: 80)'
    )
    
    parser.add_argument(
        '--disk-crit', 
        type=int, 
        default=90,
        help='Disk critical threshold percentage (default: 90)'
    )
    
    parser.add_argument(
        '--log', 
        action='store_true',
        help='Enable logging to CSV file'
    )
    
    parser.add_argument(
        '--log-file', 
        type=str, 
        default='hms_log.csv',
        help='Log file path (default: hms_log.csv)'
    )
    
    args = parser.parse_args()
    
    # Build configuration from arguments
    config = {
        'cpu_warning': args.cpu_warn,
        'cpu_critical': args.cpu_crit,
        'memory_warning': args.mem_warn,
        'memory_critical': args.mem_crit,
        'gpu_warning': args.gpu_warn,
        'gpu_critical': args.gpu_crit,
        'disk_warning': args.disk_warn,
        'disk_critical': args.disk_crit,
        'refresh_rate': args.refresh,
        'show_processes': args.processes,
        'enable_logging': args.log,
        'log_file': args.log_file
    }
    
    # Create and run monitor
    monitor = SystemMonitor(config)
    monitor.run()


if __name__ == "__main__":
    main()