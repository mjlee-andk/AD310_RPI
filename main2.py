# -*- coding: utf-8 -*-

import time
import serial
import serial.tools.list_ports
import threading

import constants as const
import classes as class_caller
import commands as command

from tkinter import *
import tkinter.font as tkFont

from tkinter import ttk

exit_thread = False  # 쓰레드 종료용 변수
display_timer = None  # 디스플레이 타이머
waiting_timer = None  # 대기시간 타이머
sp = None  # 시리얼포트
received_data_thread = None

psc = class_caller.pc_setting()
scale = class_caller.scale_flag()

# 화면 구성
window = Tk()
window.title('AD310_RPI')
# window.attributes('-fullscreen', True)
window.geometry('800x400')

window.configure(bg=const.color_lightslategray)

# label
label_frame = Frame(window, width=100, height=323, pady=20, bg=const.color_lightslategray)
label_frame.pack(side='left', anchor='w')

label_row_frame1 = Frame(label_frame, width=100, height=70)
label_row_frame1.pack()

label_row_frame2 = Frame(label_frame, width=100, height=70)
label_row_frame2.pack()

label_row_frame3 = Frame(label_frame, width=100, height=70)
label_row_frame3.pack()

label_row_frame4 = Frame(label_frame, width=100, height=70)
label_row_frame4.pack()

label_style = tkFont.Font(size=15, family=const.font_clear_gothic, weight='bold')

label_stable = Label(label_row_frame1, width=const.label_width, height=const.label_height, text='STABLE',
                     bg=const.color_lightslategray, fg=const.color_white, font=label_style)
label_stable.pack()

label_hold = Label(label_row_frame2, width=const.label_width, height=const.label_height, text='HOLD',
                   bg=const.color_lightslategray, fg=const.color_white, font=label_style)
label_hold.pack()

label_zero = Label(label_row_frame3, width=const.label_width, height=const.label_height, text='ZERO',
                   bg=const.color_lightslategray, fg=const.color_white, font=label_style)
label_zero.pack()

label_net = Label(label_row_frame4, width=const.label_width, height=const.label_height, text='NET',
                  bg=const.color_lightslategray, fg=const.color_white, font=label_style)
label_net.pack()

# button
btn_frame = Frame(window, padx=10, bg=const.color_lightslategray)
btn_frame.pack(side='right')

btn_row_frame1 = Frame(btn_frame, pady=5, bg=const.color_lightslategray)
btn_row_frame1.pack()

btn_row_frame2 = Frame(btn_frame, pady=5, bg=const.color_lightslategray)
btn_row_frame2.pack()

btn_row_frame3 = Frame(btn_frame, pady=5, bg=const.color_lightslategray)
btn_row_frame3.pack()

btn_clear_tare = Button(btn_row_frame1, width=const.btn_width, height=const.btn_height, text='CLEAR\nTARE',
                        command=lambda: command.set_clear_tare(sp, scale))
btn_clear_tare.pack(side='left')

btn_zero_tare = Button(btn_row_frame1, width=const.btn_width, height=const.btn_height, text='ZERO\nTARE',
                       command=lambda: command.set_zero_tare(sp, scale))
btn_zero_tare.pack(side='right')

btn_gross_net = Button(btn_row_frame2, width=const.btn_width, height=const.btn_height, text='GROSS\nNET',
                       command=lambda: command.set_gross_net(sp, scale))
btn_gross_net.pack(side='left')

btn_hold = Button(btn_row_frame2, width=const.btn_width, height=const.btn_height, text='HOLD',
                  command=lambda: command.set_hold(sp, scale))
btn_hold.pack(side='right')

btn_on_off = Button(btn_row_frame3, width=const.btn_width, height=const.btn_height, text='ON',
                    command=lambda: btn_click_on_off())
btn_on_off.pack(side='left')

btn_print = Button(btn_row_frame3, width=const.btn_width, height=const.btn_height, text='PRINT')
btn_print.pack(side='right')

# logo
logo_frame = Frame(window, padx=10, pady=10, bg=const.color_lightslategray)
logo_frame.pack(anchor='w')

and_logo = PhotoImage(file='Resources/and_logo.PNG')
label_logo = Label(logo_frame, image=and_logo, bg=const.color_lightslategray)
label_logo.pack(side='left')

label_name_style = tkFont.Font(size=20, family=const.font_clear_gothic)
label_name = Label(logo_frame, text='AD310-RPI', bg=const.color_lightslategray, fg=const.color_white, font=label_name_style)
label_name.pack(side='left')

# display
display_frame = Frame(window, padx=10, pady=10, bg=const.color_lightslategray)
display_frame.pack(anchor='w')

