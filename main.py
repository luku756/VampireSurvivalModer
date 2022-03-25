# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Resources import Resources
from Packer import Packer

# rs = Resources()


rs = Resources()
rs.read()
#rs.parse_resource("UI")

pk = Packer()
pk.unpack(rs)


#
