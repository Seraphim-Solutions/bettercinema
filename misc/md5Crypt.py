from hashlib import md5
from vendor.md5crypt import MAGIC
from vendor.md5crypt import to64


class md5Crypt:
    def __init__(self, pw=None, salt=None, magic=None):
        if pw and salt != None:
            if magic is None:
                magic = MAGIC

            # Take care of the magic string if present
            if salt[:len(magic)] == magic:
                salt = salt[len(magic):]

            # self.salt can have up to 8 characters:
            salt = salt.split('$', 1)[0]

            self.salt = salt[:8].encode('utf-8')
            self.magic = magic.encode('utf-8')
            self.pw = pw.encode('utf-8')

    def ctx(self):
        ctx = self.pw + self.magic + self.salt

        final = md5(self.pw + self.salt + self.pw).digest()
        for pl in range(len(self.pw), 0, -16):
            if pl > 16:
                ctx = ctx + final[:16]
            else:
                ctx = ctx + final[:pl]
        return ctx

    def get_final(self, ctx):
        i = len(self.pw)
        while i:
            if i & 1:
                ctx = ctx + chr(0).encode('utf-8')  # if ($i & 1) { $ctx->add(pack("C", 0)); }
            else:
                ctx = ctx + chr(self.pw[0]).encode('utf-8')
            i = i >> 1
        return md5(ctx).digest()

    def get_ctx1(self):
        ctx = self.ctx()
        self.final = self.get_final(ctx)
        # The following is supposed to make
        # things run slower.
        # my question: WTF???
        for i in range(1000):
            ctx1 = ''.encode('utf-8')
            if i & 1:
                ctx1 = ctx1 + self.pw
            else:
                ctx1 = ctx1 + self.final[:16]

            if i % 3:
                ctx1 = ctx1 + self.salt

            if i % 7:
                ctx1 = ctx1 + self.pw

            if i & 1:
                ctx1 = ctx1 + self.final[:16]
            else:
                ctx1 = ctx1 + self.pw

            self.final = md5(ctx1).digest()


    def return_passwd(self):
        self.get_ctx1()
        # Final xform
        passwd = ''

        num = [0, 6, 12, 1, 7, 13, 2, 8, 14, 3, 9, 15, 4, 10, 5]
        x, y, z = 0, 1, 2
        
        for _val in range(5):
            passwd = passwd + to64((int(self.final[num[x]]) << 16) | (int(self.final[num[y]]) << 8) | (int(self.final[num[z]])), 4)
            x, y, z = x + 3, y + 3, z + 3
        
        final_passwd = passwd + to64((int(self.final[11])), 2)
        
        # print(self.magic.decode() + self.salt.decode() + '$' + final_passwd)
        return self.magic.decode() + self.salt.decode() + '$' + final_passwd