display_msg_style = tkFont.Font(size=95, family='SegmentA1')
display_msg = Label(display_frame, width=5, height=1, text='off', bg=const.color_white, font=display_msg_style)
display_msg.pack(side='left')

scale_unit_style = tkFont.Font(size=35, family=const.font_clear_gothic)
scale_unit = Label(display_frame, width=2, height=1, text='kg', bg=const.color_lightslategray, font=scale_unit_style, fg=const.color_lightslategray)
scale_unit.pack(side='bottom')


# comboExample = ttk.Combobox(window,
#                             values=[
#                                 "January",
#                                 "February",
#                                 "March",
#                                 "April"])
#
# comboExample.pack()
#
#
# def test(event):
#     print(comboExample.get())
#
# comboExample.bind("<<ComboboxSelected>>", test)


def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

# TODO
# 본 쓰레드
def serial_received_data(sp):
    global exit_thread

    t = threading.currentThread()
    while getattr(t, 'do_run', True):
        if not sp.is_open or sp is None:
            exit_thread = True
            break

        rx_data = ''
        time.sleep(0.1)
        try:
            rx_data = sp.readline().decode(const.ENCODING_TYPE)
            # print('rxdata_ ' + rx_data)
            scale.waiting_sec = 0
        except:
            rx_data = ''

        if rx_data == 'EER':
            print('Log: EER')
            rx_data = ''
            # do init = true
            # init a 표시
        elif rx_data == 'INCOK' or rx_data == 'INFOK':
            print('Log: INCOK or INFOK')
            rx_data = ''
            # init f = true
            # ------ 표시
            return
        elif scale.block:
            # print('Log: block = True')
            scale.block = False
            # 수신 데이터 헤더 파악
            read_header(rx_data)

    # # 쓰레드 종료될때까지 계속 돌림
    # while not exit_thread:
    #     if not sp.is_open or sp is None:
    #         exit_thread = True
    #         break
    #
    #     rx_data = ''
    #     time.sleep(1)
    #     try:
    #         rx_data = sp.readline().decode(const.ENCODING_TYPE)
    #         # print(rx_data)
    #         scale.waiting_sec = 0
    #     except:
    #         rx_data = ''
    #
    #     if rx_data == 'EER':
    #         print('Log: EER')
    #         rx_data = ''
    #         # do init = true
    #         # init a 표시
    #     elif rx_data == 'INCOK' or rx_data == 'INFOK':
    #         print('Log: INCOK or INFOK')
    #         rx_data = ''
    #         # init f = true
    #         # ------ 표시
    #         return
    #     elif scale.block:
    #         # print('Log: block = True')
    #         scale.block = False
    #         # 수신 데이터 헤더 파악
    #         read_header(rx_data)
    #
    #     # print('Log: Nothing')


# TODO
# 수신 데이터 헤더 파악
def read_header(rx):

    if len(rx) < 18:
        scale.block = True
        return

    header_1bit = rx[0:1]
    header_2bit = rx[0:2]
    header_3bit = rx[0:3]
    header_5bit = rx[0:5]

    # print(rx)
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
            scale.is_net = True if rx[3:5] == 'NT' else False
            scale.display_msg = make_format(rx)
        elif header_2bit == 'US':
            scale.is_stable = False
            scale.is_hold = False
            scale.is_hg = False
            scale.is_net = True if rx[3:5] == 'NT' else False
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
    # print('display_msg:' + scale.display_msg)


# 데이터 포맷 형성
def make_format(data):
    result = ''
    if data == '' or data is None:
        return result

    # 부호 포함 계량값
    value = data[6:14]
    # 단위값
    unit = data[14:16]

    # 제로 서프레스
    if '.' in value:
        result = str(float(value))
    else:
        result = str(int(value))

    if '0' in result[0]:
        scale.is_zero = True
    else:
        scale.is_zero = False


    # TODO
    # # 단위값 길이가 무조건 2인 경우 아래 로직으로 진행
    # if unit[1:2] == 't':
    #     scale.unit = const.UNIT_T
    # else:
    #     scale.unit = const.UNIT_G
    #     if unit[0:1] != '':
    #         scale.unit = const.UNIT_KG



    # 단위값 길이가 가변적일 경우 아래 로직으로 진행
    if len(unit) == 2:
        scale.unit = const.UNIT_KG
    else:
        scale.unit = const.UNIT_G
        if unit == 't':
            scale.unit = const.UNIT_T

    return result


