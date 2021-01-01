import time
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMessageBox
import ocr
import hashlib
import os
from threading import Thread
from time import sleep

fl = open(ocr.outputtext, 'w')
ocr.get_file_path(ocr.root_path, ocr.file_list, ocr.dir_list)


class Stats:
    Accountverification: str = "unPass"

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('main.ui')
        self.ui.password.editingFinished.connect(self.verification)
        self.ui.account.editingFinished.connect(self.verification)
        self.ui.button.clicked.connect(self.handleCalc)
        self.ui.ocrbutton.clicked.connect(self.ocrbutton)
        self.ui.catalogbutton.clicked.connect(self.catalog)
        self.ui.outfilebutton.clicked.connect(self.outfile)
        self.ui.about.clicked.connect(self.about)
        # 统计进行中标记，不能同时做两个统计
        self.ongoing = False

    def about(self):
        QMessageBox.information(
            self.ui,
            '关于',
            '''这个是我首次使用Pyside2进行图形化编程
遇到了很多很多自己的知识盲区
最让我困扰的就是UI进程堵塞
为此查阅了大量资料...
总之最后解决的就好啦

感谢您使用此软件
新年快乐! Happy new year!

MonianHello
Github Page:monianhello.github.io
Bilibili: 陌念_Hello
QQ:2860421919
Email:zhao17292@126.com
2021.1.1
            ''')
        pass

    @staticmethod
    def outfile():
        os.system('start notepad C:\\MonianHello\\list.txt')

    @staticmethod
    def catalog():
        os.system('start C:\\MonianHello')

    def openocr(self):
        def workerThreadFunc():
            self.ongoing = True

            print('==========')
            print('M-N-H  OCR')
            print('启动时间:' + time.asctime(time.localtime(time.time())))
            print('共找到文件数:' + str(int(len(ocr.file_list)) - 1))
            Counts = (int(len(ocr.file_list)) - 1)
            time.sleep(0.5)
            self.ui.progressBar.setRange(0,Counts)
            self.ui.progressBar.setValue(0)
            print('==========')
            ocr.textlist.append('==========')
            ocr.textlist.append('M-N-H  OCR')
            ocr.textlist.append('启动时间:' + time.asctime(time.localtime(time.time())))
            ocr.textlist.append('共找到文件数:' + str(int(len(ocr.file_list) - 1)))
            ocr.textlist.append('==========')
            count = 1
            for ocr.path in ocr.file_list:
                print(ocr.file_list)

                Counts = int(Counts)
                if ocr.path == "C:\\MonianHello\\list.txt":
                    continue
                try:
                    # ocr.transimg(ocr.path)
                    time.sleep(0.5)
                    self.ui.progressBar.setValue(count)
                    print('{0} / {1}'.format(str(count), str(Counts)))
                    ocr.ocr(ocr.path)
                    count += 1
                except:
                    print('出现内部错误')
            for i in ocr.textlist:
                fl.write(i)
                fl.write('\n')
            fl.write('结束时间:' + time.asctime(time.localtime(time.time())))
            fl.close()
            print('写入成功，已将文件写入' + str(ocr.outputtext))
            print('结束时间:' + time.asctime(time.localtime(time.time())))
            print('识别完成，现在将结果写入文件...')
            time.sleep(5)
            self.ongoing = False

        if self.ongoing:
            pass
            QMessageBox.warning(
                self.ui,
                '警告','任务进行中，请等待完成')
            return

        worker = Thread(target=workerThreadFunc)
        worker.start()

    def verification(self):
        account = self.ui.account.text()
        password = self.ui.password.text()
        passwordmd5: str = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        print("验证账户密码:" + account, password)
        if "MonianHello" == account and passwordmd5 == "37d1ecdcd4e31461bff763d27c0d6224":
            self.Accountverification = "Pass"
            print("验证成功，已登录")
        else:
            print("验证失败")
            print("哈希校验(MD5)值:" + passwordmd5)
            self.Accountverification = "unPass"

    def handleCalc(self):
        if self.Accountverification == "Pass":
            self.ui.textBrowser.clear()
            self.ui.textBrowser.insertPlainText("成功登陆.\n")
        else:
            self.ui.textBrowser.clear()
            self.ui.textBrowser.insertPlainText("登录失败，请检查用户名及密码\n")
            Accountverification: str = "unPass"

    def ocrbutton(self):
        if self.Accountverification == "Pass":
            self.openocr()
        else:
            self.ui.textBrowser.clear()
            self.ui.textBrowser.insertPlainText("未登录\n")


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
