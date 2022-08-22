from hashlib import md5

def unix_md5_crypt(pw, salt, magic=None):
    from vendor.md5crypt import MAGIC
    from vendor.md5crypt import to64
    if magic is None:
        magic = MAGIC

    # Take care of the magic string if present
    if salt[:len(magic)] == magic:
        salt = salt[len(magic):]

    # salt can have up to 8 characters:
    salt = salt.split('$', 1)[0]
    salt = salt[:8]

    salt = salt.encode('utf-8')
    magic = magic.encode('utf-8')
    pw = pw.encode('utf-8')

    ctx = pw + magic + salt

    final = md5(pw + salt + pw).digest()
    for pl in range(len(pw), 0, -16):
        if pl > 16:
            ctx = ctx + final[:16]
        else:
            ctx = ctx + final[:pl]

    # Now the 'weird' xform (??)

    i = len(pw)
    while i:
        if i & 1:
            ctx = ctx + chr(0).encode('utf-8')  # if ($i & 1) { $ctx->add(pack("C", 0)); }
        else:
            ctx = ctx + chr(pw[0]).encode('utf-8')
        i = i >> 1

    final = md5(ctx).digest()

    # The following is supposed to make
    # things run slower.

    # my question: WTF???

    for i in range(1000):
        ctx1 = ''.encode('utf-8')
        if i & 1:
            ctx1 = ctx1 + pw
        else:
            ctx1 = ctx1 + final[:16]

        if i % 3:
            ctx1 = ctx1 + salt

        if i % 7:
            ctx1 = ctx1 + pw

        if i & 1:
            ctx1 = ctx1 + final[:16]
        else:
            ctx1 = ctx1 + pw

        final = md5(ctx1).digest()

    # Final xform
    passwd1 = ''

    passwd2 = passwd1 + to64((int(final[0]) << 16)
                           | (int(final[6]) << 8)
                           | (int(final[12])), 4)

    passwd3 = passwd2 + to64((int(final[1]) << 16)
                           | (int(final[7]) << 8)
                           | (int(final[13])), 4)

    passwd4 = passwd3 + to64((int(final[2]) << 16)
                           | (int(final[8]) << 8)
                           | (int(final[14])), 4)

    passwd5 = passwd4 + to64((int(final[3]) << 16)
                           | (int(final[9]) << 8)
                           | (int(final[15])), 4)

    passwd6 = passwd5 + to64((int(final[4]) << 16)
                           | (int(final[10]) << 8)
                           | (int(final[5])), 4)

    final_passwd = passwd6 + to64((int(final[11])), 2)
    

    return magic.decode() + salt.decode() + '$' + final_passwd


unix_md5_crypt = unix_md5_crypt

# assign a wrapper function:
md5crypt = unix_md5_crypt