def btn_click_on_off():
    global exit_thread, received_data_thread, display_timer, waiting_timer, sp

    if sp is None:
        try:
            # 포트 열기
            sp = serial.Serial(
                port='/dev/ttyUSB0',
                # port='COM3',
                baudrate=2400,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                xonxoff=False,
                timeout=0)
            received_data_thread = threading.Thread(target=serial_received_data, args=(sp,))
            received_data_thread.start()
            print('init thread')
            print(received_data_thread)

            scale.display_msg = ''
            scale.block = True

            scale.display_msg = ''
            scale.block = True
            scale.waiting_sec = 0
            # TODO
            # groupBoxPC.Enabled = false; -> PC설정 안되도록
            # groupBoxRS.Enabled = false;
            # groupBoxBasic.Enabled = false;
            # groupBoxComp.Enabled = false;
            # groupBoxCal.Enabled = false;
            # groupBoxBasic2.Enabled = false;
            # textBox1.Clear();
            # textBox1.TextAlign = HorizontalAlignment.Right;

            display_timer = display_timer_tick()
            waiting_timer_tick()

            # 스트림 모드 날리기
            command.set_communication_mode(sp, const.STREAM_MODE, scale)
            # TODO
            # 버튼 OFF 표시
            btn_on_off.configure(text='OFF')
            # radioButton1.Enabled = true;
            # radioButton2.Enabled = true;
            # radioButton1.Checked = true;
            return
        except serial.SerialException:
            print('Can not open port.')
            return

    if not sp.is_open:
        try:
            exit_thread = False

            sp.open()
            received_data_thread = threading.Thread(target=serial_received_data, args=(sp,))
            received_data_thread.start()
            print('sp is open!!')
            print(received_data_thread)

            scale.display_msg = ''
            scale.block = True

            scale.display_msg = ''
            scale.block = True
            scale.waiting_sec = 0
            # TODO
            # groupBoxPC.Enabled = false; -> PC설정 안되도록
            # groupBoxRS.Enabled = false;
            # groupBoxBasic.Enabled = false;
            # groupBoxComp.Enabled = false;
            # groupBoxCal.Enabled = false;
            # groupBoxBasic2.Enabled = false;
            # textBox1.Clear();
            # textBox1.TextAlign = HorizontalAlignment.Right;

            display_timer = display_timer_tick()
            waiting_timer_tick()

            # 스트림 모드 날리기
            command.set_communication_mode(sp, const.STREAM_MODE, scale)
            # TODO
            # 버튼 OFF 표시
            btn_on_off.configure(text='OFF')
            # radioButton1.Enabled = true;
            # radioButton2.Enabled = true;
            # radioButton1.Checked = true;

            return
        except serial.SerialException:
            print('Can not open port.')
            return

    if sp.is_open:
        # ON 상태
        try:
            exit_thread = True
            print(received_data_thread)
            received_data_thread.do_run = False
            received_data_thread.join()
            # 스트림 모드로 종료
            command.set_communication_mode(sp, const.STREAM_MODE, scale)
            # 디스플레이 타이머 종료
            display_timer.set()
            # if display_timer is not None:
            #     display_timer.cancel()

            # 대기시간 타이머 종료
            if waiting_timer is not None:
                scale.waiting_sec = 0
                waiting_timer.cancel()

            # 포트 닫기
            sp.close()
            # TODO
            # 버튼 ON 표시, 상태 표시 라벨 전부 초기화
            btn_on_off.configure(text='ON')
            label_stable.configure(fg=const.color_white)
            label_hold.configure(fg=const.color_white)
            label_zero.configure(fg=const.color_white)
            label_net.configure(fg=const.color_white)
            scale_unit.configure(fg=const.color_lightslategray, text='kg')
            scale.display_msg = 'off'
            # 표시창 OFF 표시
            display_msg.configure(text=scale.display_msg)
        except serial.SerialException:
            print('Can not open port.')


# TODO
@setInterval(0.1)
def display_timer_tick():
    global display_timer, sp
    if scale.is_stream_mode:
        # 응답 없이 3초 이상 지난 경우
        if scale.waiting_sec >= 3:
            scale.display_msg = '------'
            # dispMessage() 함수기능필요
            # 스트림모드, 설정모드 선택 안되도록 설정
            # 라디오버튼 비활성화
        else:
            display_msg.configure(text=scale.display_msg)
            # dispMessage() 함수기능필요
            # 스트림모드, 설정모드 선택 되도록 설정
            # 라디오버튼 활성화
            if psc.baudrate == 19200 or psc.baudrate == 38400:
                if sp is not None:
                    sp.flushInput()
        # 안정
        if scale.is_stable:
            label_stable.configure(fg=const.color_greenyellow)
        else:
            label_stable.configure(fg=const.color_white)
        # 영점
        if scale.is_zero:
            label_zero.configure(fg=const.color_greenyellow)
        else:
            label_zero.configure(fg=const.color_white)
        # Net
        if scale.is_net:
            label_net.configure(fg=const.color_greenyellow)
        else:
            label_net.configure(fg=const.color_white)

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
            if scale.is_hold:
                label_hold.configure(fg=const.color_greenyellow)
            else:
                label_hold.configure(fg=const.color_white)

        if scale.unit == const.UNIT_KG:
            # kg 글자 변경
            # print('kg 글자 변경')
            scale_unit.configure(fg=const.color_white, text='kg')
        elif scale.unit == const.UNIT_G:
            # g 글자 변경
            # print('g 글자 변경')
            scale_unit.configure(fg=const.color_white, text='g')
        elif scale.unit == const.UNIT_T:
            # t 글자 변경
            # print('t 글자 변경')
            scale_unit.configure(fg=const.color_white, text='t')
    elif scale.init_f:
        print('init_f')
        # 스트림모드, 설정모드 선택 안되도록 설정
        # 라디오버튼 활성화
        # print('스트림모드, 설정모드 선택 안되도록 설정')

    # display_timer = threading.Timer(0.1, display_timer_tick)
    # display_timer.start()


