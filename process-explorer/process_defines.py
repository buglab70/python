from ctypes import *
from ctypes.wintypes import *


TH32CS_SNAPPROCESS = 2
TH32CS_SNAPMODULE = 0x00000008
MAX_MODULE_NAME32 = 255

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = (("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", c_size_t),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", c_long),
        ("dwFlags", DWORD),
        ("szExeFile", c_char * MAX_PATH))

class MODULEENTRY32W(ctypes.Structure):
       _fields_ = (('dwSize',        DWORD),
                   ('th32ModuleID',  DWORD),
                   ('th32ProcessID', DWORD),
                   ('GlblcntUsage',  DWORD),
                   ('ProccntUsage',  DWORD),
                   ('modBaseAddr',   LPVOID),
                   ('modBaseSize',   DWORD),
                   ('hModule',       HMODULE),
                   ('szModule',      WCHAR * (MAX_MODULE_NAME32 + 1)),
                   ('szExePath',     WCHAR * MAX_PATH))

class VS_FIXEDFILEINFO(Structure):
    _fields_ = [
        ("dwSignature",         DWORD),
        ("dwStrucVersion",      DWORD),
        ("dwFileVersionMS",     DWORD),
        ("dwFileVersionLS",     DWORD),
        ("dwProductVersionMS",  DWORD),
        ("dwProductVersionLS",  DWORD),
        ("dwFileFlagsMask",     DWORD),
        ("dwFileFlags",         DWORD),
        ("dwFileOS",            DWORD),
        ("dwFileType",          DWORD),
        ("dwFileSubtype",       DWORD),
        ("dwFileDateMS",        DWORD),
        ("dwFileDateLS",        DWORD),
]

class GUID(Structure):
    _fields_ = [
        ("Data1", c_ushort),
        ("Data2", c_ushort),
        ("Data3", c_ushort),
        ("Data4", c_ubyte * 8)
]

class WINTRUST_FILE_INFO(Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("pcwszFilePath", LPCWSTR),
        ("hFile", HANDLE),
        ("pgKnownSubject", POINTER(GUID))
]

class CTL_USAGE(Structure):
    _fields_ = [
        ("cUsageIdentifier", DWORD),
        ("rgpszUsageIdentifier", POINTER(LPSTR)),
    ]

class CRYPTOAPI_BLOB(Structure):
    _fields_ = [
        ("cbData", DWORD),
        ("pbData", POINTER(BYTE)),
    ]


class CRYPT_ALGORITHM_IDENTIFIER(Structure):
    _fields_ = [
        ("pszObjId", LPSTR),
        ("Parameters", CRYPTOAPI_BLOB),
    ]


class CRYPT_ATTRIBUTE(Structure):
    _fields_ = [
        ("pszObjId", LPSTR),
        ("cValue", DWORD),
        ("rgValue", POINTER(CRYPTOAPI_BLOB)),
    ]


class CRYPT_ATTRIBUTES(Structure):
    _fields_ = [
        ("cAttr", DWORD),
        ("rgAttr", POINTER(CRYPT_ATTRIBUTE)),
    ]


class _CTL_ENTRY(Structure):
    _fields_ = [
        ("SubjectIdentifier", CRYPTOAPI_BLOB),
        ("cAttribute", DWORD),
        ("rgAttribute", POINTER(CRYPT_ATTRIBUTE)),
    ]

class CTL_ENTRY(Structure):
    _fields_ = [
        ("SubjectIdentifier", CRYPTOAPI_BLOB),
        ("cAttribute", DWORD),
        ("rgAttribute", POINTER(CRYPT_ATTRIBUTE)),
    ]

class CERT_EXTENSION(Structure):
    _fields_ = [
        ("pszObjId", LPSTR),
        ("fCritical", BOOL),
        ("Value", CRYPTOAPI_BLOB),
    ]

class CTL_INFO(Structure):
    _fields_ = [
        ("dwVersion", DWORD),
        ("SubjectUsage", CTL_USAGE),
        ("ListIdentifier", CRYPTOAPI_BLOB),
        ("SequenceNumber", CRYPTOAPI_BLOB),
        ("ThisUpdate", FILETIME),
        ("NextUpdate", FILETIME),
        ("SubjectAlgorithm", CRYPT_ALGORITHM_IDENTIFIER),
        ("cCTLEntry", DWORD),
        ("rgCTLEntry", POINTER(CTL_ENTRY)),
        ("cExtension", DWORD),
        ("rgExtension", POINTER(CERT_EXTENSION)),
    ]

class CTL_CONTEXT(Structure):
    _fields_ = [
        ("dwMsgAndCertEncodingType", DWORD),
        ("pbCtlEncoded", POINTER(BYTE)),
        ("cbCtlEncoded", DWORD),
        ("pCtlInfo", POINTER(CTL_INFO)),
        ("hCertStore", c_void_p),
        ("hCryptMsg", c_void_p),
        ("pbCtlContent", POINTER(BYTE)),
        ("cbCtlContent", DWORD),
    ]


