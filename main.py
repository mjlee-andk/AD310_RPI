import serial
import serial.tools.list_ports as list_ports
import signal
import time
import threading


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
        pass

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

disp_msg = ''  # 표시 데이터 변수
temp = ''  # 임시 변수

# 상태 표시 변수
stable = False
zero = False
net = False
hold = False
hg = False

# 단위 표시
kg = False
g = False
t = False
kg_ready = False

do_span = False  # 스팬 적용
func_mode = False  # 설정 모드
serial_mode = False  # 통신설정 모드
basic_mode = False  # 기본설정 모드
comp_mode = False  # 외부출력 모드
do_cal_mode = False  # 캘리브레이션 진행
ver_mode = False  # 버전
mode_init_f = False  # init F 모드
mode_init_a = False  # init All 모드
init_f = False  # init 응답 플래그
err_cnt = 0

next = 0  # 타이머 인덱스 지정 변수
cnt100ms = 0  # 100ms 카운터

f_data_array = [None] * 20  # f펑션 정보 배열
cf_data_array = [None] * 11  # cf 펑션 정보 배열

do_init = False  # 초기화 루틴 진입

standby_sec = 0  # 스탠바이 시간체크 변수
stanby = False  # 스탠바이 플래그

ver = True

# 초기화 함수 상수 정의
SERIAL = 1
BASIC = 2
COMP = 3
CAL = 4


def form1_load():
    #  for문으로 포트이름 보여주기
    ports = list_ports.comports()
    for port in ports:
        print(port)

    # checkBox1.Text = '설정 보이기'
    # tabControl1.Visible = false
    # base.Size = new
    # Size(757, 400)
    #
    # // 이전
    # 설정값
    # 읽어오기
    # cmbPort.Text = mySetting.Default.PortDefault
    # cmbBaudrate.Text = mySetting.Default.BpsDefault
    # cmbDatabits.Text = mySetting.Default.LengthDefault
    # cmbParity.Text = mySetting.Default.ParityDefault
    # cmbStopbits.Text = mySetting.Default.StopDefault
    # cmbTerminator.Text = mySetting.Default.TerminatorDefault


line = []  # 라인 단위로 데이터 가져올 리스트 변수
exit_thread = False  # 쓰레드 종료용 변수


# 쓰레드 종료용 시그널 함수
def handler(signum, frame):
    exit_thread = True


# 데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)

    # 출력!
    print(tmp)


# 본 쓰레드
def readThread(ser):
    global line
    global exit_thread

    # 쓰레드 종료될때까지 계속 돌림
    while not exit_thread:
        # 데이터가 있있다면
        for c in ser.read():
            # line 변수에 차곡차곡 추가하여 넣는다.
            line.append(chr(c))

            if c == 10:  # 라인의 끝을 만나면..
                # 데이터 처리 함수로 호출
                parsing_data(line)

                # line 변수 초기화
                del line[:]


def serial_port_data_received(sp):
    rx_data = ''
    stanby = False
    stanby_sec = 0

    if sp.is_open:
        try:
            rx_data = sp.readline()
        except:
            rx_data = ''

    if rx_data == 'EER':
        do_init = True
        disp_msg = 'init a'
        rx_data = ''
        rs.block = False
    elif rx_data == 'INCOK' or rx_data == 'INFOK':
        init_f = True
        rs.block = False
        rx_data = ''
        disp_msg = '------'
        return
    elif rs.block:
        rs.block = False
        msg_thread = threading.Thread(target=call_thread, args=(rx_data,))
        msg_thread.start()


def call_thread(obj):
    str_data = str(obj)

    if rs.cf and ('?' in str_data or 'I' in str_data or 'CF' in str_data or 'CS' in str_data):
        rs.cf = False
        cf_data_array[rs.array_index_cf] = str_data

    elif rs.f and (
            '?' in str_data or 'I' in str_data or 'F' in str_data or 'VER' in str_data or 'STOOK' in str_data or 'SETOK' in str_data):
        rs.f = False
        f_data_array[rs.array_index_f] = str_data
    else:
        if 'ST' in str_data:
            stable = True
            hold = False
            hg = False
            net = True if 'NT' in str_data else False
            disp_msg = make_format(str_data)
        elif 'US' in str_data:
            stable = False
            hold = False
            hg = False
            net = True if 'NT' in str_data else False
            disp_msg = make_format(str_data)
        elif 'HD' in str_data:
            stable = False
            hold = True
            hg = False
            net = False
            disp_msg = make_format(str_data)
        elif 'HG' in str_data:
            stable = False
            hold = True
            hg = True
            net = False
            disp_msg = make_format(str_data)
        elif 'OL' in str_data:
            stable = False
            hold = False
            hg = False
            net = False
            disp_msg = '   .  '
        else:
            stable = False
            hold = False
            zero = False
            hg = False
            net = False
            str_data = ''
            rs.block = True
            return
        str_data = ''
    rs.block = True


def make_format(data):
    if data != '':
        rx_data_array = list(data)
        data_array = [None] * len(rx_data_array)

        rx_sum = 0
        j = 0
        minus = False

        for i in rx_data_array:
            if i == '0' or i == '1' or i == '2':
                data_array[j] = i
                if rx_data_array != '.':
                    rx_sum = rx_sum * 10 + i - 0  # rxSum = rxSum * 10 + (rxdata_array[i] - '0')
                j = j + 1
            elif i == '-':
                minus = True
            elif i == 'k':
                kg_ready = True
            elif i == 'g':
                if kg_ready:
                    g = False
                    kg = True
                    t = False
                else:
                    g = True
                    kg = False
                    t = False
            elif i == 't':
                g = False
                kg = False
                t = True

        if minus:
            rx_sum = ~rx_sum

        zero = True if rx_sum == 0 else False

        # 제로 서프레스
        if data_array[0] == '0' and data_array[0] != '.':
            data_array[0] = '\0'
            if data_array[1] == '0' and data_array[1] != '.':
                data_array[1] = '\0'
                if data_array[2] == '0' and data_array[2] != '.':
                    data_array[2] = '\0'
                    if data_array[3] == '0' and data_array[3] != '.':
                        data_array[3] = '\0'
                        if data_array[4] == '0' and data_array[4] != '.':
                            data_array[4] = '\0'
                            if data_array[5] == '0' and data_array[5] != '.':
                                data_array[5] = '\0'
                                if data_array[6] != '0' and minus:
                                    data_array[5] = '-'

                            elif data_array[5] == '.':
                                data_array[4] = '0'
                                if minus:
                                    data_array[3] = '-'

                            elif minus:
                                data_array[4] = '-'

                        elif data_array[4] == '.':
                            data_array[3] = '0'
                            if minus: data_array[2] = '-'

                        elif minus:
                            data_array[3] = '-'

                    elif data_array[3] == '.':
                        data_array[2] = '0'
                        if minus:
                            data_array[1] = '-'
                    elif minus:
                        data_array[2] = '-'
                elif data_array[2] == '.':
                    data_array[1] = '0'
                    if minus:
                        data_array[0] = '-'

                elif minus:
                    data_array[1] = '-'
            elif data_array[1] == '.':
                data_array[0] = '0'

            elif minus:
                data_array[0] = '-'
        # 제로 서프레스 끝

        data = ''
        for i in data_array:
            if i != '\0':
                data += str(i)

    return data


def disp_message(str):
    return


if __name__ == '__main__':
    # 종료 시그널 등록
    signal.signal(signal.SIGINT, handler)

    # 시리얼 열기
    ser = serial.Serial('COM5', 2400, timeout=0)

    # 시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readThread, args=(ser,))

    # 시작!
    thread.start()
