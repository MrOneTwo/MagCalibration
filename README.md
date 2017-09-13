# Magnetometer calibration program

Folders:

- magCalPy - program for magnetometer based on PyQtGraph (use the one from
_magCalPy/pipes_)
- magCalArd - program for Arduino for random vector generation
- magCalOctave - program for Octave for magnetometer calibration

## magCalPy

To run it open two terminals. In the first one run the serial_simple.py:

```bash
python serialcom_simple.py
```

It will check if _fifo_ file exists. If not it will create it. Then it reads
data from serial (be sure to put sensor in _mag_ mode before) and writes it
to the _fifo_ file. It's a blocking write - needs a consumer.

The consumer is the _pyqtgraph_ program. Run it with:

```bash
xterm -e sudo python magCal.py
```

Running it in a new terminal window makes it easier to close.

That should be it.

