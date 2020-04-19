from ctypes import *
from ctypes.wintypes import *
import uuid, struct
from process_defines import *


winproxy = CDLL('C:\\WINDOWS\\system32\\wintrust.dll')


IID_PACK = "<I", "<H", "<H", "<B", "<B", "<B", "<B", "<B", "<B", "<B", "<B"


def get_IID_from_raw(raw):
    s = b"".join([struct.pack(i, j) for i, j in zip(IID_PACK, raw)])
    return ctypes.create_string_buffer(s)


WINTRUST_ACTION_GENERIC_VERIFY_V2_RAW = (0xaac56b, 0xcd44,  0x11d0, 0x8c, 0xc2, 0x0, 0xc0, 0x4f, 0xc2, 0x95, 0xee)

WINTRUST_ACTION_GENERIC_VERIFY_V2_STR = get_IID_from_raw(WINTRUST_ACTION_GENERIC_VERIFY_V2_RAW)
WINTRUST_ACTION_GENERIC_VERIFY_V2 = GUID.from_address(ctypes.addressof(WINTRUST_ACTION_GENERIC_VERIFY_V2_STR))
WTD_STATEACTION_CLOSE = 0x00000002


def check_signature(filename):
	file_data = WINTRUST_FILE_INFO()
	file_data.cbStruct = ctypes.sizeof(WINTRUST_FILE_INFO)
	file_data.pcwszFilePath = filename
	file_data.hFile = None
	file_data.pgKnownSubject = None
	
	WVTPolicyGUID =  WINTRUST_ACTION_GENERIC_VERIFY_V2

	win_trust_data = WINTRUST_DATA()
	win_trust_data.cbStruct = ctypes.sizeof(WINTRUST_DATA)
	win_trust_data.pPolicyCallbackData = None
	win_trust_data.pSIPClientData = None
	win_trust_data.dwUIChoice = 2
	win_trust_data.fdwRevocationChecks = 0
	win_trust_data.dwUnionChoice = 1
	win_trust_data.dwStateAction = 0x00000001
	win_trust_data.hWVTStateData = None
	win_trust_data.pwszURLReference = None
	win_trust_data.dwUIContext = 0
	
	#win_trust_data.dwProvFlags  = 0x1000 + 0x10 + 0x800
	win_trust_data.tmp_union.pFile = ctypes.pointer(file_data)

	x = winproxy.WinVerifyTrust(None, ctypes.byref(WVTPolicyGUID), ctypes.byref(win_trust_data))

	win_trust_data.dwStateAction = WTD_STATEACTION_CLOSE
	winproxy.WinVerifyTrust(None, ctypes.byref(WVTPolicyGUID), ctypes.byref(win_trust_data))
	if(x == 0):
		return True
	return False
