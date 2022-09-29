import fpdf
from utils.time import timestamp_to_datetime


def create_erasure_info(data, json_data):
    previous_os = json_data['ProductVersion']
    new_os = data['new_os']
    status = data['status']['general'].upper()
    duration = data['times']['end'] - data['times']['start']
    start_end = str(timestamp_to_datetime(data['times']['start'])) + '/' + str(timestamp_to_datetime(data['times']['end']))
    data = """Previous OS: {previous_os}
New OS: {new_os}
Duration: {duration}s
Start/End Time: {start_end}
""".format(previous_os = previous_os, new_os = new_os, duration = duration, start_end = start_end)
    if status == "SUCCESS":
        status = "ERASED"
    
    # status = "ERASED"
    
    status = ['Status:', status]
    return status, data


def create_hardware_info(info_json):
    HARDWARE_KEY = {'ActivationState': True,'BluetoothAddress''BuildVersion': True,  
    'CPUArchitecture': True, 'CertID': True, 'ChipID': True, 'ChipSerialNo': True, 
    'DeviceClass': True, 'DeviceColor': True, 'DeviceName': True,'DieID': True, 
    'EthernetAddress': True,  'FirmwareVersion': True,  'ModelNumber': True, 
    'PartitionType': True, 'PasswordProtected': True,  'PhoneNumber': True,  
    'ProductName': True,'ProductType': True, 'ProductVersion': True,'RegionInfo': True,
    'SIMGID2': True,'SerialNumber': True, 'TimeZone': True, 'TimeZoneOffsetFromUTC': True,
    'WiFiAddress': True,  'WirelessBoardSerialNumber': True}
    data = ""
    for key, value in info_json.items():
        print(key, value)
        try:
            if HARDWARE_KEY[key] == True:
                obj = key + ': ' + value + '\n'
                data += obj
        except:
            pass
    return data


class PDF(fpdf.FPDF):
    def footer(self) -> None:
        pass
        # self.set_y(-25)
        # self.set_font('Arial', 'I', 8)
        # self.cell(0, 10, 'I hereby state that the data erasure process has been carried out in accordance with the given instructions.', 0, 0, 'L')    


def make_report(name, data, info_json):
    title = "Data Erasure Report"
    erasure_results_title = 'Erasure Results'
    hardware_detail_title = "Hardware Details"
    # battery_info_title = 'Battery Information'
    
    # make data
    status_erasure, text_erasure = create_erasure_info(data, info_json)
    text_hardware = create_hardware_info(info_json)


    pdf = PDF()
    pdf.add_font("NotoSans", style="", fname=r"./fonts/NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSans", style="B", fname=r"./fonts/NotoSans-Bold.ttf", uni=True)
    pdf.add_font("NotoSans", style="I", fname=r"./fonts/NotoSans-Italic.ttf", uni=True)
    pdf.add_font("NotoSans", style="BI", fname=r"./fonts/NotoSans-BoldItalic.ttf", uni=True)
    pdf.add_page()
    
    # logo
    pdf.image('./images/logo.jpeg', 120, 10, 100)

    # add header image
    pdf.image('./images/header_bg.png', x = 0, y = 4, w = 210, h = 8, type = '', link = '')
    

    ybefore = pdf.get_y()
    pdf.set_xy(pdf.l_margin + 5, ybefore)
    # title
    pdf.set_font('NotoSans', '', 20)
    pdf.cell(0, 40, txt = title)
    pdf.ln()
    
    # Erasure Results
    ybefore = pdf.get_y()
    pdf.set_xy(pdf.l_margin + 5, ybefore-10)
    pdf.set_font('NotoSans', '', 13)
    pdf.cell(0, 10, txt = erasure_results_title)
    pdf.ln()
    
    ybefore = pdf.get_y()
    pdf.set_xy(pdf.l_margin + 5, ybefore)
    pdf.set_text_color(128)
    pdf.set_font('NotoSans', '', 8)
    ybefore = pdf.get_y()
    pdf.set_xy(pdf.l_margin + 5, ybefore)
    pdf.cell(0,5, status_erasure[0])
    
    # status_erasure[1] = 'SUCCESS'
    if status_erasure[1] == 'ERASED': 
        pdf.set_text_color(170,219,30)
    else:
        pdf.set_text_color(205,0,26)
    pdf.set_xy(pdf.l_margin + 15, ybefore)
    pdf.cell(0,5, status_erasure[1])
    pdf.ln()
    
    
    ybefore = pdf.get_y()
    pdf.set_text_color(128)
    pdf.set_xy(pdf.l_margin + 5, ybefore)
    pdf.multi_cell(0, 5, text_erasure)
    
    
    # Hardware
    ybefore = pdf.get_y()
    pdf.set_xy(pdf.l_margin + 5, ybefore)
    pdf.set_font('NotoSans', '', 13)
    pdf.set_text_color(0)
    pdf.cell(0, 13, txt = hardware_detail_title)
    pdf.ln()
    
    ybefore = pdf.get_y()
    pdf.set_xy(pdf.l_margin + 5, ybefore)
    pdf.set_text_color(128)
    pdf.set_font('NotoSans', '', 8)
    pdf.multi_cell(0, 5, text_hardware)
    pdf.ln()
    
    

    pdf.set_xy(pdf.l_margin + 5, 240)
    pdf.set_font('NotoSans', 'B', 8)
    pdf.cell(0, 10, 'I hereby state that the data erasure process has been carried out in accordance with the given instructions.', 0, 0, 'L')    
    
    
    ybefore = pdf.get_y()
    
    pdf.set_text_color(128)
    pdf.line(pdf.l_margin + 5, ybefore+20, pdf.l_margin+ 80, ybefore+20)
    pdf.line(pdf.l_margin + 100, ybefore+20, pdf.l_margin+ 160, ybefore+20)
    
    pdf.set_xy(pdf.l_margin + 20, ybefore + 19)
    pdf.set_font('NotoSans', '', 9)
    pdf.set_text_color(128)
    pdf.cell(0, 10, 'DATA ERASURE OPERATOR', 0, 0, '')
    ybefore = pdf.get_y()
    pdf.set_font('NotoSans', '', 9)
    pdf.set_text_color(128)
    pdf.set_xy(120 + pdf.l_margin, ybefore)
    pdf.cell(0, 10, 'SUPERVISOR', 0,0, '')
    
    
    
    # pdf.multi_cell(0, 5, col1)
    # pdf.set_xy(100 + pdf.l_margin, ybefore)
    # pdf.multi_cell(0, 5, col2)
    
    # buf = io.StringIO(data['battery_info'])
    # buf.readline()
    # col1, col2 = "", ""
    # for idx, line in enumerate(buf):
    #     if idx%2==0:
    #         col1 += line
    #     else:
    #         col2 += line
    # print(col1, col2)  
         
    # # battery info
    # pdf.set_font('NotoSans', '', 13)
    # pdf.set_text_color(0)
    # pdf.cell(0, 10, txt = battery_info_title)
    # pdf.ln()
    # pdf.set_text_color(128)
    # pdf.set_font('NotoSans', '', 8)
    
    # ybefore = pdf.get_y()
    # pdf.set_xy(pdf.l_margin, ybefore)
    
    # pdf.multi_cell(0, 5, col1)
    # pdf.set_xy(100 + pdf.l_margin, ybefore)
    # pdf.multi_cell(0, 5, col2)
    

    pdf.output("./storage/pdf/{}.pdf".format(name))  



