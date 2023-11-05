import re



if __name__ == "__main__":

    import re

    str_mac_address = "00:15:5d:a9:c3:a4"
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    patternB = re.compile(r'([0-9A-Fa-f])+([:-])')
    print(pattern)
    print(patternB)

    if pattern.match(str_mac_address):
        print("Valid MAC address!")
    else:
        print("Invalid MAC address.")
    
    mac_obj = pattern.match(str_mac_address)
    
    print(mac_obj[0])
    a=mac_obj.groups()
    print(a)


