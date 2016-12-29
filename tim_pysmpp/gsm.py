# -*- coding: utf8 -*-
import binascii
import random

from . import consts
from . import exceptions


# from http://stackoverflow.com/questions/2452861/python-library-for-converting-plain-text-ascii-into-gsm-7-bit-character-set
gsm = ("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>"
       "?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà")
ext = ("````````````````````^```````````````````{}`````\\````````````[~]`"
       "|````````````````````````````````````€``````````````````````````")


class EncodeError(ValueError):
    """Raised if text cannot be represented in gsm 7-bit encoding"""


def gsm_encode(plaintext, hex=False):
    """Replace non-GSM ASCII symbols"""
    res = ""
    for c in plaintext:
        idx = gsm.find(c)
        if idx != -1:
            res += chr(idx)
            continue
        idx = ext.find(c)
        if idx != -1:
            res += chr(27) + chr(idx)
            continue
        raise EncodeError()
    return binascii.b2a_hex(res) if hex else res


def make_parts(text):
    """Returns tuple(parts, encoding, esm_class)"""
    try:
        text = gsm_encode(text)
        encoding = consts.SMPP_ENCODING_DEFAULT
        need_split = len(text) > consts.SEVENBIT_SIZE
        partsize = consts.SEVENBIT_MP_SIZE
        encode = lambda s: s
        #print('NO EncodeError') ### DEBUG
    except EncodeError:
        #print('EncodeError') ### DEBUG
        encoding = consts.SMPP_ENCODING_ISO10646
        need_split = len(text) > consts.UCS2_SIZE
        partsize = consts.UCS2_MP_SIZE
        encode = lambda s: s.encode('utf-16-be')
        #encode = lambda s: s

    esm_class = consts.SMPP_MSGTYPE_DEFAULT

    #print('text:',text,type(text))### DEBUG
    if need_split:
        esm_class = consts.SMPP_GSMFEAT_UDHI

        starts = tuple(range(0, len(text), partsize))
        if len(starts) > 255:
            raise exceptions.MessageTooLong()

        parts = []
        ipart = 1
        uid = random.randint(0, 255)
        for start in starts:
            #print('text[start:start + partsize]:',text[start:start + partsize],type(text[start:start + partsize]))### DEBUG
            #text[start:start + partsize].encode('utf-16-be') ### DEBUG
            #print('encode type:',type(encode(text[start:start + partsize]))) ### DEBUG
            #print('chr(uid):', chr(uid),type(chr(uid))) ### DEBUG
            #b''.join(( encode(text[start:start + partsize]),)) ### DEBUG

            if encoding == consts.SMPP_ENCODING_DEFAULT:
                parts.append(''.join(('\x05\x00\x03', chr(uid),
                             chr(len(starts)), chr(ipart),
                             encode(text[start:start + partsize]))))
            elif encoding == consts.SMPP_ENCODING_ISO10646:
                parts.append(b''.join(('\x05\x00\x03'.encode(), chr(uid).encode(),
                             chr(len(starts)).encode(), chr(ipart).encode(),
                             encode(text[start:start + partsize]))))
            else: raise(Exception('No Encoding defined'))
            ipart += 1
    else:
        parts = (encode(text),)

    #print('parts:',parts) ### DEBUG
    #for p in parts: print('p:',p,type(p)) ### DEBUG
    #print('encoding:',encoding,type(encoding)) ### DEBUG
    #print('esm_class:',esm_class,type(esm_class)) ### DEBUG
    return parts, encoding, esm_class
