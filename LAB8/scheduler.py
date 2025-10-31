from dataclasses import dataclass
from typing import List

# 1. Packet Class
@dataclass
class Packet:
    """
    A simple dataclass to represent a network packet.
    Priority: 0 = High, 1 = Medium, 2 = Low
    """
    source_ip: str
    dest_ip: str
    payload: str
    priority: int

# 2. FIFO Scheduler
def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:

    # For FCFS, the sending order is the same as the arrival order.
    # We return a copy of the list.
    return list(packet_list)

# 3. Priority Scheduler
def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:

    # We can simply sort the list based on the 'priority' attribute.
    # Python's sort is stable, so packets with the same priority
    # will maintain their original relative order.
    return sorted(packet_list, key=lambda packet: packet.priority)

# --- Main execution for testing ---
if __name__ == "__main__":
    
    # Test Case provided in the assignment
    # Create the list of packets in their arrival order
    packets_arrival_order = [
        Packet(source_ip="10.0.0.1", dest_ip="192.168.1.10", payload="Data Packet 1", priority=2),
        Packet(source_ip="10.0.0.2", dest_ip="192.168.1.11", payload="Data Packet 2", priority=2),
        Packet(source_ip="20.0.0.1", dest_ip="192.168.1.12", payload="VOIP Packet 1", priority=0),
        Packet(source_ip="30.0.0.1", dest_ip="192.168.1.13", payload="Video Packet 1", priority=1),
        Packet(source_ip="20.0.0.2", dest_ip="192.168.1.14", payload="VOIP Packet 2", priority=0),
    ]

    print("--- Original Arrival Order (by payload) ---")
    arrival_payloads = [p.payload for p in packets_arrival_order]
    print(arrival_payloads)
    
    # --- Test FIFO Scheduler ---
    print("\n--- Testing FIFO Scheduler ---")
    fifo_result = fifo_scheduler(packets_arrival_order)
    fifo_payloads = [p.payload for p in fifo_result]
    print(fifo_payloads)
    
    # Verification
    expected_fifo = ["Data Packet 1", "Data Packet 2", "VOIP Packet 1", "Video Packet 1", "VOIP Packet 2"]
    assert fifo_payloads == expected_fifo
    print("FIFO Test: Passed")

    # --- Test Priority Scheduler ---
    print("\n--- Testing Priority Scheduler ---")
    priority_result = priority_scheduler(packets_arrival_order)
    priority_payloads = [p.payload for p in priority_result]
    print(priority_payloads)

    # Verification
    expected_priority = ["VOIP Packet 1", "VOIP Packet 2", "Video Packet 1", "Data Packet 1", "Data Packet 2"]
    assert priority_payloads == expected_priority
    print("Priority Test: Passed")