from ctypes import *
from ctypes.wintypes import *
import array
import wintrust
from process_defines import *

allProcesses = []
kernel32 = windll.kernel32


def ProcessList():
	CreateToolhelp32Snapshot = kernel32.CreateToolhelp32Snapshot
	Process32First = kernel32.Process32First
	Process32Next = kernel32.Process32Next
	CloseHandle = kernel32.CloseHandle
	try:
		hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

		pe32 = PROCESSENTRY32()
		pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)

		ret = Process32First(hProcessSnap, ctypes.pointer(pe32))
		while(ret):			
			allProcesses.append([str(pe32.th32ProcessID), str(pe32.szExeFile)[2:-1] ])
			ret = Process32Next(hProcessSnap, ctypes.pointer(pe32))
	except Exception as e:
		print(e)
	finally:
		CloseHandle(CreateToolhelp32Snapshot)

	return allProcesses


def ModuleList(processId):
	CreateToolhelp32Snapshot = kernel32.CreateToolhelp32Snapshot

	CloseHandle = kernel32.CloseHandle
	Module32First = kernel32.Module32FirstW
	Module32Next = kernel32.Module32NextW
	mod = MODULEENTRY32W()
	mod.dwSize = ctypes.sizeof(MODULEENTRY32W)
	modules = []

	try:
		hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, processId)

		res = Module32First(hSnapshot, ctypes.byref(mod))
		a = kernel32.GetLastError()
		while res:
			versionandcompany = GetFileVersionInfo(str(mod.szExePath))
			temp = ''
			if(versionandcompany[2]):
				temp = 'Trusted'
			else:
				temp = 'Untrusted'
			modules.append([ str(mod.szModule), str(mod.szExePath), versionandcompany[0], versionandcompany[1], temp])
			res = Module32Next(hSnapshot, ctypes.byref(mod))
	except Exception as e:
		print(e)
	finally:
		CloseHandle(hSnapshot)

	return modules

#return version and company name and wintrust
def GetFileVersionInfo(path):
	fixedfileinfo = VS_FIXEDFILEINFO()
	fixedfileinfo.dwSize = ctypes.sizeof(VS_FIXEDFILEINFO)

	size = windll.version.GetFileVersionInfoSizeW(path, None)
	res = ctypes.create_string_buffer(size)
	windll.version.GetFileVersionInfoW(path, 0, size, byref(res))
	lpBuffer = LPVOID(0)
	uLen = UINT(0)

	windll.version.VerQueryValueW(res, "\\VarFileInfo\\Translation", byref(lpBuffer), byref(uLen))
	isTrust = wintrust.check_signature(path)
	if(not uLen.value):
		return '', '', isTrust

	codepages = array.array('H', string_at(lpBuffer.value, uLen.value))
	codepage = tuple(codepages[:2].tolist())

	windll.version.VerQueryValueW(res, ('\\StringFileInfo\\%04x%04x\\' + 'FileVersion') % codepage, byref(lpBuffer), byref(uLen))
	fileversion = wstring_at(lpBuffer.value, uLen.value)

	windll.version.VerQueryValueW(res, ('\\StringFileInfo\\%04x%04x\\' + 'CompanyName') % codepage, byref(lpBuffer), byref(uLen))
	companyname = wstring_at(lpBuffer.value, uLen.value)
	
	

	return fileversion, companyname, isTrust


















