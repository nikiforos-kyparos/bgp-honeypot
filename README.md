# Beyond the Handshake

## Investigating Unsolicited Peering Activity with a BGP Honeypot

This repository contains the supporting material for my Master's thesis at TU Delft:

**Beyond the Handshake: Investigating Unsolicited Peering Activity with a BGP Honeypot**

## Author

**Nikiforos Kyparos**

## Supervisors

- **Georgios Smaragdakis**
- **Taha Albakour**
- **Martin Mladenov**

## Abstract
The Border Gateway Protocol (BGP) remains critical to Internet connectivity, but monitoring unsolicited traffic targeting BGP infrastructure is difficult because contact with TCP port 179 alone does not indicate actual BGP behavior. This thesis investigates whether a protocol-aware BGP honeypot can improve understanding of unsolicited TCP/179 traffic. A low-interaction BGP honeypot based on BIRD was deployed on unused IPv4 address space, and packet captures were analyzed to extract BGP session information and behavior. The honeypot received 7693 BGP OPEN requests from 1594 unique source IP addresses over 58 days. The honeypot was then compared with a larger reactive network telescope over an aligned monitoring period. The results show that the honeypot provided richer protocol-level information, while the reactive telescope provided broader visibility because of its larger monitored address space. After normalization, the honeypot showed higher BGP source density and BGP visibility, and it also observed some source IPs and real ASNs that were not present in the telescope data. However, most observed interactions remained shallow, usually ending shortly after the OPEN exchange, and no clear BGP-specific attacks were identified. Overall, this thesis shows that a BGP honeypot can serve as a useful complementary monitoring tool by adding protocol-level context to unsolicited BGP traffic observations.
