import time
import serial
import threading
import constants as CONST

exit_thread = False  # 쓰레드 종료용 변수


# 본 쓰레드
def serial_receive_data(sp):
    global exit_thread

    # 쓰레드 종료될때까지 계속 돌림
    while not exit_thread:
        if not sp.is_open or sp is None:
            exit_thread = True
            break

        rx_data = ''
        time.sleep(1)
        try:
            rx_data = sp.readline().decode(CONST.ENCODING_TYPE)
        except:
            rx_data = ''

        if rx_data == 'EER':
            rx_data = ''
            # do init = true
            # init a 표시
        elif rx_data == 'INCOK' or rx_data == 'INFOK':
            rx_data = ''
            # init f = true
            # ------ 표시
            return
        elif fc.block:
            fc.block = False
            # 수신 데이터 헤더 파악
            read_header(rx_data)
        print(sp.is_open)


class pc_setting_class:
    def __init__(self):
        self.__port = 'COM1'
        self.__baudrate = 9600
        self.__databits = 7
        self.__parity = 'NONE'
        self.__stopbits = 1
        self.__terminator = 'CRLF'

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, new_port):
        self.__port = new_port

    @property
    def baudrate(self):
        return self.__baudrate

    @baudrate.setter
    def baudrate(self, new_baudrate):
        self.__baudrate = new_baudrate

    @property
    def databits(self):
        return self.__databits

    @databits.setter
    def databits(self, new_databits):
        self.__databits = new_databits

    @property
    def parity(self):
        return self.__parity

    @parity.setter
    def parity(self, new_parity):
        self.__parity = new_parity

    @property
    def stopbits(self):
        return self.__stopbits

    @stopbits.setter
    def stopbits(self, new_stopbits):
        self.__stopbits = new_stopbits

    @property
    def terminator(self):
        return self.__terminator

    @terminator.setter
    def terminator(self, new_terminator):
        self.__terminator = new_terminator


class flag_class:
    def __init__(self):
        self.__f = False
        self.__cf = False
        self.__array_index_f = 0
        self.__array_index_cf = 0
        self.__read = False
        self.__write = False
        self.__hi = 0
        self.__lo = 0
        self.__terminator = '\r\n'
        self.__block = False

        # 상태 표시
        self.__is_stable = False
        self.__is_zero = False
        self.__is_net = False
        self.__is_hold = False
        self.__is_hg = False

        # 단위 표시
        self.__unit = CONST.UNIT_NONE

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

    @property
    def is_stable(self):
        return self.__is_stable

    @is_stable.setter
    def is_stable(self, new_is_stable):
        self.__is_stable = new_is_stable

    @property
    def is_zero(self):
        return self.__is_zero

    @is_zero.setter
    def is_zero(self, new_is_zero):
        self.__is_zero = new_is_zero

    @property
    def is_net(self):
        return self.__is_net

    @is_net.setter
    def is_net(self, new_is_net):
        self.__is_net = new_is_net

    @property
    def is_hold(self):
        return self.__is_hold

    @is_hold.setter
    def is_hold(self, new_is_hold):
        self.__is_hold = new_is_hold

    @property
    def is_hg(self):
        return self.__is_hg

    @is_hg.setter
    def is_hg(self, new_is_hg):
        self.__is_hg = new_is_hg

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, new_unit):
        self.__unit = new_unit


# 수신 데이터 헤더 파악
def read_header(rx):
    header_1bit = rx[0:0]
    header_2bit = rx[0:1]
    header_3bit = rx[0:2]
    header_5bit = rx[0:4]

    if fc.cf and \
            (header_1bit == '?' or
             header_1bit == 'I' or
             header_2bit == 'CF' or
             header_2bit == 'CS'):
        fc.cf = False
        # cfDataArray[rs.arrayIndexCF] = str;
    elif fc.f and \
            (header_1bit == '?' or
             header_1bit == 'I' or
             header_1bit == 'F' or
             header_3bit == 'VER' or
             header_5bit == 'STOOK' or
             header_5bit == 'SETOK'):
        fc.f = False
        # fDataArray[rs.arrayIndexF] = str;
    else:
        if header_2bit == 'ST':
            '''
            stable = true;
            hold = false;
            hg = false;
            net = True if rx[3:4] == 'NT' else False
            dispMsg = makeFormat(str);
            '''
        elif header_2bit == 'US':
            '''
            stable = false;
            hold = false;
            hg = false;
            net = True if rx[3:4] == 'NT' else False
            dispMsg = makeFormat(str);
            '''
        elif header_2bit == 'HD':
            '''
            stable = false;
            hold = true;
            net = false;
            hg = false;
            dispMsg = makeFormat(str);
            '''
        elif header_2bit == 'HG':
            '''
            stable = false;
            hold = true;
            net = false;
            hg = true;
            dispMsg = makeFormat(str);
            '''
        elif header_2bit == 'OL':
            '''
            stable = false;
            hold = false;
            net = false;
            hg = false;
            dispMsg = "   .  ";
            '''
        else:
            '''
            stable = false;
            hold = false;
            zero = false;
            net = false;
            hg = false;
            str = string.Empty;
            rs.Block = true;
            return;
            '''
        rx = ''
    fc.block = True


