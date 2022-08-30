# Low-power Backscatter Sensor Communications

*NSAP Capstone Project, 2021*

Eli Baum

Full report is available in `backscatter capstone.docx`.

Repo layout:

- `arduino`
    - Various experiments for the transmitter module.
    - Final prototype is in `full_proto`, using utilty functions in `util`
- `flowgraphs`
    - Various GNUradio flowgraphs
    - `proto/proto_decode.grc` is used to ingest samples from SDR for final prototype.
- `img`: images for report
- `print/case`: 3d printed transmitter enclosure
- `processing`
    - Various python experiments and decoders
    - Final prototype is `fm0/fm0_proto.py`
- `pseudocode`
    - explanatory pseudocode for both the transmitter and receiver

> MITRE Public Release Case Number: 22-2535
