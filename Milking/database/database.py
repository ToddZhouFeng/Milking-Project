import sqlite3
import datetime


class MilkDatabase(object):

    def __init__(self, db_name = 'cup.db', table_name = 'files'):
        # 初始化数据库
        self.db_name = db_name
        self.table_name = table_name
        self.col_name = ['tempCode', 'fileName', 'totalSizeByte', 'uniqueUrl', 'uploadDate', 'expireAt', 'scanDate', 'format','category']
        self.col_type = ['INT PRIMARY KEY NOT NULL', 'TEXT', 'INT', 'TEXT', 'TIME', 'TIME', 'TIME','TEXT','INT']
        self.connect()
        self.create_table()
        # tempCode: 取件码
        # fileName: 第一个文件名
        # totalSizeByte: 总字节数
        # uniqueUrl: 网址
        # uploadDate: 上传时间
        # expireAt: 过期时间
        # scanDate: 扫描时间
        # format: 文件格式
        # category: 文件类型（0：一般文件, -1: 不感兴趣的文件）

    def connect(self):
        # 连接数据库
        self.db = sqlite3.connect(self.db_name)
        print('Opened database %s successfully.'%self.db_name)

    def create_table(self):
        # 若不存在则创建表
        if len(self.col_name) != len(self.col_type):
            print('Error: length of column name and column type are unmatched.')
        else:
            command = 'CREATE TABLE IF NOT EXISTS %s (' %self.table_name
            for name, type in zip(self.col_name, self.col_type):
                command += '%s %s,'%(name, type)
            command = command[0:-1] + ');'
            self.db.execute(command)
            self.db.commit()
            print('Table %s created successfully.'%self.table_name)
    
    def insert(self, values, col_name = None, table_name = None):
        # 插入新记录
        table_name = table_name if table_name != None else self.table_name
        col_name = col_name if col_name != None else self.col_name

        if table_name == None or col_name == None:
            print('Error: table_name and col_name can\'t be None in insert()')
        
        command = 'INSERT INTO %s ('%table_name
        for name in col_name:
            command += '%s,'%name
        command = command[0:-1] + ' ) '

        command += 'VALUES ('
        for value in values:
            if type(value) == str:
                value = "'"+value+"'"
            command += '%s,'%value
        command = command[0:-1] + ' );'

        # print(command)
        self.db.execute(command)
        self.db.commit()
        print('Records created successfully.')

    def replace(self, values, col_name = None, table_name = None):
        # 插入新记录
        table_name = table_name if table_name != None else self.table_name
        col_name = col_name if col_name != None else self.col_name

        if table_name == None or col_name == None:
            print('Error: table_name and col_name can\'t be None in replace()')
        
        command = 'REPLACE INTO %s ('%table_name
        for name in col_name:
            command += '%s,'%name
        command = command[0:-1] + ' ) '

        command += 'VALUES ('
        for value in values:
            if type(value) == str:
                value = "'"+value+"'"
            command += '%s,'%value
        command = command[0:-1] + ' );'

        # print(command)
        self.db.execute(command)
        self.db.commit()
        print('Records replaced successfully.')

    def print_all(self, col_name = None, table_name = None):
        # 打印完整的表
        table_name = table_name if table_name != None else self.table_name
        col_name = col_name if col_name != None else self.col_name

        if table_name == None or col_name == None:
            print('Error: table_name and col_name can\'t be None in print_all()')
        
        command = 'SELECT '
        for name in col_name:
            command += '%s,'%name
        command = command[0:-1] + ' FROM ' + table_name
        print(command)
        result = self.db.execute(command)
        for row in result:
            print('')
            i = 0
            for name in col_name:
                print('  %s = %s'%(name,row[i]))
                i+=1
        
    def update(self, where, values, col_name = None, table_name = None):
        # 更新表内容
        table_name = table_name if table_name != None else self.table_name
        col_name = col_name if col_name != None else self.col_name

        if table_name == None or col_name == None:
            print('Error: table_name and col_name can\'t be None in update()')

        command = 'UPDATE %s set ' %table_name
        for value, name in zip(values, col_name):
            if type(value) == str:
                value = "'"+value+"'"
            command += ' %s = %s,'%(name, value)

        command = command[0:-1] + ' where %s'%where
        
        # print(command)
        self.db.execute(command)
        self.db.commit()
        print('Records updated successfully.')
        
    def close(self):
        # 关闭数据库
        self.db.commit()
        self.db.close()
        print("Database closed successfully.")

    def delete_expired(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        command = "DELETE FROM %s WHERE expireAt <= '%s'" %(self.table_name, now)
        # print(command)
        self.db.execute(command)
        self.db.commit()
        print('Delete expired files successfully.')
    
    def select(self, start = 0, num = 0, sort = None, order = 'DESC', where = ""):
        if order != 'DESC' and order !='desc':
            order = 'ASC'

        command = "SELECT * FROM %s"%self.table_name

        if where != "":
            command += " WHERE "+where

        if sort != None:
            command += " ORDER BY %s"%(sort)

        command += ' '+ order

        if num > 0:
            command += " LIMIT %d, %d"%(start, num)

        

        # print(command)
        cur = self.db.execute(command)
        # for row in cur:
        #     print(row)

        return cur.fetchall()


if __name__ == '__main__':
    db = MilkDatabase('test.db')
    # db.insert(values = (0, 'test', 123, 'hh', '2021-07-30 12:10:04', '2021-07-30 10:10:04', '2021-07-30'))
    # db.replace(values = (1, 'test', 1234, 'hh', '2021-07-30 12:10:04', '2021-07-30 21:10:04', '2021-07-30', '', 0))
    # db.replace(values = (2, 'test', 1234, 'hh', '2021-07-30 12:10', '2021-07-30 22:10:04', '2021-07-30', '', 0))
    # db.replace(values = (3, 'test', 1234, 'hh', '2021-07-30 12:10', '2021-07-30 23:10:04', '2021-07-30', '', 0))
    # db.update(where = 'tempCode = 1', values = ['update'], col_name = ['fileName'])
    # db.delete_expired()
    # db.print_all()
    print(db.select(start = 0, num = 0, sort = "scanDate", order = 'DESC', where = "instr(fileName, '1') > 0"))