class WINTRUST_CATALOG_INFO(Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("dwCatalogVersion", DWORD),
        ("pcwszCatalogFilePath", LPCWSTR),
        ("pcwszMemberTag", LPCWSTR),
        ("pcwszMemberFilePath", LPCWSTR),
        ("hMemberFile", HANDLE),
        ("pbCalculatedFileHash", POINTER(BYTE)),
        ("cbCalculatedFileHash", DWORD),
        ("pcCatalogContext", POINTER(CTL_CONTEXT)),
    ]

class WINTRUST_BLOB_INFO(Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("gSubject", GUID),
        ("pcwszDisplayName", LPCWSTR),
        ("cbMemObject", DWORD),
        ("pbMemObject", POINTER(BYTE)),
        ("cbMemSignedMsg", DWORD),
        ("pbMemSignedMsg", POINTER(BYTE)),
    ]


class CRYPT_BIT_BLOB(Structure):
    _fields_ = [
        ("cbData", DWORD),
        ("pbData", POINTER(BYTE)),
        ("cUnusedBits", DWORD),
    ]

class CERT_PUBLIC_KEY_INFO(Structure):
    _fields_ = [
        ("Algorithm", CRYPT_ALGORITHM_IDENTIFIER),
        ("PublicKey", CRYPT_BIT_BLOB),
    ]


class CERT_EXTENSION(Structure):
    _fields_ = [
        ("pszObjId", LPSTR),
        ("fCritical", BOOL),
        ("Value", CRYPTOAPI_BLOB),
    ]

class CERT_INFO(Structure):
    _fields_ = [
        ("dwVersion", DWORD),
        ("SerialNumber", CRYPTOAPI_BLOB),
        ("SignatureAlgorithm", CRYPT_ALGORITHM_IDENTIFIER),
        ("Issuer", CRYPTOAPI_BLOB),
        ("NotBefore", FILETIME),
        ("NotAfter", FILETIME),
        ("Subject", CRYPTOAPI_BLOB),
        ("SubjectPublicKeyInfo", CERT_PUBLIC_KEY_INFO),
        ("IssuerUniqueId", CRYPT_BIT_BLOB),
        ("SubjectUniqueId", CRYPT_BIT_BLOB),
        ("cExtension", DWORD),
        ("rgExtension", POINTER(CERT_EXTENSION)),
    ]

class CERT_CONTEXT(Structure):
    _fields_ = [
        ("dwCertEncodingType", DWORD),
        ("pbCertEncoded", POINTER(BYTE)),
        ("cbCertEncoded", DWORD),
        ("pCertInfo", POINTER(CERT_INFO)),
        ("hCertStore", c_void_p),
    ]

class WINTRUST_CERT_INFO(Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("pcwszDisplayName", LPCWSTR),
        ("psCertContext", POINTER(CERT_CONTEXT)),
        ("chStores", DWORD),
        ("pahStores", POINTER(c_void_p)),
        ("dwFlags", DWORD),
        ("psftVerifyAsOf", POINTER(FILETIME)),
    ]


class CMSG_SIGNER_INFO(Structure):
    _fields_ = [
        ("dwVersion", DWORD),
        ("Issuer", CRYPTOAPI_BLOB),
        ("SerialNumber", CRYPTOAPI_BLOB),
        ("HashAlgorithm", CRYPT_ALGORITHM_IDENTIFIER),
        ("HashEncryptionAlgorithm", CRYPT_ALGORITHM_IDENTIFIER),
        ("EncryptedHash", CRYPTOAPI_BLOB),
        ("AuthAttrs", CRYPT_ATTRIBUTES),
        ("UnauthAttrs", CRYPT_ATTRIBUTES),
    ]

class WINTRUST_SGNR_INFO(Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("pcwszDisplayName", LPCWSTR),
        ("psSignerInfo", POINTER(CMSG_SIGNER_INFO)),
        ("chStores", DWORD),
        ("pahStores", POINTER(c_void_p)),
    ]


class TMP_WINTRUST_UNION_TYPE(Union):
    _fields_ = [
        ("pFile", POINTER(WINTRUST_FILE_INFO)),
        ("pCatalog", POINTER(WINTRUST_CATALOG_INFO)),
        ("pBlob", POINTER(WINTRUST_BLOB_INFO)),
        ("pSgnr", POINTER(WINTRUST_SGNR_INFO)),
        ("pCert", POINTER(WINTRUST_CERT_INFO)),
    ]


class WINTRUST_DATA(Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("pPolicyCallbackData", LPVOID),
        ("pSIPClientData", LPVOID),
        ("dwUIChoice", DWORD),
        ("fdwRevocationChecks", DWORD),
        ("dwUnionChoice", DWORD),
        ("tmp_union", TMP_WINTRUST_UNION_TYPE),
        ("dwStateAction", DWORD),
        ("hWVTStateData", HANDLE),
        ("pwszURLReference", POINTER(WCHAR)),
        ("dwProvFlags", DWORD),
        ("dwUIContext", DWORD),
    ]
