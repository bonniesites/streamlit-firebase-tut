scores = {
    
        "macaco": 1545, 
        "white_hat_lady": 5810, 
        "CECyber": 0, 
        "cyberstriker": 7240, 
        "CyJens": 15, 
        "Gabriellopes": 160, 
        "graystevo": 6280, 
        "LightZ": 1665, 
        "martab": 140,  
        "MrRootbot": 15, 
        "patkilo": 5, 
        "primaryanna": 345
}


# def print_high_scores(leaderboard):
#     # Sort the dictionary by points in descending order
#     sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

#     # Find the longest username for alignment
#     max_username_length = max(len(user) for user, user[1] in sorted_leaderboard)

#     # Print the sorted leaderboard in two columns with usernames aligned left and points aligned right
#     print("\n\n")
#     for user in sorted_leaderboard:
#         print(f"  {user}  {str(points).rjust(5)}")
#     print("\n\n")

def print_leaderboard(scores):
    # Sort the dictionary by points in descending order
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Find the longest name for formatting
    longest_name_length = max(len(name) for name in scores.keys())
    
    # Print the leaderboard
    print("\n\npicoCTF Leaderboard:\n")
    for name, points in sorted_scores:
        print(f"{name.ljust(longest_name_length)} : {points}")

# Use the function
# print_high_scores(scores) 
print_leaderboard(scores)
print('\n\n')