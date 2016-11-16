# Setup

Use the default mininet VM on VirtualBox and set up host-only adapter and internet connection.

Start the VM, run `$ ifconfig` to get its host-only IP address, then minimize it.

Open a terminal on the local machine and SSH into the VM using the IP address from above.

Run `$ git clone https://github.com/nicholaslum444/cs4226-mininet ~/submission`.

Leave the terminal open for editing files if needed.


# Running POX

Open another terminal on the local machine and SSH to the VM.

Navigate to pox directory `$ cd ~/pox`.

Create a softlink to controller file: `$ ln -s ~/submission/controller_ans.py ~/pox/pox/misc/controller.py`.

Create a softlink to policy file: `$ ln -s ~/submission/policy.in ~/pox/policy.in`.

Run `$ ./pox.py log.level --DEBUG pox.misc.controller`.

Leave the terminal open so that the controller can continue running.


# Running Mininet

Ensure POX is running first; See above.

Open another terminal on the local machine and SSH to the VM.

Navigate to the submission folder `$ cd ~/submission`.

Run mininet: `$ sudo python mininetTopo.py`.

Leave the terminal open to interact with mininet.


# Learning Switch Test

Run POX and mininet as above.

On mininet, run `> pingallfull`. All hosts should be reachable. Note the RTT for the host pairs.

Run `> pingallfull` again. All hosts should still be reachable. The RTT of the host pairs should be significantly smaller than before.

Exit mininet once completed.


# Firewall Test

On **mininet**, open the xterm windows for all the hosts: `> xterm H1 H2 H3 H4 H5 H6 H7`.

### Server: H1
On the xterm of **H1**, run: `# iperf -s -D -p 4001 && iperf -s -D -p 5000`. This opens port 4001 (banned) and port 5000 (allowed).

On the xterm of **H4**, run: `# iperf -c 10.0.0.1 -p 5000 -t 5 && iperf -c 10.0.0.1 -p 4001 -t 5`. The second command should not work.

On the xterm of **all other hosts**, run: `# iperf -c 10.0.0.1 -p 5000 -t 5 && iperf -c 10.0.0.1 -p 4001 -t 5`. Both commands should work.

### Server: H4
On the xterm of **H4**, run: `# iperf -s -D -p 4001 && iperf -s -D -p 5000`. This opens port 4001 (banned) and port 5000 (allowed).

On the xterm of **H1**, run: `# iperf -c 10.0.0.4 -p 5000 -t 5 && iperf -c 10.0.0.4 -p 4001 -t 5`. The second command should not work.

On the xterm of **all other hosts**, run: `# iperf -c 10.0.0.4 -p 5000 -t 5 && iperf -c 10.0.0.4 -p 4001 -t 5`. Both commands should work.

### Server: H2
On the xterm of **H2**, run: `# iperf -s -D -p 1000 && iperf -s -D -p 5000`. This opens port 1000 (banned) and port 5000 (allowed).

On the xterm of **H5**, run: `# iperf -c 10.0.0.2 -p 5000 -t 5 && iperf -c 10.0.0.2 -p 1000 -t 5`. The second command should not work.

On the xterm of **all other hosts**, run: `# iperf -c 10.0.0.2 -p 5000 -t 5 && iperf -c 10.0.0.2 -p 1000 -t 5`. Both commands should work.

### Server: H5
On the xterm of **H5**, run: `# iperf -s -D -p 1000 && iperf -s -D -p 5000`. This opens port 1000 (banned) and port 5000 (allowed).

On the xterm of **H2**, run: `# iperf -c 10.0.0.5 -p 5000 -t 5 && iperf -c 10.0.0.5 -p 1000 -t 5`. The second command should not work.

On the xterm of **all other hosts**, run: `# iperf -c 10.0.0.5 -p 5000 -t 5 && iperf -c 10.0.0.5 -p 1000 -t 5`. Both commands should work.

Finally, close all the xterm windows and exit mininet once completed.


# VPN Test

Start mininet.

On mininet, the bandwidths reported by the following commands should be representative of 100Mbps:
```bash
# H1, H4, H5
iperf H1 H4
iperf H1 H5
iperf H4 H5

# H2, H6
iperf H2 H6

# H3, H7
iperf H3 H7
```

The bandwidths reported by the following commands should be less than 50Mbps:
```bash
# H1:x H2, H3, H6, H7
iperf H1 H2
iperf H1 H3
iperf H1 H6
iperf H1 H7

# H2:x H1, H3, H4, H5, H7
iperf H2 H3
iperf H2 H4
iperf H2 H5
iperf H2 H7

# H3:x H1, H2, H4, H5, H6
iperf H3 H4
iperf H3 H5
iperf H3 H6

# H4:x H2, H3, H6, H7
iperf H4 H6
iperf H4 H7

# H5:x H2, H3, H6, H7
iperf H5 H6
iperf H5 H7

# H6:x H1, H3, H4, H5, H7
iperf H6 H7

# H7:x H1, H2, H4, H5, H6
```

Exit mininet once completed.

