import constants as const


class scale_flag:
    def __init__(self):
        self.__f = False
        self.__cf = False
        self.__array_index_f = 0
        self.__array_index_cf = 0
        self.__read = False
        self.__write = False
        self.__hi = 0
        self.__lo = 0
        self.__terminator = '\r\n'  # CRLF
        self.__block = False

        # 표시 데이터
        self.__display_msg = ''

        # 상태 표시
        self.__is_stable = False
        self.__is_zero = False
        self.__is_net = False
        self.__is_hold = False
        self.__is_hg = False

        # 단위 표시
        self.__unit = const.UNIT_NONE

        # 스팬 적용
        self.__do_span = False

        # 통신 모드 파악
        self.__is_stream_mode = True

        # 통신 설정 모드
        self.__is_serial_mode = False

        # 기본 설정 모드
        self.__is_basic_mode = False

        # 외부 출력 모드
        self.__is_comp_mode = False

        # 교정 모드
        self.__is_cal_mode = False

        # 버전
        self.__is_ver_mode = False

        # init F 모드
        self.__mode_init_f = False

        # init All 모드
        self.__mode_init_a = False

        # init 응답 플래그
        self.__init_f = False

        # 100ms 카운터
        self.__cnt_100ms = 0

        # 초기화 루틴 진입
        self.__do_init = False

        # 대기 시간
        self.__waiting_sec = 0



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

    @property
    def waiting_sec(self):
        return self.__waiting_sec

    @waiting_sec.setter
    def waiting_sec(self, new_waiting_sec):
        self.__waiting_sec = new_waiting_sec

    @property
    def display_msg(self):
        return self.__display_msg

    @display_msg.setter
    def display_msg(self, new_display_msg):
        self.__display_msg = new_display_msg

    @property
    def is_stream_mode(self):
        return self.__is_stream_mode

    @is_stream_mode.setter
    def is_stream_mode(self, new_is_stream_mode):
        self.__is_stream_mode = new_is_stream_mode

    @property
    def init_f(self):
        return self.__init_f

    @init_f.setter
    def init_f(self, new_init_f):
        self.__init_f = new_init_f

    @property
    def mode_init_f(self):
        return self.__mode_init_f

    @mode_init_f.setter
    def mode_init_f(self, new_mode_init_f):
        self.__mode_init_f = new_mode_init_f

    @property
    def mode_init_a(self):
        return self.__mode_init_a

    @mode_init_a.setter
    def mode_init_a(self, new_mode_init_a):
        self.__mode_init_a = new_mode_init_a

    @property
    def do_span(self):
        return self.__do_span

    @do_span.setter
    def do_span(self, new_do_span):
        self.__do_span = new_do_span

    @property
    def is_serial_mode(self):
        return self.__is_serial_mode

    @is_serial_mode.setter
    def is_serial_mode(self, new_is_serial_mode):
        self.__is_serial_mode = new_is_serial_mode

    @property
    def is_basic_mode(self):
        return self.__is_basic_mode

    @is_basic_mode.setter
    def is_basic_mode(self, new_is_basic_mode):
        self.__is_basic_mode = new_is_basic_mode

    @property
    def is_comp_mode(self):
        return self.__is_comp_mode

    @is_comp_mode.setter
    def is_comp_mode(self, new_is_comp_mode):
        self.__is_comp_mode = new_is_comp_mode

    @property
    def is_cal_mode(self):
        return self.__is_cal_mode

    @is_cal_mode.setter
    def is_cal_mode(self, new_is_cal_mode):
        self.__is_cal_mode = new_is_cal_mode

    @property
    def is_ver_mode(self):
        return self.__is_ver_mode

    @is_ver_mode.setter
    def is_ver_mode(self, new_is_ver_mode):
        self.__is_ver_mode = new_is_ver_mode

    @property
    def cnt_100ms(self):
        return self.__cnt_100ms

    @cnt_100ms.setter
    def cnt_100ms(self, new_cnt_100ms):
        self.__cnt_100ms = new_cnt_100ms

    @property
    def do_init(self):
        return self.__do_init

    @do_init.setter
    def do_init(self, new_do_init):
        self.__do_init = new_do_init


class pc_setting:
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