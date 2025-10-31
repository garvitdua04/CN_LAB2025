try:
    from ip_utils import ip_to_binary, get_network_prefix
except ImportError:
    print("Error: Could not import from ip_utils.py.")
    print("Make sure ip_utils.py is in the same directory.")
    exit(1)

class Router:

    def __init__(self, routes: list):

        # self.forwarding_table will store tuples of:
        # (binary_prefix, prefix_length, output_link)
        self.forwarding_table = self.__build_forwarding_table(routes)

    def __build_forwarding_table(self, routes: list) -> list:

        processed_table = []
        for cidr, output_link in routes:
            # Get the binary prefix from the CIDR string
            binary_prefix = get_network_prefix(cidr)
            # Get the length of the prefix
            prefix_length = len(binary_prefix)
            # Store the prefix, its length, and the link
            processed_table.append((binary_prefix, prefix_length, output_link))
        
        # Sort the table by prefix length (index 1) in descending order
        # This is the crucial step for the Longest Prefix Match algorithm
        processed_table.sort(key=lambda item: item[1], reverse=True)
        
        print("--- Built and Sorted Forwarding Table (Longest to Shortest) ---")
        for prefix, length, link in processed_table:
            print(f"  Prefix: {prefix:<32} (/{length}) -> {link}")
        print("-" * 60)
        
        return processed_table

    def route_packet(self, dest_ip: str) -> str:

        # (a) Convert the destination IP to 32-bit binary
        binary_dest_ip = ip_to_binary(dest_ip)
        
        # (b) Iterate through the sorted forwarding table
        for binary_prefix, prefix_len, output_link in self.forwarding_table:
            
            # (c) Check if the binary destination IP starts with the binary prefix
            if binary_dest_ip.startswith(binary_prefix):
                # (d) First match is the longest match (due to sorting)
                return output_link
                
        # (e) If no match is found after checking all routes
        return "Default Gateway"

# --- Main execution for testing ---
if __name__ == "__main__":
    
    # Test Case provided in the assignment
    routes_list = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    
    # 1. Initialize the router
    my_router = Router(routes_list)
    
    # 2. Define test IPs
    test_ips = [
        "223.1.1.100",  # Should match "Link 0"
        "223.1.2.5",    # Should match "Link 1"
        "223.1.250.1",  # Should match "Link 4 (ISP)"
        "198.51.100.1"  # Should match "Default Gateway"
    ]
    
    # 3. Verify the routing
    print("--- Testing Packet Routing ---")
    for ip in test_ips:
        output_link = my_router.route_packet(ip)
        print(f'route_packet("{ip}") -> {output_link}')

    # Verification checks
    assert my_router.route_packet("223.1.1.100") == "Link 0"
    assert my_router.route_packet("223.1.2.5") == "Link 1"
    assert my_router.route_packet("223.1.250.1") == "Link 4 (ISP)"
    assert my_router.route_packet("198.51.100.1") == "Default Gateway"
    
    print("\n--- All Test Cases Passed ---")