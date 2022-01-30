# EmailMe

This tool allows you to send an email via smtp indicating the wireless address of the device (wlan0).

My particular use case is: When a raspberry pi is turned on, it sends me an email to a gmail email with the IP address (to be able to make ssh and rdp connection).


The first step is to install the dependencies with `python3 -m pip install -r requirements.txt`.

To configure it to run at start-up add


```
python3 /path/to/emailme.py

```

to file `/etc/rc.local` and then enable the service 


```bash
systemctl enable rc-local.service
``` 
