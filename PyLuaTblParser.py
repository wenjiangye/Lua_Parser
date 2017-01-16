#coding:utf-8
class PyLuaTblParser(object):

    def __init__(self):
        self.dd = {}               #存储该类中的dict
        self.flag = True           #标记该类当前存的是list还是dict,True表示dict，False表示list
        self.ll = []

    @staticmethod
    def check_zhuanyi(str,index):
        all_c = ['r','t','n','b','a','\\','"',"'",'v','f']
        if str[index] in all_c:
            return True       #需要转义
        return False

    @staticmethod
    def remove_comments(str):  # 去注释
        index = 0
        flag_yin = False              #标记是否在引号里面
        flag_zhujie = False            #标记是否在注释里面
        leftstr = ''              #如果在引号里面记录左边引号类型  ' 和 " 和 [[  和 [====[  等
        leftzhu = ''                #如果在注释里面记录左边注解如果是多行注解的开始标记   [[  和   [===[ 和   [======[  等
        zhushi_num = 0              #标记是单行注释还是多行注释  0 单行  1多行
        retstr = ''
        zhujie_all_str = []     #由于在Lua中，如果在注解域遇到结束符0级长括号，但是在之间被注释的字符存在对应左长括号，此时注解不结束
        yinhao_all_str = []     #同上
        #################################################################################去除注释
        while index < len(str):
            if flag_yin:                         #如果在引号里面
                if str[index] == '\\':                     #遇到反斜杠,开始检测是否有转义字符
                    if PyLuaTblParser.check_zhuanyi(str,index + 1): #在引号里面遇到转义
                        retstr = retstr + str[index:index + 2]      #直接取两个字符
                        index = index + 2
                        continue
                    else:
                        retstr = retstr + str[index]
                elif str[index] == '"':
                    if leftstr == '"':       #双引号引号作用域结束
                        flag_yin = False
                        yinhao_all_str = []
                        retstr  = retstr + '"'
                    else:
                        retstr = retstr + str[index]
                elif str[index] == "'":
                    if leftstr == "'":      #单引号作用域结束
                        flag_yin  = False
                        yinhao_all_str = []
                        retstr = retstr + "'"
                    else:
                        retstr = retstr + str[index]
                elif str[index] == '[' and PyLuaTblParser.check_long_branch(str,index) == 2:   #在引号域里面制找到0级长括号
                        yinhao_all_str.append('[[')  # 将0级长括号压入栈
                        index = index + 2
                        retstr = retstr + '[['
                        continue
                elif len(yinhao_all_str) > 0 and str[index:index + 2] == ']]':          #找到在引号域里面的匹配0级长括号
                        index = index + 2
                        retstr = retstr + ']]'
                        yinhao_all_str.pop()
                        continue
                elif str[index:index + len(leftstr)] == leftstr.replace('[',']'):   #如果遇到其他引号作用域结束符
                        flag_yin = False
                        yinhao_all_str = []
                        retstr = retstr + leftstr.replace('[',']')   #变成右作用域结束符
                        index = index + len(leftstr)
                        continue
                else:
                    retstr = retstr + str[index]
            elif flag_zhujie:                       #在注解里面
                if zhushi_num == 0:                #单行注解
                    if str[index] == '\n':       #单行注解结束
                        flag_zhujie = False
                        zhujie_all_str = []
                        retstr = retstr + str[index]
                    index = index + 1
                    continue
                elif str[index] == '[' and PyLuaTblParser.check_long_branch(str,index) == 2:   #在注解里面制找到0级长括号
                    zhujie_all_str.append('[[')    #将0级长括号压入栈
                    index  = index + 2
                    continue
                elif len(zhujie_all_str) > 0 and str[index:index + 2] == ']]':          #找到在注解里面的匹配0级长括号
                    index = index + 2
                    zhujie_all_str.pop()
                    continue
                elif str[index:index + len(leftzhu)] == leftzhu.replace('[',']'):   #找到多行注解结束标记
                        flag_zhujie = False
                        zhujie_all_str = []
                        index = index + len(leftzhu)
                        continue
                else:
                        index = index + 1
                        continue
            else:                           #在代码域里面,即将可能出现引号域或者注释域标记
                if str[index] == '"':      #出现双引号
                    flag_yin = True
                    leftstr = '"'
                    retstr = retstr + str[index]
                elif str[index] == "'":   #出现单引号
                    flag_yin = True
                    leftstr = "'"
                    retstr = retstr + str[index]
                elif str[index] == '[' :  #可能出现长括号
                    retint = PyLuaTblParser.check_long_branch(str,index)    #长括号左侧长度
                    if retint != -1:   #存在长括号
                        flag_yin = True
                        leftstr = str[index:index + retint]
                        retstr = retstr + leftstr
                        index = index + retint
                        continue
                    else:
                        retstr = retstr + str[index]
                elif str[index] == '-':              #可能出现注解
                    if str[index:index+2] == '--':       #出现注解
                        flag_zhujie = True
                        if str[index+2:index+3] == '[':    #判断是否可能多行注解
                            retint  = PyLuaTblParser.check_long_branch(str,index + 2)
                            if retint != -1:  #出现多行注解
                                zhushi_num = 1
                                leftzhu = str[index+ 2:index + 2 + retint]   #获得注解左标记
                                index = index + 2 + retint
                                continue
                        zhushi_num = 0
                        index = index + 2
                        continue
                    else:
                        retstr = retstr + str[index]
                else:                                #其他情况
                    retstr = retstr + str[index]
            index = index + 1
        return retstr
        #################################################################################去除注释

    @staticmethod
    def check_long_branch(str, index):                     #检测长括号
        if len(str[index:]) < 2:
            return -1
        elif str[index + 1] == '[':                      #0级长括号
            return 2
        elif str[index + 1] == '=':             #n级长括号
            num = 2
            tmp_index = index + 2
            while tmp_index < len(str):
                if str[tmp_index] == '=':
                    num = num + 1
                elif str[tmp_index] == '[':
                    num = num + 1
                    return num
                tmp_index = tmp_index + 1

        return -1

    @staticmethod
    def convert_char(str,index):
        if str[index + 1] == 'n':  #换行
            return '\n'
        elif str[index + 1] == 'r': #回车
            return '\r'
        elif str[index + 1] == 'a': #响铃
            return '\a'
        elif str[index + 1] == 'b': #退格
            return '\b'
        elif str[index + 1] == 'f': #表单
            return '\f'
        elif str[index + 1] == 't': #横向制表符
            return '\t'
        elif str[index + 1] == 'v': #纵向制表符
            return '\v'
        elif str[index + 1] == '\\': #反斜杠
            return '\\'
        elif str[index + 1] == '"': #双引号
            return '\"'
        elif str[index + 1] == "'": #单引号
            return '\''
        elif str[index + 1].isdigit() :  #如果是数字
            tmp = str[index + 1]
            if str[index + 2 :index + 3].isdigit(): #出现两个数字
                tmp = tmp + str[index + 2]
            if str[index + 3 :index + 4].isdigit(): #出现三个数字
                tmp = tmp + str[index + 3]
            if int(tmp) > 255:
                raise Exception
            return chr(int(tmp))
        elif str[index + 1] == 'x' or str[index + 1]  == 'X':
            tmp = str[index + 1: index + 4]
            tmp = '0' + tmp
            return chr(eval(tmp))
        else:
            return str[index + 1]
    def name_check(self,str):
        if not (str[0].isalpha() or str[0] == '_'):
            return False
        index = 1
        while index < len(str):
            if  (str[index].isdigit() or str[index].isalpha() or  str[index] == '_'):
                pass
            else:
                return False
            index = index + 1
        return True

    @staticmethod
    def remove_space(str):  # 去除左右空格和回车
        while len(str) > 0 and (str[0] == ' ' or str[0] == '\r' or str[0] == '\n' or str[0] == '\t'):
            str = str[1:]
        while len(str) > 0 and (str[-1] == ' ' or str[-1] == '\r' or str[-1] == '\n' or str[-1] == '\t'):
            str = str[:len(str) - 1]
        return str

    def __str_to_dict(self,str):  # 将一个lua_table转换为dict
        ret = {}
        index = 1
        for c in str:
            c = PyLuaTblParser.remove_space(c)
            dex = self.__convert_what(c)
            if dex != -1:  # 转换为dict
                strkey = c[0:dex]
                strvalue = c[dex + 1:]
                strkey = PyLuaTblParser.remove_space(strkey)
                strvalue = PyLuaTblParser.remove_space(strvalue)
                if self.__str_ana(strvalue) != None:
                    if strkey[0] == '[' and strkey[-1] == ']':
                        tmp_key = self.__str_ana(strkey[1:len(strkey) - 1])
                        ret[tmp_key] = self.__str_ana(strvalue)
                    else:
                        ret[strkey] = self.__str_ana(strvalue)
        #######################################################
        for c in str:               # key =  value, key = {}, [key] = value ,[key] = {}, ["key"] = {}, ["key"] = value
            c = PyLuaTblParser.remove_space(c)
            dex = self.__convert_what(c)
            if dex == -1:  # 转换为list
                if self.__str_ana(c) != None:
                    ret[index] = self.__str_ana(c)
                index = index + 1
        if ret == {}:
            return []
        return ret
    def __str_to_list(self,str):  # 将一个lua table转换为list
        ret = []
        for c in str:
            c = PyLuaTblParser.remove_space(c)
            ret.append(self.__str_ana(c))
        return ret


    def test_input(self,sstr):
        index = 0
        while index < len(sstr):
            if sstr[index].isdigit()  or sstr[index] == '.' or sstr[index] == '-' or sstr[index] == '+' or sstr[index] == ' ' or sstr[index] == 'x'or sstr[index] == 'X' or sstr[index] == 'E' or sstr[index] == 'e':
                pass
            else:
                return False
            index = index + 1
        return True
    def str_to_num(self,sstr):
        if self.test_input(sstr):
            ret = eval(sstr)
        else:
            raise
        return ret
    def __convert_what(self,str):  # 判断该str应该转换为list还是dict, -1为list, 正值为dict 返回值是 = 的索引
        flag_yin = False  # 标记是否在引号里面
        leftstr = ''
        kuohao = 0
        index = 0
        yinhao_all_str = []          #对于 0级长括号记录处理
        while index < len(str):
            if flag_yin:
                if str[index] == '\\':
                    if PyLuaTblParser.check_zhuanyi(str,index):
                        index = index + 2
                        continue
                elif str[index] == leftstr:
                        flag_yin = False
                        yinhao_all_str = []
                elif str[index] == '[' and PyLuaTblParser.check_long_branch(str,index) == 2:   #在引号域里面制找到0级长括号
                        yinhao_all_str.append('[[')  # 将0级长括号压入栈
                        index = index + 2
                        continue
                elif len(yinhao_all_str) > 0 and str[index:index + 2] == ']]':          #找到在引号域里面的匹配0级长括号
                        index = index + 2
                        yinhao_all_str.pop()
                        continue
                elif str[index:index + len(leftstr)] == leftstr.replace('[',']'):   #如果遇到其他引号作用域结束符
                        flag_yin = False
                        yinhao_all_str = []
                        index = index + len(leftstr)
                        continue
            else:
                if str[index] == '{':
                    kuohao = kuohao - 1
                elif str[index] == '}':
                    kuohao = kuohao + 1
                elif str[index] == '=' and kuohao == 0:
                    return index
                elif str[index] == '"':      #出现双引号
                    flag_yin = True
                    leftstr = '"'
                elif str[index] == "'":   #出现单引号
                    flag_yin = True
                    leftstr = "'"
                elif str[index] == '[' :  #可能出现长括号
                    retint = PyLuaTblParser.check_long_branch(str,index)    #长括号左侧长度
                    if retint != -1:   #存在长括号
                        flag_yin = True
                        leftstr = str[index:index + retint]
                        index = index + retint
                        continue
            index  = index + 1
        return -1
    def check_value(self,str):    #检查table的value是否为字符串，如果是返回转义后字符串，否则返回 False
        str = PyLuaTblParser.remove_space(str)
        index = 0
        leftstr = ''
        flag_yin = False
        retstr = ''
        yinhao_all_str = []
        while index < len(str):
            if flag_yin:
                if len(leftstr) >= 2:  #长括号
                    if str[index] == '[' and PyLuaTblParser.check_long_branch(str, index) == 2:  # 在引号域里面制找到0级长括号
                        yinhao_all_str.append('[[')  # 将0级长括号压入栈
                        retstr = retstr + str[index : index + 2]
                        index = index + 2
                        continue
                    elif len(yinhao_all_str) > 0 and str[index:index + 2] == ']]':  # 找到在引号域里面的匹配0级长括号
                        index = index + 2
                        retstr = retstr + str[index: index + 2]
                        yinhao_all_str.pop()
                        continue
                    elif str[index:index + len(leftstr)] == leftstr.replace('[', ']'):  # 如果遇到其他引号作用域结束符
                        flag_yin = False
                        return retstr
                    else:
                        retstr = retstr + str[index]
                else:           #单双引号
                    if str[index] == '\\':     #遇到转义
                        retstr = retstr + PyLuaTblParser.convert_char(str,index)
                        index = index + 2
                        if str[index - 1:index] == 'x' or str[index - 1:index] == 'X':
                            index = index + 2
                        elif str[index - 1:index].isdigit():
                            if str[index:index + 1].isdigit():  # 出现数字
                                index = index + 1
                            if str[index:index + 1].isdigit():  # 出现数字
                                index = index + 1
                        continue
                    elif str[index] == leftstr:
                        return retstr
                    retstr = retstr + str[index]
            else:
                if str[index] == '"':
                    leftstr = '"'
                    flag_yin = True
                elif str[index] == "'":
                    leftstr = "'"
                    flag_yin = True
                elif str[index] == '[' and PyLuaTblParser.check_long_branch(str,index) != -1:
                    leftint = PyLuaTblParser.check_long_branch(str,index)
                    leftstr = str[index:index + leftint]
                    flag_yin = True
                    index = index + leftint
                    continue
                else:
                    return False
            index = index + 1
        raise  Exception

    def char_recovery(self,str):
        index = 0
        retstr = ''
        while index < len(str):
            if str[index] == '\"':
                retstr = retstr + '\\\"'
            elif str[index] == '\\':
                retstr = retstr + '\\\\'
            else:
                retstr = retstr + str[index]
            index = index + 1
        return retstr
    def __str_ana(self,str):  # 是一个 table 的 value 元素     value , {}
        str = PyLuaTblParser.remove_space(str)
        if len(str) < 2:  # value
            return eval(str)
        if str[0] == '{' and str[-1] == '}':  # {}   value 是一个table
            str = str[1:len(str) - 1]  # 去左右大括号
            str = PyLuaTblParser.remove_space(str)  # 去左右空格
            if len(str) == 0:
                return []
            if str[-1] == ',' or str[-1] == ';':  # 有停止符去停止符
                str = str[0:len(str) - 1]
            #得到去除大括号的table
            strlist = []
            left = 0
            right = 0
            flag_yin = False       #标记在引号里面
            leftstr = ''          #引号左标记
            yinhao_all_str = []    #0级长括号
            kuohao = 0          #记录是否在大括号里面
            while right < len(str):
                if flag_yin:
                    if str[right] == '\\':
                        if PyLuaTblParser.check_zhuanyi(str, right):
                            right = right + 2
                            continue
                    elif str[right] == leftstr:
                        flag_yin = False
                        yinhao_all_str = []
                    elif str[right] == '[' and PyLuaTblParser.check_long_branch(str, right) == 2:  # 在引号域里面制找到0级长括号
                        yinhao_all_str.append('[[')  # 将0级长括号压入栈
                        right = right + 2
                        continue
                    elif len(yinhao_all_str) > 0 and str[right:right + 2] == ']]':  # 找到在引号域里面的匹配0级长括号
                        right = right + 2
                        yinhao_all_str.pop()
                        continue
                    elif str[right:right + len(leftstr)] == leftstr.replace('[', ']'):  # 如果遇到其他引号作用域结束符
                        flag_yin = False
                        yinhao_all_str = []
                        right = right + len(leftstr)
                        continue
                else:
                    if str[right] == '{':
                        kuohao = kuohao - 1
                    elif str[right] == '}':
                        kuohao = kuohao + 1
                    elif kuohao == 0 and (str[right] == ',' or str[right] == ';'):
                        strlist.append(str[left:right])
                        left = right + 1
                    elif str[right] == '"':      #出现双引号
                        flag_yin = True
                        leftstr = '"'
                    elif str[right] == "'":   #出现单引号
                        flag_yin = True
                        leftstr = "'"
                    elif str[right] == '[' :  #可能出现长括号
                        retint = PyLuaTblParser.check_long_branch(str,right)    #长括号左侧长度
                        if retint != -1:   #存在长括号
                            flag_yin = True
                            leftstr = str[right:right + retint]
                            right = right + retint
                            continue
                right = right + 1
            strlist.append(str[left:right ])
            if self.__convert_what(str) == -1:  # to list
                return self.__str_to_list(strlist)
            else:
                return self.__str_to_dict(strlist)
        else:
            tmp_res = self.check_value(str)
            if str == 'nil':
                return None
            elif str == 'false':
                return False
            elif str == 'true':
                return True
            elif not isinstance(tmp_res,(bool)):
                return tmp_res
            else:          #数值
                return self.str_to_num(str)

    def __list_ana(self,ll):         #将一个list解析成一个lua table字符串
        retstr = '{'
        for l in ll:
            if isinstance(l, (str)):  # 如果value是字符串类型
                retstr = retstr + '"' + self.char_recovery(l) + '"' + ','
            elif isinstance(l, (bool)):  # 如果value是布尔类型
                if l:
                    retstr = retstr + 'true' + ','
                else:
                    retstr = retstr + 'false' + ','
            elif isinstance(l, (dict)):  # 如果value是字典类型
                retstr = retstr + self.__dict_ana(l) + ','
            elif isinstance(l, (list)):  ##如果value是列表类型
                retstr = retstr + self.__list_ana(l) + ','
            elif isinstance(l, (int, float,long)):  # 如果value是数值类型
                retstr = retstr + str(l) + ','
            else:
                retstr = retstr + 'nil' + ','
        retstr = retstr + '}'
        return retstr

    def __dict_ana(self,di):                    #将一个dict解析成一个lua table字符串
        retstr = '{'
        index = 1
        tmp_d = {}
        while True:
            if di.has_key(index):
                tmp_d[index] = di[index]
                if isinstance(di[index], (str)):  # 如果value是字符串类型
                    retstr = retstr + '"' + self.char_recovery(di[index]) + '"' + ','
                elif isinstance(di[index], (bool)):
                    if di[index]:
                        retstr = retstr + 'true' + ','
                    else:
                        retstr = retstr + 'false' + ','
                elif isinstance(di[index], (dict)):  # 如果value是字典类型
                    retstr = retstr + self.__dict_ana(di[index]) + ','
                elif isinstance(di[index], (list)):  ##如果value是列表类型
                    retstr = retstr + self.__list_ana(di[index]) + ','
                elif isinstance(di[index], (int, float,long)):  # 如果value是数值类型
                    retstr = retstr + str(di[index]) + ','
                else:
                    retstr = retstr + 'nil' + ','
            else:
                break
            index = index + 1
        #############################
        for k in tmp_d:
            di.pop(k)
        #####################################
        for k in di:
            if isinstance(k, (str)):  # 如果key是字符串类型
                retstr = retstr + '["' + self.char_recovery(k) + '"]  =  '
            elif isinstance(k, (int, float)):
                retstr = retstr + '[' + str(k) + '] = '
            if isinstance(di[k], (str)):  # 如果value是字符串类型
                retstr = retstr + '"' + self.char_recovery(di[k]) + '"' + ','
            elif isinstance(di[k], (bool)):
                if di[k]:
                    retstr = retstr + 'true' + ','
                else:
                    retstr = retstr + 'false' + ','
            elif isinstance(di[k], (dict)):  # 如果value是字典类型
                retstr = retstr + self.__dict_ana(di[k]) + ','
            elif isinstance(di[k], (list)):  ##如果value是列表类型
                retstr = retstr + self.__list_ana(di[k]) + ','
            elif isinstance(di[k], (int, float,long)):  # 如果value是数值类型
                retstr = retstr + str(di[k]) + ','
            else:
                retstr = retstr + 'nil' + ','
        retstr = retstr + '}'
        return retstr

    def __mycopy(self, dd):                            #  实现深拷贝
        ret = []
        if isinstance(dd, (dict)):
            ret = {}
            for k in dd:
                if isinstance(k, (int, float, str)):  # 判断key类型,只处理数字和字符串两种类型的key,其他类型的key直接忽略
                    if isinstance(dd[k], (list, dict, tuple)):
                        ret[k] = self.__mycopy(dd[k])  # 递归深拷贝
                    elif isinstance(dd[k], (int, float, bool, str)):
                        ret[k] = dd[k]
                    else:
                        ret[k] = dd[k]
            return ret
        elif isinstance(dd, (list, tuple)):  # 我们将元组也转换为list
            for k in dd:
                if isinstance(k, (list, dict, tuple)):
                    ret.append(self.__mycopy(k))
                #elif isinstance(k, (int, float, bool, str)):
                else:
                    ret.append(k)
            return ret
        else:
            return dd

    def load(self,str):
        try:
            str = PyLuaTblParser.remove_comments(str)
            ret = self.__str_ana(str)
            if isinstance(ret,(dict)):
                self.flag = True
                self.dd = ret
                self.ll = []
            else:
                self.flag = False
                self.ll = ret
                self.dd = {}
        except Exception:
            raise

    def dump(self):
        try:
            if self.flag:
                return self.__dict_ana(self.dd)
            else:
                return self.__list_ana(self.ll)
        except Exception:
            raise

    def loadDict(self,d):               #加载一个dict到类
        try:
            if isinstance(d,(dict)):
                self.dd = self.__mycopy(d)
                self.flag = True
                self.ll = []
            elif isinstance(d,(list,tuple)):
                self.ll = self.__mycopy(d)
                self.flag = False
                self.dd = {}
        except Exception:
            raise

    def dumpDict(self):
        try:
            if self.flag:
                return self.__mycopy(self.dd)
            else:
                return self.__mycopy(self.ll)
        except Exception:
            raise

    def loadLuaTable(self, f):
        try:
            fp = open(f, 'r')
            lua_str =  fp.read()
            fp.close()
            try:
                self.load(lua_str)
            except Exception:
                raise
        except IOError:
            raise
        finally:
            if fp:
                fp.close()

    def dumpLuaTable(self,f):
        try:
            fp = open(f,'w')
            try:
                lua_str = self.dump()
            except Exception:
                raise
            fp.write(lua_str)
            fp.close()
        except IOError:
            raise
        finally:
            if fp:
                fp.close()

    def update(self,d):                      #用字典d更新类中数据
        if self.flag:                                   #如果类中是dict
            self.dd.update(self.__mycopy(d))
        else:                                           #如果类中是list
            l_index = range(1,len(self.ll) + 1)       #获取索引序列
            self.dd = dict(zip(l_index, self.ll))     #转换为dict
            if set(d.items()).issubset(self.dd.items()):
                self.dd = {}                        #转换后没又增加值也没有更新值，还是转回list
            else:
                self.flag = True
                self.ll = []
                self.dd.update(self.__mycopy(d))

    def __getitem__(self, item):            #重载[] 索引运算符,没有赋值,可以读
        if self.flag:
            return self.dd[item]           #如果是dict
        else:
            return self.ll[item]           #如果是list

    def __setitem__(self, key, value):      #重载[] 索引运算符,有赋值,可以写
        if self.flag:                     #如果是dict
            if value is not None:
                self.dd[key] = value
        else:
            tmp_d = {}
            tmp_d[key] = value           #生成一个临时dict, 然后调用已经实现的update方法
            self.update(tmp_d)





