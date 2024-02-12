# LIST options: WATCH, LIKE, DISLIKE
add_request = { 'user_ID': 12345, 'LIST': 'WATCH', 'movie_ID': 98765}

# get request just sends user ID
get_request = 12345

return_request = {
    'user_ID': 12345,
    'WATCH': [98765],
    'LIKE': [],
    'DISLIKE': []
}

