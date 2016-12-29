TIM_pysmpp
==========

SMPP library for Python 3. Forked from [python-smpplib](https://github.com/podshumok/python-smpplib) (Python 2 implementation).


Example:

```python
import logging
import sys

import tim_pysmpp.gsm
import tim_pysmpp.client
import tim_pysmpp.consts

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

# Two parts, UCS2, SMS with UDH
parts, encoding_flag, msg_type_flag = tim_pysmpp.gsm.make_parts(u'Привет мир!\n'*10)

client = tim_pysmpp.client.Client('example.com', SOMEPORTNUMBER)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
client.set_message_received_handler(
    lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))

client.connect()
client.bind_transceiver(system_id='login', password='secret')

for part in parts:
    pdu = client.send_message(
        source_addr_ton=tim_pysmpp.consts.SMPP_TON_INTL,
        #source_addr_npi=tim_pysmpp.consts.SMPP_NPI_ISDN,
        # Make sure it is a byte string, not unicode:
        source_addr='SENDERPHONENUM',

        dest_addr_ton=tim_pysmpp.consts.SMPP_TON_INTL,
        #dest_addr_npi=tim_pysmpp.consts.SMPP_NPI_ISDN,
        # Make sure thease two params are byte strings, not unicode:
        destination_addr='PHONENUMBER',
        short_message=part,

        data_coding=encoding_flag,
        esm_class=msg_type_flag,
        registered_delivery=True,
    )
    print(pdu.sequence)
client.listen()
```
You also may want to listen in a thread:
```python
from threading import Thread
t = Thread(target=client.listen)
t.start()
```

The client supports setting a custom generator that produces sequence numbers for the PDU packages. Per default a simple in memory generator is used which in conclusion is reset on (re)instantiation of the client, e.g. by an application restart. If you want to keep the sequence number to be persisted across restarts you can implement your own storage backed generator.

Example:
```python
import tim_pysmpp.client

import mymodule

generator = mymodule.PersistentSequenceGenerator()
client = tim_pysmpp.client.Client('example.com', SOMEPORTNUMBER, sequence_generator=generator)
...
```

