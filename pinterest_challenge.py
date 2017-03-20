def is_valid_socket(address):
    """Determine if the provided string is a valid socket address.
    This function declaration must be kept unmodified.

    Args:
        address: A string with a socket address, eg, 
            '127.12.23.43:5000', to be checked for validity.
    Returns:
        A boolean indicating whether the provided string is a valid 
        socket address.
    """
    dot = 0
    colon = 0
    temp_sequence = ''
    char = 0
    # We can do this priliminary check that would avoice us to go through the 
    # string address if the string length is smaller than 9 (3 dots, 1 colon, 
    # 1 number for each portion):
    if len(address) < 9:
        return False
    while char < len(address) and dot < 4 and colon < 2:
        if address[char].isdigit():
            temp_sequence += address[char] 
        elif address[char] == '.':
            if int(temp_sequence) < 0 or int(temp_sequence) > 255:
                return False
            temp_sequence = ''
            dot += 1
        elif address[char] == ':' and dot == 3:
            temp_sequence =''
            colon += 1
        else:
            return False
        char += 1
    if dot == 3 and colon == 1 and char == len(address):
        if (int(temp_sequence) >= 1) and (int(temp_sequence) <= 65535):
            return True
    return False



/*  Write and save your SQL code in this file.
    Do not rename or move it.  */



SELECT m.title
    , a.name
FROM movie m
LEFT JOIN movie_actor ma
    on ma.movie_id = m.id
LEFT JOIN actor a
    on ma.actor_id = a.id
ORDER BY m.title, a.name

# -- I initially started typing my query using the  left join, thinking that in any 
# -- case we would like the list of all the movies even if there are no actor in it
#  -- works here. The 'inner join' works as well in this case and give the same 
#  -- result. 
SELECT m.title
    , a.name
FROM movie m
INNER JOIN movie_actor ma
    on ma.movie_id = m.id
INNER JOIN actor a
    on ma.actor_id = a.id
ORDER BY m.title, a.name



"""
This is the file with your answer, do not rename or move it.
Write your code in it, and save it before submitting your answer.
"""

def is_valid_socket(address):
    """Determine if the provided string is a valid socket address.
    This function declaration must be kept unmodified.

    Args:
        address: A string with a socket address, eg, 
            '127.12.23.43:5000', to be checked for validity.
    Returns:
        A boolean indicating whether the provided string is a valid 
        socket address.
    """
    dot = 0
    colon = 0
    temp_sequence = ''
    char = 0
    
    # We can do this priliminary check which would allow to avoid going through the 
    # address string if the string length is smaller than 9 (3 dots, 1 colon, 
    # 1 number for each portion):
    if len(address) < 9:
        return False
    while char < len(address) and dot < 4 and colon < 2:
        if address[char].isdigit():
            temp_sequence += address[char] 
        elif address[char] == '.':
            if int(temp_sequence) < 0 or int(temp_sequence) > 255:
                return False
            temp_sequence = ''
            dot += 1
        elif address[char] == ':' and dot == 3:
            temp_sequence = ''
            colon += 1
        else:
            return False
        char += 1
    if dot == 3 and colon == 1 and char == len(address):
        if (int(temp_sequence) >= 1) and (int(temp_sequence) <= 65535):
            return True
    return False
 
   


 


# This tests your code with the examples given in the question, 
# and is provided only for your convenience.
if __name__ == '__main__':
    for address in ["127.12.23.43:5000",
                   "127.A:-12"]:
        print is_valid_socket(address)


