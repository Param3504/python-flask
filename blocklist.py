"""
logout functionality 

this just contains the list of jwt token that are blocked by user it will be imported by app and the logout resource so that the token when once logged out 
gets added to this block list 



"""

BLOCKLIST =set()
