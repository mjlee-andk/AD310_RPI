import constants as const


def set_clear_tare(sp, scale):
    print('what the')
    if sp is None or scale is None:
        return
    command = 'CT' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))
    scale.display_msg = 'clear tare'
    print(scale.display_msg)


def set_zero_tare(sp, scale):
    if sp is None or scale is None:
        return
    command = 'MZT' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))
    scale.display_msg = 'zero tare'


def set_gross_net(sp, scale):
    if sp is None or scale is None:
        return
    
    if scale.is_net:
        # 순중량일 때
        command = 'MG' + scale.terminator
    else:
        # 총중량일 때
        command = 'MN' + scale.terminator

    sp.write(command.encode(const.ENCODING_TYPE))


def set_hold(sp, scale):
    if sp is None or scale is None:
        return
    
    # 홀드 on일때
    if scale.is_hold:
        command = 'HC' + scale.terminator
    # 홀드 off일때
    else:
        command = 'HS' + scale.terminator

    sp.write(command.encode(const.ENCODING_TYPE))


# 통신 모드 변경
def set_communication_mode(sp, val, scale):
    if sp is None or scale is None:
        return

    command = 'F206,' + str(val) + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))


'''
통신 설정
'''
def get_baudrate(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F201' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))


def get_databits(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F202' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_parity(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F203' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_stopbits(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F204' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_terminator(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F205' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))


# 기본 설정
def get_digital_filter(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F001' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_hold_mode(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F002' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_average_time(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F003' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_zero_range(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF05' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_tracking_time(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF06' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_tracking_range(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF07' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_power_on_zero(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF08' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))


# 외부 출력
def get_print_condition(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F101' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_comparator(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F102' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_comparator_mode(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F103' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_near_zero(sp, scale):
    if sp is None or scale is None:
        return

    command = '?F104' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))


# 교정
def get_capa(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF03' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_div(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF02' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_decimal_point(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF01' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_unit(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF09' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def get_span(sp, scale):
    if sp is None or scale is None:
        return

    command = '?CF04' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def do_cal_0(sp, scale):
    if sp is None or scale is None:
        return

    command = 'CZ' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

def do_cal_f(sp, scale):
    if sp is None or scale is None:
        return

    command = 'CS' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

# 버전 확인
def get_ver(sp, scale):
    if sp is None or scale is None:
        return

    command = '?VER' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))


# F펑션 초기화
def init_f_function(sp, scale):
    if sp is None or scale is None:
        return

    command = 'INF' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))


# 모든 설정 초기화
def init_a_function(sp, scale):
    if sp is None or scale is None:
        return

    command = 'INC' + scale.terminator
    sp.write(command.encode(const.ENCODING_TYPE))

