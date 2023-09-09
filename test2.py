def find_longest_string(iterable):
    # Initialize variables to store the longest string and its length
    longest_string = ""
    max_length = 0

    # Iterate through the iterable
    for s in iterable:
        # Check if the current string is longer than the previously found longest string
        if len(s) > max_length:
            longest_string = s
            max_length = len(s)

    return longest_string

# Example usage:
my_iterable = ["read_messages", "block_channel", "read_channel_history", "connect_voice"]
longest = find_longest_string(my_iterable)
print("Longest string:", longest)
