def ip_to_binary(ip_address: str) -> str:

    # Split the IP into its four octets
    octets = ip_address.split('.')
    
    # Convert each octet to an 8-bit binary string, padding with leading zeros
    binary_octets = [bin(int(octet))[2:].zfill(8) for octet in octets]
    
    # Join the four 8-bit strings to create the 32-bit string
    return "".join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
    
    # Split the CIDR string into the IP address and the prefix length
    try:
        ip_address, prefix_length_str = ip_cidr.split('/')
        prefix_length = int(prefix_length_str)
    except ValueError:
        raise ValueError("Invalid CIDR format. Expected 'ip/prefix_length'")

    if not (0 <= prefix_length <= 32):
        raise ValueError("Prefix length must be between 0 and 32")

    # Reuse the ip_to_binary function
    binary_ip = ip_to_binary(ip_address)
    
    # Return the prefix portion of the binary IP
    return binary_ip[:prefix_length]

# --- Main execution for testing ---
if __name__ == "__main__":
    print("--- Testing ip_utils.py ---")
    
    # Test ip_to_binary
    test_ip = "192.168.1.1"
    binary_ip = ip_to_binary(test_ip)
    print(f'ip_to_binary("{test_ip}"):\n{binary_ip}')
    print(f'Length: {len(binary_ip)} bits')
    
    test_ip_2 = "200.23.16.0"
    binary_ip_2 = ip_to_binary(test_ip_2)
    print(f'\nip_to_binary("{test_ip_2}"):\n{binary_ip_2}')
    print(f'Length: {len(binary_ip_2)} bits')

    # Test get_network_prefix
    test_cidr = "200.23.16.0/23"
    network_prefix = get_network_prefix(test_cidr)
    print(f'\nget_network_prefix("{test_cidr}"):\n{network_prefix}')
    print(f'Length: {len(network_prefix)} bits')

    test_cidr_2 = "223.1.1.0/24"
    network_prefix_2 = get_network_prefix(test_cidr_2)
    print(f'\nget_network_prefix("{test_cidr_2}"):\n{network_prefix_2}')
    print(f'Length: {len(network_prefix_2)} bits')