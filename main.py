#coding:utf-8
from PyLuaTblParser import *
test_str  = r'{array = {65,23, - 222205,},dict = {mixed = {43,54.33,false,9,string = "valu\099e",},array = {3,6,4,},string = "value",},}'
test_str2 = r'{  [ 1] =   "--\x44[["    ,   [[  \v\\vvv----[{  { ]]  , [ [[  {  ]] ]   =  "2"}'
test_str3 = r"{'1'= '\\'}"
test_str4 = r'{	nil,nil,nil,{nil,nil,nil,12,nil},1	,["wwww"]=0x9,  -  -0x2222   ,[ - -  3.122e-100] =   "--\x44[["    ,   [[  \v\\vvv----[{  { ]]  , [ [[  {  ]] ] = 2,	22 =	[[222]]}'
test_str5 = r'{}'
test_str6 = r'{{{{{}}}}}'
test_str7 = r'{{--[[                      ]]}}'
test_str8 = r'{1,2,3,4,5,6,--[[wwwwwwwwwwwwwwww]]7}'
test_str9 = r'{111111,2222222,[  [=====[  \\\\\\\\\\\\\\\\\\\\\\\\\  ]=====] ] = {{},{},{},--[[ [==[    ]]}}'
test_str10 = r'{{},nil,[1] = 2, [1] = 2,[0x2000E  ] =                            "\\\\\\\\\\\\\\\\\\\\\\\\"}'
test_str11 = r'{nil,nil,nil,[1] = nil}'
test_str12 = r'{"\0x10","0x11","\097--[[--[[--[[--[[]]",}'
test_str13 = r'{"\0x10","0x11","\097"--[==[--[==[]==],}'
test_str14 = r'{{1},{2},{3},{4 = [[ \\\n\n\n\r\t\b\v\b\\!@#$%^&*]]}}'
test_str15 = r'{["\"\"\010\0x22--[[ @#*&^%  wwwwwwwwwwwwwww]]" ]=  - - - - - - - - 0x23E}'
test_str16 = r'{[   [=======[    ]=======] ] = [[                [==[   ]==]   ]]}'
test_str17 = r'{{{{}}},{{{}}},{{{{{{{{{{}}}}}}}}}}}'
test_str18 = r'{www = "www" ,"\n\t\r\b\a\v\f\0x25-----------------------------------------------[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[" }'
test_str19 = r'{{},{},{},{[2] = 2}, [  [[ [==[@#$%^&*()\0x22\090\\\\\\///////<>?]==] ]]] = "======================================="}'
test_str20 = r'{1,2,3,4,{"1" = "\\"},{},{},{},{},{            },[ [[10x0x0x0x\0x22\""]] ] = {}}'

a1 = PyLuaTblParser()

a1.load(test_str)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
############################
a1.load(test_str2)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str3)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str4)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str5)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str6)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str7)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str8)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str9)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str10)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str11)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str12)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str13)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str14)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str15)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str16)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str17)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str18)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str19)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################
a1.load(test_str20)
print a1.dumpDict()
a1.load(a1.dump())
print a1.dumpDict()
###########################



















