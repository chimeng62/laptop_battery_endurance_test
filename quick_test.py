from utils.process_manager import ProcessManager
import time

print('Testing process tracking with notepad...')
pm = ProcessManager()

# Test launching and tracking notepad
pid = pm.launch_and_track(['notepad.exe'], 'Test Notepad')
if pid:
    print(f'✅ Successfully launched and tracked notepad (PID: {pid})')
    time.sleep(1)
    
    # Show tracked processes
    processes = pm.get_tracked_processes_info()
    for proc in processes:
        print(f'  Tracked: {proc["name"]} (PID: {proc["pid"]}) Memory: {proc["memory_mb"]:.1f}MB')
    
    # Terminate
    terminated = pm.cleanup_all_tracked(force_kill=True)
    print(f'✅ Successfully terminated {terminated} processes')
else:
    print('❌ Failed to launch notepad')

print('✅ Process management test completed!')