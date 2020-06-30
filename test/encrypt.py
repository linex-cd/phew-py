import base64 


		
def encrypt(message):

	decrypted = b"abcdefghijklmnopqrstuvwxyz1234567890 "
	encrypted = b"0987654321qwertyuiopasdfghjklzxcvbnm "
	
	encrypt_table = bytes.maketrans(decrypted, encrypted)
	decrypt_table = bytes.maketrans(encrypted, decrypted)

	result = message.translate(encrypt_table)
	result = base64.b64encode(result.encode()).decode()
	result = result.translate(encrypt_table)
	
	return result
#enddef

def decrypt(message):

	

	decrypted = b"abcdefghijklmnopqrstuvwxyz1234567890 "
	encrypted = b"0987654321qwertyuiopasdfghjklzxcvbnm "
	
	encrypt_table = bytes.maketrans(decrypted, encrypted)
	decrypt_table = bytes.maketrans(encrypted, decrypted)
	
	result = message.translate(decrypt_table)
	result = base64.b64decode(result.encode()).decode()
	result = result.translate(decrypt_table)
	return result
	
#enddef

print(encrypt('job-Hangzhou-testkey12345-textise-2879'))
print(decrypt('MXQxLU4d81RtMlR3LXAk9lBfNe7u0kfc6CjdNeZdMebkLWp27ez='))