@setInterval(1)
def waiting_timer_tick():
    global waiting_timer
    if scale.is_stream_mode:
        scale.waiting_sec += 1

    # print('waiting_timer_tick')
    # print('waiting_sec: ' + str(scale.waiting_sec))
    # waiting_timer = threading.Timer(1, waiting_timer_tick)
    # waiting_timer.start()


def init_timer_tick(sp):
    if scale.mode_init_f:
        # TODO
        # timerInit.Stop();
        if not scale.init_f:
            # MessageBox.Show("응답 오류!\r\n연결 상태 확인!", "오류", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return

        scale.init_f = False

        sp.close()
        # TODO
        # 통신 설정 변경 적용
        # cmbBaudrate.Text = "2400";
        # cmbDatabits.Text = "7";
        # cmbParity.Text = "Even";
        # cmbStopbits.Text = "1";
        # cmbTerminator.Text = "CRLF";
        psc.baudrate = 2400
        psc.databits = 7
        psc.parity = 'EVEN'
        psc.stopbits = 1
        psc.terminator = 'CRLF'
        sp.open()

        scale.display_msg = ''
        scale.block = True
        scale.mode_init_f = False
        # TODO
        # textBox1.TextAlign = HorizontalAlignment.Right; -> 표시부 오른쪽 정렬
        # next = 1;
        # radioButton1.Checked = true;  -> 스트림 모드 체크
    elif scale.mode_init_a:
        # TODO
        # timerInit.Stop();
        if not scale.init_f:
            # MessageBox.Show("응답 오류!\r\n연결 상태 확인!", "오류", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return

        scale.init_f = False

        sp.close()
        # TODO
        # 통신 설정 변경 적용
        # cmbBaudrate.Text = "2400";
        # cmbDatabits.Text = "7";
        # cmbParity.Text = "Even";
        # cmbStopbits.Text = "1";
        # cmbTerminator.Text = "CRLF";
        psc.baudrate = 2400
        psc.databits = 7
        psc.parity = 'EVEN'
        psc.stopbits = 1
        psc.terminator = 'CRLF'
        sp.open()

        scale.display_msg = ''
        scale.block = True
        scale.mode_init_a = False
        # TODO
        # textBox1.TextAlign = HorizontalAlignment.Right; -> 표시부 오른쪽 정렬
        # radioButton1.Checked = true;  -> 스트림 모드 체크


def init_flag(mode):
    if mode == const.SERIAL:
        scale.f = False
        scale.read = False
        scale.write = False
        # TODO
        # serialMode = false;
        # button7.Enabled = true; -> 통신 설정 탭 설정 불러오기
    elif mode == const.BASIC:
        scale.f = False
        scale.cf = False
        scale.read = False
        scale.write = False
        # TODO
        # basicMode = false;
        # button7.Enabled = true; -> 기본 설정 탭 설정 불러오기
    elif mode == const.COMP:
        scale.f = False
        scale.read = False
        scale.write = False
        # TODO
        # compMode = false;
        # button10.Enabled = true; -> 외부 출력 탭 설정 불러오기
    elif mode == const.CAL:
        scale.cf = False
        scale.read = False
        scale.write = False
        # TODO
        # doCalMode = false;
        # button17.Enabled = true; -> 교정 탭 정보 불러오기
        # lblResult0.ForeColor = Color.Silver;
        # lblResultCalF.ForeColor = Color.Silver;
    # TODO
    # next = 1;
    # modeTimer.Stop();


# # 포트 열기
# sp = serial.Serial(
#     port='COM5',
#     baudrate=2400,
#     bytesize=serial.EIGHTBITS,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     xonxoff=False,
#     timeout=0)

# btn_click_on_off(None)


def main():
    global window

    window.mainloop()


if __name__ == '__main__':
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
        print(p.device)
    main()
