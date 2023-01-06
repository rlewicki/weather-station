import rsa

public_key, private_key = rsa.newkeys(512)
public_key_data = public_key.save_pkcs1()
private_key_data = private_key.save_pkcs1()
public_key_file = open("public.pem", "wb")
public_key_file.write(public_key_data)
public_key_file.close()
private_key_file = open("private.pem", "wb")
private_key_file.write(private_key_data)
private_key_file.close()
