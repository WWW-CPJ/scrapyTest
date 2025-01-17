from itemadapter import ItemAdapter
import sqlite3
import copy

from dpcq.items import ChapterItem

class ChaptersPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open_spider(self, spider):
        self.conn = sqlite3.connect('chapters.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            DROP TABLE IF EXISTS chapters
         ''')
        # 创建表，如果表不存在的话
        # SQLite的 TEXT 类型是不限制长度的，可以存储任意长度的字符串，但是如果字符串长度超过1000，会变成BLOB类型，所以这里设置为TEXT类型
        # 包括字母数据，标点符号，特殊字符，空格等等
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chapters (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            chapter TEXT
                )
         ''')
        
    def close_spider(self, spider):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def process_item(self, item, spider):
        # 确保不修改原始item。或者对item进行深拷贝
        # item_copy = copy.deepcopy(item)
        # item_copy['field'] = 'another_value'
        # return item_copy

        # adapter = ItemAdapter(item)
        # chapters = adapter.get('chapter', [])
        # print(f"Chpters from ItemAdapter: {chapters}")

        print ("开始处理章节")
        print (f"chapter_item: {item}")

        if item is None:
            spider.logger.error("Item is None")
            return None
        
        # # 创建 item 的副本
        # item_copy = copy.deepcopy(item)
        # # 可以在这里修改副本
        # item_copy['chapter'] = 'another_value'

        try:
            if isinstance(item, ChapterItem):
                for chapter in item['chapter']:
                    # chapter = item.get('chapter', [])
                    self.cursor.execute('''
                                    INSERT INTO chapters (chapter)
                                    VALUES (?)''', (chapter, ))
                inserted_id = self.cursor.lastrowid

                if inserted_id:
                    print(f"Data inserted successfully with ID: {inserted_id}")
                else:
                    print("Data insertion failed.")
                self.conn.commit()

                return item
            else:
                print("Item is not an instance of ChapterItem")
                print(f"chapter_item: {item}")
                print(f"Type of chapter_item: {type(item)}")
                return None
        except sqlite3.Error as e:
            spider.logger.error(f"Error inserting item into database:{e}")
            self.conn.rollback()
            return None
    
        # if isinstance(chapter_item, ChapterItem):
        #     print ("分割线")
        #     try:
        #         for chapter in chapter_item['chapter']:
        #             self.cursor.execute('''
        #                                 INSERT INTO chapters (chapter)
        #                                 VALUES (?)''', (chapter, ))
        #             inserted_id = self.cursor.lastrowid

        #             if inserted_id:
        #                 print(f"Data inserted successfully with ID: {inserted_id}")
        #             else:
        #                 print("Data insertion failed.")
        #         self.conn.commit()

        #         return chapter_item
        #     except sqlite3.Error as e:
        #         spider.logger.error(f"Error inserting item into database: {e}")
        #         self.conn.rollback()
        #         return None
        # else:
        #     print("Item is not an instance of ChapterItem")
        #     print(f"chapter_item: {chapter_item}")