# 데이터 포맷 형성
def make_format(data):
    result = ''
    if data == '' or data is None:
        return result

    # 부호 포함 계량값
    value = data[6:13]
    # 단위값
    unit = data[14:15]

    # 제로 서프레스
    if '.' in value:
        result = str(float(value))
    else:
        result = str(int(value))

    # 단위값 길이가 무조건 2인 경우 아래 로직으로 진행
    if unit[1:1] == 't':
        fc.unit = CONST.UNIT_T
    else:
        fc.unit = CONST.UNIT_G
        if unit[0:0] != '':
            fc.unit = CONST.UNIT_KG

    # 단위값 길이가 가변적일 경우 아래 로직으로 진행
    if len(unit) == 2:
        fc.unit = CONST.UNIT_KG
    else:
        fc.unit = CONST.UNIT_G
        if unit == 't':
            fc.unit = CONST.UNIT_T

    return result


# 메인 버튼
def btn_click_clear_tare(sp):
    sp.write('CT' + fc.terminator)


def btn_click_zero_tare(sp):
    sp.write('MZT' + fc.terminator)


def btn_click_gross_net(sp):
    if fc.is_net:
        # 순중량일 때
        sp.write('MG' + fc.terminator)
    else:
        # 총중량일 때
        sp.write('MN' + fc.terminator)


def btn_click_hold(sp):
    # 홀드 on일때
    sp.write('HC' + fc.terminator)
    # 홀드 off일때
    sp.write('HS' + fc.terminator)


def btn_click_onoff(sp):
    # OFF 상태
    if sp is None:
        try:
            # 포트 열기
            sp = serial.Serial(
                port='COM5',
                baudrate=2400,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                xonxoff=False,
                timeout=0)

            thread = threading.Thread(target=serial_receive_data, args=(sp,))
            thread.start()

            # 스트림 모드 날리기
            set_communication_mode(sp, CONST.STREAM_MODE)
            # 버튼 OFF 표시
        except serial.SerialException:
            print('Can not open port.')

        return

    # OFF 상태
    if not sp.is_open:
        try:
            # 포트 열기
            sp.open()

            thread = threading.Thread(target=serial_receive_data, args=(sp,))
            thread.start()

            # 스트림 모드 날리기
            set_communication_mode(sp, CONST.STREAM_MODE)
            # 버튼 OFF 표시

        except serial.SerialException:
            print('Can not open port.')

        return

    # ON 상태
    try:
        global exit_thread
        exit_thread = True
        # 스트림 모드로 종료
        set_communication_mode(sp, CONST.STREAM_MODE)
        # 포트 닫기
        sp.close()
        # 버튼 ON 표시, 상태 표시 라벨 전부 초기화
        # 표시창 OFF 표시
    except serial.SerialException:
        print('Can not open port.')


def show_message():
    return
    # if (!funcMode)
    # {
    # if (stanby)
    # {
    #     dispMsg = string.Empty;
    # dispMessage("------");
    # radioButton1.Enabled = false;
    # radioButton2.Enabled = false;
    # }
    # else
    # {
    #     dispMessage(dispMsg);
    # radioButton1.Enabled = true;
    # radioButton2.Enabled = true;
    # if ((serialPort1.BaudRate == 19200) | | (serialPort1.BaudRate == 38400))
    # serialPort1.DiscardInBuffer();
    # }
    #
    # // 안정마크
    # lblStable_.Visible = stable ? true: false;
    #
    # //
    # 영점마크
    # lblZero_.Visible = zero ? true: false;
    #
    # // net마크
    # lblNet_.Visible = net ? true: false;
    #
    # // hold
    # if (hg)
    # {
    # if (cnt100ms + + < 4)
    # {
    #     lblHold_.Visible = true;
    # }
    # else
    # {
    #     lblHold_.Visible = false;
    # if (cnt100ms > 8)
    # {
    # cnt100ms = 0;
    # }
    # }
    # }
    # else
    # {
    # lblHold_.Visible = hold ? true: false;
    # }
    #
    # if (kg)
    # lblUnit.Text = "kg";
    # else if (g & & !kgReady)
    # lblUnit.Text = "g";
    # else if (t)
    # lblUnit.Text = "t";
    # // else
    # // lblUnit.Text = string.Empty;
    # }
    # else if (initF)
    # {
    #     dispMessage(dispMsg);
    # radioButton1.Enabled = true;
    # radioButton2.Enabled = true;
    # }
    # g = false;
    # kg = false;
    # t = false;
    # kgReady = false;


# 통신 모드 변경
def set_communication_mode(sp, val):
    command = 'F206,' + str(val) + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))


'''
통신 설정
'''
def get_baudrate(sp):
    command = '?F201' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))


def get_databits(sp):
    command = '?F202' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_parity(sp):
    command = '?F203' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_stopbits(sp):
    command = '?F204' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_terminator(sp):
    command = '?F205' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))


# 기본 설정
def get_digital_filter(sp):
    command = '?F001' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_hold_mode(sp):
    command = '?F002' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_average_time(sp):
    command = '?F003' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_zero_range(sp):
    command = '?CF05' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_tracking_time(sp):
    command = '?CF06' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_tracking_range(sp):
    command = '?CF07' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_power_on_zero(sp):
    command = '?CF08' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))


# 외부 출력
def get_print_condition(sp):
    command = '?F101' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_comparator(sp):
    command = '?F102' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_comparator_mode(sp):
    command = '?F103' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_near_zero(sp):
    command = '?F104' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))


# 교정
def get_capa(sp):
    command = '?CF03' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_div(sp):
    command = '?CF02' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_decimal_point(sp):
    command = '?CF01' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_unit(sp):
    command = '?CF09' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def get_span(sp):
    command = '?CF04' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def do_cal_0(sp):
    command = 'CZ' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

def do_cal_f(sp):
    command = 'CS' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))

# 버전 확인
def get_ver(sp):
    command = '?VER' + fc.terminator
    sp.write(command.encode(CONST.ENCODING_TYPE))


psc = pc_setting_class()
fc = flag_class()

btn_click_onoff(None)