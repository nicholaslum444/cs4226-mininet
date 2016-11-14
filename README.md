# Running POX
1. Navigate to pox directory `$ cd ~/pox`
2. Create a softlink to controller file: `$ ln -s ~/submission/controller_ans.py ~/pox/pox/misc/controller.py`
3. Create a softlink to policy file: `$ ln -s ~/submission/policy.in ~/pox/policy.in`
4. Run `$ ./pox.py log.level --DEBUG pox.misc.controller`

# Running Mininet
1. Ensure POX is running first; See above
2. Place `mininetTopo.py` and `topology.in` in `~/submission/` folder
3. Navigate to that folder in command line
4. Run `$ sudo python mininetTopo.py`

# Firewall Test
```bash
H1 iperf -s -p 4001 &
H4 iperf -s -p 4001 &
H1 iperf -s -p 5000 &
H4 iperf -s -p 5000 &
H2 iperf -s -p 1000 &
H5 iperf -s -p 1000 &
H2 iperf -s -p 5000 &
H5 iperf -s -p 5000 &

H1 iperf -c H4 -p 4001 -t 1 # wont work
H4 iperf -c H1 -p 4001 -t 1 # wont work
H1 iperf -c H4 -p 5000 -t 1
H4 iperf -c H1 -p 5000 -t 1

H2 iperf -c H5 -p 1000 -t 1 # wont work
H5 iperf -c H2 -p 1000 -t 1 # wont work
H2 iperf -c H5 -p 5000 -t 1
H5 iperf -c H2 -p 5000 -t 1
```
