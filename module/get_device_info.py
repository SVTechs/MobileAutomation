import wmi
import os
import yaml

class SystemInfo:
    def __init__(self):
        self.c = wmi.WMI()

    def get_cpu_info(self):
        cpu_info = []
        for cpu in self.c.Win32_Processor():
            cpu_info.append({
                "Name": cpu.Name,
                "Number of Cores": cpu.NumberOfCores,
                "Max Clock Speed": f"{cpu.MaxClockSpeed} MHz",
                "Processor ID": cpu.ProcessorId
            })
        return cpu_info

    def get_memory_info(self):
        memory_info = []
        for memory in self.c.Win32_PhysicalMemory():
            memory_info.append({
                "Capacity": f"{int(memory.Capacity) / (1024**3)} GB",
                "Speed": f"{memory.Speed} MHz",
                "Manufacturer": memory.Manufacturer,
                "Serial Number": memory.SerialNumber
            })
        return memory_info

    def get_disk_info(self):
        disk_info = []
        for disk in self.c.Win32_DiskDrive():
            disk_info.append({
                "Model": disk.Model,
                "Serial Number": disk.SerialNumber,
                "Size": f"{int(disk.Size) / (1024**3)} GB"
            })
        return disk_info

    def get_network_info(self):
        network_info = []
        for nic in self.c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            network_info.append({
                "Description": nic.Description,
                "MAC Address": nic.MACAddress,
                "IP Address": nic.IPAddress
            })
        return network_info

    def get_os_info(self):
        os_info = []
        for os in self.c.Win32_OperatingSystem():
            os_info.append({
                "Name": os.Name,
                "Version": os.Version,
                "Manufacturer": os.Manufacturer,
                "Last Boot Up Time": os.LastBootUpTime
            })
        return os_info

    def get_motherboard_info(self):
        motherboard_info = []
        for board in self.c.Win32_BaseBoard():
            motherboard_info.append({
                "Manufacturer": board.Manufacturer,
                "Product": board.Product,
                "Serial Number": board.SerialNumber if board.SerialNumber else "Not Available"
            })
        return motherboard_info

    def save_device_info_to_file(self, directory, filename="deviceInfo.yaml"):
        filepath = os.path.join(directory, filename).replace('"', '')
        motherboard_info = self.get_motherboard_info()
        memory_info = self.get_memory_info()
        disk_info = self.get_disk_info()

        device_info = {
            "Motherboard": motherboard_info,
            "Memory": memory_info,
            "Disks": disk_info
        }

        with open(filepath, "w") as file:
            yaml.dump(device_info, file, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python get_device_info.py <output_directory>")
        sys.exit(1)

    output_directory = sys.argv[1]
    system_info = SystemInfo()
    system_info.save_device_info_to_file(output_directory)