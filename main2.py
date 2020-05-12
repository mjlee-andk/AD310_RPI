import time
import serial
import threading

import constants as const
import classes as class_caller
import commands as command

from tkinter import *
from tkinter import ttk

exit_thread = False  # 쓰레드 종료용 변수


# TODO
# 본 쓰레드
def serial_receive_data():
    global exit_thread, sp

    # 쓰레드 종료될때까지 계속 돌림
    while not exit_thread:
        if not sp.is_open or sp is None:
            exit_thread = True
            break

        rx_data = ''
        time.sleep(1)
        try:
            rx_data = sp.readline().decode(const.ENCODING_TYPE)
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
        elif scale.block:
            scale.block = False
            # 수신 데이터 헤더 파악
            read_header(rx_data)
        print(sp.is_open)


# TODO
# 수신 데이터 헤더 파악
def read_header(rx):
    header_1bit = rx[0:0]
    header_2bit = rx[0:1]
    header_3bit = rx[0:2]
    header_5bit = rx[0:4]

    if scale.cf and \
            (header_1bit == '?' or
             header_1bit == 'I' or
             header_2bit == 'CF' or
             header_2bit == 'CS'):
        scale.cf = False
        # cfDataArray[rs.arrayIndexCF] = str;
    elif scale.f and \
            (header_1bit == '?' or
             header_1bit == 'I' or
             header_1bit == 'F' or
             header_3bit == 'VER' or
             header_5bit == 'STOOK' or
             header_5bit == 'SETOK'):
        scale.f = False
        # fDataArray[rs.arrayIndexF] = str;
    else:
        if header_2bit == 'ST':
            scale.is_stable = True
            scale.is_hold = False
            scale.is_hg = False
            scale.is_net = True if rx[3:4] == 'NT' else False
            scale.display_msg = make_format(rx)
        elif header_2bit == 'US':
            scale.is_stable = False
            scale.is_hold = False
            scale.is_hg = False
            scale.is_net = True if rx[3:4] == 'NT' else False
            scale.display_msg = make_format(rx)
        elif header_2bit == 'HD':
            scale.is_stable = False
            scale.is_hold = True
            scale.is_hg = False
            scale.is_net = False
            scale.display_msg = make_format(rx)
        elif header_2bit == 'HG':
            scale.is_stable = False
            scale.is_hold = True
            scale.is_hg = True
            scale.is_net = False
            scale.display_msg = make_format(rx)
        elif header_2bit == 'OL':
            scale.is_stable = False
            scale.is_hold = False
            scale.is_hg = False
            scale.is_net = False
            scale.display_msg = '   .  '
        else:
            scale.is_stable = False
            scale.is_hold = False
            scale.is_hg = False
            scale.is_net = False
            scale.is_zero = False
            scale.block = True
            rx = ''
        rx = ''
    scale.block = True


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

    # TODO
    # 단위값 길이가 무조건 2인 경우 아래 로직으로 진행
    if unit[1:1] == 't':
        scale.unit = const.UNIT_T
    else:
        scale.unit = const.UNIT_G
        if unit[0:0] != '':
            scale.unit = const.UNIT_KG

    # 단위값 길이가 가변적일 경우 아래 로직으로 진행
    if len(unit) == 2:
        scale.unit = const.UNIT_KG
    else:
        scale.unit = const.UNIT_G
        if unit == 't':
            scale.unit = const.UNIT_T

    return result


def btn_click_on_off():
    global exit_thread, sp
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
            command.set_communication_mode(sp, const.STREAM_MODE, scale)
            # TODO
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
            command.set_communication_mode(sp, const.STREAM_MODE, scale)
            # TODO
            # 버튼 OFF 표시

        except serial.SerialException:
            print('Can not open port.')

        return

    # ON 상태
    try:
        exit_thread = True
        # 스트림 모드로 종료
        command.set_communication_mode(sp, const.STREAM_MODE, scale)
        # 포트 닫기
        sp.close()
        # TODO
        # 버튼 ON 표시, 상태 표시 라벨 전부 초기화
        # 표시창 OFF 표시
    except serial.SerialException:
        print('Can not open port.')


# TODO
def show_message():
    global sp
    if scale.is_stream_mode:
        # 응답 없이 3초 이상 지난 경우
        if scale.waiting_sec >= 3:
            scale.display_msg = '------'
            # 스트림모드, 설정모드 선택 안되도록 설정
            # 라디오버튼 비활성화
        else:
            # 스트림모드, 설정모드 선택 되도록 설정
            # 라디오버튼 활성화
            if psc.baudrate == 19200 or psc.baudrate == 38400:
                sp.flushInput()
        # 안정
        True if scale.is_stable else False
        # 영점
        True if scale.is_zero else False
        # Net
        True if scale.is_net else False
        # HOLD 마크
        if scale.is_hg:
            '''
                if (cnt100ms++ < 4)
                    {
                        lblHold_.Visible = true;
                    }
                    else
                    {
                        lblHold_.Visible = false;
                        if (cnt100ms > 8)
                        {
                            cnt100ms = 0;
                        }
                    }
            '''
        else:
            True if scale.is_hold else False

        if scale.unit == const.UNIT_KG:
            # kg 글자 변경
            return
        elif scale.unit == const.UNIT_G:
            # g 글자 변경
            return
        elif scale.unit == const.UNIT_T:
            # t 글자 변경
            return
    elif scale.init_f:
        # 스트림모드, 설정모드 선택 안되도록 설정
        # 라디오버튼 활성화
        return


psc = class_caller.pc_setting()
scale = class_caller.scale_flag()

# 포트 열기
sp = serial.Serial(
    port='COM5',
    baudrate=2400,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    xonxoff=False,
    timeout=0)

# btn_click_onoff(None)


# 화면 구성
window = Tk()
window.title('AD310_RPI')
window.geometry('750x700')

# entry_data_display = Entry(window, width=20, readonlybackground='white', fg='red')
# entry_data_display.insert(0, '334')
# entry_data_display.configure(state='readonly')
# entry_data_display.pack()

label_stable = Label(window, width=10, height=5, text='STABLE', fg='greenyellow', bg='lightslategray', relief='flat')
label_stable.pack()

label_hold = Label(window, width=10, height=5, text='HOLD', fg='red', relief='flat')
label_hold.pack()

label_zero = Label(window, width=10, height=5, text='ZERO', fg='red', relief='flat')
label_zero.pack()

label_net = Label(window, width=10, height=5, text='NET', fg='red', relief='flat')
label_net.pack()


btn_clear_tare = Button(window, width=10, height=5, text='CLEAR\nTARE', command=lambda: command.set_clear_tare(sp, scale))
btn_clear_tare.pack()

btn_zero_tare = Button(window, width=10, height=5, text='ZERO\nTARE', command=lambda: command.set_zero_tare(sp, scale))
btn_zero_tare.pack()

btn_gross_net = Button(window, width=10, height=5, text='GROSS\nNET', command=lambda: command.set_gross_net(sp, scale))
btn_gross_net.pack()

btn_hold = Button(window, width=10, height=5, text='HOLD', command=lambda: command.set_hold(sp, scale))
btn_hold.pack()

btn_on_off = Button(window, width=10, height=5, text='ON', command=lambda: btn_click_on_off())
btn_on_off.pack()

btn_print = Button(window, width=10, height=5, text='PRINT')
btn_print.pack()

window.mainloop()
