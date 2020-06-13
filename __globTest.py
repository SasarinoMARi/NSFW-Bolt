import os
from DBInterface import *
path = "D:\OneDrive\개인 중요 보관소\禁断\動画"

# conn, c = DBInterface.establish()
# DBInterface.initializeTables(c)
# for root, dirs, files in os.walk(path):
#     for file in files:
#         # print(file)
#         print(os.path.join(root, file))
#         DBInterface.insert(c, [file, root, False])
#         # instance = nsfwObj(file, root)
#     print()
# DBInterface.distroy(conn)