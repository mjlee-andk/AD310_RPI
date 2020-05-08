import time
import serial
import threading


# ser = serial.Serial('COM5', 2400, timeout=0)
#
# while 1:
#     tdata = ser.read()
#     time.sleep(1)
#     # data_left = ser.inWaiting()
#     # tdata += ser.read(data_left)
#     print(tdata)

# line = []  # 라인 단위로 데이터 가져올 리스트 변수
# exit_thread = False  # 쓰레드 종료용 변수
#
# # 본 쓰레드
# def readThread(ser):
#     global line
#     global exit_thread
#
#     # 쓰레드 종료될때까지 계속 돌림
#     while not exit_thread:
#         time.sleep(1)
#         print(type(ser))
#         # # 데이터가 있있다면
#         # for c in ser.read():
#         #     # line 변수에 차곡차곡 추가하여 넣는다.
#         #     line.append(chr(c))
#         #
#         #     if c == 10:  # 라인의 끝을 만나면..
#         #         # 데이터 처리 함수로 호출
#         #         parsing_data(line)
#         #
#         #         # line 변수 초기화
#         #         del line[:]
#
# # 시리얼 열기
# ser = serial.Serial('COM5', 2400, timeout=0)
#
# # 시리얼 읽을 쓰레드 생성
# thread = threading.Thread(target=readThread, args=(ser,))
#
# # 시작!
# thread.start()

class flagClass:
    def __init__(self):
        self.__f = False
        self.__cf = False
        self.__array_index_f = 0
        self.__array_index_cf = 0
        self.__read = False
        self.__write = False
        self.__hi = 0
        self.__lo = 0
        self.__terminator = ''
        self.__block = False

    @property
    def f(self):
        return self.__f

    @f.setter
    def f(self, new_f):
        self.__f = new_f

    @property
    def cf(self):
        return self.__cf

    @cf.setter
    def cf(self, new_cf):
        self.__cf = new_cf

    @property
    def array_index_f(self):
        return self.__array_index_f

    @array_index_f.setter
    def array_index_f(self, new_array_index_f):
        self.__array_index_f = new_array_index_f

    @property
    def array_index_cf(self):
        return self.__array_index_cf

    @array_index_cf.setter
    def array_index_cf(self, new_array_index_cf):
        self.__array_index_cf = new_array_index_cf

    @property
    def read(self):
        return self.__read

    @read.setter
    def read(self, new_read):
        self.__read = new_read

    @property
    def write(self):
        return self.__write

    @write.setter
    def write(self, new_write):
        self.__write = new_write

    @property
    def hi(self):
        return self.__hi

    @hi.setter
    def hi(self, new_hi):
        self.__hi = new_hi

    @property
    def lo(self):
        return self.__lo

    @lo.setter
    def lo(self, new_lo):
        self.__lo = new_lo

    @property
    def terminator(self):
        return self.__terminator

    @terminator.setter
    def terminator(self, new_terminator):
        self.__terminator = new_terminator

    @property
    def block(self):
        return self.__block

    @block.setter
    def block(self, new_block):
        self.__block = new_block


rs = flagClass()


def get_serial_baudrate(sp):
    sp.write('?F201' + rs.terminator)